import React from 'react';
import type { ROASTierTest } from '../../api/client';

interface ROASTierPanelProps {
  tiers: ROASTierTest[];
}

export const ROASTierPanel: React.FC<ROASTierPanelProps> = ({ tiers }) => {
  const getTierColor = (tierName: string) => {
    switch (tierName) {
      case 'High ROAS':
        return '#059669';
      case 'Mid ROAS':
        return '#d97706';
      case 'Low ROAS':
        return '#dc2626';
      default:
        return '#64748b';
    }
  };

  const getStrategyLabel = (strategy: string) => {
    const labels: Record<string, string> = {
      'BUDGET_INCREASE': '增加预算',
      'BID_ADJUST': '调整出价',
      'CREATIVE_REFRESH': '刷新创意',
    };
    return labels[strategy] || strategy;
  };

  return (
    <div className="panel-content">
      <h4>💰 ROAS 分层测试 (S084)</h4>
      <p className="panel-description">
        根据 ROAS 表现进行分层优化测试
      </p>

      {tiers.length > 0 ? (
        <div className="roas-tier-list">
          {tiers.map((tier, idx) => (
            <div
              key={idx}
              className="roas-tier-card"
              style={{ borderLeft: `4px solid ${getTierColor(tier.tier_name)}` }}
            >
              <div className="tier-header">
                <div className="tier-info">
                  <h5>{tier.campaign_name}</h5>
                  <span
                    className="tier-label"
                    style={{ background: getTierColor(tier.tier_name) + '20', color: getTierColor(tier.tier_name) }}
                  >
                    {tier.tier_name}
                  </span>
                </div>
                <div className="tier-roas">
                  <div className="current-roas">{tier.current_roas.toFixed(2)}x</div>
                  <div className="roas-range">目标: {tier.roas_min.toFixed(1)}x - {tier.roas_max.toFixed(1)}x</div>
                </div>
              </div>

              <div className="tier-metrics">
                <div className="tier-metric">
                  <span className="metric-label">当前花费</span>
                  <span className="metric-value">${tier.current_spend.toFixed(0)}</span>
                </div>
                <div className="tier-metric">
                  <span className="metric-label">转化数</span>
                  <span className="metric-value">{tier.current_conversions}</span>
                </div>
                <div className="tier-metric">
                  <span className="metric-label">测试策略</span>
                  <span className="metric-value">{getStrategyLabel(tier.test_strategy)}</span>
                </div>
              </div>

              <div className="tier-outcome">
                <div className="expected-outcome">
                  <strong>预期效果:</strong> {tier.expected_outcome}
                </div>
                {tier.test_result && (
                  <div className={`test-result ${tier.actual_lift > 0 ? 'success' : 'failed'}`}>
                    <strong>测试结果:</strong> {tier.test_result}
                    {tier.actual_lift > 0 && `(+${tier.actual_lift}%)`}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">暂无 ROAS 分层测试数据</div>
      )}
    </div>
  );
};
