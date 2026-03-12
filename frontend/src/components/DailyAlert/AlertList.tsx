import React from 'react';
import type { DailyAlert } from '../../api/client';

interface AlertListProps {
  alerts: DailyAlert[];
  onAcknowledge: (alertId: string) => void;
  onResolve: (alertId: string) => void;
}

export const AlertList: React.FC<AlertListProps> = ({
  alerts,
  onAcknowledge,
  onResolve,
}) => {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'P0':
        return '#dc2626';
      case 'P1':
        return '#d97706';
      case 'P2':
        return '#ca8a04';
      default:
        return '#64748b';
    }
  };

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'performance_anomaly': '表现异常',
      'budget_pacing': '预算进度',
      'conversion_anomaly': '转化异常',
      'delivery_issue': '投放异常',
      'tracking_health': '追踪健康',
      'search_term_waste': '搜索词浪费',
      'landing_page_alert': '落地页告警',
      'policy_violation': '政策违规',
    };
    return labels[type] || type;
  };

  const getTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      'performance_anomaly': '📊',
      'budget_pacing': '💰',
      'conversion_anomaly': '📉',
      'delivery_issue': '🚫',
      'tracking_health': '🏷️',
      'search_term_waste': '💸',
      'landing_page_alert': '🔴',
      'policy_violation': '⚠️',
    };
    return icons[type] || '🔔';
  };

  if (alerts.length === 0) {
    return (
      <div className="alert-list-empty">
        <div className="empty-icon">✅</div>
        <p>暂无匹配告警</p>
      </div>
    );
  }

  return (
    <div className="alert-list">
      {alerts.map((alert) => (
        <div
          key={alert.alert_id}
          className={`alert-item ${alert.status.toLowerCase()}`}
          style={{ borderLeftColor: getSeverityColor(alert.severity) }}
        >
          <div className="alert-header">
            <div className="alert-type-icon">{getTypeIcon(alert.alert_type)}</div>
            <div className="alert-info">
              <h5 className="alert-title">{alert.title}</h5>
              <span className="alert-meta">
                {alert.campaign_name && <span className="campaign-tag">{alert.campaign_name}</span>}
                <span className="type-tag">{getTypeLabel(alert.alert_type)}</span>
                <span
                  className="severity-badge"
                  style={{ background: getSeverityColor(alert.severity) + '20', color: getSeverityColor(alert.severity) }}
                >
                  {alert.severity}
                </span>
              </span>
            </div>
            <div className="alert-time">
              {new Date(alert.created_at).toLocaleTimeString()}
            </div>
          </div>

          <div className="alert-body">
            <p className="alert-message">{alert.message}</p>

            <div className="alert-metrics">
              <div className="metric">
                <span className="metric-label">触发值:</span>
                <span className="metric-value">{alert.trigger_value.toFixed(2)}</span>
              </div>
              <div className="metric">
                <span className="metric-label">阈值:</span>
                <span className="metric-value">{alert.threshold_value.toFixed(2)}</span>
              </div>
            </div>

            <div className="alert-recommendation">
              <strong>建议:</strong> {alert.recommended_action}
              {alert.auto_fix_available && (
                <span className="auto-fix-badge">⚡ 可自动修复</span>
              )}
            </div>
          </div>

          <div className="alert-actions">
            {alert.status === 'ACTIVE' && (
              <>
                <button
                  className="btn btn-sm btn-secondary"
                  onClick={() => onAcknowledge(alert.alert_id)}
                >
                  确认
                </button>
                <button
                  className="btn btn-sm btn-primary"
                  onClick={() => onResolve(alert.alert_id)}
                >
                  解决
                </button>
              </>
            )}
            {alert.status === 'ACKNOWLEDGED' && (
              <button
                className="btn btn-sm btn-primary"
                onClick={() => onResolve(alert.alert_id)}
              >
                标记已解决
              </button>
            )}
            {alert.status === 'RESOLVED' && (
              <span className="status-resolved">✅ 已解决</span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
