import React, { useState } from 'react';
import type { Campaign, Stage2DataResponse } from '../../api/client';

interface SearchTermsTableProps {
  data: Record<string, Stage2DataResponse>;
  campaigns: Campaign[];
}

export const SearchTermsTable: React.FC<SearchTermsTableProps> = ({ data, campaigns }) => {
  const [selectedCampaign, setSelectedCampaign] = useState<string | 'all'>('all');

  const allSearchTerms = Object.values(data).flatMap(d => d.search_terms);
  const filteredTerms = selectedCampaign === 'all'
    ? allSearchTerms
    : data[selectedCampaign]?.search_terms || [];

  const negativeCandidates = filteredTerms.filter(t => t.is_negative_candidate);
  const highIntentTerms = filteredTerms.filter(t => t.is_high_intent);

  return (
    <div>
      {/* Campaign 筛选 */}
      <div className="dashboard-section">
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <button
            onClick={() => setSelectedCampaign('all')}
            style={{
              padding: '8px 16px',
              borderRadius: '20px',
              border: 'none',
              background: selectedCampaign === 'all' ? '#3b82f6' : '#e2e8f0',
              color: selectedCampaign === 'all' ? 'white' : '#64748b',
              cursor: 'pointer',
              fontWeight: 600,
            }}
          >
            全部 Campaign
          </button>
          {campaigns.map(c => (
            <button
              key={c.id}
              onClick={() => setSelectedCampaign(c.id)}
              style={{
                padding: '8px 16px',
                borderRadius: '20px',
                border: 'none',
                background: selectedCampaign === c.id ? '#3b82f6' : '#e2e8f0',
                color: selectedCampaign === c.id ? 'white' : '#64748b',
                cursor: 'pointer',
                fontWeight: 600,
              }}
            >
              {c.name}
            </button>
          ))}
        </div>
      </div>

      {/* 统计摘要 */}
      <div className="metrics-grid" style={{ marginBottom: '20px' }}>
        <div className="metrics-card" style={{ borderLeft: '4px solid #dc2626' }}>
          <div className="metrics-card-header">
            <span className="metrics-card-title">需添加负向</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#dc2626' }}>{negativeCandidates.length}</div>
        </div>
        <div className="metrics-card" style={{ borderLeft: '4px solid #059669' }}>
          <div className="metrics-card-header">
            <span className="metrics-card-title">高意图词</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#059669' }}>{highIntentTerms.length}</div>
        </div>
        <div className="metrics-card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <div className="metrics-card-header">
            <span className="metrics-card-title">总搜索词</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#3b82f6' }}>{filteredTerms.length}</div>
        </div>
      </div>

      {/* 需添加负向词 */}
      {negativeCandidates.length > 0 && (
        <div className="dashboard-section" style={{ marginBottom: '20px' }}>
          <h3 className="dashboard-section-title" style={{ color: '#dc2626' }}>
            ⚠️ 建议添加负向词 ({negativeCandidates.length})
          </h3>
          <div style={{ overflowX: 'auto' }}>
            <table className="results-table">
              <thead>
                <tr>
                  <th>搜索词</th>
                  <th>Campaign</th>
                  <th>花费</th>
                  <th>点击</th>
                  <th>转化</th>
                  <th>匹配类型</th>
                  <th>原因</th>
                  <th>建议操作</th>
                </tr>
              </thead>
              <tbody>
                {negativeCandidates.map(term => (
                  <tr key={term.id} style={{ background: '#fef2f2' }}>
                    <td><code style={{ background: '#fee2e2', padding: '2px 6px', borderRadius: '4px' }}>{term.search_term}</code></td>
                    <td>{term.campaign_name}</td>
                    <td style={{ color: '#dc2626', fontWeight: 600 }}>${term.cost.toFixed(2)}</td>
                    <td>{term.clicks}</td>
                    <td>{term.conversions}</td>
                    <td>{term.match_type}</td>
                    <td style={{ fontSize: '13px', maxWidth: '300px' }}>{term.negative_reason}</td>
                    <td>
                      <button className="btn" style={{ background: '#dc2626', color: 'white', fontSize: '12px', padding: '6px 12px' }}>
                        添加负向
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 高意图词 */}
      {highIntentTerms.length > 0 && (
        <div className="dashboard-section" style={{ marginBottom: '20px' }}>
          <h3 className="dashboard-section-title" style={{ color: '#059669' }}>
            ✅ 高意图词 - 建议提炼为精确匹配 ({highIntentTerms.length})
          </h3>
          <div style={{ overflowX: 'auto' }}>
            <table className="results-table">
              <thead>
                <tr>
                  <th>搜索词</th>
                  <th>Campaign</th>
                  <th>花费</th>
                  <th>转化</th>
                  <th>CPA</th>
                  <th>匹配类型</th>
                  <th>建议</th>
                </tr>
              </thead>
              <tbody>
                {highIntentTerms.map(term => (
                  <tr key={term.id} style={{ background: '#f0fdf4' }}>
                    <td><code style={{ background: '#d1fae5', padding: '2px 6px', borderRadius: '4px' }}>{term.search_term}</code></td>
                    <td>{term.campaign_name}</td>
                    <td>${term.cost.toFixed(2)}</td>
                    <td style={{ color: '#059669', fontWeight: 600 }}>{term.conversions}</td>
                    <td style={{ color: '#059669' }}>${term.cpa.toFixed(2)}</td>
                    <td>{term.match_type}</td>
                    <td>
                      <button className="btn" style={{ background: '#059669', color: 'white', fontSize: '12px', padding: '6px 12px' }}>
                        添加 Exact: [{term.search_term}]
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 所有搜索词 */}
      <div className="dashboard-section">
        <h3 className="dashboard-section-title">📋 所有搜索词</h3>
        <div style={{ overflowX: 'auto' }}>
          <table className="results-table">
            <thead>
              <tr>
                <th>搜索词</th>
                <th>Campaign</th>
                <th>花费</th>
                <th>点击</th>
                <th>CTR</th>
                <th>转化</th>
                <th>CPA</th>
                <th>匹配类型</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              {filteredTerms.map(term => (
                <tr key={term.id}>
                  <td>{term.search_term}</td>
                  <td>{term.campaign_name}</td>
                  <td>${term.cost.toFixed(2)}</td>
                  <td>{term.clicks}</td>
                  <td>{term.ctr.toFixed(2)}%</td>
                  <td>{term.conversions}</td>
                  <td>{term.cpa > 0 ? `$${term.cpa.toFixed(2)}` : '-'}</td>
                  <td>{term.match_type}</td>
                  <td>
                    {term.is_negative_candidate && (
                      <span className="severity-badge P1">需负向</span>
                    )}
                    {term.is_high_intent && (
                      <span className="severity-badge OK">高意图</span>
                    )}
                    {!term.is_negative_candidate && !term.is_high_intent && (
                      <span style={{ color: '#94a3b8' }}>-</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
