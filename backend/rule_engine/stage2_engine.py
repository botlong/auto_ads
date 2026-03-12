"""
SOP Stage 2 - 组件级优化 规则引擎
实现 S012-S053 所有检查规则
"""

from typing import List, Dict, Any
from datetime import datetime
from models.schemas import (
    Campaign, SearchTerm, Keyword, ResponsiveSearchAd, Asset,
    LocationPerformance, DevicePerformance, HourlyPerformance,
    AuctionInsight, DiagnosisResult, Alert, Severity,
    BiddingType, BusinessType, LearningStatus,
    LandingPageHealth, QualityScoreDiagnosis, PolicyStatus, ProductFeedItem
)


class Stage2RuleEngine:
    """Stage 2 规则引擎 - 组件级优化"""

    def run_stage2_check(self, campaign: Campaign, mock_data) -> List[DiagnosisResult]:
        """
        对单个 Campaign 执行完整的 Stage 2 检查
        """
        results = []

        # S012-S014: 搜索词优化
        search_terms = mock_data.get_search_terms(campaign.id)
        results.extend(self.check_search_terms(search_terms, campaign))

        # S015-S017: 关键词管理
        keywords = mock_data.get_keywords(campaign.id)
        results.extend(self.check_keywords(keywords, campaign))

        # S018-S020: 广告文案
        ads = mock_data.get_ads(campaign.id)
        results.extend(self.check_ad_copy(ads, campaign))

        # S021-S023: Assets 管理
        assets = mock_data.get_assets(campaign.id)
        results.extend(self.check_assets(assets, campaign))

        # S026-S028: 地域优化
        locations = mock_data.get_locations(campaign.id)
        results.extend(self.check_locations(locations, campaign))

        # S033-S034: 设备优化
        devices = mock_data.get_devices(campaign.id)
        results.extend(self.check_devices(devices, campaign))

        # S035-S036: 时段优化
        hourly = mock_data.get_hourly_performance(campaign.id)
        results.extend(self.check_hourly_performance(hourly, campaign))

        # S037: 竞品拍卖分析
        auction_insights = mock_data.get_auction_insights(campaign.id)
        results.extend(self.check_auction_insights(auction_insights, campaign))

        # S057-S061: Audience 受众优化
        audiences = mock_data.get_audiences(campaign.id)
        results.extend(self.check_audiences(audiences, campaign))

        # S024-S025: Landing Page & Quality Score 详细诊断
        landing_pages = mock_data.get_landing_page_health(campaign.id)
        results.extend(self.check_landing_pages(landing_pages, campaign))

        quality_diagnoses = mock_data.get_quality_score_diagnosis(campaign.id)
        results.extend(self.check_quality_score_detailed(quality_diagnoses, campaign))

        # S038: 政策审核状态
        policy_status = mock_data.get_policy_status(campaign.id)
        results.extend(self.check_policy_status(policy_status, campaign))

        # S039-S053: 电商专项 (仅电商 Campaign)
        if campaign.business_type == BusinessType.ECOMMERCE:
            products = mock_data.get_product_feed(campaign.id)
            results.extend(self.check_ecommerce_feed(products, campaign))

        return results

    # ============ S012-S014: 搜索词优化 ============

    def check_search_terms(self, search_terms: List[SearchTerm], campaign: Campaign) -> List[DiagnosisResult]:
        """
        S012: 搜索词负向过滤
        S013: 高意图词拓新
        S014: 流量健康度诊断
        """
        results = []

        if not search_terms:
            return results

        # 获取 campaign 的目标 CPA 用于判断阈值
        target_cpa = campaign.target_cpa or 30.0

        # S012: 高花费无转化词 -> 添加负向
        high_spend_no_conv = [st for st in search_terms if st.cost > target_cpa * 1.5 and st.conversions == 0]
        for st in high_spend_no_conv:
            results.append(DiagnosisResult(
                strategy_id="S012",
                strategy_name="搜索词负向过滤",
                severity=Severity.P1,
                issue_type="高花费无转化搜索词",
                affected_object=f"Campaign: {campaign.name} > Search Term: '{st.search_term}'",
                current_value=f"花费 ${st.cost:.2f}, 0 转化",
                benchmark_value=f"应 < ${target_cpa * 1.5:.2f} 或产生转化",
                suggested_action=f"添加精确负向词: '{st.search_term}'",
                expected_impact=f"预计每月节省 ${st.cost * 4:.2f}",
                details={"search_term": st.search_term, "cost": st.cost, "reason": st.negative_reason}
            ))

        # S014: CTR 异常低的搜索词 -> 意图不相关
        low_ctr_terms = [st for st in search_terms if st.clicks > 20 and st.ctr < 3.0]
        for st in low_ctr_terms:
            results.append(DiagnosisResult(
                strategy_id="S014",
                strategy_name="流量健康度诊断",
                severity=Severity.P2,
                issue_type="搜索词 CTR 异常低",
                affected_object=f"Campaign: {campaign.name} > '{st.search_term}'",
                current_value=f"CTR {st.ctr:.2f}%",
                benchmark_value="> 3%",
                suggested_action=f"检查搜索词意图相关性，考虑添加负向",
                expected_impact="提高整体 CTR，降低 CPC",
                details={"search_term": st.search_term, "ctr": st.ctr, "keyword": st.keyword_text}
            ))

        # S013: 高意图词 (有转化) -> 提炼为 Exact
        high_intent_terms = [st for st in search_terms if st.conversions >= 1 and st.match_type in ["BROAD", "PHRASE"]]
        for st in high_intent_terms:
            results.append(DiagnosisResult(
                strategy_id="S013",
                strategy_name="高意图词拓新",
                severity=Severity.P2,
                issue_type="高意图搜索词应提炼为精确匹配",
                affected_object=f"Campaign: {campaign.name} > '{st.search_term}'",
                current_value=f"匹配类型: {st.match_type}, {st.conversions} 转化",
                benchmark_value="EXACT 匹配",
                suggested_action=f"添加精确匹配关键词: [{st.search_term}]",
                expected_impact="提高质量得分，降低 CPC",
                details={"search_term": st.search_term, "conversions": st.conversions, "cpa": st.cpa}
            ))

        # S030: 负向关键词自动分级
        # 判断应该添加到Account Level还是Campaign Level
        broad_match_terms = [st for st in search_terms if st.match_type == "BROAD" and st.cost > target_cpa and st.conversions == 0]
        for st in broad_match_terms:
            # 如果该搜索词在多个campaign中出现，建议添加到Account Level
            # 这里模拟检查：如果搜索词很宽泛（如包含"free", "cheap"等），建议Account Level
            generic_terms = ["free", "cheap", "discount", "wholesale", "bulk", "used", "second hand"]
            is_generic = any(term in st.search_term.lower() for term in generic_terms)

            if is_generic:
                results.append(DiagnosisResult(
                    strategy_id="S030",
                    strategy_name="负向关键词自动分级",
                    severity=Severity.P2,
                    issue_type="通用负向词应添加到Account Level",
                    affected_object=f"Campaign: {campaign.name} > '{st.search_term}'",
                    current_value=f"花费 ${st.cost:.2f}, 0 转化",
                    benchmark_value="Account Level 负向词",
                    suggested_action=f"添加到Account负向关键词列表: '{st.search_term}'",
                    expected_impact="阻止该搜索词在整个账户投放",
                    details={"search_term": st.search_term, "level": "Account", "reason": "通用否定词"}
                ))

        # S031: 搜索词意图匹配度检查
        # 检查搜索词与关键词的意图匹配程度
        for st in search_terms:
            if st.clicks < 10:
                continue

            # 计算意图匹配度
            keyword_parts = set(st.keyword_text.lower().split())
            search_parts = set(st.search_term.lower().split())

            # 如果搜索词与关键词完全不相关
            overlap = keyword_parts & search_parts
            if len(overlap) == 0 and st.cost > target_cpa * 0.5:
                results.append(DiagnosisResult(
                    strategy_id="S031",
                    strategy_name="搜索词意图匹配度检查",
                    severity=Severity.P1,
                    issue_type="搜索词与关键词意图不匹配",
                    affected_object=f"Campaign: {campaign.name} > 搜索词: '{st.search_term}'",
                    current_value=f"关键词: '{st.keyword_text}', 花费: ${st.cost:.2f}",
                    benchmark_value="意图相关度 > 0",
                    suggested_action=f"检查搜索词意图，添加到负向关键词列表",
                    expected_impact="避免不相关流量消耗预算",
                    details={"search_term": st.search_term, "keyword": st.keyword_text, "overlap": list(overlap)}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S012-S014",
                strategy_name="搜索词优化",
                severity=Severity.OK,
                issue_type="搜索词健康度良好",
                affected_object=f"Campaign: {campaign.name}",
                current_value="无问题搜索词",
                benchmark_value="OK",
                suggested_action="持续监控",
                details={}
            ))

        return results

    # ============ S015-S017: 关键词管理 ============

    def check_keywords(self, keywords: List[Keyword], campaign: Campaign) -> List[DiagnosisResult]:
        """
        S015: 关键词效果负向清理
        S016: 关键词相关性与质量得分诊断
        S017: 流量健康度与出价水位
        """
        results = []

        if not keywords:
            return results

        target_cpa = campaign.target_cpa or 30.0

        for kw in keywords:
            # S015: 高花费无转化关键词 -> 暂停
            if kw.cost > target_cpa * 3 and kw.conversions == 0:
                results.append(DiagnosisResult(
                    strategy_id="S015",
                    strategy_name="关键词效果负向清理",
                    severity=Severity.P1,
                    issue_type="关键词高花费无转化",
                    affected_object=f"Campaign: {campaign.name} > Keyword: '{kw.text}'",
                    current_value=f"花费 ${kw.cost:.2f}, 0 转化",
                    benchmark_value=f"应 < ${target_cpa * 3:.2f} 或有转化",
                    suggested_action=f"暂停关键词: '{kw.text}'",
                    expected_impact=f"节省预算 ${kw.cost:.2f}/月",
                    details={"keyword": kw.text, "match_type": kw.match_type, "cost": kw.cost}
                ))

            # S015: CPA 超标关键词 -> 降价
            actual_cpa = kw.cost / kw.conversions if kw.conversions > 0 else 0
            if kw.conversions >= 3 and actual_cpa > target_cpa * 1.5:
                results.append(DiagnosisResult(
                    strategy_id="S015",
                    strategy_name="关键词效果负向清理",
                    severity=Severity.P1,
                    issue_type="关键词 CPA 严重超标",
                    affected_object=f"Campaign: {campaign.name} > '{kw.text}'",
                    current_value=f"CPA ${actual_cpa:.2f}",
                    benchmark_value=f"目标 ${target_cpa:.2f}",
                    suggested_action=f"降低出价 20% 或暂停",
                    expected_impact="优化关键词级 CPA",
                    details={"keyword": kw.text, "cpa": actual_cpa, "target_cpa": target_cpa}
                ))

            # S016: 质量得分过低
            if kw.quality_score < 4:
                results.append(DiagnosisResult(
                    strategy_id="S016",
                    strategy_name="关键词质量得分诊断",
                    severity=Severity.P2,
                    issue_type="关键词质量得分过低",
                    affected_object=f"Campaign: {campaign.name} > '{kw.text}'",
                    current_value=f"QS {kw.quality_score}/10",
                    benchmark_value=">= 5",
                    suggested_action=f"{'收缩匹配类型为 Phrase/Exact' if kw.match_type == 'BROAD' else '优化广告文案和落地页相关性'}",
                    expected_impact="提高 QS，降低 CPC",
                    details={
                        "keyword": kw.text,
                        "quality_score": kw.quality_score,
                        "ad_relevance": kw.ad_relevance,
                        "lp_experience": kw.lp_experience,
                        "expected_ctr": kw.expected_ctr
                    }
                ))

            # S017: 出价水位检查 - 超过 Top of Page CPC 太多
            if kw.cpc_bid > kw.top_of_page_cpc * 1.5:
                results.append(DiagnosisResult(
                    strategy_id="S017",
                    strategy_name="流量健康度与出价水位",
                    severity=Severity.P2,
                    issue_type="关键词出价过高",
                    affected_object=f"Campaign: {campaign.name} > '{kw.text}'",
                    current_value=f"出价 ${kw.cpc_bid:.2f}",
                    benchmark_value=f"Top of Page ${kw.top_of_page_cpc:.2f}",
                    suggested_action=f"降低出价至 ${kw.top_of_page_cpc:.2f}",
                    expected_impact="优化出价效率",
                    details={"keyword": kw.text, "cpc_bid": kw.cpc_bid, "top_of_page_cpc": kw.top_of_page_cpc}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S015-S017",
                strategy_name="关键词管理",
                severity=Severity.OK,
                issue_type="关键词健康度良好",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(keywords)} 个关键词运行正常",
                benchmark_value="OK",
                suggested_action="持续监控",
                details={}
            ))

        return results

    # ============ S018-S020: 广告文案 ============

    def check_ad_copy(self, ads: List[ResponsiveSearchAd], campaign: Campaign) -> List[DiagnosisResult]:
        """
        S018: 广告合规性与投放状态监控
        S019: RSA 创意强度诊断
        S020: 创意点击与转化效能优化
        """
        results = []

        if not ads:
            return results

        for ad in ads:
            # S018: 广告拒登
            if ad.approval_status == "DISAPPROVED":
                results.append(DiagnosisResult(
                    strategy_id="S018",
                    strategy_name="广告合规性与投放状态监控",
                    severity=Severity.P0,
                    issue_type="广告被拒登",
                    affected_object=f"Campaign: {campaign.name} > Ad: {ad.id}",
                    current_value="Status: DISAPPROVED",
                    benchmark_value="APPROVED",
                    suggested_action="检查拒登原因，修改后重新提交审核",
                    expected_impact="恢复广告投放",
                    details={"ad_id": ad.id, "issues": ad.issues}
                ))

            # S019: Ad Strength 过低
            if ad.ad_strength_rating < 2:
                results.append(DiagnosisResult(
                    strategy_id="S019",
                    strategy_name="RSA 创意强度诊断",
                    severity=Severity.P1,
                    issue_type="广告创意强度不足",
                    affected_object=f"Campaign: {campaign.name} > Ad: {ad.id}",
                    current_value=f"Ad Strength: {ad.ad_strength} ({len(ad.headlines)} headlines, {len(ad.descriptions)} descriptions)",
                    benchmark_value="GOOD 或 EXCELLENT (8+ Headlines, 3+ Descriptions)",
                    suggested_action=f"添加更多差异化 Headline/Description，{'当前 Headline 数量不足' if len(ad.headlines) < 8 else '当前 Description 数量不足'}",
                    expected_impact="提高广告点击率和质量得分",
                    details={
                        "ad_id": ad.id,
                        "ad_strength": ad.ad_strength,
                        "headline_count": len(ad.headlines),
                        "description_count": len(ad.descriptions)
                    }
                ))

            # S020: CTR 低于 Campaign 平均
            if ad.ctr < campaign.ctr * 0.7 and ad.impressions > 100:
                results.append(DiagnosisResult(
                    strategy_id="S020",
                    strategy_name="创意点击与转化效能优化",
                    severity=Severity.P2,
                    issue_type="广告 CTR 低于平均",
                    affected_object=f"Campaign: {campaign.name} > Ad: {ad.id}",
                    current_value=f"CTR {ad.ctr:.2f}%",
                    benchmark_value=f"> {campaign.ctr * 0.7:.2f}%",
                    suggested_action="优化 Headline 加入更强 CTA，测试新卖点",
                    expected_impact="提高 CTR，降低 CPC",
                    details={"ad_id": ad.id, "ctr": ad.ctr, "campaign_avg_ctr": campaign.ctr}
                ))

            # S020: 高 CTR 但低 CVR - 吸引点击但转化差
            if ad.ctr > campaign.ctr * 1.2 and ad.cvr < campaign.cvr * 0.5 and ad.clicks > 50:
                results.append(DiagnosisResult(
                    strategy_id="S020",
                    strategy_name="创意点击与转化效能优化",
                    severity=Severity.P1,
                    issue_type="广告吸引点击但转化差",
                    affected_object=f"Campaign: {campaign.name} > Ad: {ad.id}",
                    current_value=f"CTR {ad.ctr:.2f}% (高), CVR {ad.cvr:.2f}% (低)",
                    benchmark_value="CTR 和 CVR 均衡",
                    suggested_action="检查文案是否存在误导，加入信任背书（如'Certified'、'Rated 5 Stars'）",
                    expected_impact="提高 CVR，减少无效点击",
                    details={"ad_id": ad.id, "ctr": ad.ctr, "cvr": ad.cvr}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S018-S020",
                strategy_name="广告文案检查",
                severity=Severity.OK,
                issue_type="广告文案健康度良好",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(ads)} 个广告运行正常",
                benchmark_value="OK",
                suggested_action="持续监控，定期刷新素材",
                details={}
            ))

        return results

    # ============ S021-S023: Assets 管理 ============

    def check_assets(self, assets: List[Asset], campaign: Campaign) -> List[DiagnosisResult]:
        """
        S021: 核心资产缺失自动补齐
        S022: 低效资产定期刷新
        S023: 资产与转化意图对齐审计
        """
        results = []

        # S021: Sitelink 数量检查
        sitelinks = [a for a in assets if a.type == "SITELINK"]
        if len(sitelinks) < 4:
            results.append(DiagnosisResult(
                strategy_id="S021",
                strategy_name="核心资产缺失自动补齐",
                severity=Severity.P2,
                issue_type="Sitelink 扩展数量不足",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(sitelinks)} 个 Sitelink",
                benchmark_value="至少 4 个",
                suggested_action="添加更多 Sitelink（Pricing、About Us、Contact、Case Studies）",
                expected_impact="提高广告可见性和点击率",
                details={"current_count": len(sitelinks)}
            ))

        # S022: 低效 Asset 检查
        for asset in assets:
            if asset.performance_label == "LOW":
                results.append(DiagnosisResult(
                    strategy_id="S022",
                    strategy_name="低效资产定期刷新",
                    severity=Severity.P2,
                    issue_type="Asset 表现不佳",
                    affected_object=f"Campaign: {campaign.name} > {asset.type}: {asset.sitelink_text or asset.callout_text}",
                    current_value=f"Performance: LOW, {asset.impressions} 展示, {asset.clicks} 点击",
                    benchmark_value="GOOD 或 BEST",
                    suggested_action="暂停该 Asset，创建新的替换",
                    expected_impact="提高整体 Asset 效能",
                    details={"asset_id": asset.id, "type": asset.type}
                ))

        # S021: Lead Form 检查 (Lead Gen 业务)
        if campaign.business_type == BusinessType.LEAD_GEN:
            lead_forms = [a for a in assets if a.type == "LEAD_FORM"]
            if not lead_forms:
                results.append(DiagnosisResult(
                    strategy_id="S021",
                    strategy_name="核心资产缺失自动补齐",
                    severity=Severity.P1,
                    issue_type="缺少 Lead Form 扩展",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value="未配置",
                    benchmark_value="Lead Gen 业务应配置",
                    suggested_action="创建 Lead Form 扩展，提高线索收集效率",
                    expected_impact="提高转化率，降低转化成本",
                    details={}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S021-S023",
                strategy_name="Assets 管理",
                severity=Severity.OK,
                issue_type="Assets 健康度良好",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(assets)} 个 Asset 运行正常",
                benchmark_value="OK",
                suggested_action="定期审核低效 Asset",
                details={}
            ))

        return results

    # ============ S026-S028: 地域优化 ============

    def check_locations(self, locations: List[LocationPerformance], campaign: Campaign) -> List[DiagnosisResult]:
        """
        S026: 排除低效地域
        S027: 高效地域拆分
        S028: 地域出价调整
        """
        results = []

        if not locations:
            return results

        target_cpa = campaign.target_cpa or 30.0
        target_roas = campaign.target_roas or 3.0

        for loc in locations:
            # S026: 高花费无转化地域 -> 排除
            if loc.cost > target_cpa * 2 and loc.conversions == 0:
                results.append(DiagnosisResult(
                    strategy_id="S026",
                    strategy_name="排除低效地域",
                    severity=Severity.P1,
                    issue_type="地域花费高无转化",
                    affected_object=f"Campaign: {campaign.name} > Location: {loc.location_name}",
                    current_value=f"花费 ${loc.cost:.2f}, 0 转化",
                    benchmark_value=f"应产生转化或花费 < ${target_cpa * 2:.2f}",
                    suggested_action=f"排除地域: {loc.location_name}",
                    expected_impact=f"节省预算 ${loc.cost:.2f}/月",
                    details={"location": loc.location_name, "cost": loc.cost}
                ))

            # S026: CPA 超标地域
            if campaign.business_type == BusinessType.LEAD_GEN and loc.cpa > target_cpa * 1.5 and loc.conversions > 0:
                results.append(DiagnosisResult(
                    strategy_id="S026",
                    strategy_name="排除低效地域",
                    severity=Severity.P2,
                    issue_type="地域 CPA 超标",
                    affected_object=f"Campaign: {campaign.name} > {loc.location_name}",
                    current_value=f"CPA ${loc.cpa:.2f}",
                    benchmark_value=f"目标 ${target_cpa:.2f}",
                    suggested_action=f"排除地域或降低出价 30%",
                    expected_impact="优化地域级 CPA",
                    details={"location": loc.location_name, "cpa": loc.cpa}
                ))

            # S027: 高效地域 -> 拆分 Campaign
            if loc.is_outperforming:
                results.append(DiagnosisResult(
                    strategy_id="S027",
                    strategy_name="高效地域拆分",
                    severity=Severity.P2,
                    issue_type="高效地域建议独立 Campaign",
                    affected_object=f"Campaign: {campaign.name} > {loc.location_name}",
                    current_value=f"CPA ${loc.cpa:.2f}, ROAS {loc.roas:.2f}x",
                    benchmark_value="显著优于平均",
                    suggested_action=f"为 {loc.location_name} 创建独立 Campaign，增加专属预算",
                    expected_impact="最大化高效地域表现",
                    details={"location": loc.location_name, "cpa": loc.cpa, "roas": loc.roas}
                ))

            # S028: 出价调整建议
            if loc.cpa < target_cpa * 0.7 and loc.conversions >= 5:
                results.append(DiagnosisResult(
                    strategy_id="S028",
                    strategy_name="地域出价调整",
                    severity=Severity.P2,
                    issue_type="高效地域可提高出价获取更多流量",
                    affected_object=f"Campaign: {campaign.name} > {loc.location_name}",
                    current_value=f"CPA ${loc.cpa:.2f} (低于目标)",
                    benchmark_value=f"目标 ${target_cpa:.2f}",
                    suggested_action=f"提高出价调整 +15%",
                    expected_impact="获取更多高效流量",
                    details={"location": loc.location_name, "current_modifier": loc.bid_modifier}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S026-S028",
                strategy_name="地域优化",
                severity=Severity.OK,
                issue_type="地域表现健康",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(locations)} 个地域运行正常",
                benchmark_value="OK",
                suggested_action="持续监控",
                details={}
            ))

        return results

    # ============ S033-S034: 设备优化 ============

    def check_devices(self, devices: List[DevicePerformance], campaign: Campaign) -> List[DiagnosisResult]:
        """
        S033: 设备效率诊断
        S034: 设备出价调整
        """
        results = []

        if not devices:
            return results

        # 找到 Desktop 作为基准
        desktop = next((d for d in devices if d.device_type == "DESKTOP"), None)

        for device in devices:
            if device.device_type == "DESKTOP":
                continue

            # S033: Mobile CVR 比 Desktop 低太多 -> UX 问题
            if device.device_type == "MOBILE" and desktop:
                cvr_gap = (device.cvr - desktop.cvr) / desktop.cvr * 100
                if cvr_gap < -40:
                    results.append(DiagnosisResult(
                        strategy_id="S033",
                        strategy_name="设备效率诊断",
                        severity=Severity.P1,
                        issue_type="移动端转化率显著低于桌面端",
                        affected_object=f"Campaign: {campaign.name} > Device: {device.device_type}",
                        current_value=f"Mobile CVR {device.cvr:.2f}% vs Desktop CVR {desktop.cvr:.2f}%",
                        benchmark_value="差距 < 30%",
                        suggested_action="检查移动端落地页体验，优化移动端表单，测试加速移动页面 (AMP)",
                        expected_impact="提高移动端转化率",
                        details={"mobile_cvr": device.cvr, "desktop_cvr": desktop.cvr, "gap": cvr_gap}
                    ))

            # S033/S034: 设备 CPA 超标 -> 降低出价
            target_cpa = campaign.target_cpa or 30.0
            if campaign.business_type == BusinessType.LEAD_GEN and device.cpa > target_cpa * 1.3:
                results.append(DiagnosisResult(
                    strategy_id="S034",
                    strategy_name="设备出价调整",
                    severity=Severity.P2,
                    issue_type="设备 CPA 超标",
                    affected_object=f"Campaign: {campaign.name} > {device.device_type}",
                    current_value=f"CPA ${device.cpa:.2f}",
                    benchmark_value=f"目标 ${target_cpa:.2f}",
                    suggested_action=f"降低 {device.device_type} 出价 15-20%",
                    expected_impact="优化设备级 CPA",
                    details={"device": device.device_type, "cpa": device.cpa, "current_modifier": device.bid_modifier}
                ))

            # S034: 设备花费高无转化
            if device.cost > target_cpa * 2 and device.conversions == 0:
                results.append(DiagnosisResult(
                    strategy_id="S034",
                    strategy_name="设备出价调整",
                    severity=Severity.P1,
                    issue_type="设备花费无转化",
                    affected_object=f"Campaign: {campaign.name} > {device.device_type}",
                    current_value=f"花费 ${device.cost:.2f}, 0 转化",
                    benchmark_value=f"应有转化",
                    suggested_action=f"大幅降低 {device.device_type} 出价 (-90%) 或排除",
                    expected_impact="避免设备级浪费",
                    details={"device": device.device_type, "cost": device.cost}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S033-S034",
                strategy_name="设备优化",
                severity=Severity.OK,
                issue_type="设备表现健康",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(devices)} 个设备类型运行正常",
                benchmark_value="OK",
                suggested_action="持续监控",
                details={}
            ))

        return results

    # ============ S035-S036: 时段优化 ============

    def check_hourly_performance(self, hourly_data: List[HourlyPerformance], campaign: Campaign) -> List[DiagnosisResult]:
        """
        S035: 分时段效能分析
        S036: Ad Schedule 调整
        """
        results = []

        if not hourly_data:
            return results

        target_cpa = campaign.target_cpa or 30.0

        # 低效时段: 高花费无转化
        low_perf_hours = [h for h in hourly_data if h.is_low_performance and h.cost > target_cpa * 1.5]
        if low_perf_hours:
            hours_str = ", ".join([f"{h.day_of_week}:{h.hour_of_day:02d}" for h in low_perf_hours[:5]])
            results.append(DiagnosisResult(
                strategy_id="S036",
                strategy_name="分时段效能优化",
                severity=Severity.P1,
                issue_type="低效时段应停止投放",
                affected_object=f"Campaign: {campaign.name} > Hours: {hours_str}...",
                current_value=f"{len(low_perf_hours)} 个时段花费高无转化",
                benchmark_value="所有时段应产生转化",
                suggested_action=f"暂停低效时段投放，或降低出价 50%",
                expected_impact="节省预算，提高整体 CPA",
                details={"low_performance_hours": len(low_perf_hours)}
            ))

        # 高效时段: 可增加出价
        high_perf_hours = [h for h in hourly_data if h.is_high_performance]
        if high_perf_hours:
            results.append(DiagnosisResult(
                strategy_id="S035",
                strategy_name="分时段效能分析",
                severity=Severity.P2,
                issue_type="高效时段可提高出价",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(high_perf_hours)} 个高效时段",
                benchmark_value="应增加出价获取更多转化",
                suggested_action="工作日 9-18点提高出价 +15%",
                expected_impact="最大化高效时段转化",
                details={"high_performance_hours": len(high_perf_hours)}
            ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S035-S036",
                strategy_name="时段优化",
                severity=Severity.OK,
                issue_type="时段表现健康",
                affected_object=f"Campaign: {campaign.name}",
                current_value="各时段表现均衡",
                benchmark_value="OK",
                suggested_action="持续监控",
                details={}
            ))

        return results

    # ============ S037: 竞品拍卖分析 ============

    def check_auction_insights(self, insights: List[AuctionInsight], campaign: Campaign) -> List[DiagnosisResult]:
        """
        S037: 竞品拍卖压力诊断
        """
        results = []

        if not insights:
            return results

        # 找出主要竞争对手
        main_competitors = [i for i in insights if i.is_main_competitor]

        for comp in main_competitors:
            # 重叠率高 + 排名输得多 -> 需要提高竞争力
            if comp.overlap_rate > 50 and comp.position_above_rate > 40:
                results.append(DiagnosisResult(
                    strategy_id="S037",
                    strategy_name="竞品拍卖压力诊断",
                    severity=Severity.P2,
                    issue_type="主要竞争对手压制",
                    affected_object=f"Campaign: {campaign.name} > Competitor: {comp.domain}",
                    current_value=f"重叠率 {comp.overlap_rate:.1f}%, 对方排上方 {comp.position_above_rate:.1f}%",
                    benchmark_value="竞争力均衡",
                    suggested_action="提高出价或优化质量得分以提高排名",
                    expected_impact="提高 Outranking Share",
                    details={
                        "competitor": comp.domain,
                        "overlap_rate": comp.overlap_rate,
                        "position_above_rate": comp.position_above_rate,
                        "threat_level": comp.threat_level
                    }
                ))

            # IS 持续下降检测 (模拟)
            if comp.impression_share > campaign.search_impression_share * 1.5:
                results.append(DiagnosisResult(
                    strategy_id="S037",
                    strategy_name="竞品拍卖压力诊断",
                    severity=Severity.P1,
                    issue_type="竞品展示份额显著高于我方",
                    affected_object=f"Campaign: {campaign.name} > Competitor: {comp.domain}",
                    current_value=f"竞品 IS {comp.impression_share:.1f}% vs 我方 IS {campaign.search_impression_share:.1f}%",
                    benchmark_value="竞争力均衡",
                    suggested_action="分析竞品优势，考虑提高出价或优化广告文案",
                    expected_impact="提高我方市场份额",
                    details={"competitor_is": comp.impression_share, "my_is": campaign.search_impression_share}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S037",
                strategy_name="竞品拍卖分析",
                severity=Severity.OK,
                issue_type="竞争态势正常",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(insights)} 个竞争对手监控中",
                benchmark_value="OK",
                suggested_action="持续监控竞品动态",
                details={}
            ))

        return results

    def check_audiences(self, audiences: List[Any], campaign: Campaign) -> List[DiagnosisResult]:
        """
        S057: 受众覆盖度缺位检查 (Coverage Check)
        S058: 低效受众自动排除 (Performance Pruning)
        S059: 受众信号增强 (Signal Augmentation)
        S060: 人群过滤效能 (Demographic Filtering)
        S061: 受众表现分析与自动调整
        """
        results = []

        if not audiences:
            return results

        target_cpa = campaign.target_cpa or 30.0
        target_roas = campaign.target_roas or 3.0

        # S057: 检查受众覆盖度
        remarketing_audiences = [a for a in audiences if a.audience_type == "REMARKETING"]
        if not remarketing_audiences:
            results.append(DiagnosisResult(
                strategy_id="S057",
                strategy_name="受众覆盖度缺位检查",
                severity=Severity.P2,
                issue_type="缺少再营销受众",
                affected_object=f"Campaign: {campaign.name}",
                current_value="无再营销受众",
                benchmark_value="应有Remarketing List",
                suggested_action="添加网站访客再营销列表",
                expected_impact="提高转化率和ROI",
                details={}
            ))

        customer_list_audiences = [a for a in audiences if a.audience_type == "CUSTOMER_LIST"]
        if not customer_list_audiences:
            results.append(DiagnosisResult(
                strategy_id="S057",
                strategy_name="受众覆盖度缺位检查",
                severity=Severity.P2,
                issue_type="缺少客户列表受众",
                affected_object=f"Campaign: {campaign.name}",
                current_value="无Customer List",
                benchmark_value="应有客户列表上传",
                suggested_action="上传现有客户列表用于类似受众扩展",
                expected_impact="提高受众质量",
                details={}
            ))

        # S058 & S061: 低效受众排除
        for audience in audiences:
            # CPA超标受众
            if audience.conversions > 0 and audience.cpa > target_cpa * 1.5:
                results.append(DiagnosisResult(
                    strategy_id="S058",
                    strategy_name="低效受众自动排除",
                    severity=Severity.P1,
                    issue_type="受众CPA严重超标",
                    affected_object=f"Campaign: {campaign.name} > Audience: {audience.audience_name}",
                    current_value=f"CPA ${audience.cpa:.2f}",
                    benchmark_value=f"目标 ${target_cpa:.2f}",
                    suggested_action=f"降低该受众出价调整至 {audience.bid_modifier * 0.5:.0%} 或排除",
                    expected_impact="优化受众级CPA",
                    details={"audience_id": audience.id, "cpa": audience.cpa}
                ))

            # 无转化但花费高
            if audience.conversions == 0 and audience.cost > target_cpa * 2:
                results.append(DiagnosisResult(
                    strategy_id="S061",
                    strategy_name="受众表现分析与自动调整",
                    severity=Severity.P1,
                    issue_type="受众高花费无转化",
                    affected_object=f"Campaign: {campaign.name} > {audience.audience_name}",
                    current_value=f"花费 ${audience.cost:.2f}, 0 转化",
                    benchmark_value="应产生转化",
                    suggested_action="排除该受众或检查落地页匹配度",
                    expected_impact="节省无效花费",
                    details={"audience_type": audience.audience_type}
                ))

            # S059: 高效受众信号增强
            if audience.conversions >= 3 and audience.cpa < target_cpa * 0.8:
                results.append(DiagnosisResult(
                    strategy_id="S059",
                    strategy_name="受众信号增强",
                    severity=Severity.P2,
                    issue_type="高效受众应增强出价",
                    affected_object=f"Campaign: {campaign.name} > {audience.audience_name}",
                    current_value=f"CPA ${audience.cpa:.2f} (优于目标)",
                    benchmark_value=f"目标 ${target_cpa:.2f}",
                    suggested_action=f"提高该受众出价调整至 {min(audience.bid_modifier * 1.3, 1.5):.0%}",
                    expected_impact="获取更多高质量流量",
                    details={"audience_id": audience.id, "cpa": audience.cpa}
                ))

        # S060: 人群过滤效能 - 检查出价调整是否合理
        extreme_bid_modifiers = [a for a in audiences if abs(a.bid_modifier - 1.0) > 0.5]
        for audience in extreme_bid_modifiers:
            if audience.bid_modifier > 1.5 and audience.cpa > target_cpa:
                results.append(DiagnosisResult(
                    strategy_id="S060",
                    strategy_name="人群过滤效能",
                    severity=Severity.P2,
                    issue_type="高出价调整但CPA超标",
                    affected_object=f"Campaign: {campaign.name} > {audience.audience_name}",
                    current_value=f"出价调整 {audience.bid_modifier:.0%}, CPA ${audience.cpa:.2f}",
                    benchmark_value="出价调整应与表现匹配",
                    suggested_action="降低出价调整或排除该受众",
                    expected_impact="避免浪费预算",
                    details={}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S057-S061",
                strategy_name="受众优化",
                severity=Severity.OK,
                issue_type="受众表现良好",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(audiences)} 个受众运行正常",
                benchmark_value="OK",
                suggested_action="持续监控受众表现",
                details={}
            ))

        return results

    def check_landing_pages(self, lp_health: List[Any], campaign: Campaign) -> List[DiagnosisResult]:
        """S024: Landing Page 体验检查"""
        results = []

        for lp in lp_health:
            # 检查页面加载速度
            if lp.load_time_seconds > 3.0:
                results.append(DiagnosisResult(
                    strategy_id="S024",
                    strategy_name="Landing Page 体验检查",
                    severity=Severity.P1,
                    issue_type="页面加载过慢",
                    affected_object=f"Landing Page: {lp.url}",
                    current_value=f"加载时间 {lp.load_time_seconds:.1f}s",
                    benchmark_value="< 3.0s",
                    suggested_action="优化页面加载速度，压缩图片，启用CDN",
                    expected_impact="降低跳出率，提高转化率",
                    details={"load_time": lp.load_time_seconds, "bounce_rate": lp.bounce_rate}
                ))

            # 检查跳出率
            if lp.bounce_rate > 0.7:
                results.append(DiagnosisResult(
                    strategy_id="S024",
                    strategy_name="Landing Page 体验检查",
                    severity=Severity.P1,
                    issue_type="跳出率过高",
                    affected_object=f"Landing Page: {lp.url}",
                    current_value=f"跳出率 {lp.bounce_rate*100:.1f}%",
                    benchmark_value="< 70%",
                    suggested_action="优化页面内容与广告文案的相关性，提高首屏吸引力",
                    expected_impact="提高用户留存率",
                    details={"bounce_rate": lp.bounce_rate}
                ))

            # 检查移动端适配
            if not lp.mobile_friendly:
                results.append(DiagnosisResult(
                    strategy_id="S024",
                    strategy_name="Landing Page 体验检查",
                    severity=Severity.P2,
                    issue_type="移动端体验不佳",
                    affected_object=f"Landing Page: {lp.url}",
                    current_value="非移动优先",
                    benchmark_value="移动友好",
                    suggested_action="采用响应式设计，优化移动端体验",
                    expected_impact="提高移动端转化率",
                    details={}
                ))

            # 检查搜索词匹配度
            if lp.search_term_match_rate < 0.5:
                results.append(DiagnosisResult(
                    strategy_id="S024",
                    strategy_name="Landing Page 体验检查",
                    severity=Severity.P2,
                    issue_type="搜索词匹配度低",
                    affected_object=f"Landing Page: {lp.url}",
                    current_value=f"匹配率 {lp.search_term_match_rate*100:.1f}%",
                    benchmark_value="> 50%",
                    suggested_action="优化落地页内容与搜索关键词的相关性",
                    expected_impact="提高质量得分和转化率",
                    details={"match_rate": lp.search_term_match_rate}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S024",
                strategy_name="Landing Page 体验检查",
                severity=Severity.OK,
                issue_type="Landing Page 体验良好",
                affected_object=f"Campaign: {campaign.name}",
                current_value="加载快、跳出率低、移动友好",
                benchmark_value="OK",
                suggested_action="持续监控页面性能",
                details={}
            ))

        return results

    def check_quality_score_detailed(self, qs_diagnosis: List[Any], campaign: Campaign) -> List[DiagnosisResult]:
        """S025: Quality Score 详细诊断"""
        results = []

        for qs in qs_diagnosis:
            # 检查整体质量得分
            if qs.quality_score <= 4:
                results.append(DiagnosisResult(
                    strategy_id="S025",
                    strategy_name="Quality Score 详细诊断",
                    severity=Severity.P1,
                    issue_type="质量得分过低",
                    affected_object=f"Keyword: {qs.keyword_text}",
                    current_value=f"QS {qs.quality_score}/10",
                    benchmark_value=">= 7",
                    suggested_action="检查广告相关性、落地页体验和预期点击率",
                    expected_impact="提高质量得分，降低CPC",
                    details={"quality_score": qs.quality_score, "ad_relevance": qs.ad_relevance, "landing_page_experience": qs.landing_page_experience}
                ))
            elif qs.quality_score <= 6:
                results.append(DiagnosisResult(
                    strategy_id="S025",
                    strategy_name="Quality Score 详细诊断",
                    severity=Severity.P2,
                    issue_type="质量得分有提升空间",
                    affected_object=f"Keyword: {qs.keyword_text}",
                    current_value=f"QS {qs.quality_score}/10",
                    benchmark_value=">= 7",
                    suggested_action="优化广告文案与关键词匹配度",
                    expected_impact="进一步提高质量得分",
                    details={"quality_score": qs.quality_score}
                ))

            # 检查广告相关性
            if qs.ad_relevance == "BELOW_AVERAGE":
                results.append(DiagnosisResult(
                    strategy_id="S025",
                    strategy_name="Quality Score 详细诊断",
                    severity=Severity.P2,
                    issue_type="广告相关性低",
                    affected_object=f"Keyword: {qs.keyword_text}",
                    current_value="Below average",
                    benchmark_value="Average or Above average",
                    suggested_action="在广告文案中包含关键词，提高相关性",
                    expected_impact="提高广告排名，降低CPC",
                    details={}
                ))

            # 检查落地页体验
            if qs.landing_page_experience == "BELOW_AVERAGE":
                results.append(DiagnosisResult(
                    strategy_id="S025",
                    strategy_name="Quality Score 详细诊断",
                    severity=Severity.P2,
                    issue_type="落地页体验差",
                    affected_object=f"Keyword: {qs.keyword_text}",
                    current_value="Below average",
                    benchmark_value="Average or Above average",
                    suggested_action="优化落地页加载速度和内容相关性",
                    expected_impact="提高质量得分和转化率",
                    details={}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S025",
                strategy_name="Quality Score 详细诊断",
                severity=Severity.OK,
                issue_type="质量得分良好",
                affected_object=f"Campaign: {campaign.name}",
                current_value="平均 QS >= 7",
                benchmark_value="OK",
                suggested_action="持续优化保持高分",
                details={}
            ))

        return results

    def check_policy_status(self, policy_status: Any, campaign: Campaign) -> List[DiagnosisResult]:
        """S038: 政策与合规检查"""
        results = []

        # Handle both single object and list
        policies = policy_status if isinstance(policy_status, list) else [policy_status]

        for policy in policies:
            # 检查被拒状态
            if policy.approval_status == "DISAPPROVED":
                results.append(DiagnosisResult(
                    strategy_id="S038",
                    strategy_name="政策与合规检查",
                    severity=Severity.P0,
                    issue_type="广告被拒登",
                    affected_object=f"Campaign: {policy.campaign_name}",
                    current_value=f"拒登 - {', '.join(policy.disapproval_reasons)}",
                    benchmark_value="APPROVED",
                    suggested_action="立即修改违规内容或联系Google申诉",
                    expected_impact="恢复广告展示",
                    details={"disapproval_reasons": policy.disapproval_reasons, "asset_issues": policy.asset_issues}
                ))

            # 检查URL问题
            if policy.broken_urls:
                results.append(DiagnosisResult(
                    strategy_id="S038",
                    strategy_name="政策与合规检查",
                    severity=Severity.P1,
                    issue_type="链接失效",
                    affected_object=f"Campaign: {policy.campaign_name}",
                    current_value=f"{len(policy.broken_urls)} 个失效链接",
                    benchmark_value="0",
                    suggested_action="修复失效链接",
                    expected_impact="恢复广告正常投放",
                    details={"broken_urls": policy.broken_urls}
                ))

            # 检查投放异常
            if policy.enabled_no_impressions and policy.no_impression_hours > 24:
                results.append(DiagnosisResult(
                    strategy_id="S038",
                    strategy_name="政策与合规检查",
                    severity=Severity.P1,
                    issue_type="启用但无展示",
                    affected_object=f"Campaign: {policy.campaign_name}",
                    current_value=f"{policy.no_impression_hours} 小时无展示",
                    benchmark_value="< 24 小时",
                    suggested_action="检查预算、出价、关键词匹配",
                    expected_impact="恢复广告展示",
                    details={"no_impression_hours": policy.no_impression_hours}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S038",
                strategy_name="政策与合规检查",
                severity=Severity.OK,
                issue_type="合规状态良好",
                affected_object=f"Campaign: {campaign.name}",
                current_value="所有广告符合政策",
                benchmark_value="OK",
                suggested_action="持续监控政策更新",
                details={}
            ))

        return results

    def check_ecommerce_feed(self, feed_items: List[Any], campaign: Campaign) -> List[DiagnosisResult]:
        """S039-S053: 电商Feed与PMAX专项"""
        results = []

        total_items = len(feed_items)
        if total_items == 0:
            return results

        approved_items = sum(1 for f in feed_items if f.status == "ACTIVE")
        disapproved_items = [f for f in feed_items if f.status == "DISAPPROVED"]
        low_quality_titles = [f for f in feed_items if len(f.title) < 30]  # 标题过短
        missing_images = [f for f in feed_items if not f.image_url]
        low_stock_items = [f for f in feed_items if f.availability == "OUT_OF_STOCK"]
        weak_descriptions = [f for f in feed_items if len(f.description) < 50]

        # S039: Feed整体健康度
        approval_rate = approved_items / total_items if total_items > 0 else 0
        if approval_rate < 0.95:
            severity = Severity.P1 if approval_rate < 0.9 else Severity.P2
            results.append(DiagnosisResult(
                strategy_id="S039",
                strategy_name="Feed 健康度概览",
                severity=severity,
                issue_type="Feed批准率低",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{approval_rate*100:.1f}% ({approved_items}/{total_items})",
                benchmark_value=">= 95%",
                suggested_action="检查并修复被拒登的商品，确保符合购物广告政策",
                expected_impact="提高商品曝光率",
                details={"approval_rate": approval_rate, "total": total_items, "approved": approved_items}
            ))

        # S040: 单品批准状态
        for item in disapproved_items[:5]:
            results.append(DiagnosisResult(
                strategy_id="S040",
                strategy_name="单品批准状态",
                severity=Severity.P1,
                issue_type="商品状态异常",
                affected_object=f"Product: {item.title}",
                current_value=f"状态: {item.status}",
                benchmark_value="ACTIVE",
                suggested_action="检查商品Feed，确保信息完整合规",
                expected_impact="恢复商品展示",
                details={"product_id": item.product_id}
            ))

        # S041: 标题质量
        if len(low_quality_titles) > total_items * 0.1:
            results.append(DiagnosisResult(
                strategy_id="S041",
                strategy_name="产品标题优化",
                severity=Severity.P2,
                issue_type="标题质量低",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(low_quality_titles)} 个商品标题质量低",
                benchmark_value="< 10%",
                suggested_action="优化标题，包含品牌、型号、关键属性",
                expected_impact="提高搜索匹配度",
                details={"count": len(low_quality_titles)}
            ))

        # S042: 图片质量
        if len(missing_images) > total_items * 0.05:
            results.append(DiagnosisResult(
                strategy_id="S042",
                strategy_name="图片质量",
                severity=Severity.P2,
                issue_type="图片缺失或质量低",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(missing_images)} 个商品图片问题",
                benchmark_value="< 5%",
                suggested_action="上传高质量白底产品图，尺寸至少800x800",
                expected_impact="提高点击率和转化率",
                details={"count": len(missing_images)}
            ))

        # S043: 属性完整性
        missing_gtin = sum(1 for f in feed_items if not f.gtin)
        missing_brand = sum(1 for f in feed_items if not f.brand)
        if missing_gtin > total_items * 0.2:
            results.append(DiagnosisResult(
                strategy_id="S043",
                strategy_name="属性完整性",
                severity=Severity.P2,
                issue_type="GTIN缺失",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{missing_gtin} 个商品缺少GTIN",
                benchmark_value="< 20%",
                suggested_action="补充GTIN，提高商品识别度",
                expected_impact="提高广告相关性和展示机会",
                details={"missing_gtin": missing_gtin}
            ))

        # S044: 价格竞争力 (基于ROAS评估)
        high_price_items = [f for f in feed_items if f.roas > 4.0]
        for item in high_price_items[:3]:
            results.append(DiagnosisResult(
                strategy_id="S044",
                strategy_name="价格竞争力",
                severity=Severity.OK,
                issue_type="价格具有竞争力",
                affected_object=f"Product: {item.title}",
                current_value=f"ROAS {item.roas:.1f}x",
                benchmark_value="-",
                suggested_action="保持价格优势，考虑突出显示",
                expected_impact="提高转化概率",
                details={}
            ))

        # S045: 库存状态
        if len(low_stock_items) > 0:
            results.append(DiagnosisResult(
                strategy_id="S045",
                strategy_name="库存状态",
                severity=Severity.P2,
                issue_type="库存不足或缺货",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(low_stock_items)} 个商品库存问题",
                benchmark_value="0",
                suggested_action="补充库存或暂停缺货商品广告",
                expected_impact="避免浪费广告预算",
                details={"low_stock_count": len(low_stock_items)}
            ))

        # S046: 产品描述质量
        if len(weak_descriptions) > total_items * 0.2:
            results.append(DiagnosisResult(
                strategy_id="S046",
                strategy_name="产品描述质量",
                severity=Severity.P2,
                issue_type="描述过短",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{len(weak_descriptions)} 个描述<50字符",
                benchmark_value="< 20%",
                suggested_action="撰写详细的产品描述，突出卖点和用途",
                expected_impact="提高广告质量",
                details={"count": len(weak_descriptions)}
            ))

        # S047: 品牌信息完整性
        missing_mpn = sum(1 for f in feed_items if not f.mpn)
        if missing_mpn > total_items * 0.3:
            results.append(DiagnosisResult(
                strategy_id="S047",
                strategy_name="品牌信息完整性",
                severity=Severity.P2,
                issue_type="MPN信息缺失",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{missing_mpn} 个商品无MPN",
                benchmark_value="< 30%",
                suggested_action="补充品牌MPN信息，提高商品识别度",
                expected_impact="更精准的商品匹配和展示",
                details={"missing_mpn": missing_mpn}
            ))

        # S078: Feed基础信息完整性与合规检查
        # 检查产品标题长度和品牌关键词
        for item in feed_items:
            if len(item.title) < 50 or not any(brand.lower() in item.title.lower() for brand in [item.brand, "Brand"] if brand):
                results.append(DiagnosisResult(
                    strategy_id="S078",
                    strategy_name="Feed基础信息完整性与合规检查",
                    severity=Severity.P2,
                    issue_type="产品标题不完整",
                    affected_object=f"Product: {item.title[:50]}",
                    current_value=f"标题长度 {len(item.title)}, 缺少品牌关键词",
                    benchmark_value="标题>=50字符且包含品牌",
                    suggested_action="优化标题，补充品牌关键词和产品特性",
                    expected_impact="提高搜索匹配度和点击率",
                    details={"product_id": item.product_id, "title_length": len(item.title)}
                ))
                break  # 只报告一个示例

        # 检查Custom Labels使用
        # 由于ProductFeedItem模型没有custom_labels字段，我们模拟检查
        if len(feed_items) > 10:  # 模拟检查
            results.append(DiagnosisResult(
                strategy_id="S078",
                strategy_name="Feed基础信息完整性与合规检查",
                severity=Severity.OK,
                issue_type="Custom Labels配置检查",
                affected_object=f"Campaign: {campaign.name}",
                current_value="建议配置Custom Labels用于细分",
                benchmark_value="按ROI/季节/促销分类",
                suggested_action="添加Custom Labels用于商品分组和出价调整",
                expected_impact="更精准的商品管理和竞价",
                details={}
            ))

        # S048: Feed更新频率
        results.append(DiagnosisResult(
            strategy_id="S048",
            strategy_name="Feed 更新频率",
            severity=Severity.OK,
            issue_type="建议定期更新",
            affected_object=f"Campaign: {campaign.name}",
            current_value="建议每日更新",
            benchmark_value="每日",
            suggested_action="保持Feed每日自动更新，价格库存变动时立即更新",
            expected_impact="确保广告信息准确",
            details={}
        ))

        # S049: PMAX受众信号
        results.append(DiagnosisResult(
            strategy_id="S049",
            strategy_name="PMAX受众信号",
            severity=Severity.OK,
            issue_type="检查受众信号配置",
            affected_object=f"Campaign: {campaign.name}",
            current_value="需手动检查",
            benchmark_value="配置完成",
            suggested_action="确保已添加客户列表、网站访客等受众信号",
            expected_impact="加速机器学习，提高效果",
            details={}
        ))

        # S050: 素材组多样性
        results.append(DiagnosisResult(
            strategy_id="S050",
            strategy_name="素材组多样性",
            severity=Severity.OK,
            issue_type="检查素材数量",
            affected_object=f"Campaign: {campaign.name}",
            current_value="建议每种素材至少5个",
            benchmark_value=">= 5",
            suggested_action="上传多种尺寸的图片和视频，不同文案角度",
            expected_impact="扩大覆盖面和转化机会",
            details={}
        ))

        # S051: Feed性能分析 - 低CTR商品
        low_ctr_items = [f for f in feed_items if f.ctr < 0.5 and f.impressions > 100]
        for item in low_ctr_items[:3]:
            results.append(DiagnosisResult(
                strategy_id="S051",
                strategy_name="Feed性能分析",
                severity=Severity.P2,
                issue_type="商品CTR偏低",
                affected_object=f"Product: {item.title}",
                current_value=f"CTR {item.ctr:.2f}%",
                benchmark_value="> 0.5%",
                suggested_action="优化商品标题和图片，提高吸引力",
                expected_impact="提高点击率和流量",
                details={}
            ))

        # S052: PMAX预算与ROAS监控
        if campaign.budget > 0:
            roas = campaign.conversion_value / campaign.cost if campaign.cost > 0 else 0
            if roas < 2.0 and campaign.cost > campaign.budget * 0.8:
                results.append(DiagnosisResult(
                    strategy_id="S052",
                    strategy_name="PMAX预算与ROAS监控",
                    severity=Severity.P2,
                    issue_type="PMAX ROAS偏低",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"ROAS {roas:.2f}",
                    benchmark_value=">= 2.0",
                    suggested_action="优化受众信号，增加否定关键词，调整素材",
                    expected_impact="提高PMAX广告效果",
                    details={"roas": roas}
                ))

        # S092-S093: 价格竞争力与促销审核
        # S093: 价格竞争力与促销机会自动识别
        for item in feed_items:
            if item.impressions > 1000:  # 有足够数据的商品
                # 检查CTR/CVR下降
                if item.ctr < 0.3 and item.cvr < campaign.cvr * 0.8:  # CTR和CVR都偏低
                    results.append(DiagnosisResult(
                        strategy_id="S093",
                        strategy_name="价格竞争力与促销机会自动识别",
                        severity=Severity.P1,
                        issue_type="商品CTR/CVR下降，价格可能不具竞争力",
                        affected_object=f"Product: {item.title}",
                        current_value=f"CTR {item.ctr:.2f}%, CVR {item.cvr:.2f}%",
                        benchmark_value=f"CTR>0.5%, CVR>{campaign.cvr*0.8:.2f}%",
                        suggested_action="检查价格竞争力，考虑促销或降价",
                        expected_impact="提高点击率和转化率",
                        details={"product_id": item.product_id, "ctr": item.ctr, "cvr": item.cvr}
                    ))
                    break  # 只报告一个

        # S053: 季节性产品更新
        results.append(DiagnosisResult(
            strategy_id="S053",
            strategy_name="季节性产品更新",
            severity=Severity.OK,
            issue_type="检查季节性商品",
            affected_object=f"Campaign: {campaign.name}",
            current_value="需人工确认",
            benchmark_value="-",
            suggested_action="根据季节和促销节点更新主打商品",
            expected_impact="把握销售旺季机会",
            details={}
        ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S039-S053",
                strategy_name="电商Feed与PMAX专项",
                severity=Severity.OK,
                issue_type="电商广告状态良好",
                affected_object=f"Campaign: {campaign.name}",
                current_value="Feed健康，商品状态正常",
                benchmark_value="OK",
                suggested_action="持续优化Feed质量",
                details={}
            ))

        return results
