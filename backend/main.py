"""
Google Ads 自动化管理系统 - FastAPI 后端主入口
SOP Stage 1 演示版本
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
import uvicorn

from models.schemas import (
    Campaign, DiagnosisResult, Alert,
    DiagnosisRequest, DiagnosisResponse,
    Stage2DataResponse, Stage2DiagnosisResponse,
    Stage3DiagnosisResponse, Stage4DiagnosisResponse,
    DailyAlertResponse
)
from data_sources.mock_data import MockDataSource
from rule_engine.stage1_engine import Stage1RuleEngine
from rule_engine.stage2_engine import Stage2RuleEngine
from rule_engine.stage3_engine import Stage3Engine
from rule_engine.stage4_engine import Stage4Engine
from rule_engine.daily_alert_engine import DailyAlertEngine

app = FastAPI(
    title="Google Ads Automation System",
    description="SOP Stage 1-4 + Daily Alert - Google Ads 全链路自动化诊断系统",
    version="2.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据源和规则引擎
mock_data = MockDataSource()
rule_engine = Stage1RuleEngine()
stage2_engine = Stage2RuleEngine()


@app.get("/")
def root():
    return {
        "message": "Google Ads Automation API",
        "version": "1.0.0",
        "stage": "Stage 1 - Foundation Check"
    }


@app.get("/api/campaigns", response_model=List[Campaign])
def get_campaigns():
    """获取所有 Campaign 列表"""
    return mock_data.get_campaigns()


@app.get("/api/campaigns/{campaign_id}")
def get_campaign_detail(campaign_id: str):
    """获取单个 Campaign 详情"""
    campaigns = mock_data.get_campaigns()
    for c in campaigns:
        if c.id == campaign_id:
            return c
    raise HTTPException(status_code=404, detail="Campaign not found")


@app.post("/api/diagnose/stage1", response_model=DiagnosisResponse)
def run_stage1_diagnosis(request: DiagnosisRequest):
    """
    执行 SOP Stage 1 全面诊断
    包含: S001-S011 所有检查项
    """
    # 获取数据
    campaigns = mock_data.get_campaigns()
    conversion_tracking = mock_data.get_conversion_tracking()

    results = []
    alerts = []

    # 对每个选中的 campaign 执行诊断
    for campaign_id in request.campaign_ids:
        campaign = next((c for c in campaigns if c.id == campaign_id), None)
        if not campaign:
            continue

        # 运行 Stage 1 规则
        diagnosis = rule_engine.run_stage1_check(campaign, conversion_tracking)
        results.extend(diagnosis)

    # 生成告警
    alerts = rule_engine.generate_alerts(results)

    return DiagnosisResponse(
        execution_time=datetime.now(),
        data_range=f"Last {request.days} days",
        scanned_campaigns=len(request.campaign_ids),
        results=results,
        alerts=alerts,
        summary={
            "total_issues": len([r for r in results if r.severity in ["P0", "P1"]]),
            "p0_count": len([r for r in results if r.severity == "P0"]),
            "p1_count": len([r for r in results if r.severity == "P1"]),
            "p2_count": len([r for r in results if r.severity == "P2"]),
            "optimized_count": len([r for r in results if r.severity == "OK"])
        }
    )


@app.get("/api/diagnose/conversion-tracking")
def diagnose_conversion_tracking():
    """S001-S003: 转化追踪检查"""
    tracking = mock_data.get_conversion_tracking()
    return rule_engine.check_conversion_tracking(tracking)


@app.get("/api/diagnose/bidding/{campaign_id}")
def diagnose_bidding(campaign_id: str):
    """S005: 出价策略检查"""
    campaigns = mock_data.get_campaigns()
    campaign = next((c for c in campaigns if c.id == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return rule_engine.check_bidding_strategy(campaign)


@app.get("/api/diagnose/budget/{campaign_id}")
def diagnose_budget(campaign_id: str):
    """S006: 预算限制检查"""
    campaigns = mock_data.get_campaigns()
    campaign = next((c for c in campaigns if c.id == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return rule_engine.check_budget(campaign)


@app.get("/api/alerts")
def get_active_alerts():
    """获取当前活动告警"""
    return mock_data.get_mock_alerts()


@app.get("/api/metrics/dashboard")
def get_dashboard_metrics():
    """获取仪表盘 KPI 数据"""
    campaigns = mock_data.get_campaigns()

    total_spend = sum(c.cost for c in campaigns)
    total_conversions = sum(c.conversions for c in campaigns)
    total_value = sum(c.conversion_value for c in campaigns)

    avg_cpa = total_spend / total_conversions if total_conversions > 0 else 0
    avg_roas = total_value / total_spend if total_spend > 0 else 0

    return {
        "total_spend": round(total_spend, 2),
        "total_conversions": total_conversions,
        "total_conversion_value": round(total_value, 2),
        "avg_cpa": round(avg_cpa, 2),
        "avg_roas": round(avg_roas, 2),
        "active_campaigns": len([c for c in campaigns if c.status == "ENABLED"]),
        "total_campaigns": len(campaigns),
        "alert_count": 12  # 模拟告警数
    }


# ============ Stage 2 API ============

@app.post("/api/diagnose/stage2")
def run_stage2_diagnosis(request: DiagnosisRequest):
    """
    执行 SOP Stage 2 组件级优化诊断
    包含: S012-S053 所有检查项
    """
    campaigns = mock_data.get_campaigns()
    results = []

    for campaign_id in request.campaign_ids:
        campaign = next((c for c in campaigns if c.id == campaign_id), None)
        if not campaign:
            continue

        # 运行 Stage 2 规则
        diagnosis = stage2_engine.run_stage2_check(campaign, mock_data)
        results.extend(diagnosis)

    # 按模块分组统计
    module_stats = {}
    for r in results:
        module = r.strategy_id.split('-')[0] if '-' in r.strategy_id else r.strategy_id
        if module not in module_stats:
            module_stats[module] = {"total": 0, "issues": 0}
        module_stats[module]["total"] += 1
        if r.severity != "OK":
            module_stats[module]["issues"] += 1

    return {
        "execution_time": datetime.now(),
        "data_range": f"Last {request.days} days",
        "scanned_campaigns": len(request.campaign_ids),
        "results": results,
        "module_stats": module_stats,
        "summary": {
            "total_issues": len([r for r in results if r.severity in ["P0", "P1"]]),
            "p0_count": len([r for r in results if r.severity == "P0"]),
            "p1_count": len([r for r in results if r.severity == "P1"]),
            "p2_count": len([r for r in results if r.severity == "P2"]),
            "optimized_count": len([r for r in results if r.severity == "OK"])
        }
    }


@app.get("/api/stage2-data/{campaign_id}")
def get_stage2_data(campaign_id: str):
    """
    获取 Stage 2 所需的所有组件数据
    """
    campaigns = mock_data.get_campaigns()
    campaign = next((c for c in campaigns if c.id == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign.name,
        "search_terms": mock_data.get_search_terms(campaign_id),
        "keywords": mock_data.get_keywords(campaign_id),
        "ads": mock_data.get_ads(campaign_id),
        "assets": mock_data.get_assets(campaign_id),
        "locations": mock_data.get_locations(campaign_id),
        "devices": mock_data.get_devices(campaign_id),
        "hourly": mock_data.get_hourly_performance(campaign_id),
        "auction_insights": mock_data.get_auction_insights(campaign_id),
    }


@app.get("/api/search-terms")
def get_search_terms(campaign_id: str = None):
    """S012-S014: 获取搜索词数据"""
    return mock_data.get_search_terms(campaign_id)


@app.get("/api/keywords")
def get_keywords(campaign_id: str = None):
    """S015-S017: 获取关键词数据"""
    return mock_data.get_keywords(campaign_id)


@app.get("/api/ads")
def get_ads(campaign_id: str = None):
    """S018-S020: 获取广告文案数据"""
    return mock_data.get_ads(campaign_id)


@app.get("/api/assets")
def get_assets(campaign_id: str = None):
    """S021-S023: 获取 Assets 数据"""
    return mock_data.get_assets(campaign_id)


@app.get("/api/locations")
def get_locations(campaign_id: str = None):
    """S026-S028: 获取地域表现数据"""
    return mock_data.get_locations(campaign_id)


@app.get("/api/devices")
def get_devices(campaign_id: str = None):
    """S033-S034: 获取设备表现数据"""
    return mock_data.get_devices(campaign_id)


@app.get("/api/hourly")
def get_hourly(campaign_id: str = None):
    """S035-S036: 获取分时段数据"""
    return mock_data.get_hourly_performance(campaign_id)


@app.get("/api/auction-insights")
def get_auction_insights(campaign_id: str = None):
    """S037: 获取竞品拍卖洞察"""
    return mock_data.get_auction_insights(campaign_id)


# ============ Stage 3 API ============

@app.post("/api/diagnose/stage3", response_model=Stage3DiagnosisResponse)
def run_stage3_diagnosis(request: DiagnosisRequest):
    """
    执行 SOP Stage 3 Workstream 执行诊断
    包含: W1-W8 所有工作流 (S054-S074)
    """
    campaigns = mock_data.get_campaigns()

    # 获取选中的 campaigns
    selected_campaigns = [c for c in campaigns if c.id in request.campaign_ids]

    # 获取 Stage 2 数据作为输入
    stage2_data = {}
    for campaign_id in request.campaign_ids:
        stage2_data[campaign_id] = Stage2DataResponse(
            search_terms=mock_data.get_search_terms(campaign_id),
            keywords=mock_data.get_keywords(campaign_id),
            ads=mock_data.get_ads(campaign_id),
            assets=mock_data.get_assets(campaign_id),
            locations=mock_data.get_locations(campaign_id),
            audiences=mock_data.get_audiences(campaign_id),
            devices=mock_data.get_devices(campaign_id),
            hourly=mock_data.get_hourly_performance(campaign_id),
            auction_insights=mock_data.get_auction_insights(campaign_id),
        )

    # 运行 Stage 3 引擎
    stage3_engine = Stage3Engine(selected_campaigns, stage2_data)
    result = stage3_engine.run_all_workstreams()

    return result


@app.get("/api/workstreams/status")
def get_workstream_status():
    """获取所有 Workstream 的状态概览"""
    return {
        "workstreams": [
            {"id": "W1", "name": "先修追踪", "priority": "P1", "status": "READY"},
            {"id": "W2", "name": "控制浪费", "priority": "P1", "status": "READY"},
            {"id": "W3", "name": "预算重分配", "priority": "P1", "status": "READY"},
            {"id": "W4", "name": "优化广告", "priority": "P2", "status": "READY"},
            {"id": "W5", "name": "优化落地页", "priority": "P2", "status": "READY"},
            {"id": "W6", "name": "精细化定向", "priority": "P2", "status": "READY"},
            {"id": "W7", "name": "Feed 优化", "priority": "P1", "status": "READY"},
            {"id": "W8", "name": "预算倾斜", "priority": "P1", "status": "READY"},
        ]
    }


# ============ Stage 4 API ============

@app.post("/api/diagnose/stage4", response_model=Stage4DiagnosisResponse)
def run_stage4_diagnosis(request: DiagnosisRequest):
    """
    执行 SOP Stage 4 高级测试与战略诊断
    包含: S075-S084 A/B测试、线索质量、战略复盘
    """
    campaigns = mock_data.get_campaigns()

    # 获取选中的 campaigns
    selected_campaigns = [c for c in campaigns if c.id in request.campaign_ids]

    # 运行 Stage 4 引擎
    stage4_engine = Stage4Engine(selected_campaigns)
    result = stage4_engine.run_all_checks()

    return result


@app.get("/api/strategic-review")
def get_strategic_review():
    """S080-S082: 获取战略复盘数据"""
    campaigns = mock_data.get_campaigns()
    engine = Stage4Engine(campaigns)
    review = engine.run_strategic_review()
    return review


@app.get("/api/ab-tests")
def get_ab_tests(campaign_id: str = None):
    """S075-S076: 获取 A/B 测试列表"""
    campaigns = mock_data.get_campaigns()
    if campaign_id:
        campaigns = [c for c in campaigns if c.id == campaign_id]
    engine = Stage4Engine(campaigns)
    return {"tests": engine.run_ab_tests()}


@app.get("/api/lead-quality")
def get_lead_quality():
    """S077-S079: 获取线索质量分析"""
    campaigns = mock_data.get_campaigns()
    engine = Stage4Engine(campaigns)
    return {"lead_quality": engine.analyze_lead_quality()}


# ============ Daily Alert API ============

@app.post("/api/diagnose/daily-alerts", response_model=DailyAlertResponse)
def run_daily_alerts():
    """
    执行 Daily Alert 系统诊断 (S085-S094)
    实时监控: 表现异常、预算进度、转化异常、投放异常、追踪健康、搜索词浪费、落地页、政策合规
    """
    campaigns = mock_data.get_campaigns()

    # 运行 Daily Alert 引擎
    alert_engine = DailyAlertEngine(campaigns)
    result = alert_engine.run_all_checks()

    return result


@app.get("/api/alerts/active")
def get_active_alerts():
    """获取当前活动告警"""
    campaigns = mock_data.get_campaigns()
    alert_engine = DailyAlertEngine(campaigns)
    result = alert_engine.run_all_checks()
    return {
        "alerts": [a for a in result.alerts if a.status == "ACTIVE"],
        "summary": result.summary
    }


@app.get("/api/alerts/summary")
def get_alerts_summary():
    """获取告警汇总统计"""
    campaigns = mock_data.get_campaigns()
    alert_engine = DailyAlertEngine(campaigns)
    result = alert_engine.run_all_checks()
    return result.summary


@app.get("/api/alerts/history")
def get_alerts_history(days: int = 7):
    """获取历史告警"""
    # 模拟历史告警数据
    return {
        "history": [
            {"date": "2026-03-11", "total": 15, "p0": 2, "p1": 5, "p2": 8},
            {"date": "2026-03-10", "total": 12, "p0": 1, "p1": 4, "p2": 7},
            {"date": "2026-03-09", "total": 18, "p0": 3, "p1": 6, "p2": 9},
        ]
    }


@app.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str):
    """确认告警"""
    return {"status": "success", "message": f"Alert {alert_id} acknowledged"}


@app.post("/api/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: str):
    """解决告警"""
    return {"status": "success", "message": f"Alert {alert_id} resolved"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
