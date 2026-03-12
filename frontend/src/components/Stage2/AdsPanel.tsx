import React, { useState } from 'react';
import type { Campaign, Stage2DataResponse } from '../../api/client';

interface AdsPanelProps {
  data: Record<string, Stage2DataResponse>;
  campaigns: Campaign[];
}

export const AdsPanel: React.FC<AdsPanelProps> = ({ data, campaigns }) => {
  const [selectedCampaign, setSelectedCampaign] = useState<string | 'all'>('all');

  const allAds = Object.values(data).flatMap(d => d.ads);
  const filteredAds = selectedCampaign === 'all'
    ? allAds
    : data[selectedCampaign]?.ads || [];

  const disapprovedAds = filteredAds.filter(ad => ad.approval_status === 'DISAPPROVED');
  const poorStrengthAds = filteredAds.filter(ad => ad.ad_strength_rating < 2);
  const goodAds = filteredAds.filter(ad => ad.ad_strength_rating >= 3);

  const getStrengthColor = (rating: number) => {
    if (rating >= 3) return '#059669';
    if (rating >= 2) return '#d97706';
    return '#dc2626';
  };

  const getStrengthLabel = (strength: string) => {
    const labels: Record<string, string> = {
      'EXCELLENT': '极佳',
      'GOOD': '良好',
      'AVERAGE': '一般',
      'POOR': '较差',
    };
    return labels[strength] || strength;
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
            <span className="metrics-card-title">拒登广告</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#dc2626' }}>{disapprovedAds.length}</div>
        </div>
        <div className="metrics-card" style={{ borderLeft: '4px solid #d97706' }}>
          <div className="metrics-card-header">
            <span className="metrics-card-title">强度不足</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#d97706' }}>{poorStrengthAds.length}</div>
        </div>
        <div className="metrics-card" style={{ borderLeft: '4px solid #059669' }}>
          <div className="metrics-card-header">
            <span className="metrics-card-title">优质广告</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#059669' }}>{goodAds.length}</div>
        </div>
        <div className="metrics-card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <div className="metrics-card-header">
            <span className="metrics-card-title">总广告数</span>
          </div>
          <div className="metrics-card-value" style={{ color: '#3b82f6' }}>{filteredAds.length}</div>
        </div>
      </div>

      {/* 拒登广告 */}
      {disapprovedAds.length > 0 && (
        <div className="dashboard-section" style={{ marginBottom: '20px', background: '#fef2f2' }}>
          <h3 className="dashboard-section-title" style={{ color: '#dc2626' }}>
            🚨 拒登广告 ({disapprovedAds.length}) - 需立即处理
          </h3>
          {disapprovedAds.map(ad => (
            <div key={ad.id} style={{ padding: '16px', background: 'white', borderRadius: '8px', marginBottom: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                <span className="severity-badge P0">已拒登</span>
                <span style={{ color: '#64748b', fontSize: '13px' }}>ID: {ad.id}</span>
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>问题:</strong> {ad.issues.join(', ')}
              </div>
              <div style={{ padding: '12px', background: '#f8fafc', borderRadius: '6px' }}>
                <div style={{ fontWeight: 600, marginBottom: '8px' }}>Headlines:</div>
                {ad.headlines.map((h, i) => (
                  <div key={i} style={{ padding: '4px 0' }}>• {h.text}</div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 强度不足广告 */}
      {poorStrengthAds.length > 0 && (
        <div className="dashboard-section" style={{ marginBottom: '20px' }}>
          <h3 className="dashboard-section-title" style={{ color: '#d97706' }}>
            ⚠️ Ad Strength 不足 ({poorStrengthAds.length})
          </h3>
          {poorStrengthAds.map(ad => (
            <div key={ad.id} style={{ padding: '16px', background: '#fffbeb', borderRadius: '8px', marginBottom: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{
                    padding: '4px 12px',
                    borderRadius: '4px',
                    background: getStrengthColor(ad.ad_strength_rating),
                    color: 'white',
                    fontWeight: 600,
                    fontSize: '12px',
                  }}>
                    {getStrengthLabel(ad.ad_strength)} ({ad.ad_strength_rating}/4)
                  </span>
                  <span style={{ color: '#64748b', fontSize: '13px' }}>{ad.campaign_name}</span>
                </div>
              </div>

              <div style={{ marginBottom: '12px' }}>
                <div style={{ fontSize: '13px', color: '#64748b', marginBottom: '4px' }}>
                  Headlines ({ad.headlines.length}/15):
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {ad.headlines.map((h, i) => (
                    <span key={i} style={{
                      padding: '4px 12px',
                      background: h.pinned ? '#dbeafe' : '#f1f5f9',
                      borderRadius: '4px',
                      fontSize: '13px',
                    }}>
                      {h.text} {h.pinned && '📌'}
                    </span>
                  ))}
                </div>
                {ad.headlines.length < 8 && (
                  <div style={{ color: '#dc2626', fontSize: '12px', marginTop: '4px' }}>
                    ⚠️ Headline 数量不足，建议添加至 8-10 个
                  </div>
                )}
              </div>

              <div>
                <div style={{ fontSize: '13px', color: '#64748b', marginBottom: '4px' }}>
                  Descriptions ({ad.descriptions.length}/4):
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {ad.descriptions.map((d, i) => (
                    <span key={i} style={{
                      padding: '4px 12px',
                      background: '#f1f5f9',
                      borderRadius: '4px',
                      fontSize: '13px',
                    }}>
                      {d.text.substring(0, 50)}...
                    </span>
                  ))}
                </div>
                {ad.descriptions.length < 3 && (
                  <div style={{ color: '#dc2626', fontSize: '12px', marginTop: '4px' }}>
                    ⚠️ Description 数量不足，建议添加 3-4 个
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 所有广告 */}
      <div className="dashboard-section">
        <h3 className="dashboard-section-title">📋 所有广告</h3>
        <div style={{ overflowX: 'auto' }}>
          <table className="results-table">
            <thead>
              <tr>
                <th>状态</th>
                <th>Campaign</th>
                <th>Ad Strength</th>
                <th>Headlines</th>
                <th>Descriptions</th>
                <th>CTR</th>
                <th>CVR</th>
              </tr>
            </thead>
            <tbody>
              {filteredAds.map(ad => (
                <tr key={ad.id}>
                  <td>
                    {ad.approval_status === 'APPROVED' ? (
                      <span className="severity-badge OK">已通过</span>
                    ) : (
                      <span className="severity-badge P0">已拒登</span>
                    )}
                  </td>
                  <td>{ad.campaign_name}</td>
                  <td>
                    <span style={{
                      color: getStrengthColor(ad.ad_strength_rating),
                      fontWeight: 600,
                    }}>
                      {getStrengthLabel(ad.ad_strength)}
                    </span>
                  </td>
                  <td>{ad.headlines.length}</td>
                  <td>{ad.descriptions.length}</td>
                  <td>{ad.ctr.toFixed(2)}%</td>
                  <td>{ad.cvr.toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
