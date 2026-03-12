import React from 'react';
import type { ABTest } from '../../api/client';

interface ABTestPanelProps {
  tests: ABTest[];
}

export const ABTestPanel: React.FC<ABTestPanelProps> = ({ tests }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'RUNNING':
        return '#3b82f6';
      case 'COMPLETED':
        return '#059669';
      case 'PAUSED':
        return '#d97706';
      default:
        return '#64748b';
    }
  };

  const getRecommendationLabel = (rec: string) => {
    const labels: Record<string, string> = {
      'IMPLEMENT': '实施胜出版本',
      'CONTINUE_TEST': '继续测试',
      'STOP': '停止测试',
    };
    return labels[rec] || rec;
  };

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case 'IMPLEMENT':
        return '#059669';
      case 'CONTINUE_TEST':
        return '#3b82f6';
      case 'STOP':
        return '#dc2626';
      default:
        return '#64748b';
    }
  };

  return (
    <div className="panel-content">
      <h4>🧪 A/B 测试分析 (S075-S076)</h4>
      <p className="panel-description">
        运行中测试: {tests.filter(t => t.status === 'RUNNING').length} |
        已完成: {tests.filter(t => t.status === 'COMPLETED').length}
      </p>

      {tests.length > 0 ? (
        <div className="ab-test-list">
          {tests.map(test => (
            <div key={test.test_id} className="ab-test-card">
              <div className="test-header">
                <div className="test-info">
                  <h5>{test.test_name}</h5>
                  <span className="campaign-tag">{test.campaign_name}</span>
                </div>
                <span
                  className="status-badge"
                  style={{ background: getStatusColor(test.status) + '20', color: getStatusColor(test.status) }}
                >
                  {test.status === 'RUNNING' ? '运行中' : test.status === 'COMPLETED' ? '已完成' : '已暂停'}
                </span>
              </div>

              <div className="test-variants">
                <div className="variant control">
                  <div className="variant-label">对照组</div>
                  <div className="variant-name">{test.control_variant}</div>
                  <div className="variant-metrics">
                    <span>CTR: {test.control_ctr}%</span>
                    <span>CVR: {test.control_cvr}%</span>
                    <span>CPA: ${test.control_cpa}</span>
                  </div>
                </div>

                <div className="vs-divider">VS</div>

                <div className="variant treatment">
                  <div className="variant-label">测试组</div>
                  <div className="variant-name">{test.treatment_variant}</div>
                  <div className="variant-metrics">
                    <span>CTR: {test.treatment_ctr}%</span>
                    <span>CVR: {test.treatment_cvr}%</span>
                    <span>CPA: ${test.treatment_cpa}</span>
                  </div>
                </div>
              </div>

              <div className="test-stats">
                <div className="stat-item">
                  <span className="stat-label">置信度</span>
                  <span className="stat-value">{test.confidence_level}%</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">显著性 (p-value)</span>
                  <span className={`stat-value ${test.statistical_significance < 0.05 ? 'significant' : ''}`}>
                    {test.statistical_significance.toFixed(3)}
                  </span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">样本量</span>
                  <span className="stat-value">{test.control_sample_size + test.treatment_sample_size}</span>
                </div>
              </div>

              {test.is_winner_determined && (
                <div className="winner-banner">
                  🏆 胜出版本: {test.winner_variant}
                </div>
              )}

              <div
                className="recommendation"
                style={{ background: getRecommendationColor(test.recommendation) + '10', color: getRecommendationColor(test.recommendation) }}
              >
                建议: {getRecommendationLabel(test.recommendation)}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">暂无 A/B 测试数据</div>
      )}
    </div>
  );
};
