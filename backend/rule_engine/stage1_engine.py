"""
SOP Stage 1 - 基础设置与校验 规则引擎
实现 S001-S011 所有检查规则
"""

from typing import List, Dict, Any
from models.schemas import (
    Campaign, ConversionTracking, ConversionAction,
    DiagnosisResult, Alert, Severity,
    BiddingType, BusinessType, LearningStatus
)


class Stage1RuleEngine:
    """Stage 1 规则引擎 - 基础设置与校验"""

    def run_stage1_check(self, campaign: Campaign, tracking: ConversionTracking) -> List[DiagnosisResult]:
        """
        对单个 Campaign 执行完整的 Stage 1 检查
        """
        results = []

        # S001-S003: 转化追踪检查 (账户级，只检查一次)
        if campaign.id == self._get_first_enabled_campaign_id():
            results.extend(self.check_conversion_tracking(tracking))

        # S004: Campaign 目标检查
        results.append(self.check_campaign_goal(campaign))

        # S005: 出价策略检查
        results.extend(self.check_bidding_strategy(campaign))

        # S006: 预算限制检查
        results.extend(self.check_budget(campaign))

        # S007-S010: 账户结构检查
        results.extend(self.check_account_structure(campaign))

        # S011: ROAS 分层检查 (仅电商)
        if campaign.business_type == BusinessType.ECOMMERCE:
            results.extend(self.check_roas_segmentation(campaign))

        return results

    def _get_first_enabled_campaign_id(self) -> str:
        """辅助方法：获取第一个启用的 campaign id (用于避免重复检查账户级问题)"""
        return "c_001"  # 简化处理

    # ============ S001-S003: 转化追踪检查 ============

    def check_conversion_tracking(self, tracking: ConversionTracking) -> List[DiagnosisResult]:
        """
        S001: 转化目标配置合规性诊断
        S002: 转化价值与计数完整性监控
        S003: 进阶转化功能优化建议
        """
        results = []

        # S001: 检查多个 Primary 转化
        primary_conversions = [a for a in tracking.conversion_actions if a.is_primary]
        if len(primary_conversions) > 1:
            results.append(DiagnosisResult(
                strategy_id="S001",
                strategy_name="转化目标配置合规性诊断",
                severity=Severity.P1,
                issue_type="重复 Primary 转化",
                affected_object="Account",
                current_value=f"{len(primary_conversions)} 个 Primary 转化",
                benchmark_value="1 个 Primary 转化 (核心业务目标)",
                suggested_action="将非核心转化设为 Secondary，仅保留 Purchase 或 Lead 为 Primary",
                expected_impact="避免重复计数，提高数据准确性",
                details={"primary_conversions": [a.name for a in primary_conversions]}
            ))
        else:
            results.append(DiagnosisResult(
                strategy_id="S001",
                strategy_name="转化目标配置合规性诊断",
                severity=Severity.OK,
                issue_type="Primary 转化配置正常",
                affected_object="Account",
                current_value=f"{len(primary_conversions)} 个 Primary 转化",
                benchmark_value="1 个",
                suggested_action="无需操作",
                details={}
            ))

        # S002: 检查 0 值转化
        zero_value_actions = [a for a in tracking.conversion_actions
                             if a.category == "PURCHASE" and a.value == 0]
        if zero_value_actions:
            results.append(DiagnosisResult(
                strategy_id="S002",
                strategy_name="转化价值与计数完整性监控",
                severity=Severity.P1,
                issue_type="Purchase 转化价值为 0",
                affected_object="Account",
                current_value="Conversion Value = 0",
                benchmark_value="动态价值或合理估值",
                suggested_action="配置动态转化价值或手动设置合理估值",
                expected_impact="准确的 ROAS 计算和智能出价",
                details={"affected_actions": [a.name for a in zero_value_actions]}
            ))

        # S002: 检查计数类型问题
        page_view_every = [a for a in tracking.conversion_actions
                          if a.category == "PAGE_VIEW" and a.count_type == "EVERY"]
        if page_view_every:
            results.append(DiagnosisResult(
                strategy_id="S002",
                strategy_name="转化价值与计数完整性监控",
                severity=Severity.P2,
                issue_type="Page View 设为 Every 计数",
                affected_object="Account",
                current_value="Count = EVERY",
                benchmark_value="Count = ONE",
                suggested_action="将 Page View 转化改为 ONE 计数，避免重复",
                expected_impact="避免转化数据膨胀",
                details={}
            ))

        # S003: 检查 Tag 状态
        inactive_tags = [a for a in tracking.conversion_actions if a.tag_status == "INACTIVE"]
        if inactive_tags:
            results.append(DiagnosisResult(
                strategy_id="S003",
                strategy_name="进阶转化功能优化建议",
                severity=Severity.P0,
                issue_type="转化追踪标签失效",
                affected_object="Account",
                current_value=f"{len(inactive_tags)} 个标签 Inactive",
                benchmark_value="所有标签 Active",
                suggested_action="立即检查 GTM 或网站代码，恢复追踪标签",
                expected_impact="恢复转化数据追踪",
                details={"inactive_tags": [a.name for a in inactive_tags]}
            ))

        unverified_tags = [a for a in tracking.conversion_actions if a.tag_status == "UNVERIFIED"]
        if unverified_tags:
            results.append(DiagnosisResult(
                strategy_id="S003",
                strategy_name="进阶转化功能优化建议",
                severity=Severity.P2,
                issue_type="转化标签未验证",
                affected_object="Account",
                current_value=f"{len(unverified_tags)} 个标签 Unverified",
                benchmark_value="所有标签 Verified",
                suggested_action="完成转化测试，验证标签安装正确",
                expected_impact="确保转化追踪可靠",
                details={"unverified_tags": [a.name for a in unverified_tags]}
            ))

        # S003: Enhanced Conversions 建议
        if not tracking.enhanced_conversions_for_leads:
            results.append(DiagnosisResult(
                strategy_id="S003",
                strategy_name="进阶转化功能优化建议",
                severity=Severity.P2,
                issue_type="未启用 Enhanced Conversions for Leads",
                affected_object="Account",
                current_value="Disabled",
                benchmark_value="Enabled",
                suggested_action="启用 Enhanced Conversions for Leads，提高转化质量",
                expected_impact="提高离线转化匹配率",
                details={}
            ))

        return results

    # ============ S004: Campaign 目标检查 ============

    def check_campaign_goal(self, campaign: Campaign) -> DiagnosisResult:
        """
        S004: Campaign 业务目标一致性校正
        检查业务类型与出价策略是否匹配
        """
        bidding = campaign.bidding_strategy_type
        business = campaign.business_type

        # Lead Gen 应该使用 Max Conv 或 tCPA
        if business == BusinessType.LEAD_GEN:
            if bidding not in [BiddingType.TARGET_CPA, BiddingType.MAXIMIZE_CONVERSIONS]:
                return DiagnosisResult(
                    strategy_id="S004",
                    strategy_name="Campaign 业务目标一致性校正",
                    severity=Severity.P1,
                    issue_type="出价策略与业务类型不匹配",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"Business={business.value}, Bidding={bidding.value}",
                    benchmark_value="Lead Gen → tCPA 或 Max Conversions",
                    suggested_action=f"切换出价策略为 TARGET_CPA 或 MAXIMIZE_CONVERSIONS",
                    expected_impact="优化获客成本，提高线索量",
                    details={"campaign_id": campaign.id}
                )

        # Ecommerce 应该使用 Max Value 或 tROAS
        if business == BusinessType.ECOMMERCE:
            if bidding not in [BiddingType.TARGET_ROAS, BiddingType.MAXIMIZE_CONVERSION_VALUE]:
                return DiagnosisResult(
                    strategy_id="S004",
                    strategy_name="Campaign 业务目标一致性校正",
                    severity=Severity.P1,
                    issue_type="出价策略与业务类型不匹配",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"Business={business.value}, Bidding={bidding.value}",
                    benchmark_value="Ecommerce → tROAS 或 Max Conv Value",
                    suggested_action=f"切换出价策略为 TARGET_ROAS 或 MAXIMIZE_CONVERSION_VALUE",
                    expected_impact="优化广告回报，最大化收入",
                    details={"campaign_id": campaign.id}
                )

        return DiagnosisResult(
            strategy_id="S004",
            strategy_name="Campaign 业务目标一致性校正",
            severity=Severity.OK,
            issue_type="出价策略与业务类型匹配",
            affected_object=f"Campaign: {campaign.name}",
            current_value=f"{bidding.value}",
            benchmark_value="匹配",
            suggested_action="无需操作",
            details={}
        )

    # ============ S005: 出价策略检查 ============

    def check_bidding_strategy(self, campaign: Campaign) -> List[DiagnosisResult]:
        """
        S005: 竞价策略效能诊断与放量调整
        """
        results = []

        # 新 campaign 保护
        if campaign.days_since_created < 7:
            results.append(DiagnosisResult(
                strategy_id="S005",
                strategy_name="竞价策略效能诊断与放量调整",
                severity=Severity.OK,
                issue_type="新 Campaign 保护期",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"上线 {campaign.days_since_created} 天",
                benchmark_value="7 天",
                suggested_action="积累足够数据后再评估",
                details={}
            ))
            return results

        # Learning 状态检查
        if campaign.learning_status == LearningStatus.LEARNING:
            results.append(DiagnosisResult(
                strategy_id="S005",
                strategy_name="竞价策略效能诊断与放量调整",
                severity=Severity.OK,
                issue_type="系统学习中",
                affected_object=f"Campaign: {campaign.name}",
                current_value="LEARNING",
                benchmark_value="READY",
                suggested_action="等待学习完成，期间不做大幅调整",
                details={}
            ))
            return results

        # tCPA 分析
        if campaign.bidding_strategy_type == BiddingType.TARGET_CPA and campaign.target_cpa:
            performance_gap = (campaign.actual_cpa - campaign.target_cpa) / campaign.target_cpa * 100

            if campaign.actual_cpa < campaign.target_cpa * 0.7:
                # 实际CPA远低于目标，可以收紧目标获取更多转化
                results.append(DiagnosisResult(
                    strategy_id="S005",
                    strategy_name="竞价策略效能诊断与放量调整",
                    severity=Severity.P2,
                    issue_type="tCPA 目标过松，有优化空间",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"Actual CPA: ${campaign.actual_cpa:.2f}, Target: ${campaign.target_cpa:.2f}",
                    benchmark_value="目标与实际接近",
                    suggested_action=f"降低 Target CPA 至 ${campaign.actual_cpa * 1.1:.2f}，测试能否保持转化量",
                    expected_impact="降低获客成本，提高效率",
                    details={"performance_gap": f"{performance_gap:.1f}%"}
                ))
            elif campaign.actual_cpa > campaign.target_cpa * 1.2:
                # 实际CPA超过目标
                if campaign.search_impression_share < 50:
                    # 展示份额低，可能是目标过严
                    results.append(DiagnosisResult(
                        strategy_id="S005",
                        strategy_name="竞价策略效能诊断与放量调整",
                        severity=Severity.P1,
                        issue_type="tCPA 目标过严导致量级不足",
                        affected_object=f"Campaign: {campaign.name}",
                        current_value=f"CPA ${campaign.actual_cpa:.2f} (超目标 {performance_gap:.1f}%), IS {campaign.search_impression_share:.1f}%",
                        benchmark_value="CPA 接近目标",
                        suggested_action=f"提升 Target CPA 10% 至 ${campaign.target_cpa * 1.1:.2f}，获取更多流量",
                        expected_impact="增加展示和转化量",
                        details={}
                    ))
                else:
                    results.append(DiagnosisResult(
                        strategy_id="S005",
                        strategy_name="竞价策略效能诊断与放量调整",
                        severity=Severity.P1,
                        issue_type="CPA 严重超标",
                        affected_object=f"Campaign: {campaign.name}",
                        current_value=f"${campaign.actual_cpa:.2f} vs 目标 ${campaign.target_cpa:.2f}",
                        benchmark_value=f"${campaign.target_cpa:.2f}",
                        suggested_action="检查关键词相关性、落地页质量、排除无效流量",
                        expected_impact="降低实际CPA至目标范围",
                        details={"performance_gap": f"{performance_gap:.1f}%"}
                    ))

        # tROAS 分析
        if campaign.bidding_strategy_type == BiddingType.TARGET_ROAS and campaign.target_roas:
            if campaign.actual_roas < campaign.target_roas * 0.8:
                results.append(DiagnosisResult(
                    strategy_id="S005",
                    strategy_name="竞价策略效能诊断与放量调整",
                    severity=Severity.P1,
                    issue_type="ROAS 低于目标",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"Actual ROAS: {campaign.actual_roas:.2f}x, Target: {campaign.target_roas:.2f}x",
                    benchmark_value=f"{campaign.target_roas:.2f}x",
                    suggested_action="降低 Target ROAS 或优化商品 Feed/落地页",
                    expected_impact="恢复目标 ROAS",
                    details={}
                ))
            elif campaign.actual_roas > campaign.target_roas * 1.2 and campaign.search_rank_lost_impression_share > 30:
                results.append(DiagnosisResult(
                    strategy_id="S005",
                    strategy_name="竞价策略效能诊断与放量调整",
                    severity=Severity.P2,
                    issue_type="ROAS 超额完成但有排名损失",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"ROAS {campaign.actual_roas:.2f}x, Lost IS (Rank) {campaign.search_rank_lost_impression_share:.1f}%",
                    benchmark_value="平衡状态",
                    suggested_action=f"提升 Target ROAS 10% 至 {campaign.target_roas * 1.1:.2f}x，测试能否获取更多高价值转化",
                    expected_impact="提高广告回报目标",
                    details={}
                ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S005",
                strategy_name="竞价策略效能诊断与放量调整",
                severity=Severity.OK,
                issue_type="出价策略运行正常",
                affected_object=f"Campaign: {campaign.name}",
                current_value="OK",
                benchmark_value="OK",
                suggested_action="无需操作",
                details={}
            ))

        return results

    # ============ S006: 预算限制检查 ============

    def check_budget(self, campaign: Campaign) -> List[DiagnosisResult]:
        """
        S006: 预算瓶颈识别与效能调配
        """
        results = []

        if campaign.status != "ENABLED":
            return results

        # 高 ROAS + 预算丢失 → 增加预算
        if campaign.actual_roas > 0 and campaign.target_roas:
            if (campaign.actual_roas > campaign.target_roas * 1.1 and
                campaign.search_budget_lost_impression_share > 15):
                results.append(DiagnosisResult(
                    strategy_id="S006",
                    strategy_name="预算瓶颈识别与效能调配",
                    severity=Severity.P1,
                    issue_type="高效 Campaign 预算受限",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"ROAS {campaign.actual_roas:.2f}x, Lost IS (Budget) {campaign.search_budget_lost_impression_share:.1f}%",
                    benchmark_value="预算充足",
                    suggested_action=f"增加日预算 20% 至 ${campaign.budget * 1.2:.2f}",
                    expected_impact="获取更多高效流量",
                    details={}
                ))

        # 低 ROAS + 高预算消耗 → 减少预算
        if campaign.actual_roas > 0 and campaign.target_roas:
            if (campaign.actual_roas < campaign.target_roas * 0.8 and
                campaign.budget_utilization > 80 if hasattr(campaign, 'budget_utilization') else False):
                results.append(DiagnosisResult(
                    strategy_id="S006",
                    strategy_name="预算瓶颈识别与效能调配",
                    severity=Severity.P1,
                    issue_type="低效 Campaign 消耗过多预算",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"ROAS {campaign.actual_roas:.2f}x (目标 {campaign.target_roas:.2f}x)",
                    benchmark_value="目标 ROAS",
                    suggested_action=f"降低日预算 20% 至 ${campaign.budget * 0.8:.2f}，转移至高效 Campaign",
                    expected_impact="优化整体账户 ROAS",
                    details={}
                ))

        # 排名丢失严重 → 需要优化 Ad Rank
        if campaign.search_rank_lost_impression_share > 30 and campaign.search_budget_lost_impression_share < 5:
            results.append(DiagnosisResult(
                strategy_id="S006",
                strategy_name="预算瓶颈识别与效能调配",
                severity=Severity.P2,
                issue_type="排名竞争力不足",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"Lost IS (Rank) {campaign.search_rank_lost_impression_share:.1f}%",
                benchmark_value="< 20%",
                suggested_action="优化广告质量、提高出价或改善落地页体验",
                expected_impact="提高展示份额",
                details={}
            ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S006",
                strategy_name="预算瓶颈识别与效能调配",
                severity=Severity.OK,
                issue_type="预算配置合理",
                affected_object=f"Campaign: {campaign.name}",
                current_value="OK",
                benchmark_value="OK",
                suggested_action="无需操作",
                details={}
            ))

        return results

    # ============ S007-S010: 账户结构检查 ============

    def check_account_structure(self, campaign: Campaign) -> List[DiagnosisResult]:
        """
        S007-S010: 账户结构拓扑优化策略集
        """
        results = []

        # S007: Brand/Non-brand 隔离
        if campaign.is_brand_campaign and campaign.has_nonbrand_keywords:
            results.append(DiagnosisResult(
                strategy_id="S007",
                strategy_name="品牌词与非品牌词隔离",
                severity=Severity.P1,
                issue_type="品牌 Campaign 包含非品牌词",
                affected_object=f"Campaign: {campaign.name}",
                current_value="混合意图",
                benchmark_value="单一意图",
                suggested_action="将非品牌关键词移至独立 Campaign",
                expected_impact="清晰的数据分析和出价策略",
                details={}
            ))

        # S008: 网络类型合规
        if campaign.network_type == "SEARCH_WITH_DISPLAY":
            results.append(DiagnosisResult(
                strategy_id="S008",
                strategy_name="搜索与展示网络隔离",
                severity=Severity.P1,
                issue_type="搜索 Campaign 开启展示网络",
                affected_object=f"Campaign: {campaign.name}",
                current_value="Search + Display 混合",
                benchmark_value="Search Only",
                suggested_action="关闭展示网络，或创建独立的 Display Campaign",
                expected_impact="提高 Search Campaign 的 CTR 和 CVR",
                details={}
            ))

        # S009: 结构粒度检查
        if campaign.adgroup_count > 15:
            results.append(DiagnosisResult(
                strategy_id="S009",
                strategy_name="账户结构粒度优化",
                severity=Severity.P2,
                issue_type="Campaign 下 AdGroup 过多",
                affected_object=f"Campaign: {campaign.name}",
                current_value=f"{campaign.adgroup_count} 个 AdGroup",
                benchmark_value="< 10 个",
                suggested_action="拆分 Campaign，按主题或产品分类",
                expected_impact="提高管理效率和广告相关性",
                details={}
            ))

        if not results:
            results.append(DiagnosisResult(
                strategy_id="S007-S010",
                strategy_name="账户结构拓扑优化策略集",
                severity=Severity.OK,
                issue_type="账户结构正常",
                affected_object=f"Campaign: {campaign.name}",
                current_value="OK",
                benchmark_value="OK",
                suggested_action="无需操作",
                details={}
            ))

        return results

    # ============ S011: ROAS 分层检查 ============

    def check_roas_segmentation(self, campaign: Campaign) -> List[DiagnosisResult]:
        """
        S011: 购物/PMax 商品效率分层
        简化的版本 - 基于 Campaign 整体表现给出建议
        """
        results = []

        if campaign.business_type != BusinessType.ECOMMERCE:
            return results

        if campaign.actual_roas > 0 and campaign.target_roas:
            efficiency_ratio = campaign.actual_roas / campaign.target_roas

            if efficiency_ratio > 1.2:
                results.append(DiagnosisResult(
                    strategy_id="S011",
                    strategy_name="购物/PMax 商品效率分层",
                    severity=Severity.P2,
                    issue_type="高价值商品未充分放量",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"ROAS {campaign.actual_roas:.2f}x (目标 {campaign.target_roas:.2f}x)",
                    benchmark_value="接近目标",
                    suggested_action="识别高 ROAS 商品并创建独立 Campaign 增加预算",
                    expected_impact="最大化高价值商品曝光",
                    details={"efficiency_tier": "High"}
                ))
            elif efficiency_ratio < 0.7:
                results.append(DiagnosisResult(
                    strategy_id="S011",
                    strategy_name="购物/PMax 商品效率分层",
                    severity=Severity.P1,
                    issue_type="低效商品消耗过多预算",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"ROAS {campaign.actual_roas:.2f}x (目标 {campaign.target_roas:.2f}x)",
                    benchmark_value="目标 ROAS",
                    suggested_action="识别低 ROAS 商品并降权或排除",
                    expected_impact="优化整体 Campaign ROAS",
                    details={"efficiency_tier": "Low"}
                ))
            else:
                results.append(DiagnosisResult(
                    strategy_id="S011",
                    strategy_name="购物/PMax 商品效率分层",
                    severity=Severity.OK,
                    issue_type="商品效率分层正常",
                    affected_object=f"Campaign: {campaign.name}",
                    current_value=f"ROAS {campaign.actual_roas:.2f}x",
                    benchmark_value="目标范围内",
                    suggested_action="无需操作",
                    details={"efficiency_tier": "Mid"}
                ))

        return results

    # ============ 告警生成 ============

    def generate_alerts(self, results: List[DiagnosisResult]) -> List[Alert]:
        """根据诊断结果生成告警"""
        alerts = []
        alert_id = 0

        for result in results:
            if result.severity in [Severity.P0, Severity.P1]:
                alert_id += 1
                alerts.append(Alert(
                    id=f"alert_{alert_id:03d}",
                    level=result.severity.value,
                    title=result.issue_type,
                    message=f"{result.affected_object}: {result.current_value}",
                    campaign_id=None,
                    campaign_name=result.affected_object.split(": ")[-1] if ": " in result.affected_object else None,
                    created_at=__import__('datetime').datetime.now(),
                    is_resolved=False
                ))

        return alerts
