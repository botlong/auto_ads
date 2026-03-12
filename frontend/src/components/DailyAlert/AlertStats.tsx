import React from 'react';
import type { DailyAlertSummary } from '../../api/client';

interface AlertStatsProps {
  summary: DailyAlertSummary;
  activeAlerts: number;
  needsAttention: number;
  autoFixable: number;
}

export const AlertStats: React.FC<AlertStatsProps> = ({
  summary,
  activeAlerts,
  needsAttention,
  autoFixable,
}) => {
  const getTrendIcon = (value: number) => {
    if (value > 0) return '📈';
    if (value < 0) return '📉';
    return '➡️';
  };

  return (
    <div className="alert-stats">
      <div className="stat-card total">
        <div className="stat-icon">🔔</div>
        <div className="stat-content">
          <div className="stat-value">{summary.total_alerts}</div>
          <div className="stat-label">今日告警</div>
          <div className="stat-trend">
            {getTrendIcon(summary.vs_yesterday)} {Math.abs(summary.vs_yesterday)} 较昨日
          </div>
        </div>
      </div>

      <div className="stat-card p0">
        <div className="stat-icon">🚨</div>
        <div className="stat-content">
          <div className="stat-value">{summary.p0_alerts}</div>
          <div className="stat-label">P0 紧急</div>
          <div className="stat-sub">需立即处理</div>
        </div>
      </div>

      <div className="stat-card p1">
        <div className="stat-icon">⚠️</div>
        <div className="stat-content">
          <div className="stat-value">{summary.p1_alerts}</div>
          <div className="stat-label">P1 高优</div>
          <div className="stat-sub">24小时内处理</div>
        </div>
      </div>

      <div className="stat-card p2">
        <div className="stat-icon">📋</div>
        <div className="stat-content">
          <div className="stat-value">{summary.p2_alerts}</div>
          <div className="stat-label">P2 中优</div>
          <div className="stat-sub">计划处理</div>
        </div>
      </div>

      <div className="stat-card active">
        <div className="stat-icon">🔴</div>
        <div className="stat-content">
          <div className="stat-value">{activeAlerts}</div>
          <div className="stat-label">活动告警</div>
          <div className="stat-sub">待处理</div>
        </div>
      </div>

      <div className="stat-card attention">
        <div className="stat-icon">👁️</div>
        <div className="stat-content">
          <div className="stat-value">{needsAttention}</div>
          <div className="stat-label">需关注</div>
          <div className="stat-sub">P0 + P1</div>
        </div>
      </div>

      <div className="stat-card auto-fix">
        <div className="stat-icon">⚡</div>
        <div className="stat-content">
          <div className="stat-value">{autoFixable}</div>
          <div className="stat-label">可自动修复</div>
          <div className="stat-sub">一键解决</div>
        </div>
      </div>
    </div>
  );
};
