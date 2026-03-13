import React, { useState, useEffect } from 'react';
import { api, type Campaign, type Stage3DiagnosisResponse } from '../../api/client';
import { WorkstreamCard } from './WorkstreamCard';
import { WasteControlPanel } from './WasteControlPanel';
import { BudgetReallocationPanel } from './BudgetReallocationPanel';
import { AdOptimizationPanel } from './AdOptimizationPanel';
import { LandingPagePanel } from './LandingPagePanel';
import { BidAdjustmentPanel } from './BidAdjustmentPanel';
import './Stage3Dashboard.css';

interface Stage3DashboardProps {
  campaigns: Campaign[];
  selectedCampaigns: string[];
}

export const Stage3Dashboard: React.FC<Stage3DashboardProps> = ({
  selectedCampaigns,
}) => {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [diagnosis, setDiagnosis] = useState<Stage3DiagnosisResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedCampaigns.length > 0) {
      runDiagnosis();
    }
  }, [selectedCampaigns]);

  const runDiagnosis = async () => {
    setLoading(true);
    try {
      const result = await api.runStage3Diagnosis(selectedCampaigns, 7);
      setDiagnosis(result);
    } catch (error) {
      console.error('Stage 3 diagnosis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard stage3-loading">
        <div className="spinner"></div>
        <p>正在执行 Workstream 诊断...</p>
      </div>
    );
  }

  if (!diagnosis) {
    return (
      <div className="dashboard stage3-empty">
        <h3>Stage 3 - Workstream 执行</h3>
        <p>选择 Campaign 开始执行优化工作流</p>
        <button className="btn btn-primary" onClick={runDiagnosis}>
          运行 Stage 3 诊断
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard stage3-dashboard">
      {/* Workstream 概览 */}
      <div className="workstream-overview">
        <h3 className="section-title">🚀 Stage 3 Workstream 执行概览</h3>
        <div className="workstream-grid">
          {diagnosis.workstreams.map((ws) => (
            <WorkstreamCard
              key={ws.workstream_id}
              workstream={ws}
              isActive={activeTab === ws.workstream_id}
              onClick={() => setActiveTab(ws.workstream_id)}
            />
          ))}
        </div>
      </div>

      {/* 汇总指标 */}
      <div className="metrics-summary">
        <div className="summary-card savings">
          <div className="summary-label">预计月度节省</div>
          <div className="summary-value">${diagnosis.summary.estimated_monthly_savings.toFixed(0)}</div>
        </div>
        <div className="summary-card actions">
          <div className="summary-label">推荐操作数</div>
          <div className="summary-value">{diagnosis.total_actions_recommended}</div>
        </div>
        <div className="summary-card issues">
          <div className="summary-label">发现问题数</div>
          <div className="summary-value">{diagnosis.summary.total_issues_found}</div>
        </div>
        <div className="summary-card completed">
          <div className="summary-label">已完成工作流</div>
          <div className="summary-value">{diagnosis.summary.workstreams_completed}/8</div>
        </div>
      </div>

      {/* 详细面板 */}
      <div className="detail-panel">
        {activeTab === 'W1' && (
          <div className="panel-content">
            <h4>W1: 先修追踪 - 转化数据质量审计</h4>
            <p className="panel-description">检查转化追踪配置，确保数据质量</p>
            <div className="tracking-audit-list">
              {diagnosis.tracking_audits?.map((audit, idx) => (
                <div key={idx} className={`audit-item ${audit.audit_status.toLowerCase()}`}>
                  <div className="audit-header">
                    <span className="audit-status">{audit.audit_status}</span>
                    <span className="audit-id">{audit.account_id}</span>
                  </div>
                  {audit.issues.length > 0 && (
                    <div className="audit-issues">
                      {audit.issues.map((issue, i) => (
                        <div key={i} className="issue-item">⚠️ {issue}</div>
                      ))}
                    </div>
                  )}
                  {audit.fix_recommendations.length > 0 && (
                    <div className="audit-fixes">
                      <strong>建议修复:</strong>
                      {audit.fix_recommendations.map((fix, i) => (
                        <div key={i} className="fix-item">{fix}</div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'W2' && (
          <WasteControlPanel wasteControls={diagnosis.waste_controls} />
        )}

        {activeTab === 'W3' && (
          <BudgetReallocationPanel reallocations={diagnosis.budget_reallocations} />
        )}

        {activeTab === 'W4' && (
          <AdOptimizationPanel optimizations={diagnosis.ad_optimizations} />
        )}

        {activeTab === 'W5' && (
          <LandingPagePanel issues={diagnosis.landing_page_issues} />
        )}

        {activeTab === 'W6' && (
          <BidAdjustmentPanel adjustments={diagnosis.bid_adjustments} />
        )}

        {activeTab === 'W7' && (
          <div className="panel-content">
            <h4>W7: Feed 优化 - 商品 Feed 质量</h4>
            <p className="panel-description">电商专项：优化商品 Feed 质量</p>
            <div className="feed-optimization-list">
              {diagnosis.feed_quality_issues?.length > 0 ? (
                diagnosis.feed_quality_issues.map((issue, idx) => (
                  <div key={idx} className="feed-issue-item">
                    <div className="feed-product">{issue.product_name}</div>
                    <div className="feed-issues">
                      {issue.issues.map((i, j) => (
                        <span key={j} className="issue-tag">{i}</span>
                      ))}
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty-state">Feed 质量良好，无需优化</div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'W8' && (
          <div className="panel-content">
            <h4>W8: 预算倾斜 - Hero 商品预算重分配</h4>
            <p className="panel-description">电商专项：根据商品表现分配预算</p>
            <div className="budget-tilt-list">
              {diagnosis.hero_product_budgets?.length > 0 ? (
                diagnosis.hero_product_budgets.map((budget, idx) => (
                  <div key={idx} className={`budget-tilt-item ${budget.product_label.toLowerCase()}`}>
                    <div className="tilt-header">
                      <span className="product-name">{budget.product_name}</span>
                      <span className={`product-label ${budget.product_label.toLowerCase()}`}>
                        {budget.product_label}
                      </span>
                    </div>
                    <div className="tilt-details">
                      <div>当前预算占比: {(budget.current_budget_share * 100).toFixed(0)}%</div>
                      <div>建议占比: {(budget.recommended_budget_share * 100).toFixed(0)}%</div>
                      <div className="tilt-adjustment">
                        调整: {budget.budget_adjustment > 0 ? '+' : ''}${budget.budget_adjustment.toFixed(0)}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty-state">暂无 Hero 商品预算分配建议</div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
