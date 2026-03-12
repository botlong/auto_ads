# Google Ads 自动化管理系统 — 产品需求文档 (PRD)

> **版本**: v1.0  
> **日期**: 2026-03-12  
> **来源**: Google AD SOP 9-Mar v1.xlsx  
> **系统定位**: 基于规则引擎的 Google Ads 全链路自动化诊断、监控与优化平台

---

## 1. 产品概述

### 1.1 背景与目标

将运营团队积累的 **91 条专家策略（S001-S094）** 转化为自动化系统，覆盖 Google Ads 投放全生命周期。系统通过 Google Ads API / Merchant Center API / GA4 API 自动采集数据，应用 IF-THEN 专家规则进行诊断与优化，输出操作建议或半自动执行调整。

### 1.2 核心价值

| 价值维度 | 预期效果 |
|---------|---------|
| 降低无效浪费 | 减少 15%-30% 的无效广告支出 |
| 提升人效 | 释放运营 80% 的机械巡检时间 |
| 响应速度 | 异常发现时间从"天级"缩短至"小时级" |
| 知识沉淀 | 专家经验规则化，可复制可迭代 |

---

## 2. 系统架构

### 2.1 分层架构

```
┌─────────────────────────────────────┐
│           展示层 (Frontend)           │
│  Dashboard / 报告 / 告警通知 / 审批   │
├─────────────────────────────────────┤
│          策略引擎 (Rule Engine)        │
│  IF-THEN 规则库 / 阈值管理 / 审计日志  │
├─────────────────────────────────────┤
│          数据层 (Data Layer)           │
│  Google Ads API / GMC API / GA4 API   │
│  PageSpeed API / CRM / ERP            │
├─────────────────────────────────────┤
│          存储层 (Storage)              │
│  SQLite/PostgreSQL / 审计日志 / 配置   │
└─────────────────────────────────────┘
```

### 2.2 自动化成熟度模型

| 级别 | 名称 | 描述 | 策略数 |
|------|------|------|--------|
| L1 | Monitoring | 被动监控，数据采集与展示 | ~10 |
| L2 | Diagnostic | 异常诊断，自动分析根因 | ~15 |
| L3 | Recommendation | 生成优化建议，人工确认 | ~25 |
| L4 | Semi-Automation | 系统执行，人工审批 | ~35 |
| L5 | Full-Automation | 全自动执行（远期目标） | — |

---

## 3. 功能模块详细定义

### 3.1 SOP Stage 1 — 基础设置与校验（6 个模块）

> **核心目标**: 确保账户底层配置正确，为后续优化建立可靠的数据基础。
> **执行频率**: 每月 / 重大调整后

#### 模块 1: 转化追踪检查 (S001-S003)
- **层级**: Account
- **检查内容**: Primary/Secondary 转化设置、转化价值完整性、Enhanced Conversions 状态、Tag 活性
- **KPI**: Conversions, CPA, ROAS, CVR
- **核心规则**:
  - IF 核心业务目标(Purchase)设为 Secondary → 标记高风险
  - IF 同一页面存在多个 Primary 转化 → 标记重复计费风险
  - IF Tag Status = Inactive → 紧急报警
  - IF Conversion Value = 0 (Purchase 类) → 报警：价值传递失效
- **负责人**: Ads + Analytics

#### 模块 2: Campaign 目标检查 (S004)
- **层级**: Campaign
- **检查内容**: Campaign 目标与业务类型(Lead Gen / Ecommerce)的一致性
- **核心规则**:
  - IF Business Type = Lead Gen AND Bidding ∉ {Max Conv, tCPA} → 目标偏移
  - IF Business Type = Ecommerce AND Bidding ∉ {Max Value, tROAS} → 目标偏移
- **负责人**: Ads

#### 模块 3: 出价策略检查 (S005)
- **层级**: Campaign
- **检查内容**: Bidding 效能、tCPA/tROAS 目标合理性、Learning Status
- **核心规则**:
  - IF Actual CPA < Target CPA AND IS < 50% → 提升 tCPA 10%
  - IF Status = LEARNING AND 波动 > 30% → 跳过自动调整，仅告警
  - IF 存在 Margin 数据 → 重新计算 New tCPA = Lead Value × Margin
- **负责人**: Ads

#### 模块 4: 预算限制检查 (S006)
- **层级**: Campaign
- **检查内容**: Lost IS (Budget) vs Lost IS (Rank)、Budget Pacing
- **核心规则**:
  - IF Lost IS (Budget) > 15% AND ROAS > Target×1.1 → 增加预算 20%
  - IF Lost IS (Rank) > 20% AND Lost IS (Budget) < 5% → 优化 Ad Rank
  - IF ROAS < Target×0.8 AND Spend > 80%预算 → 降低预算 20%
  - IF Campaign Label = "Testing" → 保留观察期
- **负责人**: Ads

#### 模块 5: 账户结构检查 (S007-S010)
- **层级**: Campaign / AdGroup / Account
- **检查内容**: Brand/Non-brand 隔离、搜索/展示网络混合、AdGroup 数量合理性
- **核心规则**:
  - IF Campaign 含 "Brand" 但关键词存在非品牌词 → 意图混杂
  - IF Search Campaign 开启了 Display Network → 网络混杂
  - IF 单个 Campaign 下 AdGroup > 20 → 结构过宽
  - IF 同一 Campaign 内 AdGroup CPA 标准差 > 50% → 建议拆分
- **频率**: 每月/每季度 | **负责人**: Ads

#### 模块 6: ROAS Segmentation Review (S011)
- **层级**: Campaign / Product Group
- **适用**: Shopping / PMax / Ecommerce
- **核心规则**:
  - IF SKU ROAS > Campaign Target×120% AND Spend Share > 10% → High Efficiency Core
  - IF SKU ROAS < Campaign Target×70% AND Spend Share > 30% → Budget Drainer
  - IF SKU Margin < Threshold AND ROAS < Break Even → 降权或排除
  - IF Campaign Limited by Budget AND 存在高效 SKU → 建议独立拆分
- **频率**: Weekly/Monthly | **负责人**: Ads + Ecommerce

---

### 3.2 SOP Stage 2 — 组件级优化（20 个模块）

> **核心目标**: 对广告投放各组件进行精细化诊断与优化。

#### 搜索词优化 (S012-S014)
- **频率**: 每 72 小时
- **核心规则**:
  - IF Search Term Cost > (tCPA × 1.2) AND Conversions = 0 → Add Negative Exact
  - IF Clicks > 20 AND CTR < (AdGroup Avg × 0.5) → 标记无关意图
  - IF Conversions ≥ 1 AND Match = Broad → 提炼为 Phrase/Exact

#### 关键词检查 (S015-S017)
- **频率**: 每周
- **核心规则**:
  - IF Conversions = 0 AND Cost > (tCPA × 3) → PAUSE
  - IF CPA > (tCPA × 1.5) AND Conversions ≥ 3 → 降价 20%
  - IF QS < 4 AND 相关性低 → 收缩匹配类型

#### 广告文案检查 (S018-S020)
- **频率**: 每周
- **核心规则**:
  - IF Ad Status = DISAPPROVED → 立刻申诉或重写
  - IF Headline Count < 10 → 添加差异化卖点
  - IF IS > 50% AND CTR < Baseline → 加入强 CTA
  - IF CTR > Baseline AND CVR < Target → 加入信任背书

#### Assets 检查 (S021-S023)
- **频率**: 每周/每月
- **核心规则**:
  - IF Sitelink Count < 4 → 覆盖风险，自动关联
  - IF Asset Performance = LOW → 暂停并替换
  - IF Lead Form 缺失 → P1 级告警
  - IF Asset 最后更新 > 180 天 → 内容陈旧

#### Landing Page 检查 (S024)
- **频率**: 每月
- **核心规则**:
  - IF Landing Page Status ≠ 200 → 暂停广告组 + P0 告警
  - IF Mobile Load Time > 3s AND Bounce Rate > 70% → 加速优化
  - IF Search Term Match Rate < 30% → 内容不匹配
  - IF Engagement 高 BUT CVR 极低 → 表单/CTA 摩擦

#### Quality Score 检查 (S025)
- **频率**: 每月
- **核心规则**:
  - IF Ad Relevance = BELOW_AVERAGE → 提高关键词出现频率
  - IF LP Experience = BELOW_AVERAGE → 检查速度与内容匹配
  - IF Expected CTR = BELOW_AVERAGE → 优化 CTA
  - IF QS < 4 AND CPC > 历史均值×1.5 → 高紧迫性

#### 地域表现检查 (S026-S028)
- **频率**: 每周
- **核心规则**:
  - IF Location Spend > (2×tCPA) AND Conversions = 0 → 排除地区
  - IF Location ROAS > (1.2×tROAS) AND IS < 70% → 建议拆分 Campaign
  - IF Location CVR > (1.2×Avg CVR) → Bid Modifier +15%

#### Audience 检查 (S029-S032)
- **频率**: 每周/每月
- **核心规则**:
  - IF Remarketing Audience = 0 → 告警：缺失再营销
  - IF Customer List 更新 > 30 天 → 过期告警
  - IF Audience CPA > (1.5×tCPA) AND Conversions = 0 → 排除
  - IF PMax Audience Signal < 3 → 建议增加信号

#### Device 检查 (S033-S034)
- **频率**: 每周
- **核心规则**:
  - IF Mobile CVR < (Desktop CVR × 0.6) → Mobile UX Issue
  - IF Device CPA > (tCPA × 1.3) → Bid Modifier 降低 10-15%
  - IF Device Spend > (2×tCPA) AND Conversions = 0 → 建议 -90%

#### 时间段检查 (S035-S036)
- **频率**: 每周
- **核心规则**:
  - IF 时段 Spend > (1.5×tCPA) AND Conversions = 0 → 停止投放
  - IF CPA < (0.7×tCPA) AND CVR > 1.2×Avg → Bid +15%
  - IF 非营业时间 AND CVR < 0.5×Avg → Bid -50%

#### 竞品拍卖分析 (S037)
- **频率**: 每月
- **核心规则**:
  - IF Overlap Rate > 50% AND Outranking Share < 40% → 提高出价
  - IF IS < 50% AND Top of Page < 30% → 提高素材相关性
  - IF IS 持续下降 AND 竞品 IS 上升 → 核心竞争力受损预警

#### 政策/审核异常检查 (S038)
- **频率**: 每 72 小时
- **核心规则**:
  - IF Approval Status = DISAPPROVED → P1 告警 + 提取违规原因
  - IF Asset Approval = DISAPPROVED → 标记受损素材
  - IF Final URL HTTP ≠ 200 → Broken URL 诊断
  - IF Status = ENABLED AND Impressions = 0 (72h) → 政策导致受限

#### 电商专项模块 (Shopping / PMax)

| 模块 | 策略 ID | 核心功能 | 频率 |
|------|---------|---------|------|
| Product Listings Review | S039-S041 | Feed 完整性、CTR 优化、价格竞争力 | Weekly |
| Merchant Center Health | S042-S044 | 商品获批率、高价值商品拒登诊断 | Daily/Weekly |
| Product Performance | S045 | 四象限分类(Hero/Growth/Low/Zombie) | Weekly |
| Product Title Optimization | S046 | 标题语义增强与重写 | Monthly |
| Product Image Review | S047-S048 | 主图表现诊断、GMC 合规巡检 | Monthly |
| Price & Promotion | S049 | 价格竞争力监控、促销资产关联 | Weekly |
| Availability Review | S050-S052 | 库存同步、缺货自动剔除 | Daily |
| Product Segmentation | S053 | Custom Label 动态映射 | Monthly |

---

### 3.3 SOP Stage 3 — Workstream 执行（8 个工作流）

> **核心目标**: 基于 Stage 1-2 的诊断结果，执行系统化的优化动作。

| Workstream | 策略 ID | 核心目标 | 优先级 | 频率 |
|-----------|---------|---------|--------|------|
| W1: 先修追踪 | S054-S055 | 转化数据质量审计，修正 Primary Goal | P1 | 优先 |
| W2: 控制浪费 | S056-S059 | 排除低质搜索词/地域/受众/流量 | P1 | 每周 |
| W3: 预算重分配 | S060-S062 | 跨系列预算动态平衡 | P1 | 每周 |
| W4: 优化广告 | S063-S065 | Ad Strength 补全、素材刷新、Offer 注入 | P2 | 每周/月 |
| W5: 优化落地页 | S066 | CVR 诊断：速度/相关性/表单/信任 | P2 | 每月 |
| W6: 精细化定向 | S067-S070 | 设备/地域/人群/时段多维汰换 | P2 | 每周 |
| Feed Optimization | S071-S072 | 高价值商品 Feed 质量优化 | P1 | Weekly |
| Product Budget | S073-S074 | Hero 商品预算倾斜、ROAS 分层拆分 | P1 | Weekly |

---

### 3.4 SOP Stage 4 — 高级测试与战略（4 个模块）

| 模块 | 策略 ID | 核心目标 | 频率 |
|------|---------|---------|------|
| 测试路线图 | S075-S076 | 变量受控 A/B 测试引擎 | Monthly |
| 线索质量检查 | S077-S079 | 线下 SQL Rate / Close Rate 闭环 | Monthly |
| 90 天战略复盘 | S080-S082 | 增长趋势、Channel Mix、PMax 侵蚀检测 | 每季度 |
| Product Listing Test | S083 | Feed 元素 A/B 测试 | Monthly |
| ROAS Tier Testing | S084 | ROAS 分层差异化策略测试 | Monthly |

---

### 3.5 Daily Alert 系统（7 个告警模块）

> **核心目标**: 实时监控，24 小时内发现异常。

| Alert 模块 | 策略 ID | 检查频率 | 优先级 |
|-----------|---------|---------|--------|
| Daily Tracking Alert | S085 | 每 4-6 小时 | P1 |
| Daily Budget Pacing | S086 | 每日 3 次 | P1 |
| Daily Conversion Alert | S087 | Daily | P1 |
| Daily Delivery Alert | S088 | Daily | P1 |
| Daily Tracking Health | S089 | Daily | P1 |
| Search Term Waste | S090 | Daily | P1 |
| Landing Page Alert | S091 | Daily | P1 |
| Policy/Approval Alert | S092-S094 | 每 4-8 小时 | P1 |

---

## 4. 指标字典（核心 KPI）

| 指标 | 全称 | 公式 | 用途 |
|------|------|------|------|
| CPA | Cost Per Acquisition | Cost / Conversions | 获客成本 |
| ROAS | Return on Ad Spend | Conv. Value / Cost | 广告回报 |
| CVR | Conversion Rate | Conversions / Clicks | 转化率 |
| CTR | Click-Through Rate | Clicks / Impressions | 点击率 |
| QS | Quality Score | Google 系统评分 (1-10) | 关键词质量 |
| CPC | Cost Per Click | Cost / Clicks | 点击成本 |
| IS | Impression Share | Impressions / Eligible Impressions | 展示份额 |
| Lost IS (Budget) | — | 因预算丢失的 IS | 预算限制 |
| Lost IS (Rank) | — | 因排名丢失的 IS | 竞争力 |

---

## 5. 数据源与 API

| 数据源 | API | 用途 |
|-------|-----|------|
| Google Ads | Google Ads API v17+ | 广告数据、出价、预算管理 |
| Merchant Center | Content API for Shopping | 商品 Feed、审核状态 |
| Google Analytics 4 | GA4 Data API | 用户行为、engagement |
| PageSpeed Insights | PageSpeed Insights API | 落地页速度评分 |
| CRM System | 自定义 API / CSV | 离线转化、SQL Rate |
| ERP | 自定义 API | 库存、利润率 |

---

## 6. 用户角色与权限

| 角色 | 职责 | 可执行操作 |
|------|------|----------|
| Ads 优化师 | 日常广告管理 | 查看报告、确认执行建议 |
| Analytics 专家 | 数据追踪与分析 | 追踪配置、GA4 集成 |
| Ecommerce 运营 | 商品 Feed 管理 | Feed 优化、库存同步 |
| CRO/Web 开发 | 落地页优化 | 页面性能修复 |
| Marketing Lead | 战略决策 | 90 天复盘、预算审批 |

---

## 7. 系统开发优先级

### Phase 1 (P1 — 最小可用系统)
1. **Daily Alert 系统** (S085-S094) — 实时监控告警
2. **转化追踪检查** (S001-S003) — 数据基础保障
3. **出价策略检查** (S005) — 效能诊断
4. **预算限制检查** (S006) — 预算优化
5. **搜索词优化** (S012-S014) — 流量质量控制

### Phase 2 (P1-P2 — 核心优化)
6. **关键词/广告/Assets 检查** (S015-S023)
7. **地域/受众/设备/时段优化** (S026-S036)
8. **政策审核监控** (S038)
9. **预算重分配 Workstream** (S060-S062)

### Phase 3 (电商专项)
10. **Product Performance 四象限** (S045)
11. **Feed 优化** (S039-S044, S071-S072)
12. **ROAS 分层** (S011, S073-S074)
13. **库存同步** (S050-S052)

### Phase 4 (高级功能)
14. **A/B 测试引擎** (S075-S076, S083-S084)
15. **线索质量闭环** (S077-S079)
16. **90 天战略复盘** (S080-S082)

---

## 8. 技术要求

### 8.1 后端
- **语言**: Python
- **API 框架**: FastAPI
- **数据库**: SQLite (已有 `ads_data.sqlite`) → 未来迁移 PostgreSQL
- **任务调度**: APScheduler / Celery
- **规则引擎**: 自研 IF-THEN 规则解析器

### 8.2 前端
- **框架**: React (已有)
- **图表**: Recharts / ECharts
- **通知**: Webhook (Slack / 钉钉 / 邮件)

### 8.3 Agent 集成
- **Claude CLI**: 用于策略分析、报告生成、优化建议文案
- **Agent Service**: 已有 `agent_service.py` 基础架构

---

## 9. 附录 — 策略全索引

| ID | 策略名称 | 类型 | 自动化级别 |
|----|---------|------|----------|
| S001 | 转化目标配置合规性诊断 | 诊断 | L2 |
| S002 | 转化价值与计数完整性监控 | 监控 | L1 |
| S003 | 进阶转化功能优化建议 | 优化 | L3 |
| S004 | Campaign 业务目标一致性校正 | 诊断/优化 | L3 |
| S005 | 竞价策略效能诊断与放量调整 | 优化 | L4 |
| S006 | 预算瓶颈识别与效能调配 | 诊断/优化 | L4 |
| S007-S010 | 账户结构拓扑优化策略集 | 诊断/优化 | L1-L3 |
| S011 | 购物/PMax 商品效率分层 | 诊断/优化 | L4 |
| S012 | 搜索词负向过滤 | 优化 | L4 |
| S013 | 高意图词拓新 | 优化 | L3 |
| S014 | 流量健康度诊断 | 诊断 | L2 |
| S015 | 关键词效果负向清理 | 优化 | L4 |
| S016 | 关键词相关性与质量得分诊断 | 诊断 | L3 |
| S017 | 流量健康度与出价水位 | 监控 | L2 |
| S018 | 广告合规性与投放状态监控 | 监控 | L1 |
| S019 | RSA 创意强度诊断 | 诊断 | L3 |
| S020 | 创意点击与转化效能优化 | 优化 | L4 |
| S021 | 核心资产缺失自动补齐 | 监控/优化 | L4 |
| S022 | 低效资产定期刷新 | 诊断/优化 | L3 |
| S023 | 资产与转化意图对齐审计 | 监控 | L2 |
| S024 | 落地页转化效能诊断 | 诊断 | L3 |
| S025 | 关键词质量得分诊断 | 诊断 | L3 |
| S026-S028 | 地理位置表现多维优化 | 优化 | L3-L4 |
| S029-S032 | 受众全链路效能优化 | 监控/优化 | L2-L4 |
| S033-S034 | 设备效率诊断与优化 | 诊断/优化 | L3-L4 |
| S035-S036 | 分时段效能优化 | 诊断/优化 | L2-L4 |
| S037 | 竞品拍卖压力诊断 | 诊断/优化 | L3 |
| S038 | 广告与素材合规性监控 | 监控/诊断 | L3 |
| S039-S041 | 商品列表质量优化 | 诊断/优化 | L2-L4 |
| S042-S044 | Merchant Center 健康管理 | 监控/诊断 | L1-L3 |
| S045 | 产品表现四象限分类 | 诊断/优化 | L3 |
| S046 | 电商标题语义增强 | 优化 | L4 |
| S047-S048 | 购物广告主图诊断 | 诊断/监控 | L3-L4 |
| S049 | 价格竞争力与促销关联 | 诊断/优化 | L4 |
| S050-S052 | 库存状态感知优化 | 监控/优化 | L1-L4 |
| S053 | 商品价值分层与标签重组 | 优化 | L4 |
| S054-S055 | 转化追踪数据质量审计 | 诊断/监控 | L1-L2 |
| S056-S059 | 控制浪费自动化优化 | 优化 | L4 |
| S060-S062 | 预算跨系列动态平衡 | 优化/监控 | L2-L4 |
| S063-S065 | 广告与素材智能化优化 | 诊断/优化 | L2-L4 |
| S066 | 落地页转化效能优化 | 诊断/优化 | L3 |
| S067-S070 | 多维度精细化定向 | 优化 | L3-L4 |
| S071-S072 | 商品 Feed 诊断与质量优化 | 诊断/优化 | L3-L4 |
| S073 | 高价值商品预算重分配 | 优化 | L4 |
| S074 | 商品价值分层预算倾斜 | 优化 | L4 |
| S075-S076 | 变量受控测试引擎 | 优化/监控 | L2-L4 |
| S077-S079 | 线索质量闭环优化 | 诊断/优化 | L2-L4 |
| S080-S082 | 90 天战略复盘诊断 | 诊断 | L2-L3 |
| S083 | 商品 Feed 元素 A/B 测试 | 优化 | L4 |
| S084 | ROAS Tier Testing | 优化 | L3 |
| S085 | 全维度表现异常实时预警 | 监控/诊断 | L1-L2 |
| S086 | 每日预算进度监控 | 监控/优化 | L4 |
| S087 | 全渠道转化异常监控 | 监控/诊断 | L2 |
| S088 | 全渠道投放异常监测 | 监控/诊断 | L2 |
| S089 | 全链路追踪健康度巡检 | 监控 | L1 |
| S090 | 搜索词流量浪费预警 | 监控/优化 | L4 |
| S091 | 落地页可用性与性能监控 | 监控/诊断 | L2 |
| S092-S094 | 政策合规与投放健康守卫 | 监控/诊断/优化 | L1-L3 |
