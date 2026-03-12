import React, { useState } from 'react';
import type { Campaign, DiagnosisResult } from '../../api/client';

interface CampaignDetailProps {
  campaign: Campaign;
  results: DiagnosisResult[];
}

const getSeverityColor = (severity: string) => {
  switch (severity) {
    case 'P0': return '#dc2626';
    case 'P1': return '#ea580c';
    case 'P2': return '#d97706';
    case 'OK': return '#059669';
    default: return '#64748b';
  }
};

const getStatusBadge = (status: string) => {
  const colors: Record<string, string> = {
    'ENABLED': '#22c55e',
    'PAUSED': '#f59e0b',
    'REMOVED': '#ef4444',
    'LEARNING': '#3b82f6',
    'READY': '#22c55e',
    'MISCONFIGURED': '#dc2626',
  };
  return colors[status] || '#64748b';
};

export const CampaignDetail: React.FC<CampaignDetailProps> = ({ campaign, results }) => {
  const [expanded, setExpanded] = useState(false);

  // 只显示与该 Campaign 相关的结果
  const campaignResults = results.filter(r =>
    r.affected_object.includes(campaign.name) ||
    r.affected_object === 'Account'
  );

  const issues = campaignResults.filter(r => r.severity !== 'OK');

  return (
    <div style={{
      border: '1px solid #e2e8f0',
      borderRadius: '12px',
      marginBottom: '16px',
      overflow: 'hidden'
    }}>
      {/* Campaign Header */}
      <div
        style={{
          padding: '16px 20px',
          background: issues.length > 0 ? '#fef2f2' : '#f0fdf4',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: getStatusBadge(campaign.status)
          }} />
          <div>
            <div style={{ fontWeight: 600, fontSize: '16px', color: '#1e293b' }}>
              {campaign.name}
            </div>
            <div style={{ fontSize: '13px', color: '#64748b', marginTop: '4px' }}>
              ID: {campaign.id} | {campaign.business_type} | {campaign.bidding_strategy_type}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          {/* 关键指标摘要 */}
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '12px', color: '#64748b' }}>花费</div>
            <div style={{ fontWeight: 600, color: '#1e293b' }}>${campaign.cost.toLocaleString()}</div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '12px', color: '#64748b' }}>转化</div>
            <div style={{ fontWeight: 600, color: '#1e293b' }}>{campaign.conversions}</div>
          </div>
          {campaign.actual_cpa > 0 && (
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '12px', color: '#64748b' }}>CPA</div>
              <div style={{
                fontWeight: 600,
                color: campaign.target_cpa && campaign.actual_cpa > campaign.target_cpa * 1.2
                  ? '#dc2626'
                  : '#059669'
              }}>
                ${campaign.actual_cpa.toFixed(2)}
                {campaign.target_cpa && (
                  <span style={{ fontSize: '11px', color: '#94a3b8', marginLeft: '4px' }}>
                    / ${campaign.target_cpa}
                  </span>
                )}
              </div>
            </div>
          )}
          {campaign.actual_roas > 0 && (
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '12px', color: '#64748b' }}>ROAS</div>
              <div style={{
                fontWeight: 600,
                color: campaign.target_roas && campaign.actual_roas < campaign.target_roas * 0.8
                  ? '#dc2626'
                  : '#059669'
              }}>
                {campaign.actual_roas.toFixed(2)}x
                {campaign.target_roas && (
                  <span style={{ fontSize: '11px', color: '#94a3b8', marginLeft: '4px' }}>
                    / {campaign.target_roas}x
                  </span>
                )}
              </div>
            </div>
          )}

          {/* 问题统计 */}
          {issues.length > 0 ? (
            <div style={{
              background: '#dc2626',
              color: 'white',
              padding: '4px 12px',
              borderRadius: '20px',
              fontSize: '13px',
              fontWeight: 600
            }}>
              {issues.length} 个问题
            </div>
          ) : (
            <div style={{
              background: '#059669',
              color: 'white',
              padding: '4px 12px',
              borderRadius: '20px',
              fontSize: '13px',
              fontWeight: 600
            }}>
              正常
            </div>
          )}

          <span style={{ fontSize: '20px', transform: expanded ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}>
            ▼
          </span>
        </div>
      </div>

      {/* 展开的详细内容 */}
      {expanded && (
        <div style={{ padding: '20px', background: 'white' }}>
          {/* 详细指标卡片 */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
            gap: '16px',
            marginBottom: '20px',
            padding: '16px',
            background: '#f8fafc',
            borderRadius: '8px'
          }}>
            <div>
              <div style={{ fontSize: '12px', color: '#64748b', marginBottom: '4px' }}>日预算</div>
              <div style={{ fontSize: '18px', fontWeight: 600 }}>${campaign.budget}</div>
              <div style={{ fontSize: '12px', color: '#64748b' }}>
                使用率: {((campaign.cost / campaign.budget) * 100).toFixed(1)}%
              </div>
            </div>
            <div>
              <div style={{ fontSize: '12px', color: '#64748b', marginBottom: '4px' }}>展示份额</div>
              <div style={{ fontSize: '18px', fontWeight: 600 }}>{campaign.search_impression_share.toFixed(1)}%</div>
              <div style={{ fontSize: '12px', color: '#64748b' }}>
                预算丢失: {campaign.search_budget_lost_impression_share.toFixed(1)}%
              </div>
            </div>
            <div>
              <div style={{ fontSize: '12px', color: '#64748b', marginBottom: '4px' }}>CTR</div>
              <div style={{ fontSize: '18px', fontWeight: 600 }}>{campaign.ctr.toFixed(2)}%</div>
              <div style={{ fontSize: '12px', color: '#64748b' }}>
                点击: {campaign.clicks.toLocaleString()}
              </div>
            </div>
            <div>
              <div style={{ fontSize: '12px', color: '#64748b', marginBottom: '4px' }}>CVR</div>
              <div style={{ fontSize: '18px', fontWeight: 600 }}>{campaign.cvr.toFixed(2)}%</div>
              <div style={{ fontSize: '12px', color: '#64748b' }}>
                CPC: ${campaign.cpc.toFixed(2)}
              </div>
            </div>
            <div>
              <div style={{ fontSize: '12px', color: '#64748b', marginBottom: '4px' }}>学习状态</div>
              <div style={{
                fontSize: '18px',
                fontWeight: 600,
                color: getStatusBadge(campaign.learning_status)
              }}>
                {campaign.learning_status}
              </div>
              <div style={{ fontSize: '12px', color: '#64748b' }}>
                上线: {campaign.days_since_created} 天
              </div>
            </div>
            <div>
              <div style={{ fontSize: '12px', color: '#64748b', marginBottom: '4px' }}>网络类型</div>
              <div style={{ fontSize: '18px', fontWeight: 600 }}>{campaign.network_type}</div>
              <div style={{ fontSize: '12px', color: '#64748b' }}>
                AdGroups: {campaign.adgroup_count}
              </div>
            </div>
          </div>

          {/* 诊断结果 */}
          <h4 style={{ fontSize: '14px', fontWeight: 600, marginBottom: '12px', color: '#1e293b' }}>
            诊断结果 ({campaignResults.length} 项)
          </h4>

          {campaignResults.map((result, idx) => (
            <div
              key={idx}
              style={{
                padding: '12px 16px',
                marginBottom: '8px',
                borderRadius: '8px',
                background: result.severity === 'OK' ? '#f0fdf4' : '#fef2f2',
                borderLeft: `4px solid ${getSeverityColor(result.severity)}`
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                    <span style={{
                      fontSize: '11px',
                      fontWeight: 600,
                      padding: '2px 8px',
                      borderRadius: '4px',
                      background: getSeverityColor(result.severity),
                      color: 'white'
                    }}>
                      {result.severity}
                    </span>
                    <span style={{ fontWeight: 600, color: '#1e293b' }}>{result.strategy_id}</span>
                    <span style={{ color: '#64748b' }}>{result.strategy_name}</span>
                  </div>
                  <div style={{ fontSize: '14px', color: '#1e293b', marginTop: '8px' }}>
                    {result.issue_type}
                  </div>
                  {result.severity !== 'OK' && (
                    <div style={{ marginTop: '8px', padding: '8px', background: 'rgba(0,0,0,0.03)', borderRadius: '4px' }}>
                      <div style={{ fontSize: '13px', marginBottom: '4px' }}>
                        <span style={{ color: '#64748b' }}>当前: </span>
                        <span style={{ color: '#dc2626', fontWeight: 500 }}>{String(result.current_value)}</span>
                      </div>
                      <div style={{ fontSize: '13px', marginBottom: '8px' }}>
                        <span style={{ color: '#64748b' }}>基准: </span>
                        <span style={{ color: '#059669', fontWeight: 500 }}>{String(result.benchmark_value)}</span>
                      </div>
                      <div style={{ fontSize: '13px', color: '#1e293b' }}>
                        <span style={{ color: '#64748b' }}>建议: </span>
                        {result.suggested_action}
                      </div>
                      {result.expected_impact && (
                        <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>
                          💡 {result.expected_impact}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
