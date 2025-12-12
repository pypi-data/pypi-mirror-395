from .map_tool import async_call_tool


class MapClient:
  """地图客户端"""

  async def geo(self, address, city):
    geo_result = await async_call_tool('maps_geo', address=address, city=city)
    return geo_result[0] if geo_result else None

  async def around_search(self, keywords, location, radius):
    search_result = await  async_call_tool('maps_around_search', keywords=keywords, location=location, radius=radius)
    return search_result[0] if search_result else None

  async def distance(self, origins, destination, type=3):
    search_result = await  async_call_tool('maps_distance', origins=origins, destination=destination, type=type)
    return search_result[0] if search_result else None
