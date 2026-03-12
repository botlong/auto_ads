"""
Stage 4 Rule Engine - Advanced Testing & Strategy (S075-S084)
A/B 测试引擎、线索质量闭环、战略复盘
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
from models.schemas import (
    Campaign, ABTest, LeadQuality, StrategicReview,
    FeedABTest, ROASTierTest, Stage4DiagnosisResponse
)


class Stage4Engine:
    """Stage 4 规则引擎 - 高级测试与战略"""

    def __init__(self, campaigns: List[Campaign]):
        self.campaigns = campaigns
        self.execution_time = datetime.now()

    def run_all_checks(self) -> Stage4DiagnosisResponse:
        """运行所有 Stage 4 检查"""
        ab_tests = self.run_ab_tests()
        lead_quality = self.analyze_lead_quality()
        strategic_review = self.run_strategic_review()
        feed_tests = self.run_feed_ab_tests()
        roas_tiers = self.run_roas_tier_tests()

        # 计算汇总数据
        active_tests = len([t for t in ab_tests if t.status == "RUNNING"])
        completed_tests = len([t for t in ab_tests if t.status == "COMPLETED"])

        # 计算整体线索质量
        avg_sql_rate = sum(l.sql_rate for l in lead_quality) / len(lead_quality) if lead_quality else 0
        avg_close_rate = sum(l.close_rate for l in lead_quality) / len(lead_quality) if lead_quality else 0

        return Stage4DiagnosisResponse(
            execution_time=self.execution_time,
            data_range="Last 90 Days",
            scanned_campaigns=len(self.campaigns),
            ab_tests=ab_tests,
            active_tests_count=active_tests,
            completed_tests_count=completed_tests,
            lead_quality_analysis=lead_quality,
            overall_sql_rate=avg_sql_rate,
            overall_close_rate=avg_close_rate,
            strategic_review=strategic_review,
            feed_ab_tests=feed_tests,
            roas_tier_tests=roas_tiers,
            summary={
                "ab_tests_active": active_tests,
                "ab_tests_completed": completed_tests,
                "lead_quality_campaigns": len(lead_quality),
                "sql_rate": round(avg_sql_rate * 100, 2),
                "close_rate": round(avg_close_rate * 100, 2),
                "strategic_recommendations": len(strategic_review.strategic_recommendations),
            }
        )

    # ============ S075-S076: A/B 测试引擎 ============
    def run_ab_tests(self) -> List[ABTest]:
        """S075-S076: 运行或分析 A/B 测试"""
        tests = []

        for campaign in self.campaigns:
            if campaign.status.value != "ENABLED":
                continue

            # 模拟运行中的 A/B 测试
            if campaign.ctr > 2.0:
                # Headline A/B 测试
                tests.append(ABTest(
                    test_id=f"test_{campaign.id}_headline",
                    test_name="Headline CTA 测试",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    test_type="AD_COPY",
                    control_variant="Get Started Today",
                    treatment_variant="Claim Your Free Trial",
                    status="RUNNING",
                    start_date=self.execution_time - timedelta(days=14),
                    end_date=None,
                    control_sample_size=2500,
                    treatment_sample_size=2480,
                    control_ctr=3.2,
                    treatment_ctr=3.8,
                    control_cvr=5.5,
                    treatment_cvr=6.2,
                    control_cpa=25.0,
                    treatment_cpa=22.5,
                    statistical_significance=0.03,
                    is_winner_determined=False,
                    winner_variant=None,
                    confidence_level=85.0,
                    recommendation="CONTINUE_TEST"
                ))

            # 已完成的 Bidding 测试
            if campaign.days_since_created > 60:
                tests.append(ABTest(
                    test_id=f"test_{campaign.id}_bidding",
                    test_name="tCPA vs Max Conversions",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    test_type="BIDDING",
                    control_variant="Target CPA $30",
                    treatment_variant="Maximize Conversions",
                    status="COMPLETED",
                    start_date=self.execution_time - timedelta(days=45),
                    end_date=self.execution_time - timedelta(days=5),
                    control_sample_size=5000,
                    treatment_sample_size=5200,
                    control_ctr=4.5,
                    treatment_ctr=4.3,
                    control_cvr=6.8,
                    treatment_cvr=7.5,
                    control_cpa=28.5,
                    treatment_cpa=24.2,
                    statistical_significance=0.01,
                    is_winner_determined=True,
                    winner_variant="Maximize Conversions",
                    confidence_level=95.0,
                    recommendation="IMPLEMENT"
                ))

        return tests

    # ============ S077-S079: 线索质量闭环 ============
    def analyze_lead_quality(self) -> List[LeadQuality]:
        """S077-S079: 分析线索质量"""
        lead_qualities = []

        for campaign in self.campaigns:
            # 只分析 Lead Gen 类型的 Campaign
            if campaign.business_type.value != "Lead_Gen":
                continue

            total_leads = int(campaign.conversions * 1.2)  # 假设有 20% 额外线索
            mql_count = int(total_leads * 0.7)  # 70% 是 MQL
            sql_count = int(mql_count * 0.4)   # 40% MQL 转为 SQL
            closed_won_count = int(sql_count * 0.25)  # 25% SQL 成交

            mql_rate = mql_count / total_leads if total_leads > 0 else 0
            sql_rate = sql_count / mql_count if mql_count > 0 else 0
            close_rate = closed_won_count / sql_count if sql_count > 0 else 0

            # 计算线索质量评分
            quality_score = (mql_rate * 30 + sql_rate * 40 + close_rate * 30) * 100

            # 确定质量层级
            if quality_score >= 70:
                quality_tier = "HIGH"
            elif quality_score >= 40:
                quality_tier = "MEDIUM"
            else:
                quality_tier = "LOW"

            # 生成改进建议
            suggestions = []
            if mql_rate < 0.6:
                suggestions.append("优化表单字段，提高 MQL 质量")
            if sql_rate < 0.35:
                suggestions.append("加强销售线索跟进流程")
            if close_rate < 0.2:
                suggestions.append("优化销售话术和报价策略")

            lead_qualities.append(LeadQuality(
                campaign_id=campaign.id,
                campaign_name=campaign.name,
                total_leads=total_leads,
                mql_count=mql_count,
                sql_count=sql_count,
                closed_won_count=closed_won_count,
                mql_rate=mql_rate,
                sql_rate=sql_rate,
                close_rate=close_rate,
                avg_deal_size=5000.0,
                total_pipeline_value=sql_count * 5000,
                actual_revenue=closed_won_count * 5000,
                lead_quality_score=quality_score,
                quality_tier=quality_tier,
                improvement_suggestions=suggestions
            ))

        return lead_qualities

    # ============ S080-S082: 90 天战略复盘 ============
    def run_strategic_review(self) -> StrategicReview:
        """S080-S082: 运行 90 天战略复盘"""

        # 生成 90 天趋势数据
        days = 90
        spend_trend = [random.uniform(800, 1200) for _ in range(days)]
        conversion_trend = [random.uniform(20, 45) for _ in range(days)]
        cpa_trend = [s / c if c > 0 else 0 for s, c in zip(spend_trend, conversion_trend)]
        roas_trend = [random.uniform(2.5, 4.5) for _ in range(days)]

        # Channel Mix 分析
        channel_performance = [
            {
                "channel": "Search",
                "spend_share": 45,
                "conversion_share": 52,
                "efficiency_score": 115
            },
            {
                "channel": "PMax",
                "spend_share": 35,
                "conversion_share": 38,
                "efficiency_score": 108
            },
            {
                "channel": "Display",
                "spend_share": 12,
                "conversion_share": 6,
                "efficiency_score": 50
            },
            {
                "channel": "YouTube",
                "spend_share": 8,
                "conversion_share": 4,
                "efficiency_score": 50
            }
        ]

        # 当前预算分配
        budget_allocation_current = {
            "Search": 45,
            "PMax": 35,
            "Display": 12,
            "YouTube": 8
        }

        # 建议预算分配
        budget_allocation_recommended = {
            "Search": 48,
            "PMax": 37,
            "Display": 10,
            "YouTube": 5
        }

        # 战略建议
        recommendations = [
            "增加 Search Campaign 预算 3%，ROAS 表现最佳",
            "PMax 与 Search 重叠率 25%，建议优化受众信号",
            "Display 渠道效率偏低，建议暂停低效 Placement"
        ]

        # 下季度优先级
        next_quarter_priorities = [
            "启动 Brand Awareness Campaign",
            "优化 Landing Page CVR，目标提升 15%",
            "扩展 High-Intent 关键词覆盖"
        ]

        return StrategicReview(
            review_period="2026-Q1",
            growth_metrics={
                "spend_growth": 12.5,
                "conversion_growth": 18.3,
                "cpa_improvement": -8.2,
                "roas_improvement": 5.1
            },
            spend_trend=spend_trend,
            conversion_trend=conversion_trend,
            cpa_trend=cpa_trend,
            roas_trend=roas_trend,
            channel_performance=channel_performance,
            budget_allocation_current=budget_allocation_current,
            budget_allocation_recommended=budget_allocation_recommended,
            pmax_search_overlap=25.0,
            pmax_cannibalization_rate=12.0,
            pmax_incrementality=73.0,
            strategic_recommendations=recommendations,
            next_quarter_priorities=next_quarter_priorities
        )

    # ============ S083: Feed 元素 A/B 测试 ============
    def run_feed_ab_tests(self) -> List[FeedABTest]:
        """S083: 商品 Feed A/B 测试"""
        feed_tests = []

        for campaign in self.campaigns:
            if campaign.business_type.value != "Ecommerce":
                continue

            # 模拟 Title 测试
            feed_tests.append(FeedABTest(
                test_id=f"feed_test_{campaign.id}_title",
                product_id=f"SKU_{campaign.id}_001",
                product_name=f"Product {campaign.id}",
                element_type="TITLE",
                variant_a="Wireless Bluetooth Headphones",
                variant_b="Premium Noise Cancelling Headphones - 30h Battery",
                variant_a_impressions=8500,
                variant_b_impressions=8200,
                variant_a_clicks=340,
                variant_b_clicks=410,
                variant_a_conversions=12,
                variant_b_conversions=18,
                variant_a_ctr=4.0,
                variant_b_ctr=5.0,
                winner="B",
                lift_percentage=25.0
            ))

            # 模拟 Image 测试
            feed_tests.append(FeedABTest(
                test_id=f"feed_test_{campaign.id}_image",
                product_id=f"SKU_{campaign.id}_002",
                product_name=f"Product {campaign.id} v2",
                element_type="IMAGE",
                variant_a="White Background Product Shot",
                variant_b="Lifestyle Image with Model",
                variant_a_impressions=7200,
                variant_b_impressions=7500,
                variant_a_clicks=216,
                variant_b_clicks=300,
                variant_a_conversions=8,
                variant_b_conversions=14,
                variant_a_ctr=3.0,
                variant_b_ctr=4.0,
                winner="B",
                lift_percentage=33.3
            ))

        return feed_tests

    # ============ S084: ROAS Tier Testing ============
    def run_roas_tier_tests(self) -> List[ROASTierTest]:
        """S084: ROAS 分层测试"""
        tiers = []

        for campaign in self.campaigns:
            target_roas = campaign.target_roas or 3.0
            actual_roas = campaign.actual_roas

            # High ROAS Tier
            if actual_roas > target_roas * 1.2:
                tiers.append(ROASTierTest(
                    tier_id=f"tier_{campaign.id}_high",
                    tier_name="High ROAS",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    roas_min=target_roas * 1.2,
                    roas_max=10.0,
                    current_roas=actual_roas,
                    current_spend=campaign.cost,
                    current_conversions=int(campaign.conversions),
                    test_strategy="BUDGET_INCREASE",
                    expected_outcome="保持高 ROAS 的同时提升转化量",
                    test_result="成功",
                    actual_lift=15.0
                ))

            # Low ROAS Tier
            elif actual_roas < target_roas * 0.8:
                tiers.append(ROASTierTest(
                    tier_id=f"tier_{campaign.id}_low",
                    tier_name="Low ROAS",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    roas_min=0.5,
                    roas_max=target_roas * 0.8,
                    current_roas=actual_roas,
                    current_spend=campaign.cost,
                    current_conversions=int(campaign.conversions),
                    test_strategy="BID_ADJUST",
                    expected_outcome="降低出价以改善 ROAS",
                    test_result="进行中",
                    actual_lift=0.0
                ))

        return tiers
