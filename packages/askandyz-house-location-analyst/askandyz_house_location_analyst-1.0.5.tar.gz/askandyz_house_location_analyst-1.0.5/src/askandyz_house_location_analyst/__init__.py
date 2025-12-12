from typing import List

from fastmcp import FastMCP

from .localtion_analyzer import RealEstateAnalyzer
from .map_client import MapClient
from .report_generator import ReportGenerator

mcp = FastMCP("House Location Analyst")

# Initialize components
map_client = MapClient()
analyzer = RealEstateAnalyzer(map_client)
reporter = ReportGenerator()


def to_dict(obj):
  """Convert dataclass objects to dictionary"""
  if hasattr(obj, '__dict__'):
    result = {}
    for key, value in obj.__dict__.items():
      if hasattr(value, '__dict__') or isinstance(value, (list, dict)):
        result[key] = to_dict(value)
      else:
        result[key] = value
    return result
  elif isinstance(obj, list):
    return [to_dict(item) for item in obj]
  elif isinstance(obj, dict):
    return {key: to_dict(value) for key, value in obj.items()}
  else:
    return obj


def get_city(city: str = None):
  if city:
    return city
  try:
    import requests
    response = requests.get('http://ip-api.com/json/')
    data = response.json()
    if data['status'] == 'success':
      return data.get('city')
  except:
    return None


@mcp.tool()
async def analyze_single_community(community_name: str, city: str = None) -> dict:
  """
  分析单个小区的周边配套设施情况

  Args:
      community_name: 小区名称
      city: 城市名称

  Returns:
      dict: 包含小区分析结果和HTML报告
  """
  try:
    # 执行分析
    analysis_result = await analyzer.analyze_single_community(community_name, city)

    # 生成HTML报告
    html_report = reporter.generate_single_report(analysis_result)

    return {
      "success": True,
      "analysis": to_dict(analysis_result),
      "html_report": html_report
    }
  except Exception as e:
    return {
      "success": False,
      "error": str(e)
    }


@mcp.tool()
async def compare_communities(community_names: List[str], city: str = None) -> dict:
  """
  对比多个小区的周边配套设施情况

  Args:
      community_names: 小区名称列表
      city: 城市名称

  Returns:
      dict: 包含对比分析结果和HTML报告
  """
  try:
    # 执行对比分析
    comparison_results = await analyzer.compare_communities(community_names, city)

    # 生成HTML对比报告
    html_report = reporter.generate_comparison_report(comparison_results)

    return {
      "success": True,
      "analyses": [to_dict(analysis) for analysis in comparison_results],
      "html_report": html_report
    }
  except Exception as e:
    return {
      "success": False,
      "error": str(e)
    }


def main():
  mcp.run(transport="stdio")

# if __name__ == "__main__":
#   main()
