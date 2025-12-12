import asyncio
import os
from typing import List, Dict

from .localtion_analyzer import RealEstateAnalyzer
from .map_client import MapClient
from .modal import CommunityAnalysis


class ReportGenerator:
  """报告生成器"""

  def __init__(self):
    from pybars import Compiler
    self.compiler = Compiler()
    self.helpers = {
      'eq': lambda context, *args, **kwargs: args[0] == args[1],
      'ne': lambda context, *args, **kwargs: args[0] != args[1],
      'gt': lambda context, *args, **kwargs: args[0] > args[1],
      'gte': lambda context, *args, **kwargs: args[0] >= args[1],
      'lt': lambda context, *args, **kwargs: args[0] < args[1],
      'lte': lambda context, *args, **kwargs: args[0] <= args[1],
    }
    # Get the directory where this file is located
    self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')

  def generate_single_report(self, analysis: CommunityAnalysis) -> str:
    """生成单个小区详情报告"""
    template_path = os.path.join(self.template_dir, 'community.hbs')
    with open(template_path, 'r', encoding='utf-8') as f:
      template_str = f.read()

    template = self.compiler.compile(template_str)
    data = self._prepare_single_data(analysis)
    print(data)
    return template(data, self.helpers)

  def generate_comparison_report(
      self,
      analyses: List[CommunityAnalysis]
  ) -> str:
    """生成多小区对比报告"""
    template_path = os.path.join(self.template_dir, 'comparison.hbs')
    with open(template_path, 'r', encoding='utf-8') as f:
      template_str = f.read()

    template = self.compiler.compile(template_str)
    data = self._prepare_comparison_data(analyses)
    print(data)
    return template(data, self.helpers)

  def _prepare_single_data(self, analysis: CommunityAnalysis) -> Dict:
    """准备单小区数据"""
    return {
      'community': {
        'name': analysis.community.name,
        'address': analysis.community.address,
        'city': analysis.community.city
      },
      'overall_score': round(analysis.overall_score, 2),
      'overall_rating': analysis.get_overall_rating(),
      'facilities_total': analysis.facilities_total,
      'analysis_time': analysis.analysis_time,
      'score_bar_width': int(analysis.overall_score * 10),
      'categories': [
        {
          'name': cat_score.category,
          'score': round(cat_score.score, 2),
          'rating': cat_score.get_rating(),
          'count': cat_score.count,
          'nearest_distance': cat_score.nearest_distance,
          'score_bar_width': int(cat_score.score * 10),
          'facilities': [
            {
              'name': f.name,
              'type': f.type,
              'distance': int(f.distance),
              'score': f.get_score(),
              'walking_time': f.walking_time,
              'address': f.address
            }
            for f in cat_score.facilities
          ]
        }
        for cat_score in analysis.category_scores.values()
      ]
    }

  def _prepare_comparison_data(
      self,
      analyses: List[CommunityAnalysis]
  ) -> Dict:
    """准备对比数据"""
    # 获取所有类别
    categories = list(analyses[0].category_scores.keys())

    # 准备对比表格数据
    comparison_table = []
    for category in categories:
      row = {
        'category': category,
        'communities': []
      }
      for analysis in analyses:
        cat_score = analysis.category_scores[category]
        row['communities'].append({
          'score': round(cat_score.score, 2),
          'rating': cat_score.get_rating(),
          'count': cat_score.count,
          'nearest': int(cat_score.nearest_distance)
        })
      comparison_table.append(row)

    return {
      'communities': [
        {
          'name': a.community.name,
          'address': a.community.address,
          'overall_score': round(a.overall_score, 2),
          'overall_rating': a.get_overall_rating(),
          'score_bar_width': int(a.overall_score * 10),
          'rank': idx + 1
        }
        for idx, a in enumerate(analyses)
      ],
      'comparison_table': comparison_table,
      'analysis_time': analyses[0].analysis_time
    }


if __name__ == "__main__":
  map_client = MapClient()
  analyzer = RealEstateAnalyzer(map_client)
  results = asyncio.run(analyzer.analyze_single_community("紫薇西棠", "西安"))
  print(results)
  reporter = ReportGenerator()
  report = reporter.generate_single_report(results)
  print(report)
