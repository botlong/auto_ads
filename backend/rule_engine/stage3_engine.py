"""
Stage 3 Rule Engine - Workstream Execution (S054-S074)
基于 Stage 1-2 的诊断结果，执行系统化的优化动作
"""

from typing import List, Dict, Any
from datetime import datetime
from models.schemas import (
    Campaign, SearchTerm, Keyword, ResponsiveSearchAd, LocationPerformance,
    AudiencePerformance, DevicePerformance, HourlyPerformance,
    TrackingAudit, WasteControlItem, BudgetReallocation, AdOptimization,
    LandingPageIssue, BidAdjustment, FeedQualityIssue, HeroProductBudget,
    WorkstreamResult, Stage3DiagnosisResponse, Alert, Severity,
    Stage2DataResponse
)


class Stage3Engine:
    """Stage 3 规则引擎 - Workstream 执行"""

    def __init__(self, campaigns: List[Campaign], stage2_data: Dict[str, Stage2DataResponse]):
        self.campaigns = {c.id: c for c in campaigns}
        self.stage2_data = stage2_data
        self.execution_time = datetime.now()
        self.alerts: List[Alert] = []
        self.workstreams: List[WorkstreamResult] = []

    def run_all_workstreams(self) -> Stage3DiagnosisResponse:
        """运行所有 Workstream"""
        # 运行各个 Workstream
        tracking_audits = self.run_w1_tracking_audit()
        waste_controls = self.run_w2_waste_control()
        budget_reallocations = self.run_w3_budget_reallocation()
        ad_optimizations = self.run_w4_ad_optimization()
        landing_page_issues = self.run_w5_landing_page_optimization()
        bid_adjustments = self.run_w6_refined_targeting()
        feed_quality_issues = self.run_w7_feed_optimization()
        hero_product_budgets = self.run_w8_budget_tilt()

        # 计算汇总数据
        total_savings = sum(w.estimated_savings for w in waste_controls)
        total_actions = (
            len(waste_controls) + len(budget_reallocations) +
            len(ad_optimizations) + len(bid_adjustments)
        )

        return Stage3DiagnosisResponse(
            execution_time=self.execution_time,
            data_range="Last 7 Days",
            scanned_campaigns=len(self.campaigns),
            workstreams=self.workstreams,
            tracking_audits=tracking_audits,
            waste_controls=waste_controls,
            budget_reallocations=budget_reallocations,
            ad_optimizations=ad_optimizations,
            landing_page_issues=landing_page_issues,
            bid_adjustments=bid_adjustments,
            feed_quality_issues=feed_quality_issues,
            hero_product_budgets=hero_product_budgets,
            total_estimated_savings=total_savings,
            total_actions_recommended=total_actions,
            summary={
                "workstreams_completed": len(self.workstreams),
                "total_issues_found": sum(w.issues_found for w in self.workstreams),
                "total_actions": total_actions,
                "estimated_monthly_savings": total_savings * 4,
            }
        )

    # ============ W1: 先修追踪 (S054-S055) ============
    def run_w1_tracking_audit(self) -> List[TrackingAudit]:
        """W1: 转化数据质量审计"""
        audits = []
        issues_found = 0

        for campaign_id, campaign in self.campaigns.items():
            data = self.stage2_data.get(campaign_id)
            if not data:
                continue

            # 检查追踪质量
            issues = []
            fixes = []

            # S054: 检查转化目标配置
            if campaign.conversions == 0 and campaign.cost > 100:
                issues.append("有花费但无转化记录，可能存在追踪问题")
                fixes.append("检查转化代码是否正确安装")
                issues_found += 1

            # S055: 检查转化价值准确性
            if campaign.conversions > 0 and campaign.conversion_value == 0:
                if campaign.business_type.value == "Ecommerce":
                    issues.append("电商 Campaign 转化价值为 0，需配置价值追踪")
                    fixes.append("设置动态转化价值或更新转化代码")
                    issues_found += 1

            # 确定审计状态
            audit_status = "PASS" if len(issues) == 0 else ("CRITICAL" if len(issues) > 1 else "WARNING")

            audits.append(TrackingAudit(
                account_id=campaign_id,
                audit_status=audit_status,
                primary_goal_correct=len(issues) == 0,
                conversion_value_accurate=campaign.conversion_value > 0 or campaign.conversions == 0,
                tag_active=campaign.conversions > 0 or campaign.cost < 50,
                enhanced_conversions_working=True,  # 简化处理
                issues=issues,
                fix_recommendations=fixes
            ))

        # 记录 Workstream 结果
        self.workstreams.append(WorkstreamResult(
            workstream_id="W1",
            workstream_name="先修追踪",
            description="转化数据质量审计，修正 Primary Goal",
            status="COMPLETED",
            priority="P1",
            issues_found=issues_found,
            issues_resolved=0,
            actions_recommended=len([a for a in audits if a.audit_status != "PASS"]),
            estimated_savings=0,
            estimated_gain=0
        ))

        return audits

    # ============ W2: 控制浪费 (S056-S059) ============
    def run_w2_waste_control(self) -> List[WasteControlItem]:
        """W2: 多维度无效流量清理"""
        waste_items = []
        total_savings = 0

        for campaign_id, data in self.stage2_data.items():
            campaign = self.campaigns.get(campaign_id)
            if not campaign:
                continue

            target_cpa = campaign.target_cpa or campaign.actual_cpa * 1.2

            # S056: 搜索词负向过滤
            for term in data.search_terms:
                if term.is_negative_candidate and term.cost > target_cpa * 1.2:
                    waste_items.append(WasteControlItem(
                        item_type="SEARCH_TERM",
                        item_id=term.id,
                        item_name=term.search_term,
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        cost=term.cost,
                        conversions=term.conversions,
                        cpa_vs_target=term.cpa / target_cpa if target_cpa > 0 else 999,
                        recommended_action="ADD_NEGATIVE",
                        estimated_savings=term.cost * 0.8  # 预计可节省 80%
                    ))
                    total_savings += term.cost * 0.8

            # S057: 地域排除
            for loc in data.locations:
                if loc.is_underperforming and loc.cost > target_cpa * 2:
                    waste_items.append(WasteControlItem(
                        item_type="LOCATION",
                        item_id=loc.id,
                        item_name=loc.location_name,
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        cost=loc.cost,
                        conversions=loc.conversions,
                        cpa_vs_target=loc.cpa / target_cpa if target_cpa > 0 else 999,
                        recommended_action="EXCLUDE_LOCATION",
                        estimated_savings=loc.cost * 0.7
                    ))
                    total_savings += loc.cost * 0.7

            # S058: 受众排除
            for aud in data.audiences:
                if aud.is_underperforming and aud.cost > target_cpa * 1.5:
                    waste_items.append(WasteControlItem(
                        item_type="AUDIENCE",
                        item_id=aud.id,
                        item_name=aud.audience_name,
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        cost=aud.cost,
                        conversions=aud.conversions,
                        cpa_vs_target=aud.cpa / target_cpa if target_cpa > 0 else 999,
                        recommended_action="EXCLUDE_AUDIENCE",
                        estimated_savings=aud.cost * 0.6
                    ))
                    total_savings += aud.cost * 0.6

            # S059: 设备出价调整
            for device in data.devices:
                if device.is_underperforming and device.cost > target_cpa * 2:
                    waste_items.append(WasteControlItem(
                        item_type="DEVICE",
                        item_id=f"{campaign_id}_{device.device_type}",
                        item_name=device.device_type,
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        cost=device.cost,
                        conversions=device.conversions,
                        cpa_vs_target=device.cpa / target_cpa if target_cpa > 0 else 999,
                        recommended_action="REDUCE_BID",
                        estimated_savings=device.cost * 0.5
                    ))
                    total_savings += device.cost * 0.5

        # 记录 Workstream 结果
        self.workstreams.append(WorkstreamResult(
            workstream_id="W2",
            workstream_name="控制浪费",
            description="排除低质搜索词/地域/受众/流量",
            status="COMPLETED",
            priority="P1",
            issues_found=len(waste_items),
            issues_resolved=0,
            actions_recommended=len(waste_items),
            estimated_savings=total_savings,
            estimated_gain=0
        ))

        return waste_items

    # ============ W3: 预算重分配 (S060-S062) ============
    def run_w3_budget_reallocation(self) -> List[BudgetReallocation]:
        """W3: 跨系列预算动态平衡"""
        reallocations = []

        # 分析所有 Campaign 的效率
        efficient_campaigns = []
        inefficient_campaigns = []

        for campaign_id, campaign in self.campaigns.items():
            if campaign.status.value != "ENABLED":
                continue

            roas = campaign.actual_roas
            target_roas = campaign.target_roas or roas * 1.2
            cpa = campaign.actual_cpa
            target_cpa = campaign.target_cpa or cpa * 0.8

            # 判断效率
            if roas > target_roas * 1.1 and campaign.search_budget_lost_impression_share > 15:
                efficient_campaigns.append(campaign)
            elif roas < target_roas * 0.8 or cpa > target_cpa * 1.3:
                inefficient_campaigns.append(campaign)

        # S060-S062: 生成预算重分配建议
        for ineff_campaign in inefficient_campaigns:
            for eff_campaign in efficient_campaigns:
                if ineff_campaign.cost > 100:
                    transfer_amount = min(ineff_campaign.cost * 0.2, 500)
                    reallocations.append(BudgetReallocation(
                        source_campaign_id=ineff_campaign.id,
                        source_campaign_name=ineff_campaign.name,
                        target_campaign_id=eff_campaign.id,
                        target_campaign_name=eff_campaign.name,
                        source_performance="UNDERPERFORMING",
                        target_potential="HIGH_POTENTIAL",
                        suggested_amount=transfer_amount,
                        suggested_percent=20,
                        reason=f"{ineff_campaign.name} ROAS 低于目标，建议转移部分预算至高效 Campaign"
                    ))

        # 记录 Workstream 结果
        self.workstreams.append(WorkstreamResult(
            workstream_id="W3",
            workstream_name="预算重分配",
            description="跨系列预算动态平衡",
            status="COMPLETED",
            priority="P1",
            issues_found=len(inefficient_campaigns),
            issues_resolved=0,
            actions_recommended=len(reallocations),
            estimated_savings=sum(r.suggested_amount for r in reallocations) * 0.3,
            estimated_gain=sum(r.suggested_amount for r in reallocations) * 0.2
        ))

        return reallocations

    # ============ W4: 优化广告 (S063-S065) ============
    def run_w4_ad_optimization(self) -> List[AdOptimization]:
        """W4: Ad Strength 补全、素材刷新"""
        optimizations = []

        for campaign_id, data in self.stage2_data.items():
            campaign = self.campaigns.get(campaign_id)
            if not campaign:
                continue

            for ad in data.ads:
                suggestions = []
                priority = "LOW"

                # S063: Ad Strength 补全
                if ad.ad_strength_rating < 3:
                    if len(ad.headlines) < 10:
                        suggestions.append("ADD_HEADLINES")
                        priority = "HIGH"
                    if len(ad.descriptions) < 3:
                        suggestions.append("ADD_DESCRIPTIONS")
                        priority = "HIGH" if priority == "HIGH" else "MEDIUM"

                # S064: 素材刷新 (检查 CTR 和 CVR)
                if ad.ctr < 1.0 and ad.impressions > 1000:
                    suggestions.append("REFRESH_ASSETS")
                    priority = "MEDIUM"

                # S065: Offer 注入 (检查 CVR)
                if ad.cvr < campaign.cvr * 0.5 and ad.clicks > 50:
                    suggestions.append("ADD_OFFER")
                    priority = "HIGH"

                # S064: 检查过度固定
                pinned_count = sum(1 for h in ad.headlines if h.pinned)
                if pinned_count > 3:
                    suggestions.append("UNPIN_HEADLINES")

                if suggestions:
                    optimizations.append(AdOptimization(
                        ad_id=ad.id,
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        current_strength=ad.ad_strength,
                        headline_count=len(ad.headlines),
                        description_count=len(ad.descriptions),
                        pinned_count=pinned_count,
                        suggestions=suggestions,
                        priority=priority
                    ))

        # 记录 Workstream 结果
        self.workstreams.append(WorkstreamResult(
            workstream_id="W4",
            workstream_name="优化广告",
            description="Ad Strength 补全、素材刷新、Offer 注入",
            status="COMPLETED",
            priority="P2",
            issues_found=len(optimizations),
            issues_resolved=0,
            actions_recommended=len(optimizations),
            estimated_savings=0,
            estimated_gain=len(optimizations) * 50  # 预估每个广告优化带来 $50 增益
        ))

        return optimizations

    # ============ W5: 优化落地页 (S066) ============
    def run_w5_landing_page_optimization(self) -> List[LandingPageIssue]:
        """W5: CVR 诊断 - 速度/相关性/表单/信任"""
        issues = []

        for campaign_id, campaign in self.campaigns.items():
            # 模拟落地页问题检测
            cvr_gap = campaign.cvr - 0.02  # 假设基准 CVR 为 2%

            if cvr_gap < -0.01 and campaign.clicks > 100:
                # CVR 明显低于基准
                landing_issues = []
                fix_priority = "P2"

                if campaign.cvr < 0.01:
                    landing_issues.append("HIGH_BOUNCE")
                    fix_priority = "P1"
                if campaign.business_type.value == "Lead_Gen" and campaign.cvr < 0.015:
                    landing_issues.append("FORM_FRICTION")

                issues.append(LandingPageIssue(
                    url=f"https://example.com/landing/{campaign_id}",
                    campaign_id=campaign_id,
                    campaign_name=campaign.name,
                    http_status=200,
                    load_time_seconds=3.5,
                    mobile_friendly=True,
                    bounce_rate=0.75,
                    expected_cvr=0.025,
                    actual_cvr=campaign.cvr,
                    cvr_gap=abs(cvr_gap),
                    issues=landing_issues,
                    fix_priority=fix_priority
                ))

        # 记录 Workstream 结果
        self.workstreams.append(WorkstreamResult(
            workstream_id="W5",
            workstream_name="优化落地页",
            description="CVR 诊断：速度/相关性/表单/信任",
            status="COMPLETED",
            priority="P2",
            issues_found=len(issues),
            issues_resolved=0,
            actions_recommended=len(issues),
            estimated_savings=0,
            estimated_gain=sum(i.cvr_gap * campaign.cost for i, (_, campaign) in zip(issues, self.campaigns.items())) if issues else 0
        ))

        return issues

    # ============ W6: 精细化定向 (S067-S070) ============
    def run_w6_refined_targeting(self) -> List[BidAdjustment]:
        """W6: 设备/地域/人群/时段多维汰换"""
        adjustments = []

        for campaign_id, data in self.stage2_data.items():
            campaign = self.campaigns.get(campaign_id)
            if not campaign:
                continue

            avg_cpa = campaign.actual_cpa
            avg_roas = campaign.actual_roas

            # S067: 设备出价调整
            for device in data.devices:
                if device.cpa > avg_cpa * 1.3 and device.conversions > 0:
                    adjustments.append(BidAdjustment(
                        dimension="DEVICE",
                        dimension_id=f"{campaign_id}_{device.device_type}",
                        dimension_name=device.device_type,
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        current_modifier=device.bid_modifier,
                        performance_vs_avg=device.cpa / avg_cpa if avg_cpa > 0 else 1,
                        cpa=device.cpa,
                        roas=0,
                        suggested_modifier=device.bid_modifier - 15,
                        adjustment_reason="CPA 高于平均值 30% 以上，建议降低出价",
                        expected_impact="降低该设备出价以减少低效花费"
                    ))
                elif device.cpa < avg_cpa * 0.7 and device.conversions >= 3:
                    adjustments.append(BidAdjustment(
                        dimension="DEVICE",
                        dimension_id=f"{campaign_id}_{device.device_type}",
                        dimension_name=device.device_type,
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        current_modifier=device.bid_modifier,
                        performance_vs_avg=device.cpa / avg_cpa if avg_cpa > 0 else 1,
                        cpa=device.cpa,
                        roas=0,
                        suggested_modifier=min(device.bid_modifier + 15, 100),
                        adjustment_reason="CPA 低于平均值 30% 以上，建议提高出价",
                        expected_impact="增加该设备出价以获取更多高效流量"
                    ))

            # S068: 地域出价调整
            for loc in data.locations:
                if loc.roas > avg_roas * 1.2 and loc.conversions > 0:
                    adjustments.append(BidAdjustment(
                        dimension="LOCATION",
                        dimension_id=loc.id,
                        dimension_name=loc.location_name,
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        current_modifier=loc.bid_modifier,
                        performance_vs_avg=loc.roas / avg_roas if avg_roas > 0 else 1,
                        cpa=loc.cpa,
                        roas=loc.roas,
                        suggested_modifier=min(loc.bid_modifier + 15, 100),
                        adjustment_reason="ROAS 高于平均值 20% 以上",
                        expected_impact="提高该地域出价以获取更多转化"
                    ))

            # S069-S070: 时段出价调整
            for hour in data.hourly:
                if hour.is_high_performance and hour.cpa < avg_cpa * 0.7:
                    adjustments.append(BidAdjustment(
                        dimension="TIME_SLOT",
                        dimension_id=f"{hour.day_of_week}_{hour.hour_of_day}",
                        dimension_name=f"周{hour.day_of_week + 1} {hour.hour_of_day}:00",
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        current_modifier=hour.bid_modifier,
                        performance_vs_avg=hour.cpa / avg_cpa if avg_cpa > 0 else 1,
                        cpa=hour.cpa,
                        roas=0,
                        suggested_modifier=min(hour.bid_modifier + 15, 50),
                        adjustment_reason="高效时段，CPA 低于平均值",
                        expected_impact="在高效时段提高竞价"
                    ))
                elif hour.is_low_performance:
                    adjustments.append(BidAdjustment(
                        dimension="TIME_SLOT",
                        dimension_id=f"{hour.day_of_week}_{hour.hour_of_day}",
                        dimension_name=f"周{hour.day_of_week + 1} {hour.hour_of_day}:00",
                        campaign_id=campaign_id,
                        campaign_name=campaign.name,
                        current_modifier=hour.bid_modifier,
                        performance_vs_avg=hour.cpa / avg_cpa if avg_cpa > 0 else 2,
                        cpa=hour.cpa,
                        roas=0,
                        suggested_modifier=max(hour.bid_modifier - 20, -50),
                        adjustment_reason="低效时段，建议降低出价或暂停",
                        expected_impact="减少低效时段的花费"
                    ))

        # 记录 Workstream 结果
        self.workstreams.append(WorkstreamResult(
            workstream_id="W6",
            workstream_name="精细化定向",
            description="设备/地域/人群/时段多维出价调整",
            status="COMPLETED",
            priority="P2",
            issues_found=len(adjustments),
            issues_resolved=0,
            actions_recommended=len(adjustments),
            estimated_savings=sum(a.current_modifier - a.suggested_modifier for a in adjustments if a.suggested_modifier < a.current_modifier) * 10,
            estimated_gain=sum(a.suggested_modifier - a.current_modifier for a in adjustments if a.suggested_modifier > a.current_modifier) * 10
        ))

        return adjustments

    # ============ W7: Feed 优化 (S071-S072) ============
    def run_w7_feed_optimization(self) -> List[FeedQualityIssue]:
        """W7: 高价值商品 Feed 质量优化 (电商)"""
        issues = []

        # 模拟 Feed 质量问题
        for campaign_id, campaign in self.campaigns.items():
            if campaign.business_type.value != "Ecommerce":
                continue

            # S071: Feed 质量检查
            if campaign.actual_roas < 2.0:
                issues.append(FeedQualityIssue(
                    product_id=f"SKU_{campaign_id}_001",
                    product_name=f"产品 {campaign_id}",
                    campaign_id=campaign_id,
                    title_quality="NEEDS_IMPROVEMENT",
                    image_quality="GOOD",
                    description_quality="POOR",
                    attributes_complete=False,
                    issues=["TITLE_TOO_SHORT", "MISSING_ATTRIBUTES"],
                    improvement_suggestions=["添加品牌名到标题", "补充产品属性"]
                ))

        # 记录 Workstream 结果
        self.workstreams.append(WorkstreamResult(
            workstream_id="W7",
            workstream_name="Feed 优化",
            description="高价值商品 Feed 质量优化",
            status="COMPLETED",
            priority="P1",
            issues_found=len(issues),
            issues_resolved=0,
            actions_recommended=len(issues) * 2,
            estimated_savings=0,
            estimated_gain=len(issues) * 100
        ))

        return issues

    # ============ W8: 预算倾斜 (S073-S074) ============
    def run_w8_budget_tilt(self) -> List[HeroProductBudget]:
        """W8: Hero 商品预算重分配"""
        budgets = []

        for campaign_id, campaign in self.campaigns.items():
            if campaign.business_type.value != "Ecommerce":
                continue

            target_roas = campaign.target_roas or 3.0

            # S073-S074: 商品预算倾斜分析
            if campaign.actual_roas > target_roas * 1.2:
                # Hero 商品
                current_share = 0.3
                recommended_share = 0.5
                budgets.append(HeroProductBudget(
                    product_id=f"HERO_{campaign_id}",
                    product_name=f"Hero Product {campaign_id}",
                    campaign_id=campaign_id,
                    campaign_name=campaign.name,
                    product_label="Hero",
                    current_spend=campaign.cost * 0.3,
                    current_roas=campaign.actual_roas,
                    target_roas=target_roas,
                    current_budget_share=current_share,
                    recommended_budget_share=recommended_share,
                    budget_adjustment=campaign.budget * (recommended_share - current_share)
                ))
            elif campaign.actual_roas < target_roas * 0.7:
                # 低效商品，减少预算
                budgets.append(HeroProductBudget(
                    product_id=f"LOW_{campaign_id}",
                    product_name=f"Low Product {campaign_id}",
                    campaign_id=campaign_id,
                    campaign_name=campaign.name,
                    product_label="Low-efficiency",
                    current_spend=campaign.cost * 0.3,
                    current_roas=campaign.actual_roas,
                    target_roas=target_roas,
                    current_budget_share=0.3,
                    recommended_budget_share=0.15,
                    budget_adjustment=-campaign.budget * 0.15
                ))

        # 记录 Workstream 结果
        self.workstreams.append(WorkstreamResult(
            workstream_id="W8",
            workstream_name="预算倾斜",
            description="Hero 商品预算重分配",
            status="COMPLETED",
            priority="P1",
            issues_found=len(budgets),
            issues_resolved=0,
            actions_recommended=len(budgets),
            estimated_savings=sum(b.budget_adjustment for b in budgets if b.budget_adjustment < 0) * -1,
            estimated_gain=sum(b.budget_adjustment for b in budgets if b.budget_adjustment > 0) * 0.3
        ))

        return budgets
