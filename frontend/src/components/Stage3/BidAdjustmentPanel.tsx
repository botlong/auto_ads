import React, { useState } from 'react';
import type { BidAdjustment } from '../../api/client';

interface BidAdjustmentPanelProps {
  adjustments: BidAdjustment[];
}

export const BidAdjustmentPanel: React.FC<BidAdjustmentPanelProps> = ({ adjustments }) => {
  const [filter, setFilter] = useState<string>('all');

  const filteredAdjustments = filter === 'all'
    ? adjustments
    : adjustments.filter(a => a.dimension === filter);

  const getDimensionLabel = (dim: string) => {
    const labels: Record<string, string> = {
      'DEVICE': '设备',
      'LOCATION': '地域',
      'AUDIENCE': '受众',
      'TIME_SLOT': '时段',
    };
    return labels[dim] || dim;
  };

  const getAdjustmentColor = (current: number, suggested: number) => {
    if (suggested > current) return '#059669'; // 提高
    if (suggested < current) return '#dc2626'; // 降低
    return '#64748b';
  };

  return (
    <div className="panel-content">
      <h4>W6: 精细化定向 - 多维度出价调整</h4>
      <p className="panel-description">
        建议 {adjustments.length} 个出价调整，优化投放效率
      </p>

      {/* 维度筛选 */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        {['all', 'DEVICE', 'LOCATION', 'TIME_SLOT'].map(type => (
          <button
            key={type}
            onClick={() => setFilter(type)}
            style={{
              padding: '6px 12px',
              borderRadius: '4px',
              border: 'none',
              background: filter === type ? '#3b82f6' : '#e2e8f0',
              color: filter === type ? 'white' : '#64748b',
              cursor: 'pointer',
              fontSize: '13px',
            }}
          >
            {type === 'all' ? '全部' : getDimensionLabel(type)}
          </button>
        ))}
      </div>

      {filteredAdjustments.length > 0 ? (
        <div style={{ overflowX: 'auto' }}>
          <table className="results-table">
            <thead>
              <tr>
                <th>维度</th>
                <th>名称</th>
                <th>Campaign</th>
                <th>当前出价调整</th>
                <th>建议调整</th>
                <th>CPA</th>
                <th>原因</th>
              </tr>
            </thead>
            <tbody>
              {filteredAdjustments.map((adj, idx) => (
                <tr key={idx}>
                  <td>
                    <span style={{
                      padding: '2px 8px',
                      borderRadius: '4px',
                      background: '#e0e7ff',
                      color: '#4338ca',
                      fontSize: '11px',
                    }}>
                      {getDimensionLabel(adj.dimension)}
                    </span>
                  </td>
                  <td><strong>{adj.dimension_name}</strong></td>
                  <td>{adj.campaign_name}</td>
                  <td>{adj.current_modifier > 0 ? '+' : ''}{adj.current_modifier}%</td>
                  <td style={{
                    color: getAdjustmentColor(adj.current_modifier, adj.suggested_modifier),
                    fontWeight: 600,
                  }}>
                    {adj.suggested_modifier > 0 ? '+' : ''}{adj.suggested_modifier}%
                  </td>
                  <td>${adj.cpa.toFixed(2)}</td>
                  <td style={{ fontSize: '12px', maxWidth: '200px' }}>{adj.adjustment_reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state">当前出价调整已优化，无需修改</div>
      )}
    </div>
  );
};
