import React, { useState } from 'react';
import { api, type Campaign, type Stage2DiagnosisResponse, type Stage2DataResponse } from '../../api/client';
import { SearchTermsTable } from './SearchTermsTable';
import { KeywordsTable } from './KeywordsTable';
import { AdsPanel } from './AdsPanel';
import { DeviceLocationPanel } from './DeviceLocationPanel';
import '../Dashboard/Dashboard.css';

interface Stage2DashboardProps {
  campaigns: Campaign[];
  selectedCampaigns: string[];
}

export const Stage2Dashboard: React.FC<Stage2DashboardProps> = ({
  campaigns,
  selectedCampaigns,
}) => {
  const [activeTab, setActiveTab] = useState<'diagnosis' | 'search-terms' | 'keywords' | 'ads' | 'devices'>('diagnosis');
  const [diagnosis, setDiagnosis] = useState<Stage2DiagnosisResponse | null>(null);
  const [stage2Data, setStage2Data] = useState<Record<string, Stage2DataResponse>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runStage2Diagnosis = async () => {
    if (selectedCampaigns.length === 0) {
      alert('请至少选择一个 Campaign');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const [diagnosisResult, ...dataResults] = await Promise.all([
        api.runStage2Diagnosis(selectedCampaigns, 7),
        ...selectedCampaigns.map(id => api.getStage2Data(id))
      ]);

      setDiagnosis(diagnosisResult);

      const dataMap: Record<string, Stage2DataResponse> = {};
      selectedCampaigns.forEach((id, index) => {
        dataMap[id] = dataResults[index];
      });
      setStage2Data(dataMap);
    } catch (err) {
      setError('诊断失败，请检查后端服务');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getModuleColor = (moduleId: string) => {
    const colors: Record<string, string> = {
      'S012': '#3b82f6', 'S013': '#3b82f6', 'S014': '#3b82f6',
      'S015': '#10b981', 'S016': '#10b981', 'S017': '#10b981',
      'S018': '#f59e0b', 'S019': '#f59e0b', 'S020': '#f59e0b',
      'S021': '#8b5cf6', 'S022': '#8b5cf6', 'S023': '#8b5cf6',
      'S026': '#ec4899', 'S027': '#ec4899', 'S028': '#ec4899',
      'S033': '#06b6d4', 'S034': '#06b6d4',
      'S035': '#84cc16', 'S036': '#84cc16',
      'S037': '#f97316',
    };
    return colors[moduleId] || '#6b7280';
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>SOP Stage 2 - 组件级优化</h1>
        <p>搜索词、关键词、广告、地域、设备、时段精细化诊断</p>
      </div>

      {/* 操作按钮 */}
      <div className="dashboard-section">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <span style={{ fontWeight: 600, marginRight: '12px' }}>已选择 {selectedCampaigns.length} 个 Campaign</span>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              className="btn btn-primary"
              onClick={runStage2Diagnosis}
              disabled={loading || selectedCampaigns.length === 0}
            >
              {loading ? (
                <>
                  <span className="spinner" style={{ width: '16px', height: '16px', marginRight: '8px' }}></span>
                  诊断中...
                </>
              ) : (
                <>🔍 运行 Stage 2 诊断</>
              )}
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div style={{ padding: '16px', background: '#fee2e2', color: '#dc2626', borderRadius: '8px', marginBottom: '20px' }}>
          {error}
        </div>
      )}

      {/* Tab 导航 */}
      {diagnosis && (
        <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', flexWrap: 'wrap' }}>
          {[
            { id: 'diagnosis', label: '📊 诊断摘要', count: diagnosis.summary.total_issues },
            { id: 'search-terms', label: '🔍 搜索词', count: Object.values(stage2Data).reduce((acc, d) => acc + d.search_terms.length, 0) },
            { id: 'keywords', label: '🎯 关键词', count: Object.values(stage2Data).reduce((acc, d) => acc + d.keywords.length, 0) },
            { id: 'ads', label: '📝 广告文案', count: Object.values(stage2Data).reduce((acc, d) => acc + d.ads.length, 0) },
            { id: 'devices', label: '📱 设备/地域', count: Object.values(stage2Data).reduce((acc, d) => acc + d.devices.length + d.locations.length, 0) },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              style={{
                padding: '10px 20px',
                borderRadius: '8px',
                border: 'none',
                background: activeTab === tab.id ? '#3b82f6' : '#f1f5f9',
                color: activeTab === tab.id ? 'white' : '#64748b',
                cursor: 'pointer',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
              }}
            >
              {tab.label}
              {tab.count > 0 && (
                <span style={{
                  background: activeTab === tab.id ? 'rgba(255,255,255,0.3)' : '#e2e8f0',
                  padding: '2px 8px',
                  borderRadius: '12px',
                  fontSize: '12px',
                }}>
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </div>
      )}

      {/* 诊断摘要 Tab */}
      {activeTab === 'diagnosis' && diagnosis && (
        <>
          {/* 统计卡片 */}
          <div className="metrics-grid">
            <div className="metrics-card" style={{ borderLeft: '4px solid #dc2626' }}>
              <div className="metrics-card-header">
                <span className="metrics-card-title">P0 紧急</span>
              </div>
              <div className="metrics-card-value" style={{ color: '#dc2626' }}>{diagnosis.summary.p0_count}</div>
            </div>
            <div className="metrics-card" style={{ borderLeft: '4px solid #ea580c' }}>
              <div className="metrics-card-header">
                <span className="metrics-card-title">P1 高优先级</span>
              </div>
              <div className="metrics-card-value" style={{ color: '#ea580c' }}>{diagnosis.summary.p1_count}</div>
            </div>
            <div className="metrics-card" style={{ borderLeft: '4px solid #d97706' }}>
              <div className="metrics-card-header">
                <span className="metrics-card-title">P2 中优先级</span>
              </div>
              <div className="metrics-card-value" style={{ color: '#d97706' }}>{diagnosis.summary.p2_count}</div>
            </div>
            <div className="metrics-card" style={{ borderLeft: '4px solid #059669' }}>
              <div className="metrics-card-header">
                <span className="metrics-card-title">已优化</span>
              </div>
              <div className="metrics-card-value" style={{ color: '#059669' }}>{diagnosis.summary.optimized_count}</div>
            </div>
          </div>

          {/* 模块统计 */}
          <div className="dashboard-section">
            <h3 className="dashboard-section-title">📈 各模块问题统计</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
              {Object.entries(diagnosis.module_stats).map(([module, stats]) => (
                <div
                  key={module}
                  style={{
                    padding: '12px 20px',
                    borderRadius: '8px',
                    background: stats.issues > 0 ? '#fef3c7' : '#d1fae5',
                    border: `2px solid ${stats.issues > 0 ? '#f59e0b' : '#10b981'}`,
                  }}
                >
                  <div style={{ fontWeight: 600, fontSize: '14px' }}>{module}</div>
                  <div style={{ fontSize: '12px', color: stats.issues > 0 ? '#d97706' : '#059669' }}>
                    {stats.issues > 0 ? `${stats.issues} 个问题` : '全部正常'}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 详细结果 */}
          <div className="dashboard-section">
            <h3 className="dashboard-section-title">🔍 详细诊断结果</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {diagnosis.results
                .filter(r => r.severity !== 'OK')
                .sort((a, b) => {
                  const order = { 'P0': 0, 'P1': 1, 'P2': 2, 'OK': 3 };
                  return order[a.severity] - order[b.severity];
                })
                .map((result, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: '16px',
                      borderRadius: '8px',
                      borderLeft: `4px solid ${
                        result.severity === 'P0' ? '#dc2626' :
                        result.severity === 'P1' ? '#ea580c' :
                        result.severity === 'P2' ? '#d97706' : '#059669'
                      }`,
                      background: '#f8fafc',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <span
                          className={`severity-badge ${result.severity}`}
                          style={{ fontSize: '11px', padding: '2px 8px' }}
                        >
                          {result.severity}
                        </span>
                        <span style={{ fontWeight: 600, color: getModuleColor(result.strategy_id) }}>
                          {result.strategy_id}
                        </span>
                        <span style={{ color: '#64748b', fontSize: '14px' }}>{result.strategy_name}</span>
                      </div>
                    </div>
                    <div style={{ fontWeight: 600, marginBottom: '8px', color: '#1e293b' }}>
                      {result.issue_type}
                    </div>
                    <div style={{ fontSize: '13px', color: '#64748b', marginBottom: '8px' }}>
                      {result.affected_object}
                    </div>
                    <div style={{
                      padding: '12px',
                      background: 'white',
                      borderRadius: '6px',
                      fontSize: '13px',
                    }}>
                      <div style={{ marginBottom: '4px' }}>
                        <span style={{ color: '#64748b' }}>当前: </span>
                        <span style={{ color: '#dc2626', fontWeight: 500 }}>{String(result.current_value)}</span>
                      </div>
                      <div style={{ marginBottom: '4px' }}>
                        <span style={{ color: '#64748b' }}>基准: </span>
                        <span style={{ color: '#059669', fontWeight: 500 }}>{String(result.benchmark_value)}</span>
                      </div>
                      <div>
                        <span style={{ color: '#64748b' }}>建议: </span>
                        <span style={{ color: '#1e293b' }}>{result.suggested_action}</span>
                      </div>
                      {result.expected_impact && (
                        <div style={{ marginTop: '4px', color: '#3b82f6' }}>
                          💡 {result.expected_impact}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </>
      )}

      {/* 搜索词 Tab */}
      {activeTab === 'search-terms' && (
        <SearchTermsTable
          data={stage2Data}
          campaigns={campaigns.filter(c => selectedCampaigns.includes(c.id))}
        />
      )}

      {/* 关键词 Tab */}
      {activeTab === 'keywords' && (
        <KeywordsTable
          data={stage2Data}
          campaigns={campaigns.filter(c => selectedCampaigns.includes(c.id))}
        />
      )}

      {/* 广告 Tab */}
      {activeTab === 'ads' && (
        <AdsPanel
          data={stage2Data}
          campaigns={campaigns.filter(c => selectedCampaigns.includes(c.id))}
        />
      )}

      {/* 设备/地域 Tab */}
      {activeTab === 'devices' && (
        <DeviceLocationPanel
          data={stage2Data}
          campaigns={campaigns.filter(c => selectedCampaigns.includes(c.id))}
        />
      )}

      {/* 空状态 */}
      {!diagnosis && !loading && (
        <div className="dashboard-section" style={{ textAlign: 'center', padding: '60px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>🔍</div>
          <h3 style={{ marginBottom: '8px', color: '#1e293b' }}>运行 Stage 2 诊断</h3>
          <p style={{ color: '#64748b' }}>选择 Campaign 并点击诊断按钮，获取组件级优化建议</p>
        </div>
      )}
    </div>
  );
};
