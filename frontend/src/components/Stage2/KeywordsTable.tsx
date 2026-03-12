import React, { useState } from 'react';
import type { Campaign, Stage2DataResponse } from '../../api/client';

interface KeywordsTableProps {
  data: Record<string, Stage2DataResponse>;
  campaigns: Campaign[];
}

export const KeywordsTable: React.FC<KeywordsTableProps> = ({ data, campaigns }) => {
  const [selectedCampaign, setSelectedCampaign] = useState<string | 'all'>('all');

  const allKeywords = Object.values(data).flatMap(d => d.keywords);
  const filteredKeywords = selectedCampaign === 'all'
    ? allKeywords
    : data[selectedCampaign]?.keywords || [];

  const underperforming = filteredKeywords.filter(k => k.is_underperforming);
  const lowQS = filteredKeywords.filter(k => k.quality_score < 4);
  const highQS = filteredKeywords.filter(k => k.quality_score >= 7);

  const getQSColor = (qs: number) => {
    if (qs >= 7) return '#059669';
    if (qs >= 4) return '#d97706';
    return '#dc2626';
  };

  const getActionLabel = (action: string | undefined) => {
    const labels: Record<string, string> = {
      'PAUSE': '暂停',
      'REDUCE_BID': '降价',
      'IMPROVE_QS': '优化QS',
      'REFINE_MATCH': '收缩匹配',
    };
    return action ? labels[action] || action : '-';
  };

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
            <span className="metrics-card-title">需优化</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#dc2626' }}>{underperforming.length}</div>
        </div>
        <div className="metrics-card" style={{ borderLeft: '4px solid #d97706' }}>
          <div className="metrics-card-header">
            <span className="metrics-card-title">QS &lt; 4</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#d97706' }}>{lowQS.length}</div>
        </div>
        <div className="metrics-card" style={{ borderLeft: '4px solid #059669' }}>
          <div className="metrics-card-header">
            <span className="metrics-card-title">QS ≥ 7</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#059669' }}>{highQS.length}</div>
        </div>
        <div className="metrics-card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <div className="metrics-card-header">
            <span className="metrics-card-title">总关键词</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#3b82f6' }}>{filteredKeywords.length}</div>
        </div>
      </div>

      {/* 需优化的关键词 */}
      {underperforming.length > 0 && (
        <div className="dashboard-section" style={{ marginBottom: '20px' }}>
          <h3 className="dashboard-section-title" style={{ color: '#dc2626' }}>
            ⚠️ 需优化的关键词 ({underperforming.length})
          </h3>
          <div style={{ overflowX: 'auto' }}>
            <table className="results-table">
              <thead>
                <tr>
                  <th>关键词</th>
                  <th>匹配类型</th>
                  <th>QS</th>
                  <th>花费</th>
                  <th>转化</th>
                  <th>CPA</th>
                  <th>建议操作</th>
                </tr>
              </thead>
              <tbody>
                {underperforming.map(kw => (
                  <tr key={kw.id} style={{ background: '#fef2f2' }}>
                    <td><strong>{kw.text}</strong></td>
                    <td>{kw.match_type}</td>
                    <td style={{ color: getQSColor(kw.quality_score), fontWeight: 700 }}>
                      {kw.quality_score}
                    </td>
                    <td style={{ color: '#dc2626' }}>${kw.cost.toFixed(2)}</td>
                    <td>{kw.conversions}</td>
                    <td>{kw.cpa > 0 ? `$${kw.cpa.toFixed(2)}` : '-'}</td>
                    <td>
                      <span style={{
                        background: kw.action_recommended === 'PAUSE' ? '#fee2e2' : '#ffedd5',
                        color: kw.action_recommended === 'PAUSE' ? '#dc2626' : '#ea580c',
                        padding: '4px 12px',
                        borderRadius: '4px',
                        fontSize: '12px',
                        fontWeight: 600,
                      }}>
                        {getActionLabel(kw.action_recommended)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 质量得分分析 */}
      <div className="dashboard-section">
        <h3 className="dashboard-section-title">📊 质量得分分析</h3>
        <div style={{ overflowX: 'auto' }}>
          <table className="results-table">
            <thead>
              <tr>
                <th>关键词</th>
                <th>Campaign</th>
                <th>QS</th>
                <th>广告相关性</th>
                <th>落地页体验</th>
                <th>预期CTR</th>
                <th>当前出价</th>
                <th>页首出价</th>
              </tr>
            </thead>
            <tbody>
              {filteredKeywords.map(kw => (
                <tr key={kw.id}>
                  <td><strong>{kw.text}</strong></td>
                  <td>{kw.campaign_name}</td>
                  <td style={{ color: getQSColor(kw.quality_score), fontWeight: 700, fontSize: '16px' }}>
                    {kw.quality_score}/10
                  </td>
                  <td>
                    <QSIndicator value={kw.ad_relevance} />
                  </td>
                  <td>
                    <QSIndicator value={kw.lp_experience} />
                  </td>
                  <td>
                    <QSIndicator value={kw.expected_ctr} />
                  </td>
                  <td>${kw.cpc_bid.toFixed(2)}</td>
                  <td>${kw.top_of_page_cpc.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const QSIndicator: React.FC<{ value: string }> = ({ value }) => {
  const colors: Record<string, string> = {
    'ABOVE_AVERAGE': '#059669',
    'AVERAGE': '#d97706',
    'BELOW_AVERAGE': '#dc2626',
  };
  const labels: Record<string, string> = {
    'ABOVE_AVERAGE': '高于平均',
    'AVERAGE': '平均',
    'BELOW_AVERAGE': '低于平均',
  };

  return (
    <span style={{
      color: colors[value] || '#64748b',
      fontWeight: 600,
      fontSize: '12px',
    }}>
      {labels[value] || value}
    </span>
  );
};
