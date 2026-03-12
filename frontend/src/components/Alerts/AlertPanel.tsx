import React from 'react';
import type { Alert } from '../../api/client';

interface AlertPanelProps {
  alerts: Alert[];
}

const getAlertIcon = (level: string) => {
  switch (level) {
    case 'P0': return '🚨';
    case 'P1': return '⚠️';
    case 'P2': return '💡';
    default: return 'ℹ️';
  }
};

const formatTime = (time: string) => {
  const date = new Date(time);
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const AlertPanel: React.FC<AlertPanelProps> = ({ alerts }) => {
  if (alerts.length === 0) {
    return (
      <div className="dashboard-section">
        <h3 className="dashboard-section-title">🎉 当前无告警</h3>
        <p style={{ color: '#64748b', textAlign: 'center', padding: '20px' }}>
          所有检查项均正常，系统运行良好
        </p>
      </div>
    );
  }

  const p0Count = alerts.filter(a => a.level === 'P0').length;
  const p1Count = alerts.filter(a => a.level === 'P1').length;

  return (
    <div className="dashboard-section">
      <h3 className="dashboard-section-title">
        🚨 活动告警 ({alerts.length})
        {p0Count > 0 && <span className="severity-badge P0" style={{ marginLeft: '12px' }}>P0: {p0Count}</span>}
        {p1Count > 0 && <span className="severity-badge P1" style={{ marginLeft: '8px' }}>P1: {p1Count}</span>}
      </h3>

      {alerts.map((alert) => (
        <div key={alert.id} className={`alert-card ${alert.level}`}>
          <div className="alert-icon">{getAlertIcon(alert.level)}</div>
          <div className="alert-content">
            <div className="alert-title">{alert.title}</div>
            <div className="alert-message">{alert.message}</div>
            <div className="alert-meta">
              <span>ID: {alert.id}</span>
              <span>时间: {formatTime(alert.created_at)}</span>
              {alert.campaign_name && <span>Campaign: {alert.campaign_name}</span>}
            </div>
          </div>
          <span className={`severity-badge ${alert.level}`}>{alert.level}</span>
        </div>
      ))}
    </div>
  );
};
