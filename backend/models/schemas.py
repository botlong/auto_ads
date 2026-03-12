"""
Pydantic 数据模型定义
对应 SOP Stage 1 所需的所有数据结构
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class Severity(str, Enum):
    """严重程度等级"""
    P0 = "P0"  # 紧急
    P1 = "P1"  # 高优先级
    P2 = "P2"  # 中优先级
    OK = "OK"  # 正常


class CampaignStatus(str, Enum):
    """Campaign 状态"""
    ENABLED = "ENABLED"
    PAUSED = "PAUSED"
    REMOVED = "REMOVED"


class BiddingType(str, Enum):
    """出价策略类型"""
    TARGET_CPA = "TARGET_CPA"
    TARGET_ROAS = "TARGET_ROAS"
    MAXIMIZE_CONVERSIONS = "MAXIMIZE_CONVERSIONS"
    MAXIMIZE_CONVERSION_VALUE = "MAXIMIZE_CONVERSION_VALUE"
    MANUAL_CPC = "MANUAL_CPC"


class BusinessType(str, Enum):
    """业务类型"""
    LEAD_GEN = "Lead_Gen"
    ECOMMERCE = "Ecommerce"


class LearningStatus(str, Enum):
    """学习状态"""
    LEARNING = "LEARNING"
    READY = "READY"
    MISCONFIGURED = "MISCONFIGURED"


# ============ Campaign 模型 ============

class Campaign(BaseModel):
    """Campaign 数据模型"""
    id: str
    name: str
    status: CampaignStatus
    bidding_strategy_type: BiddingType
    target_cpa: Optional[float] = None  # 目标CPA (美分)
    target_roas: Optional[float] = None  # 目标ROAS (倍数)

    # 核心指标
    cost: float  # 花费 (美元)
    conversions: float  # 转化数
    conversion_value: float  # 转化价值 (美元)
    clicks: int
    impressions: int
    ctr: float  # 点击率
    cvr: float  # 转化率
    cpc: float  # 平均点击成本

    # 展示份额
    search_impression_share: float  # 搜索展示份额 (百分比)
    search_budget_lost_impression_share: float  # 预算丢失份额
    search_rank_lost_impression_share: float  # 排名丢失份额

    # 附加信息
    budget: float  # 日预算
    actual_cpa: float  # 实际CPA
    actual_roas: float  # 实际ROAS
    learning_status: LearningStatus
    days_since_created: int

    # 结构信息
    is_brand_campaign: bool = False
    has_nonbrand_keywords: bool = False  # S007: Brand campaign包含非品牌词
    network_type: str = "SEARCH"  # SEARCH, DISPLAY, YOUTUBE, SEARCH_WITH_DISPLAY
    adgroup_count: int = 5

    business_type: BusinessType = BusinessType.LEAD_GEN

    class Config:
        from_attributes = True


# ============ S001-S003: 转化追踪检查 ============

class ConversionAction(BaseModel):
    """转化操作定义"""
    id: str
    name: str
    category: str  # PURCHASE, LEAD, SIGNUP, etc.
    is_primary: bool
    count_type: str  # ONE, EVERY
    value_type: str  # STATIC, DYNAMIC
    value: Optional[float] = None
    status: str  # ENABLED, REMOVED
    tag_status: str  # ACTIVE, INACTIVE, UNVERIFIED


class ConversionTracking(BaseModel):
    """转化追踪配置"""
    account_id: str
    account_name: str

    # 转化操作列表
    conversion_actions: List[ConversionAction]

    # Enhanced Conversions 状态
    enhanced_conversions_enabled: bool
    enhanced_conversions_for_leads: bool

    # Tag 状态
    global_site_tag_status: str
    conversion_linker_status: str

    # 数据新鲜度
    last_conversion_time: Optional[datetime]
    conversion_delay_hours: int

    # 问题标记
    duplicate_primary_conversions: bool = False
    zero_value_purchase: bool = False
    inactive_tags: List[str] = []


# ============ S004: Campaign 目标检查 ============

class CampaignGoalCheck(BaseModel):
    """Campaign 目标一致性检查结果"""
    campaign_id: str
    campaign_name: str
    business_type: BusinessType
    bidding_type: BiddingType
    is_aligned: bool
    expected_bidding: List[BiddingType]
    issue_description: Optional[str] = None


# ============ S005: 出价策略检查 ============

class BiddingStrategyCheck(BaseModel):
    """出价策略检查结果"""
    campaign_id: str
    campaign_name: str
    bidding_type: BiddingType
    target_value: Optional[float]
    actual_value: float
    learning_status: LearningStatus

    # 性能分析
    performance_gap: float  # 实际vs目标的差距百分比
    is_underperforming: bool
    is_overperforming: bool

    # 调整建议
    suggested_adjustment: Optional[str] = None
    suggested_value: Optional[float] = None

    # 限制条件
    can_adjust: bool  # 是否允许调整
    restrictions: List[str] = []  # 限制原因


# ============ S006: 预算限制检查 ============

class BudgetCheck(BaseModel):
    """预算限制检查结果"""
    campaign_id: str
    campaign_name: str
    daily_budget: float
    actual_spend: float
    budget_utilization: float  # 预算使用率

    # 展示份额分析
    lost_is_budget: float  # 因预算丢失的份额
    lost_is_rank: float  # 因排名丢失的份额

    # 效率指标
    roas: float
    target_roas: Optional[float]
    cpa: float
    target_cpa: Optional[float]

    # 建议
    suggested_budget_change: Optional[float] = None  # 建议预算调整金额
    suggested_budget_change_percent: Optional[float] = None
    reason: Optional[str] = None


# ============ S007-S010: 账户结构检查 ============

class AccountStructure(BaseModel):
    """账户结构检查结果"""
    campaign_id: str
    campaign_name: str

    # 品牌词检查
    is_brand_campaign: bool
    has_nonbrand_keywords: bool  # 品牌campaign包含非品牌词

    # 网络类型检查
    network_type: str
    has_display_in_search: bool  # 搜索campaign包含展示网络

    # 结构粒度
    adgroup_count: int
    keywords_per_adgroup: float
    is_structure_too_wide: bool  # AdGroup过多
    is_structure_too_narrow: bool  # 结构过细

    # CPA一致性
    cpa_variance: float  # AdGroup间CPA方差
    has_high_cpa_variance: bool  # CPA差异过大

    # 建议
    suggestions: List[str] = []


# ============ S011: ROAS 分层检查 ============

class ProductROAS(BaseModel):
    """单个商品ROAS表现"""
    product_id: str
    product_name: str
    cost: float
    conversion_value: float
    roas: float
    spend_share: float  # 花费占比
    value_share: float  # 转化价值占比

    # 分类
    tier: str  # High, Mid, Low
    label: str  # Hero, Growth, Low-efficiency, Zombie


class ROASAnalysis(BaseModel):
    """ROAS分层分析结果"""
    campaign_id: str
    campaign_name: str
    target_roas: float

    products: List[ProductROAS]

    # 分层统计
    high_efficiency_count: int
    mid_efficiency_count: int
    low_efficiency_count: int

    # 预算倾斜建议
    budget_drainers: List[str]  # 需要减少预算的商品
    hero_products: List[str]  # 核心高效商品

    # 拆分建议
    should_split_campaign: bool
    split_reason: Optional[str] = None


# ============ 诊断结果通用模型 ============

class DiagnosisResult(BaseModel):
    """通用诊断结果项"""
    strategy_id: str  # S001-S094
    strategy_name: str
    severity: Severity

    # 问题描述
    issue_type: str
    affected_object: str  # 受影响对象
    current_value: Any  # 当前值
    benchmark_value: Any  # 基准值

    # 建议操作
    suggested_action: str
    expected_impact: Optional[str] = None

    # 元数据
    details: Dict[str, Any] = {}


class Alert(BaseModel):
    """告警通知"""
    id: str
    level: str  # P0, P1, P2
    title: str
    message: str
    campaign_id: Optional[str]
    campaign_name: Optional[str]
    created_at: datetime
    is_resolved: bool = False


# ============ API 请求/响应模型 ============

class DiagnosisRequest(BaseModel):
    """诊断请求"""
    campaign_ids: List[str] = Field(default=[], description="要诊断的Campaign ID列表，为空则诊断所有")
    days: int = Field(default=7, description="数据观察周期(天)")
    focus_areas: List[str] = Field(default=[], description="重点关注区域")


class DiagnosisResponse(BaseModel):
    """诊断响应"""
    execution_time: datetime
    data_range: str
    scanned_campaigns: int
    results: List[DiagnosisResult]
    alerts: List[Alert]
    summary: Dict[str, Any]


# ============ Stage 2: 组件级优化 ============

# S012-S014: 搜索词优化
class SearchTerm(BaseModel):
    """搜索词数据"""
    id: str
    search_term: str  # 用户实际搜索的词
    campaign_id: str
    campaign_name: str
    adgroup_id: str
    adgroup_name: str

    # 性能指标
    cost: float
    clicks: int
    impressions: int
    ctr: float
    conversions: float
    cpa: float  # 该搜索词的CPA

    # 匹配信息
    match_type: str  # BROAD, PHRASE, EXACT
    keyword_text: str  # 匹配到的关键词

    # 分析标记
    is_negative_candidate: bool = False  # 是否应添加为负向词
    is_high_intent: bool = False  # 是否高意图词(有转化)
    negative_reason: Optional[str] = None  # 建议添加负向的原因


# S015-S017: 关键词管理
class Keyword(BaseModel):
    """关键词数据"""
    id: str
    text: str
    campaign_id: str
    campaign_name: str
    adgroup_id: str
    adgroup_name: str
    match_type: str  # BROAD, PHRASE, EXACT
    status: str  # ENABLED, PAUSED

    # 性能指标
    cost: float
    clicks: int
    impressions: int
    ctr: float
    cvr: float
    cpc: float
    conversions: float

    # 质量得分
    quality_score: int  # 1-10
    ad_relevance: str  # BELOW_AVERAGE, AVERAGE, ABOVE_AVERAGE
    lp_experience: str
    expected_ctr: str

    # 出价
    cpc_bid: float
    first_page_cpc: float
    top_of_page_cpc: float

    # 分析标记
    is_underperforming: bool = False
    action_recommended: Optional[str] = None  # PAUSE, REDUCE_BID, IMPROVE_QS, REFINE_MATCH


# S018-S020: 广告文案
class AdAsset(BaseModel):
    """广告素材 (Headline/Description)"""
    text: str
    pinned: bool = False
    pin_position: Optional[int] = None
    performance_label: str  # LOW, GOOD, BEST

class ResponsiveSearchAd(BaseModel):
    """自适应搜索广告"""
    id: str
    campaign_id: str
    campaign_name: str
    adgroup_id: str
    adgroup_name: str
    status: str  # ENABLED, PAUSED, DISAPPROVED
    approval_status: str

    # 素材
    headlines: List[AdAsset]  # 至少3个,最多15个
    descriptions: List[AdAsset]  # 至少2个,最多4个

    # 性能
    ctr: float
    cvr: float
    impressions: int
    clicks: int
    conversions: float

    # Ad Strength
    ad_strength: str  # POOR, AVERAGE, GOOD, EXCELLENT
    ad_strength_rating: int  # 1-4

    # 问题标记
    issues: List[str] = []  # HEADLINE_COUNT_LOW, DESCRIPTION_COUNT_LOW, PINNING_EXCESSIVE, etc.


# S021-S023: Assets 管理
class Asset(BaseModel):
    """广告附加资源"""
    id: str
    type: str  # SITELINK, CALLOUT, STRUCTURED_SNIPPET, IMAGE, LEAD_FORM
    status: str
    performance_label: str  # LOW, GOOD, BEST

    # 具体内容
    sitelink_text: Optional[str] = None
    sitelink_url: Optional[str] = None
    callout_text: Optional[str] = None

    # 统计
    impressions: int
    clicks: int

    # 更新状态
    days_since_updated: int


# S026-S028: 地域优化
class LocationPerformance(BaseModel):
    """地域表现数据"""
    id: str
    location_name: str
    location_type: str  # TARGETED, EXCLUDED
    campaign_id: str
    campaign_name: str

    # 性能指标
    cost: float
    clicks: int
    impressions: int
    ctr: float
    conversions: float
    cpa: float
    roas: float

    # 出价调整
    bid_modifier: float  # -90% to +900%

    # 分析
    is_underperforming: bool = False
    is_outperforming: bool = False
    recommended_action: Optional[str] = None  # EXCLUDE, INCREASE_BID, SPLIT_CAMPAIGN


# S024: Landing Page 健康检查
class LandingPageHealth(BaseModel):
    """落地页健康度数据"""
    url: str
    campaign_id: str
    campaign_name: str

    # HTTP 状态
    http_status: int  # 200, 404, 500等
    is_accessible: bool

    # 性能指标
    load_time_seconds: float
    mobile_load_time_seconds: float

    # 用户体验
    bounce_rate: float  # 跳出率 (%)
    mobile_bounce_rate: float

    # 搜索词匹配
    search_term_match_rate: float  # 搜索词与落地页内容匹配率 (%)

    # 转化表现
    engagement_rate: float  # 互动率 (%)
    cvr: float  # 转化率 (%)

    # 移动端适配
    mobile_friendly: bool

    # 最后检测时间
    last_checked: datetime


# S025: Quality Score 详细诊断
class QualityScoreDiagnosis(BaseModel):
    """质量得分详细诊断"""
    keyword_id: str
    keyword_text: str
    campaign_id: str
    campaign_name: str

    # 质量得分组件
    quality_score: int  # 1-10
    ad_relevance: str  # BELOW_AVERAGE, AVERAGE, ABOVE_AVERAGE
    landing_page_experience: str
    expected_ctr: str

    # 历史对比
    historical_cpc_avg: float
    current_cpc: float
    cpc_increase_ratio: float  # 当前CPC vs 历史均值

    # 诊断结果
    issues: List[str] = []  # AD_RELEVANCE_LOW, LP_EXPERIENCE_LOW, EXPECTED_CTR_LOW
    fix_priority: str  # P0, P1, P2


# S038: 政策审核状态
class PolicyStatus(BaseModel):
    """政策合规状态"""
    campaign_id: str
    campaign_name: str

    # 广告状态
    approval_status: str  # APPROVED, DISAPPROVED, UNDER_REVIEW
    disapproval_reasons: List[str] = []

    # Asset 状态
    asset_issues: List[Dict[str, str]] = []  # [{"asset_id": "", "issue": ""}]

    # URL 健康
    broken_urls: List[str] = []

    # 投放异常 (ENABLED 但无展示)
    enabled_no_impressions: bool
    no_impression_hours: int = 0


# S039-S053: 电商专项 - 商品 Feed
class ProductFeedItem(BaseModel):
    """Feed 商品项"""
    product_id: str
    product_name: str
    status: str  # ACTIVE, DISAPPROVED, PENDING

    # Feed 完整性
    title: str
    description: str
    image_url: str
    price: float
    availability: str  # IN_STOCK, OUT_OF_STOCK, PREORDER
    brand: str
    gtin: Optional[str] = None
    mpn: Optional[str] = None

    # 表现数据
    impressions: int
    clicks: int
    ctr: float
    conversions: float
    cpa: float
    roas: float

    # 四象限分类
    performance_quadrant: str  # HERO, GROWTH, LOW_PERFORMER, ZOMBIE

    # 价格竞争力
    price_competitiveness: str  # COMPETITIVE, HIGH, LOW
    competitor_price_avg: Optional[float] = None

    # 自定义标签
    custom_labels: List[str] = []


# S029-S032: 受众优化
class AudiencePerformance(BaseModel):
    """受众表现数据"""
    id: str
    audience_name: str
    audience_type: str  # REMARKETING, CUSTOMER_LIST, SIMILAR, IN_MARKET, etc.
    campaign_id: str
    campaign_name: str

    # 覆盖
    audience_size: int
    targeting_setting: str  # TARGETING, OBSERVATION

    # 性能
    cost: float
    clicks: int
    impressions: int
    ctr: float
    conversions: float
    cpa: float

    # 出价调整
    bid_modifier: float

    # 分析
    is_underperforming: bool = False
    recommended_action: Optional[str] = None


# S033-S034: 设备优化
class DevicePerformance(BaseModel):
    """设备表现数据"""
    device_type: str  # MOBILE, DESKTOP, TABLET
    campaign_id: str
    campaign_name: str

    # 性能
    cost: float
    clicks: int
    impressions: int
    ctr: float
    conversions: float
    cpa: float
    cvr: float

    # 出价调整
    bid_modifier: float

    # 分析
    mobile_cvr_gap: Optional[float] = None  # 移动端CVR与桌面端差距
    is_underperforming: bool = False
    recommended_action: Optional[str] = None


# S035-S036: 时段优化
class HourlyPerformance(BaseModel):
    """分时段表现数据"""
    day_of_week: int  # 0=Monday, 6=Sunday
    hour_of_day: int  # 0-23
    campaign_id: str
    campaign_name: str

    # 性能
    cost: float
    clicks: int
    impressions: int
    conversions: float
    cpa: float
    cvr: float

    # 出价调整
    bid_modifier: float

    # 分析
    is_high_performance: bool = False
    is_low_performance: bool = False
    recommended_action: Optional[str] = None  # INCREASE_BID, DECREASE_BID, PAUSE


# S037: 竞品拍卖分析
class AuctionInsight(BaseModel):
    """竞品拍卖洞察"""
    campaign_id: str
    campaign_name: str
    domain: str  # 竞争对手域名

    # 份额指标
    impression_share: float
    overlap_rate: float  # 你与竞品同时出现的比例
    position_above_rate: float  # 竞品排在你上面的比例
    top_of_page_rate: float  # 竞品出现在页首的比例
    outranking_share: float  # 你超过竞品的比例

    # 分析
    is_main_competitor: bool = False
    threat_level: str  # LOW, MEDIUM, HIGH


# Stage 2 诊断响应
class Stage2DiagnosisResponse(BaseModel):
    """Stage 2 诊断响应"""
    execution_time: datetime
    data_range: str
    scanned_campaigns: int

    # 诊断结果列表
    results: List[DiagnosisResult]
    module_stats: Dict[str, Any]
    summary: Dict[str, Any]


# Stage 2 数据响应
class Stage2DataResponse(BaseModel):
    """Stage 2 数据查询响应"""
    search_terms: List[SearchTerm] = []
    keywords: List[Keyword] = []
    ads: List[ResponsiveSearchAd] = []
    assets: List[Asset] = []
    locations: List[LocationPerformance] = []
    audiences: List[AudiencePerformance] = []
    devices: List[DevicePerformance] = []
    hourly: List[HourlyPerformance] = []
    auction_insights: List[AuctionInsight] = []
    # S024-S025, S038, S039-S053
    landing_pages: List[LandingPageHealth] = []
    quality_score_diagnoses: List[QualityScoreDiagnosis] = []
    policy_status: Optional[PolicyStatus] = None
    product_feed: List[ProductFeedItem] = []


# ============ Stage 3: Workstream 执行 (S054-S074) ============

# S054-S055: 转化追踪质量审计
class TrackingAudit(BaseModel):
    """追踪质量审计结果"""
    account_id: str
    audit_status: str  # PASS, WARNING, CRITICAL

    # 检查项
    primary_goal_correct: bool  # 主要目标是否正确设置
    conversion_value_accurate: bool  # 转化价值是否准确
    tag_active: bool  # Tag 是否活跃
    enhanced_conversions_working: bool  # EC 是否工作

    # 问题列表
    issues: List[str] = []
    fix_recommendations: List[str] = []


# S056-S059: 浪费控制
class WasteControlItem(BaseModel):
    """浪费控制项目"""
    item_type: str  # SEARCH_TERM, LOCATION, AUDIENCE, DEVICE, TIME_SLOT
    item_id: str
    item_name: str
    campaign_id: str
    campaign_name: str

    # 浪费指标
    cost: float
    conversions: float
    cpa_vs_target: float  # 与目标CPA的对比

    # 建议操作
    recommended_action: str  # ADD_NEGATIVE, EXCLUDE_LOCATION, EXCLUDE_AUDIENCE, REDUCE_BID, PAUSE
    estimated_savings: float  # 预计节省金额


# S060-S062: 预算重分配
class BudgetReallocation(BaseModel):
    """预算重分配建议"""
    source_campaign_id: str
    source_campaign_name: str
    target_campaign_id: str
    target_campaign_name: str

    # 原因
    source_performance: str  # UNDERPERFORMING, OVERPERFORMING
    target_potential: str  # HIGH_POTENTIAL, EFFICIENT

    # 调整建议
    suggested_amount: float  # 建议转移金额
    suggested_percent: float  # 建议调整百分比
    reason: str


# S063-S065: 广告优化
class AdOptimization(BaseModel):
    """广告优化建议"""
    ad_id: str
    campaign_id: str
    campaign_name: str

    # 当前状态
    current_strength: str
    headline_count: int
    description_count: int
    pinned_count: int

    # 优化建议
    suggestions: List[str] = []  # ADD_HEADLINES, ADD_DESCRIPTIONS, UNPIN, REFRESH_ASSETS
    priority: str  # HIGH, MEDIUM, LOW


# S066: 落地页优化
class LandingPageIssue(BaseModel):
    """落地页问题"""
    url: str
    campaign_id: str
    campaign_name: str

    # 检测问题
    http_status: int
    load_time_seconds: float
    mobile_friendly: bool

    # 性能影响
    bounce_rate: float
    expected_cvr: float  # 预期转化率
    actual_cvr: float  # 实际转化率
    cvr_gap: float  # 转化率差距

    # 优化建议
    issues: List[str] = []  # SLOW_LOAD, NOT_MOBILE_FRIENDLY, HIGH_BOUNCE, POOR_RELEVANCE
    fix_priority: str  # P0, P1, P2


# S067-S070: 精细化定向
class BidAdjustment(BaseModel):
    """出价调整建议"""
    dimension: str  # DEVICE, LOCATION, AUDIENCE, TIME_SLOT
    dimension_id: str
    dimension_name: str
    campaign_id: str
    campaign_name: str

    # 当前表现
    current_modifier: float  # 当前出价调整百分比
    performance_vs_avg: float  # 与平均表现的对比
    cpa: float
    roas: float

    # 建议调整
    suggested_modifier: float
    adjustment_reason: str
    expected_impact: str


# S071-S072: Feed 优化 (电商)
class FeedQualityIssue(BaseModel):
    """Feed 质量问题"""
    product_id: str
    product_name: str
    campaign_id: str

    # 质量检查
    title_quality: str  # GOOD, NEEDS_IMPROVEMENT, POOR
    image_quality: str
    description_quality: str
    attributes_complete: bool

    # 具体问题
    issues: List[str] = []  # TITLE_TOO_SHORT, IMAGE_LOW_RES, MISSING_ATTRIBUTES, PRICE_UNCOMPETITIVE
    improvement_suggestions: List[str] = []


# S073-S074: Hero 商品预算倾斜
class HeroProductBudget(BaseModel):
    """Hero 商品预算分配"""
    product_id: str
    product_name: str
    campaign_id: str
    campaign_name: str

    # 商品分类
    product_label: str  # Hero, Growth, Low-efficiency, Zombie
    current_spend: float
    current_roas: float
    target_roas: float

    # 预算建议
    current_budget_share: float  # 当前预算占比
    recommended_budget_share: float  # 建议预算占比
    budget_adjustment: float  # 预算调整金额 (+增加, -减少)


# Stage 3 Workstream 结果
class WorkstreamResult(BaseModel):
    """单个 Workstream 执行结果"""
    workstream_id: str  # W1-W8
    workstream_name: str
    description: str

    # 执行状态
    status: str  # COMPLETED, PARTIAL, SKIPPED
    priority: str  # P1, P2

    # 发现的问题
    issues_found: int
    issues_resolved: int
    actions_recommended: int

    # 预估影响
    estimated_savings: float  # 预计节省
    estimated_gain: float  # 预计增益


# Stage 3 诊断响应
class Stage3DiagnosisResponse(BaseModel):
    """Stage 3 诊断响应"""
    execution_time: datetime
    data_range: str
    scanned_campaigns: int

    # 各 Workstream 结果
    workstreams: List[WorkstreamResult]

    # 详细建议
    tracking_audits: List[TrackingAudit]
    waste_controls: List[WasteControlItem]
    budget_reallocations: List[BudgetReallocation]
    ad_optimizations: List[AdOptimization]
    landing_page_issues: List[LandingPageIssue]
    bid_adjustments: List[BidAdjustment]
    feed_quality_issues: List[FeedQualityIssue]
    hero_product_budgets: List[HeroProductBudget]

    # 汇总
    total_estimated_savings: float
    total_actions_recommended: int
    summary: Dict[str, Any]


# ============ Stage 4: 高级测试与战略 (S075-S084) ============

# S075-S076: A/B 测试引擎
class ABTest(BaseModel):
    """A/B 测试定义"""
    test_id: str
    test_name: str
    campaign_id: str
    campaign_name: str

    # 测试配置
    test_type: str  # AD_COPY, LANDING_PAGE, BIDDING, AUDIENCE
    control_variant: str
    treatment_variant: str

    # 测试状态
    status: str  # RUNNING, COMPLETED, PAUSED
    start_date: datetime
    end_date: Optional[datetime]

    # 样本量
    control_sample_size: int
    treatment_sample_size: int

    # 结果统计
    control_ctr: float
    treatment_ctr: float
    control_cvr: float
    treatment_cvr: float
    control_cpa: float
    treatment_cpa: float

    # 显著性检验
    statistical_significance: float  # p-value
    is_winner_determined: bool
    winner_variant: Optional[str]
    confidence_level: float  # e.g., 95%

    # 建议
    recommendation: str  # IMPLEMENT, CONTINUE_TEST, STOP


# S077-S079: 线索质量闭环
class LeadQuality(BaseModel):
    """线索质量分析"""
    campaign_id: str
    campaign_name: str

    # 线索指标
    total_leads: int
    mql_count: int  # Marketing Qualified Leads
    sql_count: int  # Sales Qualified Leads
    closed_won_count: int

    # 转化率
    mql_rate: float  # MQL / Total Leads
    sql_rate: float  # SQL / MQL
    close_rate: float  # Closed / SQL

    # 价值分析
    avg_deal_size: float
    total_pipeline_value: float
    actual_revenue: float

    # 质量评分
    lead_quality_score: float  # 0-100
    quality_tier: str  # HIGH, MEDIUM, LOW

    # 优化建议
    improvement_suggestions: List[str]


# S080-S082: 90 天战略复盘
class StrategicReview(BaseModel):
    """战略复盘分析"""
    review_period: str  # e.g., "2026-Q1"

    # 增长趋势 (S080)
    growth_metrics: Dict[str, Any]  # 包含环比增长、同比增长
    spend_trend: List[float]  # 90 天花费趋势
    conversion_trend: List[float]  # 90 天转化趋势
    cpa_trend: List[float]  # 90 天 CPA 趋势
    roas_trend: List[float]  # 90 天 ROAS 趋势

    # Channel Mix 分析 (S081)
    channel_performance: List[Dict[str, Any]]  # 各渠道表现
    budget_allocation_current: Dict[str, float]  # 当前预算分配
    budget_allocation_recommended: Dict[str, float]  # 建议预算分配

    # PMax 侵蚀检测 (S082)
    pmax_search_overlap: float  # PMax 与 Search 的重叠率
    pmax_cannibalization_rate: float  # PMax 侵蚀 Search 的比例
    pmax_incrementality: float  # PMax 的真实增量贡献

    # 战略建议
    strategic_recommendations: List[str]
    next_quarter_priorities: List[str]


# S083: Feed 元素 A/B 测试
class FeedABTest(BaseModel):
    """商品 Feed A/B 测试"""
    test_id: str
    product_id: str
    product_name: str

    # 测试元素
    element_type: str  # TITLE, IMAGE, DESCRIPTION, PRICE
    variant_a: str
    variant_b: str

    # 表现数据
    variant_a_impressions: int
    variant_b_impressions: int
    variant_a_clicks: int
    variant_b_clicks: int
    variant_a_conversions: int
    variant_b_conversions: int
    variant_a_ctr: float
    variant_b_ctr: float

    # 结果
    winner: Optional[str]
    lift_percentage: float


# S084: ROAS Tier Testing
class ROASTierTest(BaseModel):
    """ROAS 分层测试"""
    tier_id: str
    tier_name: str  # High ROAS, Mid ROAS, Low ROAS
    campaign_id: str
    campaign_name: str

    # 分层标准
    roas_min: float
    roas_max: float

    # 当前表现
    current_roas: float
    current_spend: float
    current_conversions: int

    # 测试策略
    test_strategy: str  # BUDGET_INCREASE, BID_ADJUST, CREATIVE_REFRESH
    expected_outcome: str

    # 结果
    test_result: Optional[str]
    actual_lift: float


# Stage 4 诊断响应
class Stage4DiagnosisResponse(BaseModel):
    """Stage 4 诊断响应"""
    execution_time: datetime
    data_range: str
    scanned_campaigns: int

    # A/B 测试
    ab_tests: List[ABTest]
    active_tests_count: int
    completed_tests_count: int

    # 线索质量
    lead_quality_analysis: List[LeadQuality]
    overall_sql_rate: float
    overall_close_rate: float

    # 战略复盘
    strategic_review: StrategicReview

    # Feed 测试
    feed_ab_tests: List[FeedABTest]

    # ROAS 分层
    roas_tier_tests: List[ROASTierTest]

    # 汇总
    summary: Dict[str, Any]


# ============ Daily Alert System (S085-S094) ============

class DailyAlertType(str, Enum):
    """Daily Alert 类型"""
    PERFORMANCE_ANOMALY = "performance_anomaly"  # S085
    BUDGET_PACING = "budget_pacing"  # S086
    CONVERSION_ANOMALY = "conversion_anomaly"  # S087
    DELIVERY_ISSUE = "delivery_issue"  # S088
    TRACKING_HEALTH = "tracking_health"  # S089
    SEARCH_TERM_WASTE = "search_term_waste"  # S090
    LANDING_PAGE_ALERT = "landing_page_alert"  # S091
    POLICY_VIOLATION = "policy_violation"  # S092-S094


class DailyAlert(BaseModel):
    """每日告警项"""
    alert_id: str
    alert_type: DailyAlertType
    severity: Severity

    # 告警内容
    title: str
    message: str

    # 关联对象
    campaign_id: Optional[str]
    campaign_name: Optional[str]

    # 触发条件
    trigger_metric: str  # 触发指标
    trigger_value: float  # 当前值
    threshold_value: float  # 阈值

    # 时间信息
    created_at: datetime
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]

    # 状态
    status: str  # ACTIVE, ACKNOWLEDGED, RESOLVED, IGNORED

    # 建议操作
    recommended_action: str
    auto_fix_available: bool  # 是否支持自动修复


class DailyAlertSummary(BaseModel):
    """每日告警汇总"""
    date: str
    total_alerts: int
    p0_alerts: int
    p1_alerts: int
    p2_alerts: int

    # 按类型统计
    alerts_by_type: Dict[str, int]

    # 按 Campaign 统计
    alerts_by_campaign: Dict[str, int]

    # 趋势
    vs_yesterday: int  # 与昨天对比


class DailyAlertResponse(BaseModel):
    """Daily Alert 响应"""
    execution_time: datetime
    data_range: str

    # 告警列表
    alerts: List[DailyAlert]

    # 汇总
    summary: DailyAlertSummary

    # 统计
    active_alerts: int
    needs_attention: int  # P0 + P1
    auto_fixable: int  # 可自动修复的数量
