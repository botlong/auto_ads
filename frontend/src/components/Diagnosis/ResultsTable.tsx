import React, { useState } from 'react';
import type { Campaign, DiagnosisResult } from '../../api/client';
import { CampaignDetail } from './CampaignDetail';

interface ResultsTableProps {
  results: DiagnosisResult[];
  campaigns: Campaign[];
}

export const ResultsTable: React.FC<ResultsTableProps> = ({ results, campaigns }) => {
  const [viewMode, setViewMode] = useState<'campaign' | 'table'>('campaign');

  // 按严重程度和策略ID排序
  const sortedResults = [...results].sort((a, b) => {
    const severityOrder = { 'P0': 0, 'P1': 1, 'P2': 2, 'OK': 3 };
    return severityOrder[a.severity] - severityOrder[b.severity];
  });

  // 按策略分组统计
  const strategyGroups = sortedResults.reduce((acc, result) => {
    if (!acc[result.strategy_id]) {
      acc[result.strategy_id] = {
        name: result.strategy_name,
        results: [],
      };
    }
    acc[result.strategy_id].results.push(result);
    return acc;
  }, {} as Record<string, { name: string; results: DiagnosisResult[] }>);

  // 获取有问题的Campaign
  const campaignsWithIssues = campaigns.filter(c =>
    results.some(r =>
      r.affected_object.includes(c.name) && r.severity !== 'OK'
    )
  );

  return (
    <div className="dashboard-section">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h3 className="dashboard-section-title" style={{ marginBottom: 0 }}>
          📊 Stage 1 诊断详情
          <span style={{ fontSize: '14px', fontWeight: 'normal', color: '#64748b', marginLeft: '12px' }}>
            共 {results.length} 项检查结果
          </span>
        </h3>

        {/* 视图切换 */}
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={() => setViewMode('campaign')}
            style={{
              padding: '8px 16px',
              borderRadius: '6px',
              border: 'none',
              background: viewMode === 'campaign' ? '#3b82f6' : '#e2e8f0',
              color: viewMode === 'campaign' ? 'white' : '#64748b',
              cursor: 'pointer',
              fontWeight: 500,
            }}
          >
            按 Campaign 查看
          </button>
          <button
            onClick={() => setViewMode('table')}
            style={{
              padding: '8px 16px',
              borderRadius: '6px',
              border: 'none',
              background: viewMode === 'table' ? '#3b82f6' : '#e2e8f0',
              color: viewMode === 'table' ? 'white' : '#64748b',
              cursor: 'pointer',
              fontWeight: 500,
            }}
          >
            表格视图
          </button>
        </div>
      </div>

      {/* 策略分组统计 */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', marginBottom: '20px' }}>
        {Object.entries(strategyGroups).map(([id, group]) => {
          const issues = group.results.filter(r => r.severity !== 'OK');
          const okCount = group.results.filter(r => r.severity === 'OK').length;
          return (
            <div
              key={id}
              style={{
                padding: '8px 16px',
                borderRadius: '8px',
                background: issues.length > 0 ? '#fef3c7' : '#d1fae5',
                border: `1px solid ${issues.length > 0 ? '#fde68a' : '#a7f3d0'}`,
                fontSize: '13px',
              }}
            >
              <strong>{id}</strong>: {group.name}
              {issues.length > 0 ? (
                <span style={{ color: '#d97706', marginLeft: '8px' }}>
                  ({issues.length} 问题)
                </span>
              ) : (
                <span style={{ color: '#059669', marginLeft: '8px' }}>
                  ({okCount} 正常)
                </span>
              )}
            </div>
          );
        })}
      </div>

      {/* Campaign 视图 */}
      {viewMode === 'campaign' && (
        <div>
          {/* 有问题的 Campaign */}
          {campaignsWithIssues.length > 0 && (
            <div style={{ marginBottom: '24px' }}>
              <h4 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '12px', color: '#dc2626' }}>
                ⚠️ 需要关注的 Campaign ({campaignsWithIssues.length})
              </h4>
              {campaignsWithIssues.map(campaign => (
                <CampaignDetail
                  key={campaign.id}
                  campaign={campaign}
                  results={results}
                />
              ))}
            </div>
          )}

          {/* 正常的 Campaign */}
          {campaigns.filter(c => !campaignsWithIssues.find(ci => ci.id === c.id)).length > 0 && (
            <div>
              <h4 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '12px', color: '#059669' }}>
                ✅ 运行正常的 Campaign ({campaigns.filter(c => !campaignsWithIssues.find(ci => ci.id === c.id)).length})
              </h4>
              {campaigns
                .filter(c => !campaignsWithIssues.find(ci => ci.id === c.id))
                .map(campaign => (
                  <CampaignDetail
                    key={campaign.id}
                    campaign={campaign}
                    results={results}
                  />
                ))}
            </div>
          )}
        </div>
      )}

      {/* 表格视图 */}
      {viewMode === 'table' && (
        <div style={{ overflowX: 'auto' }}>
          <table className="results-table">
            <thead>
              <tr>
                <th>策略</th>
                <th>严重程度</th>
                <th>问题类型</th>
                <th>影响对象</th>
                <th>当前值</th>
                <th>基准值</th>
                <th>建议操作</th>
              </tr>
            </thead>
            <tbody>
              {sortedResults.map((result, index) => (
                <tr key={index}>
                  <td>
                    <div style={{ fontWeight: 600 }}>{result.strategy_id}</div>
                    <div style={{ fontSize: '12px', color: '#64748b' }}>
                      {result.strategy_name.length > 20
                        ? result.strategy_name.substring(0, 20) + '...'
                        : result.strategy_name}
                    </div>
                  </td>
                  <td>
                    <span className={`severity-badge ${result.severity}`}>
                      {result.severity}
                    </span>
                  </td>
                  <td>{result.issue_type}</td>
                  <td style={{ maxWidth: '200px', fontSize: '13px' }}>
                    {result.affected_object}
                  </td>
                  <td style={{ color: '#dc2626', fontWeight: 500 }}>
                    {String(result.current_value)}
                  </td>
                  <td style={{ color: '#059669' }}>
                    {String(result.benchmark_value)}
                  </td>
                  <td style={{ maxWidth: '300px', fontSize: '13px' }}>
                    <div>{result.suggested_action}</div>
                    {result.expected_impact && (
                      <div style={{ color: '#64748b', marginTop: '4px', fontSize: '12px' }}>
                        💡 {result.expected_impact}
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
