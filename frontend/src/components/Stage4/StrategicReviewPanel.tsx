import React from 'react';
import type { StrategicReview } from '../../api/client';

interface StrategicReviewPanelProps {
  review: StrategicReview;
}

export const StrategicReviewPanel: React.FC<StrategicReviewPanelProps> = ({ review }) => {
  // 简化的趋势图（使用 Canvas 或简单 div）
  const renderTrend = (data: number[], color: string, label: string) => {
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min || 1;

    return (
      <div className="trend-chart">
        <div className="trend-label">{label}</div>
        <div className="trend-bars">
          {data.slice(0, 30).map((value, idx) => (
            <div
              key={idx}
              className="trend-bar"
              style={{
                height: `${((value - min) / range) * 100}%`,
                backgroundColor: color,
              }}
              title={`Day ${idx + 1}: ${value.toFixed(2)}`}
            />
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="panel-content">
      <h4>🎯 90 天战略复盘 (S080-S082)</h4>
      <p className="panel-description">
        复盘周期: {review.review_period} | PMax 侵蚀率: {review.pmax_cannibalization_rate}%
      </p>

      {/* 增长指标 */}
      <div className="growth-metrics">
        <h5>📈 增长趋势</h5>
        <div className="metrics-grid">
          <div className="growth-card">
            <div className="growth-label">花费增长</div>
            <div className={`growth-value ${review.growth_metrics.spend_growth > 0 ? 'positive' : 'negative'}`}>
              {review.growth_metrics.spend_growth > 0 ? '+' : ''}{review.growth_metrics.spend_growth}%
            </div>
          </div>
          <div className="growth-card">
            <div className="growth-label">转化增长</div>
            <div className={`growth-value ${review.growth_metrics.conversion_growth > 0 ? 'positive' : 'negative'}`}>
              {review.growth_metrics.conversion_growth > 0 ? '+' : ''}{review.growth_metrics.conversion_growth}%
            </div>
          </div>
          <div className="growth-card">
            <div className="growth-label">CPA 改善</div>
            <div className={`growth-value ${review.growth_metrics.cpa_improvement < 0 ? 'positive' : 'negative'}`}>
              {review.growth_metrics.cpa_improvement > 0 ? '+' : ''}{review.growth_metrics.cpa_improvement}%
            </div>
          </div>
          <div className="growth-card">
            <div className="growth-label">ROAS 提升</div>
            <div className={`growth-value ${review.growth_metrics.roas_improvement > 0 ? 'positive' : 'negative'}`}>
              {review.growth_metrics.roas_improvement > 0 ? '+' : ''}{review.growth_metrics.roas_improvement}%
            </div>
          </div>
        </div>
      </div>

      {/* 趋势图 */}
      <div className="trends-section">
        <h5>📊 90 天趋势</h5>
        <div className="trends-grid">
          {renderTrend(review.spend_trend, '#3b82f6', '花费')}
          {renderTrend(review.conversion_trend, '#059669', '转化')}
          {renderTrend(review.cpa_trend, '#d97706', 'CPA')}
          {renderTrend(review.roas_trend, '#8b5cf6', 'ROAS')}
        </div>
      </div>

      {/* Channel Mix */}
      <div className="channel-mix-section">
        <h5>🌐 Channel Mix 分析</h5>
        <div className="channel-table">
          <table className="results-table">
            <thead>
              <tr>
                <th>渠道</th>
                <th>预算占比</th>
                <th>转化占比</th>
                <th>效率评分</th>
                <th>建议调整</th>
              </tr>
            </thead>
            <tbody>
              {review.channel_performance.map((channel, idx) => {
                const current = review.budget_allocation_current[channel.channel];
                const recommended = review.budget_allocation_recommended[channel.channel];
                const diff = recommended - current;
                return (
                  <tr key={idx}>
                    <td><strong>{channel.channel}</strong></td>
                    <td>{channel.spend_share}%</td>
                    <td>{channel.conversion_share}%</td>
                    <td>
                      <span className={`efficiency-score ${channel.efficiency_score >= 100 ? 'good' : 'poor'}`}>
                        {channel.efficiency_score}
                      </span>
                    </td>
                    <td>
                      {diff !== 0 ? (
                        <span className={diff > 0 ? 'increase' : 'decrease'}>
                          {diff > 0 ? '+' : ''}{diff}%
                        </span>
                      ) : (
                        <span className="no-change">-</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* PMax 分析 */}
      <div className="pmax-analysis">
        <h5>🛒 PMax 侵蚀检测</h5>
        <div className="pmax-metrics">
          <div className="pmax-metric">
            <span className="metric-label">Search 重叠率</span>
            <span className="metric-value">{review.pmax_search_overlap}%</span>
          </div>
          <div className="pmax-metric">
            <span className="metric-label">侵蚀率</span>
            <span className="metric-value">{review.pmax_cannibalization_rate}%</span>
          </div>
          <div className="pmax-metric">
            <span className="metric-label">增量贡献</span>
            <span className="metric-value">{review.pmax_incrementality}%</span>
          </div>
        </div>
      </div>

      {/* 战略建议 */}
      <div className="strategic-recommendations">
        <h5>💡 战略建议</h5>
        <ul className="recommendation-list">
          {review.strategic_recommendations.map((rec, idx) => (
            <li key={idx} className="recommendation-item">{rec}</li>
          ))}
        </ul>
      </div>

      {/* 下季度优先级 */}
      <div className="next-quarter-priorities">
        <h5>🎯 下季度优先级</h5>
        <ol className="priority-list">
          {review.next_quarter_priorities.map((priority, idx) => (
            <li key={idx} className="priority-item">
              <span className="priority-number">{idx + 1}</span>
              {priority}
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
};
