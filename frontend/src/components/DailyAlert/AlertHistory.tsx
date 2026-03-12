import React, { useState, useEffect } from 'react';
import { api, type AlertHistory as AlertHistoryItem } from '../../api/client';

export const AlertHistory: React.FC = () => {
  const [history, setHistory] = useState<AlertHistoryItem[]>([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const result = await api.getAlertsHistory(7);
        setHistory(result.history);
      } catch (error) {
        console.error('Failed to fetch alert history:', error);
      }
    };

    fetchHistory();
  }, []);

  const maxTotal = Math.max(...history.map(h => h.total), 1);

  return (
    <div className="alert-history">
      <h4>📈 告警趋势 (7天)</h4>

      <div className="history-chart">
        {history.map((day, idx) => (
          <div key={idx} className="history-bar-group">
            <div className="history-bars">
              <div
                className="history-bar p0"
                style={{ height: `${(day.p0 / maxTotal) * 100}%` }}
                title={`P0: ${day.p0}`}
              />
              <div
                className="history-bar p1"
                style={{ height: `${(day.p1 / maxTotal) * 100}%` }}
                title={`P1: ${day.p1}`}
              />
              <div
                className="history-bar p2"
                style={{ height: `${(day.p2 / maxTotal) * 100}%` }}
                title={`P2: ${day.p2}`}
              />
            </div>
            <div className="history-date">{day.date.slice(5)}</div>
          </div>
        ))}
      </div>

      <div className="history-legend">
        <div className="legend-item">
          <span className="legend-color p0" />
          <span>P0 紧急</span>
        </div>
        <div className="legend-item">
          <span className="legend-color p1" />
          <span>P1 高优</span>
        </div>
        <div className="legend-item">
          <span className="legend-color p2" />
          <span>P2 中优</span>
        </div>
      </div>

      <div className="history-summary">
        <h5>告警分布</h5>
        <div className="distribution-list">
          <div className="distribution-item">
            <span>表现异常 (S085)</span>
            <span className="count">12</span>
          </div>
          <div className="distribution-item">
            <span>预算进度 (S086)</span>
            <span className="count">8</span>
          </div>
          <div className="distribution-item">
            <span>转化异常 (S087)</span>
            <span className="count">5</span>
          </div>
          <div className="distribution-item">
            <span>投放异常 (S088)</span>
            <span className="count">3</span>
          </div>
          <div className="distribution-item">
            <span>追踪健康 (S089)</span>
            <span className="count">2</span>
          </div>
          <div className="distribution-item">
            <span>搜索词浪费 (S090)</span>
            <span className="count">7</span>
          </div>
          <div className="distribution-item">
            <span>落地页告警 (S091)</span>
            <span className="count">4</span>
          </div>
          <div className="distribution-item">
            <span>政策合规 (S092-S094)</span>
            <span className="count">1</span>
          </div>
        </div>
      </div>
    </div>
  );
};
