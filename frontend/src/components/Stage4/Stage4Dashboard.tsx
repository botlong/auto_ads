import { useState } from 'react';
import { api, type Campaign, type Stage4DiagnosisResponse } from '../../api/client';
import { ABTestPanel } from './ABTestPanel';
import { LeadQualityPanel } from './LeadQualityPanel';
import { StrategicReviewPanel } from './StrategicReviewPanel';
import { FeedTestPanel } from './FeedTestPanel';
import { ROASTierPanel } from './ROASTierPanel';
import './Stage4Dashboard.css';

interface Stage4DashboardProps {
  campaigns: Campaign[];
  selectedCampaigns: string[];
}

export const Stage4Dashboard: React.FC<Stage4DashboardProps> = ({
  selectedCampaigns,
}) => {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [diagnosis, setDiagnosis] = useState<Stage4DiagnosisResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const runDiagnosis = async () => {
    setLoading(true);
    try {
      const result = await api.runStage4Diagnosis(selectedCampaigns, 90);
      setDiagnosis(result);
    } catch (error) {
      console.error('Stage 4 diagnosis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard stage4-loading">
        <div className="spinner"></div>
        <p>正在执行战略分析...</p>
      </div>
    );
  }

  if (!diagnosis) {
    return (
      <div className="dashboard stage4-empty">
        <h3>Stage 4 - 高级测试与战略</h3>
        <p>选择 Campaign 开始 90 天战略复盘与 A/B 测试分析</p>
        <button className="btn btn-primary" onClick={runDiagnosis}>
          运行 Stage 4 诊断
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard stage4-dashboard">
      {/* 汇总概览 */}
      <div className="stage4-overview">
        <h3 className="section-title">🎯 Stage 4 战略概览</h3>
        <div className="overview-grid">
          <div className="overview-card ab-tests">
            <div className="overview-icon">🧪</div>
            <div className="overview-content">
              <div className="overview-value">{diagnosis.active_tests_count}</div>
              <div className="overview-label">运行中 A/B 测试</div>
              <div className="overview-sub">已完成: {diagnosis.completed_tests_count}</div>
            </div>
          </div>
          <div className="overview-card lead-quality">
            <div className="overview-icon">📊</div>
            <div className="overview-content">
              <div className="overview-value">{(diagnosis.overall_sql_rate * 100).toFixed(1)}%</div>
              <div className="overview-label">SQL 转化率</div>
              <div className="overview-sub">成交率: {(diagnosis.overall_close_rate * 100).toFixed(1)}%</div>
            </div>
          </div>
          <div className="overview-card strategy">
            <div className="overview-icon">🎯</div>
            <div className="overview-content">
              <div className="overview-value">{diagnosis.summary.strategic_recommendations}</div>
              <div className="overview-label">战略建议</div>
              <div className="overview-sub">复盘周期: {diagnosis.strategic_review.review_period}</div>
            </div>
          </div>
          <div className="overview-card feed">
            <div className="overview-icon">🛍️</div>
            <div className="overview-content">
              <div className="overview-value">{diagnosis.feed_ab_tests.length}</div>
              <div className="overview-label">Feed 测试</div>
              <div className="overview-sub">ROAS 分层: {diagnosis.roas_tier_tests.length}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tab 导航 */}
      <div className="stage4-tabs">
        {[
          { id: 'ab-tests', label: '🧪 A/B 测试', count: diagnosis.ab_tests.length },
          { id: 'lead-quality', label: '📊 线索质量', count: diagnosis.lead_quality_analysis.length },
          { id: 'strategic', label: '🎯 战略复盘', count: null },
          { id: 'feed-tests', label: '🛍️ Feed 测试', count: diagnosis.feed_ab_tests.length },
          { id: 'roas-tier', label: '💰 ROAS 分层', count: diagnosis.roas_tier_tests.length },
        ].map(tab => (
          <button
            key={tab.id}
            className={`stage4-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
            {tab.count !== null && (
              <span className="tab-badge">{tab.count}</span>
            )}
          </button>
        ))}
      </div>

      {/* 内容面板 */}
      <div className="stage4-content">
        {activeTab === 'ab-tests' && (
          <ABTestPanel tests={diagnosis.ab_tests} />
        )}
        {activeTab === 'lead-quality' && (
          <LeadQualityPanel leadQuality={diagnosis.lead_quality_analysis} />
        )}
        {activeTab === 'strategic' && (
          <StrategicReviewPanel review={diagnosis.strategic_review} />
        )}
        {activeTab === 'feed-tests' && (
          <FeedTestPanel tests={diagnosis.feed_ab_tests} />
        )}
        {activeTab === 'roas-tier' && (
          <ROASTierPanel tiers={diagnosis.roas_tier_tests} />
        )}
      </div>
    </div>
  );
};
