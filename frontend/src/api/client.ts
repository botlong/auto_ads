/**
 * API 客户端
 * 连接后端 FastAPI 服务
 */

const API_BASE_URL = '';  // 使用相对路径，通过 Vite 代理

export interface Campaign {
  id: string;
  name: string;
  status: 'ENABLED' | 'PAUSED' | 'REMOVED';
  bidding_strategy_type: string;
  target_cpa?: number;
  target_roas?: number;
  cost: number;
  conversions: number;
  conversion_value: number;
  clicks: number;
  impressions: number;
  ctr: number;
  cvr: number;
  cpc: number;
  search_impression_share: number;
  search_budget_lost_impression_share: number;
  search_rank_lost_impression_share: number;
  budget: number;
  actual_cpa: number;
  actual_roas: number;
  learning_status: string;
  days_since_created: number;
  is_brand_campaign: boolean;
  network_type: string;
  adgroup_count: number;
  business_type: string;
}

export interface DiagnosisResult {
  strategy_id: string;
  strategy_name: string;
  severity: 'P0' | 'P1' | 'P2' | 'OK';
  issue_type: string;
  affected_object: string;
  current_value: any;
  benchmark_value: any;
  suggested_action: string;
  expected_impact?: string;
  details: Record<string, any>;
}

export interface Alert {
  id: string;
  level: string;
  title: string;
  message: string;
  campaign_id?: string;
  campaign_name?: string;
  created_at: string;
  is_resolved: boolean;
}

export interface DiagnosisResponse {
  execution_time: string;
  data_range: string;
  scanned_campaigns: number;
  results: DiagnosisResult[];
  alerts: Alert[];
  summary: {
    total_issues: number;
    p0_count: number;
    p1_count: number;
    p2_count: number;
    optimized_count: number;
  };
}

// ============ Stage 2 Types ============

export interface SearchTerm {
  id: string;
  search_term: string;
  campaign_id: string;
  campaign_name: string;
  cost: number;
  clicks: number;
  ctr: number;
  conversions: number;
  cpa: number;
  match_type: string;
  is_negative_candidate: boolean;
  is_high_intent: boolean;
  negative_reason?: string;
}

export interface Keyword {
  id: string;
  text: string;
  campaign_id: string;
  campaign_name: string;
  match_type: string;
  status: string;
  cost: number;
  clicks: number;
  ctr: number;
  cvr: number;
  cpc: number;
  conversions: number;
  cpa: number;
  quality_score: number;
  ad_relevance: string;
  lp_experience: string;
  expected_ctr: string;
  cpc_bid: number;
  first_page_cpc: number;
  top_of_page_cpc: number;
  is_underperforming: boolean;
  action_recommended?: string;
}

export interface AdAsset {
  text: string;
  pinned: boolean;
  pin_position?: number;
  performance_label: string;
}

export interface ResponsiveSearchAd {
  id: string;
  campaign_id: string;
  campaign_name: string;
  status: string;
  approval_status: string;
  headlines: AdAsset[];
  descriptions: AdAsset[];
  ctr: number;
  cvr: number;
  impressions: number;
  clicks: number;
  conversions: number;
  ad_strength: string;
  ad_strength_rating: number;
  issues: string[];
}

export interface Asset {
  id: string;
  type: string;
  status: string;
  performance_label: string;
  sitelink_text?: string;
  sitelink_url?: string;
  callout_text?: string;
  impressions: number;
  clicks: number;
  days_since_updated: number;
}

export interface LocationPerformance {
  id: string;
  location_name: string;
  cost: number;
  clicks: number;
  ctr: number;
  conversions: number;
  cpa: number;
  roas: number;
  bid_modifier: number;
  is_underperforming: boolean;
  is_outperforming: boolean;
  recommended_action?: string;
}

export interface DevicePerformance {
  device_type: string;
  cost: number;
  clicks: number;
  ctr: number;
  conversions: number;
  cpa: number;
  cvr: number;
  bid_modifier: number;
  mobile_cvr_gap?: number;
  is_underperforming: boolean;
  recommended_action?: string;
}

export interface HourlyPerformance {
  day_of_week: number;
  hour_of_day: number;
  cost: number;
  clicks: number;
  conversions: number;
  cpa: number;
  cvr: number;
  is_high_performance: boolean;
  is_low_performance: boolean;
  recommended_action?: string;
}

export interface AuctionInsight {
  domain: string;
  impression_share: number;
  overlap_rate: number;
  position_above_rate: number;
  top_of_page_rate: number;
  outranking_share: number;
  is_main_competitor: boolean;
  threat_level: string;
}

export interface Stage2DataResponse {
  campaign_id: string;
  campaign_name: string;
  search_terms: SearchTerm[];
  keywords: Keyword[];
  ads: ResponsiveSearchAd[];
  assets: Asset[];
  locations: LocationPerformance[];
  devices: DevicePerformance[];
  hourly: HourlyPerformance[];
  auction_insights: AuctionInsight[];
}

export interface Stage2DiagnosisResponse {
  execution_time: string;
  data_range: string;
  scanned_campaigns: number;
  results: DiagnosisResult[];
  module_stats: Record<string, { total: number; issues: number }>;
  summary: {
    total_issues: number;
    p0_count: number;
    p1_count: number;
    p2_count: number;
    optimized_count: number;
  };
}

// ============ Stage 3 Types ============

export interface WorkstreamResult {
  workstream_id: string;
  workstream_name: string;
  description: string;
  status: string;
  priority: string;
  issues_found: number;
  issues_resolved: number;
  actions_recommended: number;
  estimated_savings: number;
  estimated_gain: number;
}

export interface WasteControlItem {
  item_type: string;
  item_id: string;
  item_name: string;
  campaign_id: string;
  campaign_name: string;
  cost: number;
  conversions: number;
  cpa_vs_target: number;
  recommended_action: string;
  estimated_savings: number;
}

export interface BudgetReallocation {
  source_campaign_id: string;
  source_campaign_name: string;
  target_campaign_id: string;
  target_campaign_name: string;
  source_performance: string;
  target_potential: string;
  suggested_amount: number;
  suggested_percent: number;
  reason: string;
}

export interface AdOptimization {
  ad_id: string;
  campaign_id: string;
  campaign_name: string;
  current_strength: string;
  headline_count: number;
  description_count: number;
  pinned_count: number;
  suggestions: string[];
  priority: string;
}

export interface LandingPageIssue {
  url: string;
  campaign_id: string;
  campaign_name: string;
  http_status: number;
  load_time_seconds: number;
  mobile_friendly: boolean;
  bounce_rate: number;
  expected_cvr: number;
  actual_cvr: number;
  cvr_gap: number;
  issues: string[];
  fix_priority: string;
}

export interface BidAdjustment {
  dimension: string;
  dimension_id: string;
  dimension_name: string;
  campaign_id: string;
  campaign_name: string;
  current_modifier: number;
  performance_vs_avg: number;
  cpa: number;
  roas: number;
  suggested_modifier: number;
  adjustment_reason: string;
  expected_impact: string;
}

// Stage 3 Additional Types
export interface TrackingAudit {
  account_id: string;
  audit_status: string;
  primary_goal_correct: boolean;
  conversion_value_accurate: boolean;
  tag_active: boolean;
  enhanced_conversions_working: boolean;
  issues: string[];
  fix_recommendations: string[];
}

export interface FeedQualityIssue {
  product_id: string;
  product_name: string;
  campaign_id: string;
  title_quality: string;
  image_quality: string;
  description_quality: string;
  attributes_complete: boolean;
  issues: string[];
  improvement_suggestions: string[];
}

export interface HeroProductBudget {
  product_id: string;
  product_name: string;
  campaign_id: string;
  campaign_name: string;
  product_label: string;
  current_spend: number;
  current_roas: number;
  target_roas: number;
  current_budget_share: number;
  recommended_budget_share: number;
  budget_adjustment: number;
}

export interface Stage3DiagnosisResponse {
  execution_time: string;
  data_range: string;
  scanned_campaigns: number;
  workstreams: WorkstreamResult[];
  tracking_audits: TrackingAudit[];
  waste_controls: WasteControlItem[];
  budget_reallocations: BudgetReallocation[];
  ad_optimizations: AdOptimization[];
  landing_page_issues: LandingPageIssue[];
  bid_adjustments: BidAdjustment[];
  feed_quality_issues: FeedQualityIssue[];
  hero_product_budgets: HeroProductBudget[];
  total_estimated_savings: number;
  total_actions_recommended: number;
  summary: {
    workstreams_completed: number;
    total_issues_found: number;
    total_actions: number;
    estimated_monthly_savings: number;
  };
}

// ============ Stage 4 Types ============

export interface ABTest {
  test_id: string;
  test_name: string;
  campaign_id: string;
  campaign_name: string;
  test_type: string;
  control_variant: string;
  treatment_variant: string;
  status: string;
  start_date: string;
  end_date?: string;
  control_sample_size: number;
  treatment_sample_size: number;
  control_ctr: number;
  treatment_ctr: number;
  control_cvr: number;
  treatment_cvr: number;
  control_cpa: number;
  treatment_cpa: number;
  statistical_significance: number;
  is_winner_determined: boolean;
  winner_variant?: string;
  confidence_level: number;
  recommendation: string;
}

export interface LeadQuality {
  campaign_id: string;
  campaign_name: string;
  total_leads: number;
  mql_count: number;
  sql_count: number;
  closed_won_count: number;
  mql_rate: number;
  sql_rate: number;
  close_rate: number;
  avg_deal_size: number;
  total_pipeline_value: number;
  actual_revenue: number;
  lead_quality_score: number;
  quality_tier: string;
  improvement_suggestions: string[];
}

export interface StrategicReview {
  review_period: string;
  growth_metrics: Record<string, any>;
  spend_trend: number[];
  conversion_trend: number[];
  cpa_trend: number[];
  roas_trend: number[];
  channel_performance: Array<{
    channel: string;
    spend_share: number;
    conversion_share: number;
    efficiency_score: number;
  }>;
  budget_allocation_current: Record<string, number>;
  budget_allocation_recommended: Record<string, number>;
  pmax_search_overlap: number;
  pmax_cannibalization_rate: number;
  pmax_incrementality: number;
  strategic_recommendations: string[];
  next_quarter_priorities: string[];
}

export interface FeedABTest {
  test_id: string;
  product_id: string;
  product_name: string;
  element_type: string;
  variant_a: string;
  variant_b: string;
  variant_a_impressions: number;
  variant_b_impressions: number;
  variant_a_clicks: number;
  variant_b_clicks: number;
  variant_a_conversions: number;
  variant_b_conversions: number;
  variant_a_ctr: number;
  variant_b_ctr: number;
  winner?: string;
  lift_percentage: number;
}

export interface ROASTierTest {
  tier_id: string;
  tier_name: string;
  campaign_id: string;
  campaign_name: string;
  roas_min: number;
  roas_max: number;
  current_roas: number;
  current_spend: number;
  current_conversions: number;
  test_strategy: string;
  expected_outcome: string;
  test_result?: string;
  actual_lift: number;
}

export interface Stage4DiagnosisResponse {
  execution_time: string;
  data_range: string;
  scanned_campaigns: number;
  ab_tests: ABTest[];
  active_tests_count: number;
  completed_tests_count: number;
  lead_quality_analysis: LeadQuality[];
  overall_sql_rate: number;
  overall_close_rate: number;
  strategic_review: StrategicReview;
  feed_ab_tests: FeedABTest[];
  roas_tier_tests: ROASTierTest[];
  summary: {
    ab_tests_active: number;
    ab_tests_completed: number;
    lead_quality_campaigns: number;
    sql_rate: number;
    close_rate: number;
    strategic_recommendations: number;
  };
}

// ============ Daily Alert Types ============

export type DailyAlertType =
  | 'performance_anomaly'   // S085
  | 'budget_pacing'         // S086
  | 'conversion_anomaly'    // S087
  | 'delivery_issue'        // S088
  | 'tracking_health'       // S089
  | 'search_term_waste'     // S090
  | 'landing_page_alert'    // S091
  | 'policy_violation';     // S092-S094

export interface DailyAlert {
  alert_id: string;
  alert_type: DailyAlertType;
  severity: 'P0' | 'P1' | 'P2' | 'OK';
  title: string;
  message: string;
  campaign_id?: string;
  campaign_name?: string;
  trigger_metric: string;
  trigger_value: number;
  threshold_value: number;
  created_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
  status: 'ACTIVE' | 'ACKNOWLEDGED' | 'RESOLVED' | 'IGNORED';
  recommended_action: string;
  auto_fix_available: boolean;
}

export interface DailyAlertSummary {
  date: string;
  total_alerts: number;
  p0_alerts: number;
  p1_alerts: number;
  p2_alerts: number;
  alerts_by_type: Record<string, number>;
  alerts_by_campaign: Record<string, number>;
  vs_yesterday: number;
}

export interface DailyAlertResponse {
  execution_time: string;
  data_range: string;
  alerts: DailyAlert[];
  summary: DailyAlertSummary;
  active_alerts: number;
  needs_attention: number;
  auto_fixable: number;
}

export interface AlertHistory {
  date: string;
  total: number;
  p0: number;
  p1: number;
  p2: number;
}

export interface DashboardMetrics {
  total_spend: number;
  total_conversions: number;
  total_conversion_value: number;
  avg_cpa: number;
  avg_roas: number;
  active_campaigns: number;
  total_campaigns: number;
  alert_count: number;
}

class ApiClient {
  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Campaign APIs
  async getCampaigns(): Promise<Campaign[]> {
    return this.fetch('/api/campaigns');
  }

  async getCampaignDetail(campaignId: string): Promise<Campaign> {
    return this.fetch(`/api/campaigns/${campaignId}`);
  }

  // Diagnosis APIs
  async runStage1Diagnosis(campaignIds: string[], days: number = 7): Promise<DiagnosisResponse> {
    return this.fetch('/api/diagnose/stage1', {
      method: 'POST',
      body: JSON.stringify({ campaign_ids: campaignIds, days }),
    });
  }

  async diagnoseConversionTracking(): Promise<DiagnosisResult[]> {
    return this.fetch('/api/diagnose/conversion-tracking');
  }

  async diagnoseBidding(campaignId: string): Promise<DiagnosisResult[]> {
    return this.fetch(`/api/diagnose/bidding/${campaignId}`);
  }

  async diagnoseBudget(campaignId: string): Promise<DiagnosisResult[]> {
    return this.fetch(`/api/diagnose/budget/${campaignId}`);
  }

  // Legacy Alert APIs
  async getLegacyAlerts(): Promise<Alert[]> {
    return this.fetch('/api/alerts');
  }

  // Dashboard APIs
  async getDashboardMetrics(): Promise<DashboardMetrics> {
    return this.fetch('/api/metrics/dashboard');
  }

  // ============ Stage 2 APIs ============
  async runStage2Diagnosis(campaignIds: string[], days: number = 7): Promise<Stage2DiagnosisResponse> {
    return this.fetch('/api/diagnose/stage2', {
      method: 'POST',
      body: JSON.stringify({ campaign_ids: campaignIds, days }),
    });
  }

  async getStage2Data(campaignId: string): Promise<Stage2DataResponse> {
    return this.fetch(`/api/stage2-data/${campaignId}`);
  }

  async getSearchTerms(campaignId?: string): Promise<SearchTerm[]> {
    const query = campaignId ? `?campaign_id=${campaignId}` : '';
    return this.fetch(`/api/search-terms${query}`);
  }

  async getKeywords(campaignId?: string): Promise<Keyword[]> {
    const query = campaignId ? `?campaign_id=${campaignId}` : '';
    return this.fetch(`/api/keywords${query}`);
  }

  async getAds(campaignId?: string): Promise<ResponsiveSearchAd[]> {
    const query = campaignId ? `?campaign_id=${campaignId}` : '';
    return this.fetch(`/api/ads${query}`);
  }

  async getAssets(campaignId?: string): Promise<Asset[]> {
    const query = campaignId ? `?campaign_id=${campaignId}` : '';
    return this.fetch(`/api/assets${query}`);
  }

  async getLocations(campaignId?: string): Promise<LocationPerformance[]> {
    const query = campaignId ? `?campaign_id=${campaignId}` : '';
    return this.fetch(`/api/locations${query}`);
  }

  async getDevices(campaignId?: string): Promise<DevicePerformance[]> {
    const query = campaignId ? `?campaign_id=${campaignId}` : '';
    return this.fetch(`/api/devices${query}`);
  }

  async getHourlyPerformance(campaignId?: string): Promise<HourlyPerformance[]> {
    const query = campaignId ? `?campaign_id=${campaignId}` : '';
    return this.fetch(`/api/hourly${query}`);
  }

  async getAuctionInsights(campaignId?: string): Promise<AuctionInsight[]> {
    const query = campaignId ? `?campaign_id=${campaignId}` : '';
    return this.fetch(`/api/auction-insights${query}`);
  }

  // ============ Stage 3 APIs ============
  async runStage3Diagnosis(campaignIds: string[], days: number = 7): Promise<Stage3DiagnosisResponse> {
    return this.fetch('/api/diagnose/stage3', {
      method: 'POST',
      body: JSON.stringify({ campaign_ids: campaignIds, days }),
    });
  }

  async getWorkstreamStatus(): Promise<{ workstreams: WorkstreamResult[] }> {
    return this.fetch('/api/workstreams/status');
  }

  // ============ Stage 4 APIs ============
  async runStage4Diagnosis(campaignIds: string[], days: number = 90): Promise<Stage4DiagnosisResponse> {
    return this.fetch('/api/diagnose/stage4', {
      method: 'POST',
      body: JSON.stringify({ campaign_ids: campaignIds, days }),
    });
  }

  async getStrategicReview(): Promise<StrategicReview> {
    return this.fetch('/api/strategic-review');
  }

  async getABTests(campaignId?: string): Promise<{ tests: ABTest[] }> {
    const query = campaignId ? `?campaign_id=${campaignId}` : '';
    return this.fetch(`/api/ab-tests${query}`);
  }

  async getLeadQuality(): Promise<{ lead_quality: LeadQuality[] }> {
    return this.fetch('/api/lead-quality');
  }

  // ============ Daily Alert APIs ============
  async runDailyAlerts(): Promise<DailyAlertResponse> {
    return this.fetch('/api/diagnose/daily-alerts', {
      method: 'POST',
    });
  }

  async getActiveAlerts(): Promise<{ alerts: DailyAlert[]; summary: DailyAlertSummary }> {
    return this.fetch('/api/alerts/active');
  }

  async getAlertsSummary(): Promise<DailyAlertSummary> {
    return this.fetch('/api/alerts/summary');
  }

  async getAlertsHistory(days: number = 7): Promise<{ history: AlertHistory[] }> {
    return this.fetch(`/api/alerts/history?days=${days}`);
  }

  async acknowledgeAlert(alertId: string): Promise<{ status: string; message: string }> {
    return this.fetch(`/api/alerts/${alertId}/acknowledge`, {
      method: 'POST',
    });
  }

  async resolveAlert(alertId: string): Promise<{ status: string; message: string }> {
    return this.fetch(`/api/alerts/${alertId}/resolve`, {
      method: 'POST',
    });
  }
}

export const api = new ApiClient();
