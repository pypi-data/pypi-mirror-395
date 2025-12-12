from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class FacilityType(Enum):
  """配套设施类型"""
  METRO = "地铁站"
  HOSPITAL = "医院"
  SCHOOL = "学校"
  KINDERGARTEN = "幼儿园"
  SUPERMARKET = "超市"
  MALL = "商场"
  PARK = "公园"
  BANK = "银行"
  GYM = "健身房"
  RESTAURANT = "餐饮"


@dataclass
class Facility:
  """配套设施"""
  name: str
  type: str
  distance: float  # 米
  walking_time: int  # 分钟
  address: str
  poi_id: str
  lon: float
  lat: float

  def get_score(self) -> float:
    """根据距离计算得分"""
    if self.distance <= 500:
      return 10
    elif self.distance <= 1000:
      return 8
    elif self.distance <= 2000:
      return 6
    elif self.distance <= 3000:
      return 4
    else:
      return 2


@dataclass
class CommunityLocation:
  """小区位置信息"""
  name: str
  address: str
  lon: float
  lat: float
  city: str


@dataclass
class CategoryScore:
  """类别评分"""
  category: str
  score: float
  facilities: List[Facility]
  count: int
  nearest_distance: float
  positive: bool

  def get_rating(self) -> str:
    """获取评级"""
    if self.score >= 9:
      return "优秀"
    elif self.score >= 7:
      return "良好"
    elif self.score >= 5:
      return "一般"
    elif self.score >= 3:
      return "较差"
    else:
      return "很差"


@dataclass
class CommunityAnalysis:
  """小区分析结果"""
  community: CommunityLocation
  category_scores: Dict[str, CategoryScore]
  overall_score: float
  facilities_total: int
  analysis_time: str

  def get_overall_rating(self) -> str:
    """获取总体评级"""
    if self.overall_score >= 9:
      return "优秀"
    elif self.overall_score >= 7:
      return "良好"
    elif self.overall_score >= 5:
      return "一般"
    elif self.overall_score >= 3:
      return "较差"
    else:
      return "很差"
