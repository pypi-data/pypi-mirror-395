import asyncio
import json
import os

from dotenv import load_dotenv
from fastmcp import Client

from .cache import ToolCache

load_dotenv(verbose=True)
ref_mcp_server_base_url = os.getenv('REF_MCP_SERVER_BASE_URL', default='https://mcp.amap.com/sse?key=')
amap_key = os.getenv('AMAP_KEY', default='')
ref_mcp_server_url = ref_mcp_server_base_url + amap_key
amap_client = Client(ref_mcp_server_url)

tool_cache = ToolCache()


async def async_call_tool(tool_name, to_json=True, **kwargs):
  # Try to get cached result first
  cached_result = tool_cache.get_cached_result(tool_name, to_json=to_json, **kwargs)
  if cached_result is not None:
    print(f"Cache hit for: {tool_name} with params {kwargs}")
    cached_result = json.loads(cached_result) if to_json and cached_result else cached_result
    print(f"Cache hit result: {cached_result}")
    return cached_result

  async with amap_client:
    print(f"Executing: {tool_name} with params {kwargs}")
    try:
      result = await amap_client.call_tool(tool_name, arguments=kwargs)
    except Exception as e:
      print(f"Executing tool {tool_name} failed with error: {e}.")
      tool_cache.save_result(tool_name, None, to_json=to_json, **kwargs)
      return None

    print(f"Result: {result}")
    if not to_json:
      result_text = result.content[0].text
      tool_cache.save_result(tool_name, result_text, to_json=to_json, **kwargs)
      return result_text

    result_text = result.content[0].text
    parsed_result = json.loads(result_text)
    final_result = parsed_result['results'] if 'results' in parsed_result else parsed_result
    final_result = final_result if isinstance(final_result, list) else [final_result]

    # Cache the parsed result
    tool_cache.save_result(tool_name, final_result, to_json=to_json, **kwargs)

    return final_result


def call_tool(tool_name, to_json=True, **kwargs):
  return asyncio.run(async_call_tool(tool_name, to_json, **kwargs))


if __name__ == "__main__":
  # result = call_tool('maps_weather', city='西安')
  # result = call_tool('maps_geo', address='西安电子科技大学')
  result = call_tool('maps_geo', address='紫薇西棠', city='西安')
  print(result)
  result = call_tool('maps_distance', origins='108.829559,34.241958', destination='108.833541,34.242677', type=3)
  print(result)
  result = call_tool('maps_direction_walking', origin='108.829559,34.241958', destination='108.833541,34.242677')
  print(result)

  # origin_geo = call_tool('maps_geo', address='西安电子科技大学')
  # destination_geo = call_tool('maps_geo', address='清华大学')
  # transit = call_tool('maps_direction_transit_integrated', origin=origin_geo[0]['location'], destination=destination_geo[0]['location'], city=origin_geo[0]['city'], cityd=destination_geo[0]['city'])
  # print(transit)
