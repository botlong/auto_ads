"""
Daily Alert Engine - Real-time Monitoring (S085-S094)
实时监控与告警系统
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
from models.schemas import (
    Campaign, DailyAlert, DailyAlertSummary, DailyAlertResponse,
    DailyAlertType, Severity
)


class DailyAlertEngine:
    """Daily Alert 引擎 - 实时监控"""

    def __init__(self, campaigns: List[Campaign]):
        self.campaigns = campaigns
        self.execution_time = datetime.now()
        self.alerts: List[DailyAlert] = []

    def run_all_checks(self) -> DailyAlertResponse:
        """运行所有 Daily Alert 检查"""
        # 清空之前的告警
        self.alerts = []

        # 运行各项检查
        self.check_performance_anomaly()  # S085
        self.check_budget_pacing()  # S086
        self.check_conversion_anomaly()  # S087
        self.check_delivery_issues()  # S088
        self.check_tracking_health()  # S089
        self.check_search_term_waste()  # S090
        self.check_landing_page_health()  # S091
        self.check_policy_violations()  # S092-S094

        # 生成汇总
        summary = self._generate_summary()

        return DailyAlertResponse(
            execution_time=self.execution_time,
            data_range="Last 24 Hours",
            alerts=self.alerts,
            summary=summary,
            active_alerts=len([a for a in self.alerts if a.status == "ACTIVE"]),
            needs_attention=len([a for a in self.alerts if a.severity in [Severity.P0, Severity.P1]]),
            auto_fixable=len([a for a in self.alerts if a.auto_fix_available])
        )

    def _generate_summary(self) -> DailyAlertSummary:
        """生成告警汇总"""
        # 按类型统计
        alerts_by_type: Dict[str, int] = {}
        for alert in self.alerts:
            alert_type = alert.alert_type.value
            alerts_by_type[alert_type] = alerts_by_type.get(alert_type, 0) + 1

        # 按 Campaign 统计
        alerts_by_campaign: Dict[str, int] = {}
        for alert in self.alerts:
            if alert.campaign_name:
                alerts_by_campaign[alert.campaign_name] = alerts_by_campaign.get(alert.campaign_name, 0) + 1

        return DailyAlertSummary(
            date=self.execution_time.strftime("%Y-%m-%d"),
            total_alerts=len(self.alerts),
            p0_alerts=len([a for a in self.alerts if a.severity == Severity.P0]),
            p1_alerts=len([a for a in self.alerts if a.severity == Severity.P1]),
            p2_alerts=len([a for a in self.alerts if a.severity == Severity.P2]),
            alerts_by_type=alerts_by_type,
            alerts_by_campaign=alerts_by_campaign,
            vs_yesterday=random.randint(-5, 10)  # 模拟与昨天对比
        )

    # ============ S085: 表现异常实时预警 ============
    def check_performance_anomaly(self):
        """S085: 检测花费、点击、展示、转化的异常波动"""
        for campaign in self.campaigns:
            if campaign.status.value != "ENABLED":
                continue

            # 模拟异常检测
            # 花费异常增长
            if campaign.cost > 500 and campaign.days_since_created > 7:
                self.alerts.append(DailyAlert(
                    alert_id=f"perf_{campaign.id}_spend",
                    alert_type=DailyAlertType.PERFORMANCE_ANOMALY,
                    severity=Severity.P1,
                    title="⚠️ 花费异常增长",
                    message=f"{campaign.name} 今日花费较昨日增长 45%，请检查预算设置",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    trigger_metric="spend_change",
                    trigger_value=145.0,  # 145% of yesterday
                    threshold_value=120.0,  # 阈值 120%
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="检查预算上限和出价策略",
                    auto_fix_available=False
                ))

            # 转化断层
            if campaign.conversions == 0 and campaign.clicks > 50:
                self.alerts.append(DailyAlert(
                    alert_id=f"perf_{campaign.id}_conversion",
                    alert_type=DailyAlertType.PERFORMANCE_ANOMALY,
                    severity=Severity.P0,
                    title="🚨 转化断层预警",
                    message=f"{campaign.name} 有 {campaign.clicks} 次点击但无转化，可能存在追踪问题",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    trigger_metric="conversions",
                    trigger_value=0,
                    threshold_value=1,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="立即检查转化追踪代码",
                    auto_fix_available=False
                ))

            # CTR 骤降
            if campaign.ctr < 1.0 and campaign.impressions > 1000:
                self.alerts.append(DailyAlert(
                    alert_id=f"perf_{campaign.id}_ctr",
                    alert_type=DailyAlertType.PERFORMANCE_ANOMALY,
                    severity=Severity.P2,
                    title="📉 CTR 异常降低",
                    message=f"{campaign.name} CTR 降至 {campaign.ctr}%，低于正常水平",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    trigger_metric="ctr",
                    trigger_value=campaign.ctr,
                    threshold_value=1.5,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="检查广告相关性和关键词匹配",
                    auto_fix_available=False
                ))

    # ============ S086: 每日预算进度监控 ============
    def check_budget_pacing(self):
        """S086: 监控预算消耗进度"""
        for campaign in self.campaigns:
            if campaign.status.value != "ENABLED":
                continue

            # 计算预算使用率（假设是日预算）
            budget_utilization = (campaign.cost / campaign.budget) * 100 if campaign.budget > 0 else 0

            # 预算即将耗尽
            if budget_utilization > 90:
                self.alerts.append(DailyAlert(
                    alert_id=f"budget_{campaign.id}_critical",
                    alert_type=DailyAlertType.BUDGET_PACING,
                    severity=Severity.P1,
                    title="⚠️ 预算即将耗尽",
                    message=f"{campaign.name} 预算使用率达 {budget_utilization:.1f}%，预计 2 小时内耗尽",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    trigger_metric="budget_utilization",
                    trigger_value=budget_utilization,
                    threshold_value=90.0,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="增加日预算或调整出价",
                    auto_fix_available=True
                ))

            # 预算消耗过快（上午就消耗超过 70%）
            elif budget_utilization > 70 and self.execution_time.hour < 12:
                self.alerts.append(DailyAlert(
                    alert_id=f"budget_{campaign.id}_fast",
                    alert_type=DailyAlertType.BUDGET_PACING,
                    severity=Severity.P2,
                    title="🚀 预算消耗过快",
                    message=f"{campaign.name} 上午预算已消耗 {budget_utilization:.1f}%",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    trigger_metric="budget_pacing",
                    trigger_value=budget_utilization,
                    threshold_value=50.0,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="检查出价是否过高或启用加速投放",
                    auto_fix_available=False
                ))

    # ============ S087: 全渠道转化异常监控 ============
    def check_conversion_anomaly(self):
        """S087: 转化异常检测"""
        for campaign in self.campaigns:
            if campaign.status.value != "ENABLED":
                continue

            # CVR 异常降低
            if campaign.cvr < 1.0 and campaign.clicks > 100:
                self.alerts.append(DailyAlert(
                    alert_id=f"conv_{campaign.id}_cvr",
                    alert_type=DailyAlertType.CONVERSION_ANOMALY,
                    severity=Severity.P1,
                    title="📉 转化率异常降低",
                    message=f"{campaign.name} CVR 仅 {campaign.cvr}%，低于历史平均",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    trigger_metric="cvr",
                    trigger_value=campaign.cvr,
                    threshold_value=2.0,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="检查落地页可用性和加载速度",
                    auto_fix_available=False
                ))

            # CPA 异常飙升
            if campaign.actual_cpa > 50 and campaign.target_cpa and campaign.actual_cpa > campaign.target_cpa * 1.5:
                self.alerts.append(DailyAlert(
                    alert_id=f"conv_{campaign.id}_cpa",
                    alert_type=DailyAlertType.CONVERSION_ANOMALY,
                    severity=Severity.P1,
                    title="💸 CPA 异常飙升",
                    message=f"{campaign.name} 实际 CPA ${campaign.actual_cpa:.2f} 超过目标 {campaign.target_cpa * 1.5:.2f}",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    trigger_metric="cpa",
                    trigger_value=campaign.actual_cpa,
                    threshold_value=campaign.target_cpa * 1.5 if campaign.target_cpa else 50,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="暂停低效关键词或降低出价",
                    auto_fix_available=True
                ))

    # ============ S088: 全渠道投放异常监测 ============
    def check_delivery_issues(self):
        """S088: 投放异常检测"""
        for campaign in self.campaigns:
            if campaign.status.value != "ENABLED":
                continue

            # 零展示
            if campaign.impressions == 0 and campaign.status.value == "ENABLED":
                self.alerts.append(DailyAlert(
                    alert_id=f"delivery_{campaign.id}_zero_impr",
                    alert_type=DailyAlertType.DELIVERY_ISSUE,
                    severity=Severity.P0,
                    title="🚫 零展示预警",
                    message=f"{campaign.name} 已启用但过去 4 小时无展示",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    trigger_metric="impressions",
                    trigger_value=0,
                    threshold_value=1,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="检查广告审核状态、预算、出价设置",
                    auto_fix_available=False
                ))

            # 点击骤降
            if campaign.clicks == 0 and campaign.impressions > 500:
                self.alerts.append(DailyAlert(
                    alert_id=f"delivery_{campaign.id}_zero_clicks",
                    alert_type=DailyAlertType.DELIVERY_ISSUE,
                    severity=Severity.P1,
                    title="👆 点击异常",
                    message=f"{campaign.name} 有 {campaign.impressions} 展示但无点击",
                    campaign_id=campaign.id,
                    campaign_name=campaign.name,
                    trigger_metric="clicks",
                    trigger_value=0,
                    threshold_value=1,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="检查广告素材和 CTA 按钮",
                    auto_fix_available=False
                ))

    # ============ S089: 全链路追踪健康巡检 ============
    def check_tracking_health(self):
        """S089: 追踪健康检查"""
        for campaign in self.campaigns:
            # 有花费但转化追踪可能有问题
            if campaign.cost > 100 and campaign.conversions == 0:
                # 检查是否是长期趋势
                if campaign.days_since_created > 3:
                    self.alerts.append(DailyAlert(
                        alert_id=f"tracking_{campaign.id}_health",
                        alert_type=DailyAlertType.TRACKING_HEALTH,
                        severity=Severity.P0,
                        title="🏷️ 追踪健康告警",
                        message=f"{campaign.name} 有花费但连续 3 天无转化记录，可能存在追踪问题",
                        campaign_id=campaign.id,
                        campaign_name=campaign.name,
                        trigger_metric="tracking_health",
                        trigger_value=0,
                        threshold_value=1,
                        created_at=self.execution_time,
                        acknowledged_at=None,
                        resolved_at=None,
                        status="ACTIVE",
                        recommended_action="检查 Google Tag 和 Conversion Action 设置",
                        auto_fix_available=False
                    ))

    # ============ S090: 搜索词流量浪费预警 ============
    def check_search_term_waste(self):
        """S090: 搜索词浪费检测"""
        # 模拟一些搜索词浪费的情况
        waste_terms = [
            ("free marketing software", 45.20, 0),
            ("how to start a business", 38.50, 0),
            ("marketing jobs near me", 32.80, 0),
        ]

        for term, cost, conv in waste_terms:
            self.alerts.append(DailyAlert(
                alert_id=f"search_term_{term.replace(' ', '_')}",
                alert_type=DailyAlertType.SEARCH_TERM_WASTE,
                severity=Severity.P1,
                title="💸 搜索词流量浪费",
                message=f"搜索词 '{term}' 花费 ${cost:.2f} 无转化，建议添加为负向词",
                campaign_id="c_003",
                campaign_name="US_Search_Generic",
                trigger_metric="search_term_cost",
                trigger_value=cost,
                threshold_value=30.0,
                created_at=self.execution_time,
                acknowledged_at=None,
                resolved_at=None,
                status="ACTIVE",
                recommended_action=f"添加精确匹配负向词: [{term}]",
                auto_fix_available=True
            ))

    # ============ S091: 落地页可用性与性能监控 ============
    def check_landing_page_health(self):
        """S091: 落地页健康检查"""
        # 模拟落地页问题
        lp_issues = [
            ("c_001", "US_Search_Brand", 404, 0),
            ("c_002", "US_Search_NonBrand", 200, 5.2),
        ]

        for camp_id, camp_name, status, load_time in lp_issues:
            if status != 200:
                self.alerts.append(DailyAlert(
                    alert_id=f"lp_{camp_id}_error",
                    alert_type=DailyAlertType.LANDING_PAGE_ALERT,
                    severity=Severity.P0,
                    title="🔴 落地页故障",
                    message=f"{camp_name} 落地页返回 HTTP {status} 错误",
                    campaign_id=camp_id,
                    campaign_name=camp_name,
                    trigger_metric="http_status",
                    trigger_value=status,
                    threshold_value=200,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="立即修复落地页或暂停广告投放",
                    auto_fix_available=False
                ))

            if load_time > 3.0:
                self.alerts.append(DailyAlert(
                    alert_id=f"lp_{camp_id}_slow",
                    alert_type=DailyAlertType.LANDING_PAGE_ALERT,
                    severity=Severity.P2,
                    title="🐌 落地页加载缓慢",
                    message=f"{camp_name} 落地页加载时间 {load_time} 秒，影响用户体验",
                    campaign_id=camp_id,
                    campaign_name=camp_name,
                    trigger_metric="load_time",
                    trigger_value=load_time,
                    threshold_value=3.0,
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="优化图片大小、启用 CDN、压缩资源",
                    auto_fix_available=False
                ))

    # ============ S092-S094: 政策合规监控 ============
    def check_policy_violations(self):
        """S092-S094: 政策合规检查"""
        # 模拟政策违规
        policy_issues = [
            ("c_003", "US_Search_Generic", "DISAPPROVED", "误导性声明"),
        ]

        for camp_id, camp_name, status, reason in policy_issues:
            if status == "DISAPPROVED":
                self.alerts.append(DailyAlert(
                    alert_id=f"policy_{camp_id}_disapproved",
                    alert_type=DailyAlertType.POLICY_VIOLATION,
                    severity=Severity.P0,
                    title="🚨 广告被拒登",
                    message=f"{camp_name} 因 '{reason}' 被拒登，请立即修改",
                    campaign_id=camp_id,
                    campaign_name=camp_name,
                    trigger_metric="approval_status",
                    trigger_value=0,  # 0 = disapproved
                    threshold_value=1,  # 1 = approved
                    created_at=self.execution_time,
                    acknowledged_at=None,
                    resolved_at=None,
                    status="ACTIVE",
                    recommended_action="根据拒登原因修改广告内容并申诉",
                    auto_fix_available=False
                ))
