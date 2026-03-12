import React from 'react';
import type { BudgetReallocation } from '../../api/client';

interface BudgetReallocationPanelProps {
  reallocations: BudgetReallocation[];
}

export const BudgetReallocationPanel: React.FC<BudgetReallocationPanelProps> = ({ reallocations }) => {
  const totalAmount = reallocations.reduce((sum, r) => sum + r.suggested_amount, 0);

  return (
    <div className="panel-content">
      <h4>W3: 预算重分配 - 跨系列动态平衡</h4>
      <p className="panel-description">
        建议转移预算 ${totalAmount.toFixed(2)} 到更高效 Campaign
      </p>

      {reallocations.length > 0 ? (
        <div className="reallocation-list">
          {reallocations.map((item, idx) => (
            <div key={idx} className="reallocation-item" style={{
              padding: '16px',
              background: '#f8fafc',
              borderRadius: '8px',
              marginBottom: '12px',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                <div style={{
                  padding: '8px 16px',
                  background: '#fee2e2',
                  borderRadius: '4px',
                  fontSize: '13px',
                }}>
                  {item.source_campaign_name}
                </div>
                <span style={{ fontSize: '20px' }}>→</span>
                <div style={{
                  padding: '8px 16px',
                  background: '#d1fae5',
                  borderRadius: '4px',
                  fontSize: '13px',
                }}>
                  {item.target_campaign_name}
                </div>
              </div>
              <div style={{ display: 'flex', gap: '24px', fontSize: '13px', color: '#64748b' }}>
                <div>转移金额: <strong style={{ color: '#3b82f6' }}>${item.suggested_amount.toFixed(2)}</strong></div>
                <div>调整幅度: <strong>{item.suggested_percent}%</strong></div>
              </div>
              <div style={{ marginTop: '8px', fontSize: '13px', color: '#475569' }}>
                原因: {item.reason}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">当前预算分配合理，无需调整</div>
      )}
    </div>
  );
};
