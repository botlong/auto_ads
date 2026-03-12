"""
假数据生成器
模拟 Google Ads API 返回的真实数据结构
"""

from datetime import datetime, timedelta
from typing import List
import random

from models.schemas import (
    Campaign, CampaignStatus, BiddingType, LearningStatus, BusinessType,
    ConversionTracking, ConversionAction,
    Alert,
    # Stage 2 models
    SearchTerm, Keyword, AdAsset, ResponsiveSearchAd,
    Asset, LocationPerformance, AudiencePerformance,
    DevicePerformance, HourlyPerformance, AuctionInsight,
    # S024-S053 models
    LandingPageHealth, QualityScoreDiagnosis, PolicyStatus,
    ProductFeedItem
)


class MockDataSource:
    """模拟数据源 - 生成各种场景的测试数据"""

    def __init__(self):
        self.campaigns = self._generate_campaigns()
        self.conversion_tracking = self._generate_conversion_tracking()
        self.alerts = self._generate_alerts()

    def _generate_campaigns(self) -> List[Campaign]:
        """生成模拟 Campaign 数据 - 包含各种典型场景"""

        campaigns = [
            # ===== 场景 1: 表现优秀的 Brand Campaign =====
            Campaign(
                id="c_001",
                name="US_Search_Brand",
                status=CampaignStatus.ENABLED,
                bidding_strategy_type=BiddingType.TARGET_CPA,
                target_cpa=25.0,
                cost=1250.0,
                conversions=52,
                conversion_value=0,  # Lead Gen 无转化价值
                clicks=850,
                impressions=12500,
                ctr=6.8,
                cvr=6.12,
                cpc=1.47,
                search_impression_share=85.0,
                search_budget_lost_impression_share=5.0,
                search_rank_lost_impression_share=10.0,
                budget=150.0,
                actual_cpa=24.04,
                actual_roas=0,
                learning_status=LearningStatus.READY,
                days_since_created=45,
                is_brand_campaign=True,
                has_nonbrand_keywords=False,
                network_type="SEARCH",
                adgroup_count=3,
                business_type=BusinessType.LEAD_GEN
            ),

            # ===== 场景 2: 预算受限的高效 Campaign =====
            Campaign(
                id="c_002",
                name="US_Search_NonBrand_HighIntent",
                status=CampaignStatus.ENABLED,
                bidding_strategy_type=BiddingType.TARGET_ROAS,
                target_roas=3.5,
                cost=3200.0,
                conversions=128,
                conversion_value=14500.0,
                clicks=2100,
                impressions=28500,
                ctr=7.37,
                cvr=6.1,
                cpc=1.52,
                search_impression_share=45.0,  # 低展示份额
                search_budget_lost_impression_share=35.0,  # 大量预算丢失 - 需要增加预算
                search_rank_lost_impression_share=20.0,
                budget=200.0,
                actual_cpa=0,  # Ecommerce 关注ROAS
                actual_roas=4.53,  # ROAS 超过目标
                learning_status=LearningStatus.READY,
                days_since_created=60,
                is_brand_campaign=False,
                network_type="SEARCH",
                adgroup_count=8,
                business_type=BusinessType.ECOMMERCE
            ),

            # ===== 场景 3: 表现不佳需要优化 =====
            Campaign(
                id="c_003",
                name="US_Search_Generic",
                status=CampaignStatus.ENABLED,
                bidding_strategy_type=BiddingType.TARGET_CPA,
                target_cpa=30.0,
                cost=2800.0,
                conversions=45,
                conversion_value=0,
                clicks=1800,
                impressions=45000,
                ctr=4.0,
                cvr=2.5,
                cpc=1.56,
                search_impression_share=65.0,
                search_budget_lost_impression_share=15.0,
                search_rank_lost_impression_share=20.0,
                budget=250.0,
                actual_cpa=62.22,  # CPA 超过目标2倍
                actual_roas=0,
                learning_status=LearningStatus.LEARNING,  # 学习中 - 不应调整
                days_since_created=5,  # 新 campaign - 受保护
                is_brand_campaign=False,
                network_type="SEARCH",
                adgroup_count=12,  # AdGroup 过多 - 结构问题
                business_type=BusinessType.LEAD_GEN
            ),

            # ===== 场景 4: 学习目标过严 =====
            Campaign(
                id="c_004",
                name="US_PMax_Product",
                status=CampaignStatus.ENABLED,
                bidding_strategy_type=BiddingType.TARGET_ROAS,
                target_roas=8.0,  # 目标过高
                cost=1500.0,
                conversions=35,
                conversion_value=4200.0,
                clicks=1200,
                impressions=15000,
                ctr=8.0,
                cvr=2.92,
                cpc=1.25,
                search_impression_share=25.0,  # 展示份额低
                search_budget_lost_impression_share=10.0,
                search_rank_lost_impression_share=65.0,  # 大量排名丢失
                budget=180.0,
                actual_cpa=0,
                actual_roas=2.8,  # ROAS 低于目标
                learning_status=LearningStatus.MISCONFIGURED,
                days_since_created=30,
                is_brand_campaign=False,
                network_type="PMAX",
                adgroup_count=1,
                business_type=BusinessType.ECOMMERCE
            ),

            # ===== 场景 5: 网络混杂问题 =====
            Campaign(
                id="c_005",
                name="US_Search_Display_Mixed",
                status=CampaignStatus.ENABLED,
                bidding_strategy_type=BiddingType.TARGET_CPA,
                target_cpa=35.0,
                cost=1800.0,
                conversions=28,
                conversion_value=0,
                clicks=2200,
                impressions=85000,  # 展示量异常高 - 可能是展示网络
                ctr=2.59,  # CTR 低
                cvr=1.27,
                cpc=0.82,
                search_impression_share=70.0,
                search_budget_lost_impression_share=10.0,
                search_rank_lost_impression_share=20.0,
                budget=220.0,
                actual_cpa=64.29,
                actual_roas=0,
                learning_status=LearningStatus.READY,
                days_since_created=90,
                is_brand_campaign=False,
                network_type="SEARCH_WITH_DISPLAY",  # 混杂网络
                adgroup_count=5,
                business_type=BusinessType.LEAD_GEN
            ),

            # ===== 场景 6: 暂停的 Campaign =====
            Campaign(
                id="c_006",
                name="US_Search_Paused",
                status=CampaignStatus.PAUSED,
                bidding_strategy_type=BiddingType.MANUAL_CPC,
                cost=0,
                conversions=0,
                conversion_value=0,
                clicks=0,
                impressions=0,
                ctr=0,
                cvr=0,
                cpc=0,
                search_impression_share=0,
                search_budget_lost_impression_share=0,
                search_rank_lost_impression_share=0,
                budget=100.0,
                actual_cpa=0,
                actual_roas=0,
                learning_status=LearningStatus.READY,
                days_since_created=120,
                is_brand_campaign=False,
                network_type="SEARCH",
                adgroup_count=4,
                business_type=BusinessType.LEAD_GEN
            ),

            # ===== 场景 7: 目标与业务不匹配 =====
            Campaign(
                id="c_007",
                name="US_LeadGen_MaxConv",
                status=CampaignStatus.ENABLED,
                bidding_strategy_type=BiddingType.MAXIMIZE_CONVERSIONS,  # Lead Gen 用 Max Conv
                cost=2200.0,
                conversions=75,
                conversion_value=0,
                clicks=1650,
                impressions=22000,
                ctr=7.5,
                cvr=4.55,
                cpc=1.33,
                search_impression_share=55.0,
                search_budget_lost_impression_share=25.0,
                search_rank_lost_impression_share=20.0,
                budget=280.0,
                actual_cpa=29.33,
                actual_roas=0,
                learning_status=LearningStatus.READY,
                days_since_created=75,
                is_brand_campaign=False,
                network_type="SEARCH",
                adgroup_count=6,
                business_type=BusinessType.LEAD_GEN
            ),

            # ===== 场景 8: 电商使用 tCPA (不匹配) =====
            Campaign(
                id="c_008",
                name="US_Ecommerce_tCPA",
                status=CampaignStatus.ENABLED,
                bidding_strategy_type=BiddingType.TARGET_CPA,  # Ecommerce 应该用 ROAS
                target_cpa=50.0,
                cost=3500.0,
                conversions=45,
                conversion_value=9800.0,
                clicks=2400,
                impressions=32000,
                ctr=7.5,
                cvr=1.88,
                cpc=1.46,
                search_impression_share=60.0,
                search_budget_lost_impression_share=20.0,
                search_rank_lost_impression_share=20.0,
                budget=300.0,
                actual_cpa=77.78,
                actual_roas=2.8,
                learning_status=LearningStatus.READY,
                days_since_created=100,
                is_brand_campaign=False,
                network_type="SEARCH",
                adgroup_count=10,
                business_type=BusinessType.ECOMMERCE
            ),
        ]

        return campaigns

    def _generate_conversion_tracking(self) -> ConversionTracking:
        """生成转化追踪配置 - 包含一些问题"""

        actions = [
            ConversionAction(
                id="conv_001",
                name="Purchase",
                category="PURCHASE",
                is_primary=True,
                count_type="EVERY",
                value_type="DYNAMIC",
                value=None,
                status="ENABLED",
                tag_status="ACTIVE"
            ),
            ConversionAction(
                id="conv_002",
                name="Lead Form Submit",
                category="SUBMIT_LEAD_FORM",
                is_primary=True,  # 问题：与 Purchase 同为 Primary
                count_type="ONE",
                value_type="STATIC",
                value=50.0,
                status="ENABLED",
                tag_status="ACTIVE"
            ),
            ConversionAction(
                id="conv_003",
                name="Phone Call",
                category="PHONE_CALL",
                is_primary=False,
                count_type="ONE",
                value_type="STATIC",
                value=30.0,
                status="ENABLED",
                tag_status="UNVERIFIED"  # 问题：Tag 未验证
            ),
            ConversionAction(
                id="conv_004",
                name="Page View (Backup)",
                category="PAGE_VIEW",
                is_primary=False,
                count_type="EVERY",  # 问题：Page View 设为 Every 会导致重复计数
                value_type="STATIC",
                value=0.0,  # 问题：Purchase 类转化为 0 值
                status="ENABLED",
                tag_status="INACTIVE"  # 问题：Tag 失效
            ),
        ]

        return ConversionTracking(
            account_id="acc_123456",
            account_name="Demo Account - US Market",
            conversion_actions=actions,
            enhanced_conversions_enabled=True,
            enhanced_conversions_for_leads=False,  # 问题：Lead Gen 应启用
            global_site_tag_status="ACTIVE",
            conversion_linker_status="ACTIVE",
            last_conversion_time=datetime.now() - timedelta(hours=2),
            conversion_delay_hours=24,
            duplicate_primary_conversions=True,
            zero_value_purchase=False,
            inactive_tags=["conv_004"]
        )

    def _generate_alerts(self) -> List[Alert]:
        """生成模拟告警"""
        return [
            Alert(
                id="alert_001",
                level="P0",
                title="转化标签失效",
                message="Conversion Action 'Page View (Backup)' 的 Tag 状态为 INACTIVE",
                campaign_id=None,
                campaign_name=None,
                created_at=datetime.now() - timedelta(hours=2),
                is_resolved=False
            ),
            Alert(
                id="alert_002",
                level="P1",
                title="预算受限导致展示丢失",
                message="Campaign 'US_Search_NonBrand_HighIntent' 因预算丢失 35% 展示份额",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                created_at=datetime.now() - timedelta(hours=5),
                is_resolved=False
            ),
            Alert(
                id="alert_003",
                level="P1",
                title="CPA 严重超标",
                message="Campaign 'US_Search_Generic' CPA $62.22 超过目标 $30.00 107%",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                created_at=datetime.now() - timedelta(hours=8),
                is_resolved=False
            ),
        ]

    def get_campaigns(self) -> List[Campaign]:
        """获取所有 Campaign"""
        return self.campaigns

    def get_conversion_tracking(self) -> ConversionTracking:
        """获取转化追踪配置"""
        return self.conversion_tracking

    def get_mock_alerts(self) -> List[Alert]:
        """获取模拟告警"""
        return self.alerts

    # ============ Stage 2: 组件级优化数据 ============

    def get_search_terms(self, campaign_id: str = None) -> List[SearchTerm]:
        """S012-S014: 生成搜索词数据 - 包含浪费词和高意图词"""
        search_terms = [
            # ===== 高花费无转化词 (应添加为负向) =====
            SearchTerm(
                id="st_001",
                search_term="free google ads tool",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                adgroup_id="ag_001",
                adgroup_name="Generic Keywords",
                cost=85.50,
                clicks=45,
                impressions=320,
                ctr=14.06,
                conversions=0,
                cpa=0,
                match_type="BROAD",
                keyword_text="google ads",
                is_negative_candidate=True,
                is_high_intent=False,
                negative_reason="高花费($85.50)无转化，包含'free'表示低购买意向"
            ),
            SearchTerm(
                id="st_002",
                search_term="how to do marketing",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                adgroup_id="ag_001",
                adgroup_name="Generic Keywords",
                cost=62.30,
                clicks=38,
                impressions=450,
                ctr=8.44,
                conversions=0,
                cpa=0,
                match_type="BROAD",
                keyword_text="marketing",
                is_negative_candidate=True,
                is_high_intent=False,
                negative_reason="信息类查询，无购买意向，花费$62.30"
            ),
            # ===== 高意图有转化词 (应提炼为Exact) =====
            SearchTerm(
                id="st_003",
                search_term="best google ads agency near me",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                adgroup_id="ag_002",
                adgroup_name="Agency Keywords",
                cost=45.20,
                clicks=12,
                impressions=45,
                ctr=26.67,
                conversions=3,
                cpa=15.07,
                match_type="BROAD",
                keyword_text="google ads agency",
                is_negative_candidate=False,
                is_high_intent=True,
                negative_reason=None
            ),
            SearchTerm(
                id="st_004",
                search_term="hire ppc expert",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                adgroup_id="ag_002",
                adgroup_name="Agency Keywords",
                cost=78.90,
                clicks=22,
                impressions=88,
                ctr=25.0,
                conversions=4,
                cpa=19.73,
                match_type="PHRASE",
                keyword_text="ppc expert",
                is_negative_candidate=False,
                is_high_intent=True,
                negative_reason=None
            ),
            # ===== CTR异常低的词 =====
            SearchTerm(
                id="st_005",
                search_term="ads google what is",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                adgroup_id="ag_001",
                adgroup_name="Generic Keywords",
                cost=32.10,
                clicks=15,
                impressions=680,
                ctr=2.21,
                conversions=0,
                cpa=0,
                match_type="BROAD",
                keyword_text="google ads",
                is_negative_candidate=True,
                is_high_intent=False,
                negative_reason="CTR异常低(2.21%)，词序混乱，意图不相关"
            ),
        ]

        if campaign_id:
            return [st for st in search_terms if st.campaign_id == campaign_id]
        return search_terms

    def get_keywords(self, campaign_id: str = None) -> List[Keyword]:
        """S015-S017: 生成关键词数据 - 包含低效词和质量得分问题"""
        keywords = [
            # ===== 高花费无转化关键词 (应暂停) =====
            Keyword(
                id="kw_001",
                text="marketing tips",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                adgroup_id="ag_001",
                adgroup_name="Generic Keywords",
                match_type="BROAD",
                status="ENABLED",
                cost=245.80,
                clicks=156,
                impressions=2100,
                ctr=7.43,
                cvr=0,
                cpc=1.58,
                conversions=0,
                quality_score=4,
                ad_relevance="AVERAGE",
                lp_experience="AVERAGE",
                expected_ctr="BELOW_AVERAGE",
                cpc_bid=2.50,
                first_page_cpc=1.20,
                top_of_page_cpc=2.80,
                is_underperforming=True,
                action_recommended="PAUSE"
            ),
            Keyword(
                id="kw_002",
                text="digital marketing guide",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                adgroup_id="ag_001",
                adgroup_name="Generic Keywords",
                match_type="BROAD",
                status="ENABLED",
                cost=198.40,
                clicks=124,
                impressions=1850,
                ctr=6.70,
                cvr=0.81,
                cpc=1.60,
                conversions=1,
                quality_score=3,
                ad_relevance="BELOW_AVERAGE",
                lp_experience="AVERAGE",
                expected_ctr="BELOW_AVERAGE",
                cpc_bid=2.80,
                first_page_cpc=1.50,
                top_of_page_cpc=3.20,
                is_underperforming=True,
                action_recommended="REFINE_MATCH"
            ),
            # ===== 高质量得分高效关键词 =====
            Keyword(
                id="kw_003",
                text="google ads management agency",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                adgroup_id="ag_002",
                adgroup_name="Agency Keywords",
                match_type="PHRASE",
                status="ENABLED",
                cost=320.50,
                clicks=85,
                impressions=340,
                ctr=25.0,
                cvr=12.94,
                cpc=3.77,
                conversions=11,
                quality_score=8,
                ad_relevance="ABOVE_AVERAGE",
                lp_experience="ABOVE_AVERAGE",
                expected_ctr="ABOVE_AVERAGE",
                cpc_bid=4.50,
                first_page_cpc=3.20,
                top_of_page_cpc=5.80,
                is_underperforming=False,
                action_recommended=None
            ),
            # ===== QS < 4 需要优化的关键词 =====
            Keyword(
                id="kw_004",
                text="cheap advertising",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                adgroup_id="ag_001",
                adgroup_name="Generic Keywords",
                match_type="BROAD",
                status="ENABLED",
                cost=156.30,
                clicks=98,
                impressions=1650,
                ctr=5.94,
                cvr=0,
                cpc=1.60,
                conversions=0,
                quality_score=2,
                ad_relevance="BELOW_AVERAGE",
                lp_experience="BELOW_AVERAGE",
                expected_ctr="BELOW_AVERAGE",
                cpc_bid=3.20,
                first_page_cpc=2.10,
                top_of_page_cpc=4.50,
                is_underperforming=True,
                action_recommended="IMPROVE_QS"
            ),
        ]

        if campaign_id:
            return [k for k in keywords if k.campaign_id == campaign_id]
        return keywords

    def get_ads(self, campaign_id: str = None) -> List[ResponsiveSearchAd]:
        """S018-S020: 生成广告文案数据 - 包含Ad Strength问题和拒登"""
        ads = [
            ResponsiveSearchAd(
                id="ad_001",
                campaign_id="c_001",
                campaign_name="US_Search_Brand",
                adgroup_id="ag_001",
                adgroup_name="Brand Terms",
                status="ENABLED",
                approval_status="APPROVED",
                headlines=[
                    AdAsset(text="Premium Agency", pinned=False, performance_label="GOOD"),
                    AdAsset(text="Google Ads Experts", pinned=False, performance_label="BEST"),
                    AdAsset(text="Get More Leads", pinned=False, performance_label="GOOD"),
                    AdAsset(text="Free Audit", pinned=True, pin_position=1, performance_label="LOW"),
                ],
                descriptions=[
                    AdAsset(text="We help businesses grow with data-driven Google Ads strategies.", pinned=False, performance_label="GOOD"),
                    AdAsset(text="Certified Google Partner with 10+ years experience.", pinned=False, performance_label="BEST"),
                ],
                ctr=8.5,
                cvr=6.2,
                impressions=5200,
                clicks=442,
                conversions=27,
                ad_strength="GOOD",
                ad_strength_rating=3,
                issues=[]
            ),
            ResponsiveSearchAd(
                id="ad_002",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                adgroup_id="ag_001",
                adgroup_name="Generic Keywords",
                status="ENABLED",
                approval_status="APPROVED",
                headlines=[
                    AdAsset(text="Digital Marketing", pinned=False, performance_label="LOW"),
                    AdAsset(text="Best Services", pinned=False, performance_label="AVERAGE"),
                ],
                descriptions=[
                    AdAsset(text="We offer marketing services.", pinned=False, performance_label="LOW"),
                ],
                ctr=3.2,
                cvr=1.5,
                impressions=8400,
                clicks=269,
                conversions=4,
                ad_strength="POOR",
                ad_strength_rating=1,
                issues=["HEADLINE_COUNT_LOW", "DESCRIPTION_COUNT_LOW", "LOW_PERFORMING_ASSETS"]
            ),
            ResponsiveSearchAd(
                id="ad_003",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                adgroup_id="ag_002",
                adgroup_name="Agency Keywords",
                status="PAUSED",
                approval_status="DISAPPROVED",
                headlines=[
                    AdAsset(text="#1 Agency Guarantee", pinned=False, performance_label="LOW"),
                ],
                descriptions=[
                    AdAsset(text="We are the best agency guaranteed results or money back.", pinned=False, performance_label="LOW"),
                ],
                ctr=0,
                cvr=0,
                impressions=0,
                clicks=0,
                conversions=0,
                ad_strength="POOR",
                ad_strength_rating=1,
                issues=["DISAPPROVED", "MISLEADING_CONTENT"]
            ),
        ]

        if campaign_id:
            return [ad for ad in ads if ad.campaign_id == campaign_id]
        return ads

    def get_assets(self, campaign_id: str = None) -> List[Asset]:
        """S021-S023: 生成Asset数据 - 包含缺失和低效资源"""
        return [
            Asset(
                id="asset_001",
                type="SITELINK",
                status="ENABLED",
                performance_label="GOOD",
                sitelink_text="Our Services",
                sitelink_url="/services",
                impressions=4200,
                clicks=168,
                days_since_updated=15
            ),
            Asset(
                id="asset_002",
                type="SITELINK",
                status="ENABLED",
                performance_label="LOW",
                sitelink_text="About Us",
                sitelink_url="/about",
                impressions=1200,
                clicks=12,
                days_since_updated=180
            ),
            Asset(
                id="asset_003",
                type="CALLOUT",
                status="ENABLED",
                performance_label="BEST",
                callout_text="Free Consultation",
                impressions=6800,
                clicks=0,
                days_since_updated=30
            ),
            # 缺失 Lead Form Asset - 应在诊断中标记
        ]

    def get_audiences(self, campaign_id: str = None) -> List[AudiencePerformance]:
        """S029-S032: 生成受众表现数据"""
        audiences = [
            AudiencePerformance(
                id="aud_001",
                audience_name="Website Visitors (30d)",
                audience_type="REMARKETING",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                audience_size=15000,
                targeting_setting="TARGETING",
                cost=450.20,
                clicks=85,
                impressions=850,
                ctr=10.0,
                conversions=12,
                cpa=37.52,
                bid_modifier=0,
                is_underperforming=False,
                recommended_action=None
            ),
            AudiencePerformance(
                id="aud_002",
                audience_name="Similar Audiences",
                audience_type="SIMILAR",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                audience_size=85000,
                targeting_setting="OBSERVATION",
                cost=320.50,
                clicks=62,
                impressions=720,
                ctr=8.61,
                conversions=8,
                cpa=40.06,
                bid_modifier=10,
                is_underperforming=False,
                recommended_action=None
            ),
            AudiencePerformance(
                id="aud_003",
                audience_name="In-Market: Business Services",
                audience_type="IN_MARKET",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                audience_size=125000,
                targeting_setting="TARGETING",
                cost=580.80,
                clicks=95,
                impressions=1200,
                ctr=7.92,
                conversions=2,
                cpa=290.40,
                bid_modifier=0,
                is_underperforming=True,
                recommended_action="EXCLUDE"
            ),
        ]

        if campaign_id:
            return [a for a in audiences if a.campaign_id == campaign_id]
        return audiences

    def get_locations(self, campaign_id: str = None) -> List[LocationPerformance]:
        """S026-S028: 生成地域表现数据"""
        locations = [
            LocationPerformance(
                id="loc_001",
                location_name="California",
                location_type="TARGETED",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                cost=850.40,
                clicks=220,
                impressions=1450,
                ctr=15.17,
                conversions=28,
                cpa=30.37,
                roas=4.2,
                bid_modifier=0,
                is_underperforming=False,
                is_outperforming=True,
                recommended_action=None
            ),
            LocationPerformance(
                id="loc_002",
                location_name="New York",
                location_type="TARGETED",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                cost=920.60,
                clicks=245,
                impressions=1680,
                ctr=14.58,
                conversions=31,
                cpa=29.70,
                roas=4.5,
                bid_modifier=0,
                is_underperforming=False,
                is_outperforming=True,
                recommended_action=None
            ),
            LocationPerformance(
                id="loc_003",
                location_name="Texas",
                location_type="TARGETED",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                cost=420.80,
                clicks=165,
                impressions=1980,
                ctr=8.33,
                conversions=2,
                cpa=210.40,
                roas=0,
                bid_modifier=0,
                is_underperforming=True,
                is_outperforming=False,
                recommended_action="EXCLUDE"
            ),
            LocationPerformance(
                id="loc_004",
                location_name="Florida",
                location_type="TARGETED",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                cost=380.50,
                clicks=142,
                impressions=1750,
                ctr=8.11,
                conversions=0,
                cpa=0,
                roas=0,
                bid_modifier=0,
                is_underperforming=True,
                is_outperforming=False,
                recommended_action="EXCLUDE"
            ),
        ]

        if campaign_id:
            return [loc for loc in locations if loc.campaign_id == campaign_id]
        return locations

    def get_devices(self, campaign_id: str = None) -> List[DevicePerformance]:
        """S033-S034: 生成设备表现数据"""
        devices = [
            DevicePerformance(
                device_type="DESKTOP",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                cost=1850.40,
                clicks=480,
                impressions=2800,
                ctr=17.14,
                conversions=62,
                cpa=29.85,
                cvr=12.92,
                bid_modifier=0,
                mobile_cvr_gap=None,
                is_underperforming=False,
                recommended_action=None
            ),
            DevicePerformance(
                device_type="MOBILE",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                cost=920.20,
                clicks=280,
                impressions=2100,
                ctr=13.33,
                conversions=18,
                cpa=51.12,
                cvr=6.43,
                bid_modifier=-20,
                mobile_cvr_gap=-50.2,
                is_underperforming=True,
                recommended_action="REDUCE_BID"
            ),
            DevicePerformance(
                device_type="TABLET",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                cost=85.40,
                clicks=32,
                impressions=320,
                ctr=10.0,
                conversions=1,
                cpa=85.40,
                cvr=3.13,
                bid_modifier=-40,
                mobile_cvr_gap=None,
                is_underperforming=True,
                recommended_action="REDUCE_BID"
            ),
        ]

        if campaign_id:
            return [d for d in devices if d.campaign_id == campaign_id]
        return devices

    def get_hourly_performance(self, campaign_id: str = None) -> List[HourlyPerformance]:
        """S035-S036: 生成分时段表现数据"""
        hourly_data = []

        # 高效时段: 工作日 9-17点
        for day in range(5):  # Mon-Fri
            for hour in range(9, 18):
                hourly_data.append(HourlyPerformance(
                    day_of_week=day,
                    hour_of_day=hour,
                    campaign_id="c_002",
                    campaign_name="US_Search_NonBrand_HighIntent",
                    cost=random.uniform(15, 35),
                    clicks=random.randint(8, 18),
                    impressions=random.randint(60, 120),
                    conversions=random.uniform(0.5, 2.0),
                    cpa=random.uniform(18, 28),
                    cvr=random.uniform(8, 15),
                    bid_modifier=0,
                    is_high_performance=True,
                    is_low_performance=False,
                    recommended_action="INCREASE_BID"
                ))

        # 低效时段: 凌晨 0-6点
        for day in range(7):  # All days
            for hour in range(0, 7):
                hourly_data.append(HourlyPerformance(
                    day_of_week=day,
                    hour_of_day=hour,
                    campaign_id="c_003",
                    campaign_name="US_Search_Generic",
                    cost=random.uniform(20, 40),
                    clicks=random.randint(5, 12),
                    impressions=random.randint(80, 150),
                    conversions=0,
                    cpa=0,
                    cvr=0,
                    bid_modifier=0,
                    is_high_performance=False,
                    is_low_performance=True,
                    recommended_action="PAUSE"
                ))

        if campaign_id:
            return [h for h in hourly_data if h.campaign_id == campaign_id]
        return hourly_data[:48]  # 限制返回数量

    def get_auction_insights(self, campaign_id: str = None) -> List[AuctionInsight]:
        """S037: 生成竞品拍卖洞察数据"""
        insights = [
            AuctionInsight(
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                domain="competitor-a.com",
                impression_share=65.0,
                overlap_rate=45.0,
                position_above_rate=35.0,
                top_of_page_rate=55.0,
                outranking_share=40.0,
                is_main_competitor=True,
                threat_level="HIGH"
            ),
            AuctionInsight(
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                domain="competitor-b.com",
                impression_share=42.0,
                overlap_rate=28.0,
                position_above_rate=22.0,
                top_of_page_rate=38.0,
                outranking_share=58.0,
                is_main_competitor=True,
                threat_level="MEDIUM"
            ),
            AuctionInsight(
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand_HighIntent",
                domain="small-player.com",
                impression_share=12.0,
                overlap_rate=8.0,
                position_above_rate=5.0,
                top_of_page_rate=10.0,
                outranking_share=85.0,
                is_main_competitor=False,
                threat_level="LOW"
            ),
        ]

        if campaign_id:
            return [ai for ai in insights if ai.campaign_id == campaign_id]
        return insights

    # ============ S024: Landing Page 健康检查 ============
    def get_landing_page_health(self, campaign_id: str = None) -> List[LandingPageHealth]:
        """S024: 生成落地页健康数据"""
        from datetime import datetime

        landing_pages = [
            # 正常落地页
            LandingPageHealth(
                url="https://example.com/landing-page-1",
                campaign_id="c_001",
                campaign_name="US_Search_Brand",
                http_status=200,
                is_accessible=True,
                load_time_seconds=2.1,
                mobile_load_time_seconds=2.5,
                bounce_rate=45.0,
                mobile_bounce_rate=48.0,
                search_term_match_rate=65.0,
                engagement_rate=35.0,
                cvr=8.5,
                mobile_friendly=True,
                last_checked=datetime.now()
            ),
            # HTTP 404 错误 (P0)
            LandingPageHealth(
                url="https://example.com/broken-page",
                campaign_id="c_002",
                campaign_name="US_Search_NonBrand",
                http_status=404,
                is_accessible=False,
                load_time_seconds=0.0,
                mobile_load_time_seconds=0.0,
                bounce_rate=100.0,
                mobile_bounce_rate=100.0,
                search_term_match_rate=0.0,
                engagement_rate=0.0,
                cvr=0.0,
                mobile_friendly=False,
                last_checked=datetime.now()
            ),
            # 加载缓慢 (P1)
            LandingPageHealth(
                url="https://example.com/slow-page",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                http_status=200,
                is_accessible=True,
                load_time_seconds=5.2,
                mobile_load_time_seconds=6.8,
                bounce_rate=78.0,
                mobile_bounce_rate=82.0,
                search_term_match_rate=25.0,
                engagement_rate=15.0,
                cvr=2.1,
                mobile_friendly=True,
                last_checked=datetime.now()
            ),
            # 高互动低转化 (P1)
            LandingPageHealth(
                url="https://example.com/high-engagement-low-cvr",
                campaign_id="c_004",
                campaign_name="US_PMax_Product",
                http_status=200,
                is_accessible=True,
                load_time_seconds=1.8,
                mobile_load_time_seconds=2.2,
                bounce_rate=35.0,
                mobile_bounce_rate=38.0,
                search_term_match_rate=70.0,
                engagement_rate=65.0,  # 高互动
                cvr=1.2,  # 但低转化
                mobile_friendly=True,
                last_checked=datetime.now()
            ),
        ]

        if campaign_id:
            return [lp for lp in landing_pages if lp.campaign_id == campaign_id]
        return landing_pages

    # ============ S025: Quality Score 详细诊断 ============
    def get_quality_score_diagnosis(self, campaign_id: str = None) -> List[QualityScoreDiagnosis]:
        """S025: 生成 Quality Score 详细诊断数据"""

        diagnoses = [
            # Ad Relevance 低
            QualityScoreDiagnosis(
                keyword_id="kw_001",
                keyword_text="marketing software",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                quality_score=3,
                ad_relevance="BELOW_AVERAGE",
                landing_page_experience="AVERAGE",
                expected_ctr="AVERAGE",
                historical_cpc_avg=1.2,
                current_cpc=2.1,
                cpc_increase_ratio=1.75,  # CPC 上涨 75%
                issues=["AD_RELEVANCE_LOW"],
                fix_priority="P1"
            ),
            # LP Experience 低
            QualityScoreDiagnosis(
                keyword_id="kw_002",
                keyword_text="digital marketing guide",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                quality_score=2,
                ad_relevance="AVERAGE",
                landing_page_experience="BELOW_AVERAGE",
                expected_ctr="BELOW_AVERAGE",
                historical_cpc_avg=0.8,
                current_cpc=1.8,
                cpc_increase_ratio=2.25,  # CPC 上涨 125%
                issues=["LP_EXPERIENCE_LOW", "EXPECTED_CTR_LOW"],
                fix_priority="P0"
            ),
            # QS 低且 CPC 高
            QualityScoreDiagnosis(
                keyword_id="kw_003",
                keyword_text="cheap advertising",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                quality_score=2,
                ad_relevance="BELOW_AVERAGE",
                landing_page_experience="BELOW_AVERAGE",
                expected_ctr="BELOW_AVERAGE",
                historical_cpc_avg=0.5,
                current_cpc=1.6,
                cpc_increase_ratio=3.2,  # CPC 上涨 220%
                issues=["AD_RELEVANCE_LOW", "LP_EXPERIENCE_LOW", "EXPECTED_CTR_LOW"],
                fix_priority="P0"
            ),
        ]

        if campaign_id:
            return [d for d in diagnoses if d.campaign_id == campaign_id]
        return diagnoses

    # ============ S038: 政策审核状态 ============
    def get_policy_status(self, campaign_id: str = None) -> PolicyStatus:
        """S038: 生成政策合规状态"""

        # 模拟 c_003 有政策违规
        if campaign_id == "c_003":
            return PolicyStatus(
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                approval_status="DISAPPROVED",
                disapproval_reasons=["误导性声明", "不允许的内容"],
                asset_issues=[
                    {"asset_id": "asset_001", "issue": "图片包含过多文字"},
                    {"asset_id": "asset_003", "issue": "声明未经证实"}
                ],
                broken_urls=["https://example.com/broken-link"],
                enabled_no_impressions=True,
                no_impression_hours=96
            )

        # 默认正常状态
        return PolicyStatus(
            campaign_id=campaign_id or "c_001",
            campaign_name="US_Search_Brand",
            approval_status="APPROVED",
            disapproval_reasons=[],
            asset_issues=[],
            broken_urls=[],
            enabled_no_impressions=False,
            no_impression_hours=0
        )

    # ============ S039-S053: 电商专项 - 商品 Feed ============
    def get_product_feed(self, campaign_id: str = None) -> List[ProductFeedItem]:
        """S039-S053: 生成商品 Feed 数据"""

        products = [
            # Hero 商品 - 高 ROAS
            ProductFeedItem(
                product_id="prod_001",
                product_name="Pro Marketing Software Suite",
                status="ACTIVE",
                title="专业营销软件套件 - 年度订阅",
                description="完整营销自动化解决方案，包含邮件营销、社交媒体管理、数据分析",
                image_url="https://example.com/images/pro-suite.jpg",
                price=299.0,
                availability="IN_STOCK",
                brand="MarketingPro",
                gtin="1234567890123",
                mpn="MP-PRO-001",
                impressions=15000,
                clicks=850,
                ctr=5.67,
                conversions=45,
                cpa=28.5,
                roas=5.2,
                performance_quadrant="HERO",
                price_competitiveness="COMPETITIVE",
                competitor_price_avg=310.0,
                custom_labels=["high_margin", "bestseller"]
            ),
            # Growth 商品 - 潜力股
            ProductFeedItem(
                product_id="prod_002",
                product_name="Email Marketing Tool Basic",
                status="ACTIVE",
                title="邮件营销工具基础版",
                description="入门级邮件营销解决方案",
                image_url="https://example.com/images/email-basic.jpg",
                price=49.0,
                availability="IN_STOCK",
                brand="MarketingPro",
                gtin="1234567890124",
                impressions=8500,
                clicks=420,
                ctr=4.94,
                conversions=12,
                cpa=24.5,
                roas=3.8,
                performance_quadrant="GROWTH",
                price_competitiveness="COMPETITIVE",
                competitor_price_avg=52.0,
                custom_labels=["starter", "high_potential"]
            ),
            # Low Performer - 低效商品
            ProductFeedItem(
                product_id="prod_003",
                product_name="Legacy Analytics Dashboard",
                status="ACTIVE",
                title="旧版分析仪表板",
                description="传统数据分析工具（即将下架）",
                image_url="https://example.com/images/old-dashboard.jpg",
                price=199.0,
                availability="IN_STOCK",
                brand="MarketingPro",
                impressions=5200,
                clicks=85,
                ctr=1.63,
                conversions=2,
                cpa=95.0,
                roas=1.1,
                performance_quadrant="LOW_PERFORMER",
                price_competitiveness="HIGH",
                competitor_price_avg=150.0,
                custom_labels=["legacy", "end_of_life"]
            ),
            # Zombie - 僵尸商品
            ProductFeedItem(
                product_id="prod_004",
                product_name="Discontinued Social Tool",
                status="DISAPPROVED",
                title="已停产的社交工具",
                description="此产品已停止维护",
                image_url="https://example.com/images/discontinued.jpg",
                price=99.0,
                availability="OUT_OF_STOCK",
                brand="MarketingPro",
                impressions=1200,
                clicks=12,
                ctr=1.0,
                conversions=0,
                cpa=0.0,
                roas=0.0,
                performance_quadrant="ZOMBIE",
                price_competitiveness="LOW",
                custom_labels=["discontinued"]
            ),
            # Feed 不完整商品
            ProductFeedItem(
                product_id="prod_005",
                product_name="Incomplete Product",
                status="PENDING",
                title="",
                description="",
                image_url="",
                price=0.0,
                availability="PREORDER",
                brand="",
                impressions=0,
                clicks=0,
                ctr=0.0,
                conversions=0,
                cpa=0.0,
                roas=0.0,
                performance_quadrant="ZOMBIE",
                price_competitiveness="LOW",
                custom_labels=[]
            ),
        ]

        if campaign_id:
            # 只为电商 campaign 返回商品
            if campaign_id in ["c_002", "c_004", "c_008"]:
                return products
            return []
        return products
