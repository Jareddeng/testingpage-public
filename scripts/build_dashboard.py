#!/usr/bin/env python3
"""
AI Industry Dashboard Builder
自动抓取最新AI行业数据，生成静态看板HTML
支持：GitHub Actions定时构建 / 本地手动运行
"""

import json
import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# ============ 数据抓取层 ============

class DataFetcher:
    """数据抓取器 - 可替换为真实API"""

    def __init__(self):
        self.cache_dir = Path(__file__).parent.parent / "cache"
        self.cache_dir.mkdir(exist_ok=True)

    def fetch_all(self):
        """主入口：抓取所有数据"""
        print(f"[{datetime.now()}] 开始抓取数据...")

        data = {
            "meta": {
                "build_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0",
                "data_source": "综合研报数据 (模拟+真实框架)"
            },
            "kpis": self._fetch_kpis(),
            "reports": self._fetch_reports(),
            "market_trend": self._fetch_market_trend(),
            "region_share": self._fetch_region_share(),
            "segments": self._fetch_segments(),
            "investment": self._fetch_investment(),
            "radar": self._fetch_radar(),
            "timeline": self._fetch_timeline(),
            "facts": self._fetch_facts()
        }

        # 保存缓存
        cache_file = self.cache_dir / f"data_{datetime.now().strftime('%Y%m%d')}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"[{datetime.now()}] 数据抓取完成，已缓存至 {cache_file}")
        return data

    def _fetch_kpis(self):
        """核心KPI数据 - 此处可接入真实API"""
        # TODO: 接入真实数据源如：
        # - 中商产业研究院API
        # - IDC季度报告
        # - Wind/同花顺金融终端
        return {
            "global_market": {"value": 1839, "unit": "亿美元", "growth": "+39.7%", "cagr": "CAGR"},
            "china_market": {"value": 12534, "unit": "亿元", "growth": "+41.0%", "cagr": "YoY"},
            "investment_growth": {"value": 2859, "unit": "亿美元", "growth": "+127.5%", "cagr": "美国私人投资"},
            "model_count": {"value": 1509, "unit": "个", "growth": "全球第一", "cagr": "中国大模型数量"}
        }

    def _fetch_reports(self):
        """每日研报 - 此处可接入：
        - 券商研报API（中信证券、中金等）
        - 知识图谱/NLP自动摘要服务
        - 或配置OpenAI API自动生成摘要
        """
        # 模拟研报数据，实际可替换为真实抓取
        return [
            {
                "source": "中信证券",
                "source_short": "中信",
                "title": "AI商业化加速科技行情震荡分化",
                "category": "strategy",
                "category_label": "策略",
                "summary": "站在当前时点，AI产业进展处于早期阶段，AI带来的机遇大于挑战。视频生成模型、世界模型与物理AI等新方向层出不穷。预计模型迭代周期将持续缩短，以Anthropic为代表的模型公司ARR持续提升。",
                "date": "2026-06-02",
                "confidence": 92,
                "color": "red"
            },
            {
                "source": "Gartner",
                "source_short": "Gartner",
                "title": "2026年十大战略技术趋势：从模型崇拜到经济实用",
                "category": "tech",
                "category_label": "技术",
                "summary": "2026年AI技术趋势将从模型崇拜转向经济实用。特定领域语言模型（DSLM）凭借更高准确性、更低成本和更好合规性填补空白。预测到2028年，企业使用的生成式AI模型中将有超过半数属于特定领域模型。",
                "date": "2026-01-14",
                "confidence": 95,
                "color": "purple"
            },
            {
                "source": "中投顾问",
                "source_short": "中投",
                "title": "智能机器人：从技术验证迈向商业化落地",
                "category": "strategy",
                "category_label": "产业",
                "summary": "2026年标志着全球智能机器人产业从技术验证正式迈向商业化落地的历史性转折。预计2026年全球人形机器人出货量将突破5万台，中国市场占比提升至30%。",
                "date": "2026-05-07",
                "confidence": 88,
                "color": "green"
            },
            {
                "source": "中研普华",
                "source_short": "中研",
                "title": "AI服务器行业全景：异构计算与液冷技术双重革命",
                "category": "tech",
                "category_label": "技术",
                "summary": "AI服务器正从单一GPU架构向CPU+GPU+NPU+ASIC多元异构体系演进。液冷技术从可选配置升级为必选项，浸没式液冷使数据中心PUE值逼近理论极限。",
                "date": "2026-04-09",
                "confidence": 90,
                "color": "blue"
            },
            {
                "source": "斯坦福HAI",
                "source_short": "斯坦福",
                "title": "2026年人工智能指数报告：私人投资翻倍增长",
                "category": "strategy",
                "category_label": "数据",
                "summary": "2025年全球企业AI投资规模实现翻倍，私人领域AI投资同比增长127.5%，其中生成式AI相关投资增幅超200%。美国私人领域AI投资规模达2859亿美元，是中国的23倍。",
                "date": "2026-04-15",
                "confidence": 96,
                "color": "amber"
            }
        ]

    def _fetch_market_trend(self):
        """市场规模趋势数据"""
        return {
            "years": ["2021", "2022", "2023", "2024", "2025E", "2026E"],
            "market_size": [3100, 4200, 5300, 7470, 9800, 12534],
            "growth_rate": [35, 35, 26, 41, 31, 28]
        }

    def _fetch_region_share(self):
        """全球区域份额"""
        return [
            {"name": "北美", "value": 1151, "color": "#38bdf8"},
            {"name": "亚太", "value": 1121, "color": "#818cf8"},
            {"name": "欧洲", "value": 819, "color": "#c084fc"},
            {"name": "中东非洲", "value": 467, "color": "#fb923c"},
            {"name": "拉美", "value": 200, "color": "#4ade80"}
        ]

    def _fetch_segments(self):
        """细分赛道数据"""
        return {
            "categories": ["AI服务器", "AI芯片", "大模型服务", "AI眼镜", "智能机器人", "自动驾驶"],
            "years": ["2024", "2025E", "2026E"],
            "data": {
                "2024": [850, 420, 180, 65, 120, 380],
                "2025E": [1150, 580, 320, 95, 210, 480],
                "2026E": [1580, 820, 550, 145, 380, 620]
            }
        }

    def _fetch_investment(self):
        """投资对比数据"""
        return {
            "countries": ["美国", "中国", "英国", "德国", "法国", "日本"],
            "values": [2859, 124, 193, 149, 121, 209],
            "colors": ["#f87171", "#38bdf8", "#818cf8", "#c084fc", "#fb923c", "#4ade80"]
        }

    def _fetch_radar(self):
        """雷达图数据"""
        return {
            "indicators": [
                {"name": "技术创新", "max": 100},
                {"name": "商业化", "max": 100},
                {"name": "资本热度", "max": 100},
                {"name": "政策支持", "max": 100},
                {"name": "人才储备", "max": 100},
                {"name": "生态完善", "max": 100}
            ],
            "series": [
                {"name": "生成式AI", "value": [92, 78, 95, 88, 75, 82], "color": "#38bdf8"},
                {"name": "AI硬件", "value": [85, 65, 70, 82, 68, 60], "color": "#c084fc"},
                {"name": "AI应用", "value": [78, 88, 82, 75, 80, 85], "color": "#4ade80"}
            ]
        }

    def _fetch_timeline(self):
        """时间线事件"""
        return [
            {
                "quarter": "2026 Q1",
                "label": "已发生",
                "tag_color": "blue",
                "content": "SpaceX合并xAI，与Anthropic、谷歌达成大规模算力租赁协议"
            },
            {
                "quarter": "2026 Q2",
                "label": "进行中",
                "tag_color": "purple",
                "content": "Cursor ARR达40亿美元；中国AI大模型数量突破1500个"
            },
            {
                "quarter": "2026 H2",
                "label": "预测",
                "tag_color": "green",
                "content": "SpaceX、Anthropic、OpenAI预计IPO；人形机器人出货量突破5万台"
            },
            {
                "quarter": "2026-2030",
                "label": "展望",
                "tag_color": "orange",
                "content": "欧盟AI大陆行动计划投入2250亿美元；80%企业通过AI原生平台转型"
            }
        ]

    def _fetch_facts(self):
        """事实面板数据"""
        return {
            "penetration": [
                {"industry": "互联网", "rate": 89, "color": "#10b981"},
                {"industry": "电信", "rate": 68, "color": "#38bdf8"},
                {"industry": "政务", "rate": 65, "color": "#a855f7"},
                {"industry": "金融", "rate": 64, "color": "#f59e0b"}
            ],
            "segment_growth": [
                {"name": "AI服务器", "growth": 45, "color": "#38bdf8"},
                {"name": "AI眼镜", "growth": 38, "color": "#a855f7"},
                {"name": "人形机器人", "growth": 52, "color": "#10b981"},
                {"name": "可穿戴AI", "growth": 23, "color": "#f59e0b"}
            ],
            "investment_geo": [
                {"region": "北京", "share": 42, "color": "#ef4444"},
                {"region": "上海", "share": 24, "color": "#38bdf8"},
                {"region": "浙江", "share": 12, "color": "#10b981"},
                {"region": "广东", "share": 11, "color": "#f59e0b"}
            ]
        }


# ============ HTML构建层 ============

class DashboardBuilder:
    """看板构建器"""

    def __init__(self, data):
        self.data = data
        self.template_dir = Path(__file__).parent.parent / "templates"
        self.output_dir = Path(__file__).parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)

    def build(self):
        """构建最终HTML"""
        print(f"[{datetime.now()}] 开始构建HTML...")

        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('dashboard.html')

        html = template.render(
            meta=self.data["meta"],
            kpis=self.data["kpis"],
            reports=self.data["reports"],
            market_trend=json.dumps(self.data["market_trend"]),
            region_share=json.dumps(self.data["region_share"]),
            segments=json.dumps(self.data["segments"]),
            investment=json.dumps(self.data["investment"]),
            radar=json.dumps(self.data["radar"]),
            timeline=self.data["timeline"],
            facts=self.data["facts"]
        )

        output_path = self.output_dir / "index.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[{datetime.now()}] 构建完成: {output_path}")
        print(f"  文件大小: {len(html)} bytes")
        return output_path


# ============ 主入口 ============

def main():
    try:
        fetcher = DataFetcher()
        data = fetcher.fetch_all()

        builder = DashboardBuilder(data)
        output_path = builder.build()

        print(f"\n✅ 成功构建看板: {output_path}")
        print(f"   构建时间: {data['meta']['build_time']}")

    except Exception as e:
        print(f"\n❌ 构建失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
