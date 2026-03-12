import React from 'react';
import type { LeadQuality } from '../../api/client';

interface LeadQualityPanelProps {
  leadQuality: LeadQuality[];
}

export const LeadQualityPanel: React.FC<LeadQualityPanelProps> = ({ leadQuality }) => {
  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'HIGH':
        return '#059669';
      case 'MEDIUM':
        return '#d97706';
      case 'LOW':
        return '#dc2626';
      default:
        return '#64748b';
    }
  };

  const getTierLabel = (tier: string) => {
    const labels: Record<string, string> = {
      'HIGH': '高质量',
      'MEDIUM': '中质量',
      'LOW': '低质量',
    };
    return labels[tier] || tier;
  };

  // 计算总计
  const totalLeads = leadQuality.reduce((sum, l) => sum + l.total_leads, 0);
  const totalMQL = leadQuality.reduce((sum, l) => sum + l.mql_count, 0);
  const totalSQL = leadQuality.reduce((sum, l) => sum + l.sql_count, 0);
  const totalRevenue = leadQuality.reduce((sum, l) => sum + l.actual_revenue, 0);

  return (
    <div className="panel-content">
      <h4>📊 线索质量闭环分析 (S077-S079)</h4>
      <p className="panel-description">
        分析 {leadQuality.length} 个 Lead Gen Campaign 的线索转化漏斗
      </p>

      {/* 总计卡片 */}
      <div className="quality-summary">
        <div className="quality-card">
          <div className="quality-value">{totalLeads}</div>
          <div className="quality-label">总线索数</div>
        </div>
        <div className="quality-card">
          <div className="quality-value">{totalMQL}</div>
          <div className="quality-label">MQL 数</div>
          <div className="quality-rate">{((totalMQL / totalLeads) * 100).toFixed(1)}%</div>
        </div>
        <div className="quality-card">
          <div className="quality-value">{totalSQL}</div>
          <div className="quality-label">SQL 数</div>
          <div className="quality-rate">{((totalSQL / totalMQL) * 100).toFixed(1)}%</div>
        </div>
        <div className="quality-card revenue">
          <div className="quality-value">${(totalRevenue / 1000).toFixed(1)}k</div>
          <div className="quality-label">实际收入</div>
        </div>
      </div>

      {/* 详细列表 */}
      {leadQuality.length > 0 ? (
        <div className="lead-quality-list">
          {leadQuality.map((item, idx) => (
            <div key={idx} className="lead-quality-card">
              <div className="quality-header">
                <h5>{item.campaign_name}</h5>
                <span
                  className="tier-badge"
                  style={{ background: getTierColor(item.quality_tier) + '20', color: getTierColor(item.quality_tier) }}
                >
                  {getTierLabel(item.quality_tier)}
                </span>
              </div>

              <div className="funnel-visualization">
                <div className="funnel-stage">
                  <div className="stage-bar" style={{ width: '100%' }}>
                    <span className="stage-label">线索</span>
                    <span className="stage-value">{item.total_leads}</span>
                  </div>
                </div>
                <div className="funnel-stage">
                  <div className="stage-bar" style={{ width: `${item.mql_rate * 100}%` }}>
                    <span className="stage-label">MQL</span>
                    <span className="stage-value">{item.mql_count} ({(item.mql_rate * 100).toFixed(1)}%)</span>
                  </div>
                </div>
                <div className="funnel-stage">
                  <div className="stage-bar" style={{ width: `${item.mql_rate * item.sql_rate * 100}%` }}>
                    <span className="stage-label">SQL</span>
                    <span className="stage-value">{item.sql_count} ({(item.sql_rate * 100).toFixed(1)}%)</span>
                  </div>
                </div>
                <div className="funnel-stage">
                  <div className="stage-bar won" style={{ width: `${item.mql_rate * item.sql_rate * item.close_rate * 100}%` }}>
                    <span className="stage-label">成交</span>
                    <span className="stage-value">{item.closed_won_count} ({(item.close_rate * 100).toFixed(1)}%)</span>
                  </div>
                </div>
              </div>

              <div className="quality-metrics">
                <div className="metric">
                  <span className="metric-label">质量评分</span>
                  <span className="metric-value">{item.lead_quality_score.toFixed(0)}/100</span>
                </div>
                <div className="metric">
                  <span className="metric-label">平均客单价</span>
                  <span className="metric-value">${item.avg_deal_size.toFixed(0)}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Pipeline</span>
                  <span className="metric-value">${(item.total_pipeline_value / 1000).toFixed(1)}k</span>
                </div>
              </div>

              {item.improvement_suggestions.length > 0 && (
                <div className="suggestions">
                  <strong>改进建议:</strong>
                  {item.improvement_suggestions.map((suggestion, i) => (
                    <div key={i} className="suggestion-item">💡 {suggestion}</div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">暂无 Lead Gen Campaign 数据</div>
      )}
    </div>
  );
};
