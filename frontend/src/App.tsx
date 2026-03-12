import { useState, useEffect } from 'react';
import { api, type Campaign, type DiagnosisResponse, type DashboardMetrics } from './api/client';
import { MetricsCard } from './components/Dashboard/MetricsCard';
import { CampaignList } from './components/Dashboard/CampaignList';
import { AlertPanel } from './components/Alerts/AlertPanel';
import { ResultsTable } from './components/Diagnosis/ResultsTable';
import { Stage2Dashboard } from './components/Stage2/Stage2Dashboard';
import { Stage3Dashboard } from './components/Stage3/Stage3Dashboard';
import { Stage4Dashboard } from './components/Stage4/Stage4Dashboard';
import { DailyAlertDashboard } from './components/DailyAlert/DailyAlertDashboard';
import './components/Dashboard/Dashboard.css';

function App() {
  const [activeStage, setActiveStage] = useState<'stage1' | 'stage2' | 'stage3' | 'stage4' | 'daily-alert'>('stage1');
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [selectedCampaigns, setSelectedCampaigns] = useState<string[]>([]);
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [diagnosis, setDiagnosis] = useState<DiagnosisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [diagnosing, setDiagnosing] = useState(false);

  // 初始加载
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [campaignsData, metricsData] = await Promise.all([
        api.getCampaigns(),
        api.getDashboardMetrics(),
      ]);
      setCampaigns(campaignsData);
      setMetrics(metricsData);
      // 默认全选
      setSelectedCampaigns(campaignsData.filter(c => c.status === 'ENABLED').map(c => c.id));
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRunDiagnosis = async () => {
    if (selectedCampaigns.length === 0) {
      alert('请至少选择一个 Campaign');
      return;
    }

    setDiagnosing(true);
    try {
      const result = await api.runStage1Diagnosis(selectedCampaigns, 7);
      setDiagnosis(result);
    } catch (error) {
      console.error('Diagnosis failed:', error);
      alert('诊断失败，请检查后端服务是否运行');
    } finally {
      setDiagnosing(false);
    }
  };

  const handleSelectCampaign = (id: string) => {
    setSelectedCampaigns(prev =>
      prev.includes(id)
        ? prev.filter(c => c !== id)
        : [...prev, id]
    );
  };

  const handleSelectAll = () => {
    if (selectedCampaigns.length === campaigns.length) {
      setSelectedCampaigns([]);
    } else {
      setSelectedCampaigns(campaigns.map(c => c.id));
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        加载中...
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Google Ads 自动化管理系统</h1>
        <p>SOP Stage 1, 2 & 3 - 基础设置、组件级优化与 Workstream 执行 | 实时监控与诊断</p>

        {/* Stage 切换 */}
        <div style={{ display: 'flex', gap: '12px', marginTop: '16px', flexWrap: 'wrap' }}>
          <button
            onClick={() => setActiveStage('stage1')}
            style={{
              padding: '10px 24px',
              borderRadius: '8px',
              border: 'none',
              background: activeStage === 'stage1' ? '#3b82f6' : '#f1f5f9',
              color: activeStage === 'stage1' ? 'white' : '#64748b',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '14px',
            }}
          >
            📊 Stage 1 - 基础设置
          </button>
          <button
            onClick={() => setActiveStage('stage2')}
            style={{
              padding: '10px 24px',
              borderRadius: '8px',
              border: 'none',
              background: activeStage === 'stage2' ? '#3b82f6' : '#f1f5f9',
              color: activeStage === 'stage2' ? 'white' : '#64748b',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '14px',
            }}
          >
            🔍 Stage 2 - 组件优化
          </button>
          <button
            onClick={() => setActiveStage('stage3')}
            style={{
              padding: '10px 24px',
              borderRadius: '8px',
              border: 'none',
              background: activeStage === 'stage3' ? '#3b82f6' : '#f1f5f9',
              color: activeStage === 'stage3' ? 'white' : '#64748b',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '14px',
            }}
          >
            🚀 Stage 3 - Workstream 执行
          </button>
          <button
            onClick={() => setActiveStage('stage4')}
            style={{
              padding: '10px 24px',
              borderRadius: '8px',
              border: 'none',
              background: activeStage === 'stage4' ? '#8b5cf6' : '#f1f5f9',
              color: activeStage === 'stage4' ? 'white' : '#64748b',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '14px',
            }}
          >
            🎯 Stage 4 - 战略复盘
          </button>
          <button
            onClick={() => setActiveStage('daily-alert')}
            style={{
              padding: '10px 24px',
              borderRadius: '8px',
              border: 'none',
              background: activeStage === 'daily-alert' ? '#dc2626' : '#f1f5f9',
              color: activeStage === 'daily-alert' ? 'white' : '#64748b',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '14px',
            }}
          >
            🚨 Daily Alert - 实时监控
          </button>
        </div>
      </div>

      {activeStage === 'stage2' ? (
        <Stage2Dashboard
          campaigns={campaigns}
          selectedCampaigns={selectedCampaigns}
        />
      ) : activeStage === 'stage3' ? (
        <Stage3Dashboard
          campaigns={campaigns}
          selectedCampaigns={selectedCampaigns}
        />
      ) : activeStage === 'stage4' ? (
        <Stage4Dashboard
          campaigns={campaigns}
          selectedCampaigns={selectedCampaigns}
        />
      ) : activeStage === 'daily-alert' ? (
        <DailyAlertDashboard />
      ) : (
      <>
      {/* KPI 指标卡片 */}
      {metrics && (
        <div className="metrics-grid">
          <MetricsCard
            title="总花费"
            value={`$${metrics.total_spend.toLocaleString()}`}
            subtitle={`${metrics.total_conversions} 次转化`}
            color="blue"
          />
          <MetricsCard
            title="平均 CPA"
            value={`$${metrics.avg_cpa.toFixed(2)}`}
            subtitle="每次转化成本"
            color="green"
          />
          <MetricsCard
            title="平均 ROAS"
            value={`${metrics.avg_roas.toFixed(2)}x`}
            subtitle="广告回报率"
            color="purple"
          />
          <MetricsCard
            title="活跃 Campaign"
            value={`${metrics.active_campaigns}/${metrics.total_campaigns}`}
            subtitle={`${metrics.alert_count} 个活动告警`}
            color={metrics.alert_count > 0 ? 'red' : 'green'}
          />
        </div>
      )}

      {/* Campaign 选择器 */}
      <div className="dashboard-section">
        <h3 className="dashboard-section-title">📋 选择要诊断的 Campaign</h3>
        <CampaignList
          campaigns={campaigns}
          selectedIds={selectedCampaigns}
          onSelect={handleSelectCampaign}
          onSelectAll={handleSelectAll}
        />
        <div style={{ marginTop: '20px', display: 'flex', gap: '12px' }}>
          <button
            className="btn btn-primary"
            onClick={handleRunDiagnosis}
            disabled={diagnosing || selectedCampaigns.length === 0}
          >
            {diagnosing ? (
              <>
                <span className="spinner" style={{ width: '16px', height: '16px', marginRight: '8px' }}></span>
                诊断中...
              </>
            ) : (
              <>🔍 运行 Stage 1 诊断</>
            )}
          </button>
          <button className="btn" onClick={loadData} style={{ background: '#f1f5f9', color: '#475569' }}>
            🔄 刷新数据
          </button>
        </div>
      </div>

      {/* 诊断摘要 */}
      {diagnosis && (
        <div className="dashboard-section" style={{ background: '#f8fafc' }}>
          <h3 className="dashboard-section-title">📈 诊断摘要</h3>
          <div className="metrics-grid" style={{ gridTemplateColumns: 'repeat(5, 1fr)' }}>
            <MetricsCard
              title="扫描 Campaign"
              value={diagnosis.scanned_campaigns}
              color="blue"
            />
            <MetricsCard
              title="P0 紧急问题"
              value={diagnosis.summary.p0_count}
              color="red"
            />
            <MetricsCard
              title="P1 高优先级"
              value={diagnosis.summary.p1_count}
              color="orange"
            />
            <MetricsCard
              title="P2 中优先级"
              value={diagnosis.summary.p2_count}
              color="purple"
            />
            <MetricsCard
              title="已优化"
              value={diagnosis.summary.optimized_count}
              color="green"
            />
          </div>
        </div>
      )}

      {/* 告警面板 */}
      {diagnosis && diagnosis.alerts.length > 0 && (
        <AlertPanel alerts={diagnosis.alerts} />
      )}

      {/* 详细结果表格 */}
      {diagnosis && diagnosis.results.length > 0 && (
        <ResultsTable results={diagnosis.results} campaigns={campaigns.filter(c => selectedCampaigns.includes(c.id))} />
      )}

      {/* 说明文档 */}
      {!diagnosis && (
        <div className="dashboard-section">
          <h3 className="dashboard-section-title">📚 Stage 1 检查项说明</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
            <div style={{ padding: '16px', background: '#f8fafc', borderRadius: '8px' }}>
              <h4 style={{ marginBottom: '8px', color: '#1e293b' }}>S001-S003 转化追踪检查</h4>
              <p style={{ fontSize: '13px', color: '#64748b' }}>
                检查 Primary/Secondary 转化设置、转化价值完整性、Tag 活性、Enhanced Conversions 状态
              </p>
            </div>
            <div style={{ padding: '16px', background: '#f8fafc', borderRadius: '8px' }}>
              <h4 style={{ marginBottom: '8px', color: '#1e293b' }}>S004 Campaign 目标检查</h4>
              <p style={{ fontSize: '13px', color: '#64748b' }}>
                校验业务类型(Lead Gen/Ecommerce)与出价策略(tCPA/tROAS)的匹配度
              </p>
            </div>
            <div style={{ padding: '16px', background: '#f8fafc', borderRadius: '8px' }}>
              <h4 style={{ marginBottom: '8px', color: '#1e293b' }}>S005 出价策略检查</h4>
              <p style={{ fontSize: '13px', color: '#64748b' }}>
                诊断 tCPA/tROAS 效能、Learning Status、目标合理性、放量可行性
              </p>
            </div>
            <div style={{ padding: '16px', background: '#f8fafc', borderRadius: '8px' }}>
              <h4 style={{ marginBottom: '8px', color: '#1e293b' }}>S006 预算限制检查</h4>
              <p style={{ fontSize: '13px', color: '#64748b' }}>
                分析 Lost IS (Budget/Rank)、预算 vs 排名限制、建议预算调整
              </p>
            </div>
            <div style={{ padding: '16px', background: '#f8fafc', borderRadius: '8px' }}>
              <h4 style={{ marginBottom: '8px', color: '#1e293b' }}>S007-S010 账户结构检查</h4>
              <p style={{ fontSize: '13px', color: '#64748b' }}>
                Brand/Non-brand 隔离、网络合规、结构粒度评估、CPA一致性
              </p>
            </div>
            <div style={{ padding: '16px', background: '#f8fafc', borderRadius: '8px' }}>
              <h4 style={{ marginBottom: '8px', color: '#1e293b' }}>S011 ROAS 分层检查</h4>
              <p style={{ fontSize: '13px', color: '#64748b' }}>
                商品效率 High/Mid/Low 分类、预算倾斜建议、拆分建议
              </p>
            </div>
          </div>
        </div>
      )}
      </>)}
    </div>
  );
}

export default App;
