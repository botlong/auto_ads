import React from 'react';
import type { LandingPageIssue } from '../../api/client';

interface LandingPagePanelProps {
  issues: LandingPageIssue[];
}

export const LandingPagePanel: React.FC<LandingPagePanelProps> = ({ issues }) => {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'P0':
        return '#dc2626';
      case 'P1':
        return '#d97706';
      default:
        return '#64748b';
    }
  };

  const getIssueLabel = (issue: string) => {
    const labels: Record<string, string> = {
      'SLOW_LOAD': '加载缓慢',
      'NOT_MOBILE_FRIENDLY': '移动端不友好',
      'HIGH_BOUNCE': '跳出率高',
      'POOR_RELEVANCE': '相关性差',
      'FORM_FRICTION': '表单摩擦',
    };
    return labels[issue] || issue;
  };

  return (
    <div className="panel-content">
      <h4>W5: 优化落地页 - CVR 诊断与提升</h4>
      <p className="panel-description">
        发现 {issues.length} 个需要优化的落地页
      </p>

      {issues.length > 0 ? (
        <div className="lp-issue-list">
          {issues.map((issue, idx) => (
            <div key={idx} className="lp-issue-item" style={{
              padding: '16px',
              background: '#f8fafc',
              borderRadius: '8px',
              marginBottom: '12px',
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                <strong>{issue.campaign_name}</strong>
                <span style={{
                  padding: '2px 8px',
                  borderRadius: '4px',
                  background: getPriorityColor(issue.fix_priority) + '20',
                  color: getPriorityColor(issue.fix_priority),
                  fontSize: '11px',
                  fontWeight: 600,
                }}>
                  {issue.fix_priority}
                </span>
              </div>

              <div style={{ fontSize: '13px', color: '#64748b', marginBottom: '8px' }}>
                URL: {issue.url}
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '12px', fontSize: '13px' }}>
                <div>加载时间: <strong>{issue.load_time_seconds}s</strong></div>
                <div>跳出率: <strong>{(issue.bounce_rate * 100).toFixed(0)}%</strong></div>
                <div>HTTP状态: <strong>{issue.http_status}</strong></div>
              </div>

              <div style={{ display: 'flex', gap: '16px', marginBottom: '12px', fontSize: '13px' }}>
                <div>实际CVR: <strong style={{ color: '#dc2626' }}>{(issue.actual_cvr * 100).toFixed(2)}%</strong></div>
                <div>预期CVR: <strong style={{ color: '#059669' }}>{(issue.expected_cvr * 100).toFixed(2)}%</strong></div>
                <div>差距: <strong>{(issue.cvr_gap * 100).toFixed(2)}%</strong></div>
              </div>

              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {issue.issues.map((item, i) => (
                  <span key={i} style={{
                    padding: '4px 12px',
                    background: '#fee2e2',
                    color: '#dc2626',
                    borderRadius: '4px',
                    fontSize: '12px',
                  }}>
                    {getIssueLabel(item)}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">落地页表现良好，无需优化</div>
      )}
    </div>
  );
};
