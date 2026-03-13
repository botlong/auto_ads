# Google Ads SOP 自动诊断系统

基于 Google Ads SOP 9-Mar v1.xlsx 实现的智能诊断与优化建议系统，覆盖 94 个完整 SOP 检查项。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        前端层 (React)                        │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│ Dashboard   │ Stage 1-4   │ Daily Alert │ Campaign List     │
└─────────────┴─────────────┴─────────────┴───────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     API 层 (FastAPI)                        │
├─────────────────────────────────────────────────────────────┤
│  /api/diagnose/stage1  │  账户架构诊断 (S001-S011)           │
│  /api/diagnose/stage2  │  组件优化诊断 (S012-S053)           │
│  /api/diagnose/stage3  │  Workstream 执行 (S054-S074)       │
│  /api/diagnose/stage4  │  战略复盘 (S075-S084)              │
│  /api/diagnose/daily   │  日常告警 (S085-S094)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     规则引擎层                              │
├─────────────────────────────────────────────────────────────┤
│  Stage1Engine  │ Stage2Engine  │ Stage3Engine  │ Stage4    │
│  DailyAlert    │ MockDataSource │ Schemas      │           │
└─────────────────────────────────────────────────────────────┘
```

## 功能特性

### 4 阶段诊断流程

| 阶段 | SOP 范围 | 功能描述 |
|------|----------|----------|
| **Stage 1** | S001-S011 | 账户架构审计 - 转化追踪、账户结构、业务目标一致性检查 |
| **Stage 2** | S012-S053 | 组件级优化 - 搜索词、关键词、广告文案、受众、地域、设备优化 |
| **Stage 3** | S054-S074 | Workstream 执行 - 转化追踪修复、流量控制、受众优化、再营销激活 |
| **Stage 4** | S075-S084 | 战略复盘 - A/B 测试、线索质量闭环、Feed 优化、ROAS 分层测试 |
| **Daily Alert** | S085-S094 | 实时监控 - 异常预警、预算进度、转化异常、落地页健康、政策合规 |

### 94 个 SOP 检查项全覆盖

- ✅ S001-S003: 转化追踪架构配置
- ✅ S004-S005: 转化价值与追踪健康
- ✅ S006-S008: Enhanced Conversions 优化
- ✅ S009-S011: Campaign 目标一致性、竞价策略、预算优化
- ✅ S012-S014: 搜索词负向过滤、意图拓新、流量健康
- ✅ S015-S017: 关键词效果清理、相关性诊断、出价水位
- ✅ S018-S020: 广告文案优化、RSA 检查
- ✅ S021-S023: Assets 管理、SiteLinks、图片/视频
- ✅ S024-S025: Landing Page 体验、Quality Score 诊断
- ✅ S026-S028: 地域表现分析
- ✅ S029-S032: 受众优化（新增 S030-S031）
- ✅ S033-S037: 设备、时段、竞品拍卖分析
- ✅ S038: 政策合规检查
- ✅ S039-S053: 电商 Feed 与 PMAX 专项（新增 S078）
- ✅ S054-S074: Workstream 1-4 完整执行
- ✅ S075-S084: 测试与战略复盘
- ✅ S085-S094: Daily Alert 实时监控（新增 S093）

## 技术栈

### 后端
- **Python 3.12**
- **FastAPI** - 高性能 API 框架
- **Pydantic** - 数据模型与验证
- **Uvicorn** - ASGI 服务器

### 前端
- **React 18**
- **TypeScript**
- **Vite** - 构建工具
- **Axios** - HTTP 客户端

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/google-ads-sop.git
cd google-ads-sop
```

### 2. 启动后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

后端服务将在 `http://localhost:8000` 启动

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

### 4. 访问系统

打开浏览器访问 `http://localhost:5173`

## API 端点

### 诊断接口

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/diagnose/stage1` | 执行 Stage 1 账户架构诊断 |
| POST | `/api/diagnose/stage2` | 执行 Stage 2 组件优化诊断 |
| POST | `/api/diagnose/stage3` | 执行 Stage 3 Workstream 诊断 |
| POST | `/api/diagnose/stage4` | 执行 Stage 4 战略复盘诊断 |
| POST | `/api/diagnose/daily` | 执行 Daily Alert 日常告警检查 |
| POST | `/api/diagnose/all` | 执行全部 4 阶段 + Daily Alert 诊断 |

### 数据接口

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/campaigns` | 获取所有 Campaign 列表 |
| GET | `/api/campaigns/{id}` | 获取单个 Campaign 详情 |
| GET | `/health` | 健康检查 |

## 诊断结果格式

```json
{
  "execution_time": "2026-03-12T20:33:01",
  "data_range": "Last 7 days",
  "scanned_campaigns": 5,
  "results": [
    {
      "strategy_id": "S012",
      "strategy_name": "搜索词负向过滤",
      "severity": "P1",
      "issue_type": "高花费无转化搜索词",
      "affected_object": "Campaign: US_Search > 'free software'",
      "current_value": "花费 $45.20, 0 转化",
      "benchmark_value": "应 < $45.00 或产生转化",
      "suggested_action": "添加精确负向词: 'free software'",
      "expected_impact": "预计每月节省 $180.80",
      "details": {...}
    }
  ]
}
```

## 严重程度说明

| 等级 | 描述 | 响应时间 |
|------|------|----------|
| **P0** | 紧急 - 广告被拒登、追踪失效 | 立即处理 |
| **P1** | 高优先级 - CPA 超标、高花费无转化 | 24小时内 |
| **P2** | 中优先级 - 优化建议、潜在提升 | 72小时内 |
| **OK** | 正常 - 符合基准 | 持续监控 |

## 开发路线图

- [x] 核心 94 个 SOP 检查项实现
- [x] FastAPI 后端 + React 前端
- [x] Mock 数据源支持
- [ ] Google Ads API 集成
- [ ] 数据库持久化
- [ ] 用户认证与权限管理
- [ ] 自动化执行调度
- [ ] 报告导出 (PDF/Excel)
- [ ] 邮件/Slack 通知

## 项目结构

```
google-ads-sop/
├── backend/
│   ├── main.py                    # FastAPI 主入口
│   ├── requirements.txt           # Python 依赖
│   ├── models/
│   │   └── schemas.py             # Pydantic 数据模型
│   ├── data_sources/
│   │   └── mock_data.py           # Mock 数据生成
│   └── rule_engine/
│       ├── stage1_engine.py       # Stage 1 规则引擎
│       ├── stage2_engine.py       # Stage 2 规则引擎
│       ├── stage3_engine.py       # Stage 3 规则引擎
│       ├── stage4_engine.py       # Stage 4 规则引擎
│       └── daily_alert_engine.py  # Daily Alert 引擎
├── frontend/
│   ├── src/
│   │   ├── App.tsx                # 主应用组件
│   │   ├── api/
│   │   │   └── client.ts          # API 客户端
│   │   └── components/
│   │       ├── Dashboard/         # 仪表板组件
│   │       ├── Stage2/            # Stage 2 诊断组件
│   │       ├── Stage3/            # Stage 3 诊断组件
│   │       ├── Stage4/            # Stage 4 诊断组件
│   │       └── DailyAlert/        # Daily Alert 组件
│   ├── package.json
│   └── vite.config.ts
├── Google AD SOP 9-Mar v1.xlsx    # 原始 SOP 文档
└── README.md                      # 本文件
```

## 许可证

MIT License

## 致谢

基于 Google Ads SOP 9-Mar v1.xlsx 规范实现

---

**系统版本**: v1.0.1
**最后更新**: 2026-03-13
**SOP 覆盖**: 94/94 (100%)
