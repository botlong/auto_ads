import { useState, useEffect } from 'react';
import { api, type DailyAlertResponse, type DailyAlert } from '../../api/client';
import { AlertList } from './AlertList';
import { AlertStats } from './AlertStats';
import { AlertHistory } from './AlertHistory';
import './DailyAlertDashboard.css';

export const DailyAlertDashboard: React.FC = () => {
  const [alertData, setAlertData] = useState<DailyAlertResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeFilter, setActiveFilter] = useState<string>('all');
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const result = await api.runDailyAlerts();
      setAlertData(result);
    } catch (error) {
      console.error('Failed to fetch alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();

    // 自动刷新 (每 60 秒)
    let interval: ReturnType<typeof setInterval> | null = null;
    if (autoRefresh) {
      interval = setInterval(fetchAlerts, 60000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const handleAcknowledge = async (alertId: string) => {
    try {
      await api.acknowledgeAlert(alertId);
      fetchAlerts(); // 刷新数据
    } catch (error) {
      console.error('Failed to acknowledge alert:', error);
    }
  };

  const handleResolve = async (alertId: string) => {
    try {
      await api.resolveAlert(alertId);
      fetchAlerts(); // 刷新数据
    } catch (error) {
      console.error('Failed to resolve alert:', error);
    }
  };

  const getFilteredAlerts = (): DailyAlert[] => {
    if (!alertData) return [];
    if (activeFilter === 'all') return alertData.alerts;
    if (activeFilter === 'p0') return alertData.alerts.filter(a => a.severity === 'P0');
    if (activeFilter === 'p1') return alertData.alerts.filter(a => a.severity === 'P1');
    if (activeFilter === 'p2') return alertData.alerts.filter(a => a.severity === 'P2');
    if (activeFilter === 'auto-fix') return alertData.alerts.filter(a => a.auto_fix_available);
    return alertData.alerts.filter(a => a.alert_type === activeFilter);
  };

  if (loading && !alertData) {
    return (
      <div className="dashboard alert-dashboard-loading">
        <div className="spinner"></div>
        <p>正在扫描告警...</p>
      </div>
    );
  }

  if (!alertData) {
    return (
      <div className="dashboard alert-dashboard-empty">
        <h3>🚨 Daily Alert 实时监控</h3>
        <p>24/7 自动监控账户异常</p>
        <button className="btn btn-primary" onClick={fetchAlerts}>
          启动监控扫描
        </button>
      </div>
    );
  }

  const filteredAlerts = getFilteredAlerts();

  return (
    <div className="dashboard daily-alert-dashboard">
      {/* 头部控制栏 */}
      <div className="alert-dashboard-header">
        <div className="header-left">
          <h3>🚨 Daily Alert 实时监控</h3>
          <span className="last-updated">
            最后更新: {new Date(alertData.execution_time).toLocaleTimeString()}
          </span>
        </div>
        <div className="header-right">
          <label className="auto-refresh-toggle">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            自动刷新
          </label>
          <button className="btn btn-secondary" onClick={fetchAlerts} disabled={loading}>
            {loading ? '🔄 刷新中...' : '🔄 立即刷新'}
          </button>
        </div>
      </div>

      {/* 统计概览 */}
      <AlertStats
        summary={alertData.summary}
        activeAlerts={alertData.active_alerts}
        needsAttention={alertData.needs_attention}
        autoFixable={alertData.auto_fixable}
      />

      {/* 过滤器 */}
      <div className="alert-filters">
        {[
          { id: 'all', label: '全部', count: alertData.alerts.length },
          { id: 'p0', label: '🔴 P0 紧急', count: alertData.summary.p0_alerts },
          { id: 'p1', label: '🟠 P1 高优', count: alertData.summary.p1_alerts },
          { id: 'p2', label: '🟡 P2 中优', count: alertData.summary.p2_alerts },
          { id: 'auto-fix', label: '⚡ 可自动修复', count: alertData.auto_fixable },
        ].map(filter => (
          <button
            key={filter.id}
            className={`filter-btn ${activeFilter === filter.id ? 'active' : ''}`}
            onClick={() => setActiveFilter(filter.id)}
          >
            {filter.label}
            <span className="filter-count">{filter.count}</span>
          </button>
        ))}
      </div>

      {/* 主内容区 */}
      <div className="alert-dashboard-content">
        <div className="alert-list-section">
          <h4>
            告警列表
            <span className="alert-count">({filteredAlerts.length})</span>
          </h4>
          <AlertList
            alerts={filteredAlerts}
            onAcknowledge={handleAcknowledge}
            onResolve={handleResolve}
          />
        </div>

        <div className="alert-sidebar">
          <AlertHistory />
        </div>
      </div>
    </div>
  );
};
