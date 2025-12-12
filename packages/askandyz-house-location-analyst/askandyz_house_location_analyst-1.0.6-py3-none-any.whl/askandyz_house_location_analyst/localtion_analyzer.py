import asyncio
from typing import List

from .map_client import MapClient
from .modal import CommunityAnalysis, CategoryScore, CommunityLocation, Facility


class RealEstateAnalyzer:
  """房产选址分析器"""

  # 配置各类设施的搜索关键词和权重
  FACILITY_CONFIG = {
    # ========== 正面设施(加分项) ==========
    "交通": {
      "keywords": ["地铁站", "公交站", "长途汽车站", "火车站", "轻轨站", "有轨电车站"],
      "weight": 0.18,
      "radius": 2000,
      "score_type": "positive"
    },

    "教育": {
      "keywords": ["幼儿园", "小学", "中学", "高中", "国际学校", "培训机构", "早教中心"],
      "weight": 0.15,
      "radius": 2000,
      "score_type": "positive"
    },

    "医疗": {
      "keywords": ["医院", "三甲医院", "诊所", "社区卫生服务中心", "药店", "口腔诊所", "体检中心"],
      "weight": 0.13,
      "radius": 2000,
      "score_type": "positive"
    },

    "商业": {
      "keywords": ["超市", "商场", "购物中心", "便利店", "大型超市", "百货商店"],
      "weight": 0.10,
      "radius": 1500,
      "score_type": "positive"
    },

    "生活服务": {
      "keywords": ["银行", "ATM", "邮局", "菜市场", "农贸市场", "快递站", "洗衣店", "理发店", "维修店"],
      "weight": 0.08,
      "radius": 1500,
      "score_type": "positive"
    },

    "餐饮": {
      "keywords": ["餐厅", "快餐", "美食广场", "咖啡厅", "茶馆", "小吃街", "食堂", "面包店"],
      "weight": 0.07,
      "radius": 1000,
      "score_type": "positive"
    },

    "儿童设施": {
      "keywords": ["儿童游乐场", "早教中心", "托育中心", "儿童医院", "儿童图书馆", "亲子乐园", "游乐园"],
      "weight": 0.09,
      "radius": 1500,
      "score_type": "positive"
    },

    "养老": {
      "keywords": ["养老院", "老年活动中心", "康复中心", "护理院", "老年大学", "日间照料中心"],
      "weight": 0.05,
      "radius": 2500,
      "score_type": "positive"
    },

    "环境": {
      "keywords": ["公园", "绿地", "湿地公园", "河道", "景观带", "森林公园", "植物园", "广场"],
      "weight": 0.08,
      "radius": 3000,
      "score_type": "positive"
    },

    "运动健身": {
      "keywords": ["健身房", "体育馆", "游泳馆", "羽毛球馆", "篮球场", "足球场", "网球场", "瑜伽馆", "健身步道"],
      "weight": 0.03,
      "radius": 2000,
      "score_type": "positive"
    },

    "文化娱乐": {
      "keywords": ["电影院", "剧院", "博物馆", "文化中心", "KTV", "书店", "展览馆", "艺术馆"],
      "weight": 0.02,
      "radius": 3000,
      "score_type": "positive"
    },

    "公共服务": {
      "keywords": ["派出所", "社区服务中心", "政务中心", "图书馆", "街道办事处", "居委会", "公证处"],
      "weight": 0.02,
      "radius": 2500,
      "score_type": "positive"
    },

    # ========== 负面设施(减分项) ==========
    "环境污染源": {
      "keywords": ["垃圾站", "垃圾处理站", "垃圾中转站", "垃圾焚烧厂", "污水处理厂", "化工厂", "炼油厂"],
      "weight": -0.15,  # 负权重
      "radius": 800,    # 较小范围内影响极大
      "score_type": "negative"
    },

    "电磁辐射源": {
      "keywords": ["变电站", "高压线", "输电塔", "变压器", "通信基站"],
      "weight": -0.12,
      "radius": 500,
      "score_type": "negative"
    },

    "噪音污染源": {
      "keywords": ["高架桥", "高速公路", "铁路", "机场", "工地", "夜市", "酒吧街", "KTV聚集区"],
      "weight": -0.10,
      "radius": 1000,
      "score_type": "negative"
    },

    "安全隐患": {
      "keywords": ["加油站", "液化气站", "危险品仓库", "化学品仓库", "爆炸物仓库"],
      "weight": -0.08,
      "radius": 600,
      "score_type": "negative"
    },

    "殡葬设施": {
      "keywords": ["殡仪馆", "火葬场", "公墓", "陵园", "墓地"],
      "weight": -0.12,
      "radius": 1500,
      "score_type": "negative"
    },

    "治安问题区": {
      "keywords": ["看守所", "拘留所", "监狱", "戒毒所", "城中村", "群租房集中区"],
      "weight": -0.08,
      "radius": 1000,
      "score_type": "negative"
    },

    "空气污染源": {
      "keywords": ["养殖场", "屠宰场", "食品加工厂", "印刷厂", "喷漆厂", "橡胶厂"],
      "weight": -0.10,
      "radius": 1000,
      "score_type": "negative"
    },

    "视觉污染": {
      "keywords": ["废品回收站", "汽修厂", "洗车场聚集区", "二手市场"],
      "weight": -0.05,
      "radius": 500,
      "score_type": "negative"
    }
  }

  def __init__(self, map_client: MapClient):
    """
    初始化分析器
    :param map_client: 地图API客户端(包含所有工具方法)
    """
    self.map_client = map_client

  async def analyze_single_community(
      self,
      community_name: str,
      city: str
  ) -> CommunityAnalysis:
    """
    分析单个小区

    流程:
    1. 地理编码获取坐标
    2. 周边搜索各类设施
    3. 计算距离
    4. 评分
    """
    # Step 1: 获取小区位置
    curr_city = self._get_city()
    location = await self._get_community_location(community_name, city, curr_city)

    # Step 2: 搜索各类配套设施
    category_scores = {}
    all_facilities_count = 0

    for category, config in self.FACILITY_CONFIG.items():
      facilities = await self._search_facilities(
        location,
        config["keywords"],
        config["radius"]
      )

      # 计算该类别得分
      positive = config["score_type"] == "positive"
      if facilities:
        avg_score = sum(f.get_score() for f in facilities) / len(facilities)
        nearest = min(facilities, key=lambda f: f.distance)

        category_scores[category] = CategoryScore(
          category=category,
          score=avg_score,
          facilities=facilities[:10],
          count=len(facilities),
          nearest_distance=nearest.distance,
          positive= positive
        )
      else:
        category_scores[category] = CategoryScore(
          category=category,
          score=0,
          facilities=[],
          count=0,
          nearest_distance=float('inf'),
          positive= positive
        )

      all_facilities_count += len(facilities)

    # Step 3: 计算总体得分(加权平均)
    overall_score = sum(
      score.score * self.FACILITY_CONFIG[category]["weight"]
      for category, score in category_scores.items()
    )

    from datetime import datetime

    return CommunityAnalysis(
      community=location,
      category_scores=category_scores,
      overall_score=round(overall_score, 1),
      facilities_total=all_facilities_count,
      analysis_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

  async def compare_communities(
      self,
      community_names: List[str],
      city: str
  ) -> List[CommunityAnalysis]:
    """对比多个小区"""
    results = []
    city = city or self._get_city()
    for name in community_names:
      analysis = await self.analyze_single_community(name, city)
      results.append(analysis)

    # 按总分排序
    results.sort(key=lambda a: a.overall_score, reverse=True)
    return results

  async def _get_community_location(
      self,
      community_name: str,
      city: str,
      curr_city: str
  ) -> CommunityLocation:
    """获取小区位置"""
    result = await self.map_client.geo(address=community_name, city=city or curr_city)
    if not result and curr_city and city != curr_city:
      result = await self.map_client.geo(address=community_name, city=curr_city)
    if not result and (curr_city or city):
      result = await self.map_client.geo(address=community_name, city=None)

    if not result or 'location' not in result:
      raise ValueError(f"未找到小区: {community_name}")

    lon, lat = map(float, result['location'].split(','))

    return CommunityLocation(
      name=community_name,
      address=result['street'].join(" ") if len(result['street']) > 0 else community_name,
      lon=lon,
      lat=lat,
      city=result['city']
    )

  async def _get_poi_location(self, poi: dict, location: CommunityLocation) -> dict:
    """
    获取POI位置信息，支持多种地址查询方式
    """
    # 尝试多种地址查询方式
    address_attempts = [
      poi.get('name'),
      poi.get('address'),
      f"{poi.get('name')} {poi.get('address', '')}".strip()
    ]

    for address in address_attempts:
      if address:
        poi_geo = await self.map_client.geo(address=address, city=location.city)
        if poi_geo and 'location' in poi_geo:
          return poi_geo

    return None

  async def _search_facilities(
      self,
      location: CommunityLocation,
      keywords: List[str],
      radius: int
  ) -> List[Facility]:
    """搜索周边设施"""
    all_facilities = []
    location_str = f"{location.lon},{location.lat}"

    for keyword in keywords:
      result = await self.map_client.around_search(
        keywords=keyword,
        location=location_str,
        radius=str(radius)
      )

      if not result or not result.get('pois'):
        continue

      for poi in result['pois']:
        poi_geo = await self._get_poi_location(poi, location)
        if not poi_geo:
          continue
        poi_lon, poi_lat = map(float, poi_geo['location'].split(','))
        distance = await self.map_client.distance(location_str, poi_geo['location'])
        dis = float(distance.get('distance', 0))
        if dis > radius:
          continue

        facility = Facility(
          name=poi['name'],
          type=keyword,
          distance=dis,
          walking_time=round(float(distance.get('duration', 0)) / 60, 2),
          address=poi.get('address', ''),
          poi_id=poi['id'],
          lon=poi_lon,
          lat=poi_lat
        )
        all_facilities.append(facility)

    # 按距离排序
    all_facilities.sort(key=lambda f: f.distance)
    return all_facilities

  def _get_city(self):
    try:
      import requests
      response = requests.get('http://ip-api.com/json/')
      data = response.json()
      if data['status'] == 'success':
        print(f"当前城市: {data.get('city')}")
        return data.get('city')
    except:
      return None


if __name__ == "__main__":
  map_client = MapClient()
  analyzer = RealEstateAnalyzer(map_client)
  # results = asyncio.run(analyzer.analyze_single_community("紫薇西棠", "西安"))
  results = asyncio.run(analyzer.analyze_single_community("紫薇西棠", "北京"))
  print(results)
