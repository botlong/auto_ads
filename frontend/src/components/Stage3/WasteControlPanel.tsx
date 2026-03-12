import React, { useState } from 'react';
import type { WasteControlItem } from '../../api/client';

interface WasteControlPanelProps {
  wasteControls: WasteControlItem[];
}

export const WasteControlPanel: React.FC<WasteControlPanelProps> = ({ wasteControls }) => {
  const [filter, setFilter] = useState<string>('all');

  const filteredItems = filter === 'all'
    ? wasteControls
    : wasteControls.filter(item => item.item_type === filter);

  const getActionLabel = (action: string) => {
    const labels: Record<string, string> = {
      'ADD_NEGATIVE': '添加负向词',
      'EXCLUDE_LOCATION': '排除地域',
      'EXCLUDE_AUDIENCE': '排除受众',
      'REDUCE_BID': '降低出价',
      'PAUSE': '暂停',
    };
    return labels[action] || action;
  };

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'SEARCH_TERM': '搜索词',
      'LOCATION': '地域',
      'AUDIENCE': '受众',
      'DEVICE': '设备',
      'TIME_SLOT': '时段',
    };
    return labels[type] || type;
  };

  const totalSavings = wasteControls.reduce((sum, item) => sum + item.estimated_savings, 0);

  return (
    <div className="panel-content">
      <h4>W2: 控制浪费 - 多维度无效流量清理</h4>
      <p className="panel-description">
        识别并排除低效流量来源，预计可节省 ${totalSavings.toFixed(2)}
      </p>

      {/* 类型筛选 */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        {['all', 'SEARCH_TERM', 'LOCATION', 'AUDIENCE', 'DEVICE'].map(type => (
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
            {type === 'all' ? '全部' : getTypeLabel(type)}
          </button>
        ))}
      </div>

      {filteredItems.length > 0 ? (
        <div style={{ overflowX: 'auto' }}>
          <table className="results-table">
            <thead>
              <tr>
                <th>类型</th>
                <th>名称</th>
                <th>Campaign</th>
                <th>花费</th>
                <th>转化</th>
                <th>建议操作</th>
                <th>预计节省</th>
              </tr>
            </thead>
            <tbody>
              {filteredItems.map((item, idx) => (
                <tr key={idx} style={{ background: item.estimated_savings > 50 ? '#fef2f2' : 'transparent' }}>
                  <td>
                    <span style={{
                      padding: '2px 8px',
                      borderRadius: '4px',
                      background: '#e0e7ff',
                      color: '#4338ca',
                      fontSize: '11px',
                    }}>
                      {getTypeLabel(item.item_type)}
                    </span>
                  </td>
                  <td><strong>{item.item_name}</strong></td>
                  <td>{item.campaign_name}</td>
                  <td style={{ color: '#dc2626' }}>${item.cost.toFixed(2)}</td>
                  <td>{item.conversions}</td>
                  <td>
                    <span style={{
                      padding: '4px 12px',
                      borderRadius: '4px',
                      background: item.recommended_action === 'ADD_NEGATIVE' ? '#fee2e2' :
                        item.recommended_action === 'EXCLUDE_LOCATION' ? '#ffedd5' : '#dbeafe',
                      color: item.recommended_action === 'ADD_NEGATIVE' ? '#dc2626' :
                        item.recommended_action === 'EXCLUDE_LOCATION' ? '#ea580c' : '#2563eb',
                      fontSize: '12px',
                      fontWeight: 600,
                    }}>
                      {getActionLabel(item.recommended_action)}
                    </span>
                  </td>
                  <td style={{ color: '#059669', fontWeight: 600 }}>
                    ${item.estimated_savings.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state">未发现明显的流量浪费，表现良好！</div>
      )}
    </div>
  );
};
