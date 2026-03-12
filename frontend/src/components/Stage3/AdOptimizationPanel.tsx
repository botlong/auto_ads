import React from 'react';
import type { AdOptimization } from '../../api/client';

interface AdOptimizationPanelProps {
  optimizations: AdOptimization[];
}

export const AdOptimizationPanel: React.FC<AdOptimizationPanelProps> = ({ optimizations }) => {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return '#dc2626';
      case 'MEDIUM':
        return '#d97706';
      default:
        return '#059669';
    }
  };

  const getSuggestionLabel = (suggestion: string) => {
    const labels: Record<string, string> = {
      'ADD_HEADLINES': '添加 Headlines',
      'ADD_DESCRIPTIONS': '添加 Descriptions',
      'REFRESH_ASSETS': '刷新素材',
      'ADD_OFFER': '添加 Offer',
      'UNPIN_HEADLINES': '取消固定 Headlines',
    };
    return labels[suggestion] || suggestion;
  };

  return (
    <div className="panel-content">
      <h4>W4: 优化广告 - Ad Strength 补全与素材刷新</h4>
      <p className="panel-description">
        识别 {optimizations.length} 个需要优化的广告
      </p>

      {optimizations.length > 0 ? (
        <div className="ad-optimization-list">
          {optimizations.map((opt, idx) => (
            <div key={idx} className="ad-optimization-item" style={{
              padding: '16px',
              background: '#f8fafc',
              borderRadius: '8px',
              marginBottom: '12px',
              borderLeft: `4px solid ${getPriorityColor(opt.priority)}`,
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <strong>{opt.campaign_name}</strong>
                <span style={{
                  padding: '2px 8px',
                  borderRadius: '4px',
                  background: getPriorityColor(opt.priority) + '20',
                  color: getPriorityColor(opt.priority),
                  fontSize: '11px',
                  fontWeight: 600,
                }}>
                  {opt.priority} 优先级
                </span>
              </div>

              <div style={{ display: 'flex', gap: '24px', marginBottom: '12px', fontSize: '13px' }}>
                <div>当前强度: <strong>{opt.current_strength}</strong></div>
                <div>Headlines: {opt.headline_count}</div>
                <div>Descriptions: {opt.description_count}</div>
                <div>固定: {opt.pinned_count}</div>
              </div>

              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {opt.suggestions.map((suggestion, i) => (
                  <span key={i} style={{
                    padding: '4px 12px',
                    background: '#dbeafe',
                    color: '#1e40af',
                    borderRadius: '4px',
                    fontSize: '12px',
                  }}>
                    {getSuggestionLabel(suggestion)}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">广告质量良好，无需优化</div>
      )}
    </div>
  );
};
