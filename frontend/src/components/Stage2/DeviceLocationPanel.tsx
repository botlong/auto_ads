import React, { useState } from 'react';
import type { Campaign, Stage2DataResponse } from '../../api/client';

interface DeviceLocationPanelProps {
  data: Record<string, Stage2DataResponse>;
  campaigns: Campaign[];
}

export const DeviceLocationPanel: React.FC<DeviceLocationPanelProps> = ({ data, campaigns }) => {
  const [activeTab, setActiveTab] = useState<'devices' | 'locations' | 'hourly'>('devices');
  const [selectedCampaign, setSelectedCampaign] = useState<string>('all');

  const selectedData = selectedCampaign === 'all'
    ? Object.values(data).reduce<{ devices: any[], locations: any[], hourly: any[] }>((acc, d) => ({
        devices: [...acc.devices, ...d.devices],
        locations: [...acc.locations, ...d.locations],
        hourly: [...acc.hourly, ...d.hourly],
      }), { devices: [], locations: [], hourly: [] })
    : data[selectedCampaign] || { devices: [], locations: [], hourly: [] };

  const underperformingDevices = selectedData.devices.filter(d => d.is_underperforming);
  const underperformingLocations = selectedData.locations.filter(l => l.is_underperforming);
  const highPerfHours = selectedData.hourly.filter(h => h.is_high_performance);

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

      {/* 子 Tab */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        {[
          { id: 'devices', label: '📱 设备分析', count: selectedData.devices.length },
          { id: 'locations', label: '🌍 地域分析', count: selectedData.locations.length },
          { id: 'hourly', label: '⏰ 时段分析', count: selectedData.hourly.length },
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
            }}
          >
            {tab.label}
            <span style={{
              marginLeft: '8px',
              background: activeTab === tab.id ? 'rgba(255,255,255,0.3)' : '#e2e8f0',
              padding: '2px 8px',
              borderRadius: '12px',
              fontSize: '12px',
            }}>
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* 设备分析 */}
      {activeTab === 'devices' && (
        <>
          {underperformingDevices.length > 0 && (
            <div className="dashboard-section" style={{ marginBottom: '20px', background: '#fef2f2' }}>
              <h3 className="dashboard-section-title" style={{ color: '#dc2626' }}>
                ⚠️ 低效设备 ({underperformingDevices.length})
              </h3>
              <div style={{ overflowX: 'auto' }}>
                <table className="results-table">
                  <thead>
                    <tr>
                      <th>设备类型</th>
                      <th>花费</th>
                      <th>转化</th>
                      <th>CPA</th>
                      <th>CVR</th>
                      <th>当前出价调整</th>
                      <th>建议</th>
                    </tr>
                  </thead>
                  <tbody>
                    {underperformingDevices.map((device, idx) => (
                      <tr key={idx}>
                        <td><strong>{device.device_type}</strong></td>
                        <td style={{ color: '#dc2626' }}>${device.cost.toFixed(2)}</td>
                        <td>{device.conversions}</td>
                        <td>${device.cpa.toFixed(2)}</td>
                        <td>{device.cvr.toFixed(2)}%</td>
                        <td>{device.bid_modifier}%</td>
                        <td>
                          <span style={{
                            background: '#fee2e2',
                            color: '#dc2626',
                            padding: '4px 12px',
                            borderRadius: '4px',
                            fontSize: '12px',
                            fontWeight: 600,
                          }}>
                            {device.recommended_action === 'REDUCE_BID' ? '降低出价' : '排除'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="dashboard-section">
            <h3 className="dashboard-section-title">📊 设备表现对比</h3>
            <div style={{ overflowX: 'auto' }}>
              <table className="results-table">
                <thead>
                  <tr>
                    <th>设备类型</th>
                    <th>花费</th>
                    <th>点击</th>
                    <th>CTR</th>
                    <th>转化</th>
                    <th>CPA</th>
                    <th>CVR</th>
                    <th>出价调整</th>
                    <th>状态</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedData.devices.map((device, idx) => (
                    <tr key={idx}>
                      <td><strong>{device.device_type}</strong></td>
                      <td>${device.cost.toFixed(2)}</td>
                      <td>{device.clicks}</td>
                      <td>{device.ctr.toFixed(2)}%</td>
                      <td>{device.conversions}</td>
                      <td>${device.cpa.toFixed(2)}</td>
                      <td>{device.cvr.toFixed(2)}%</td>
                      <td>{device.bid_modifier}%</td>
                      <td>
                        {device.is_underperforming ? (
                          <span className="severity-badge P1">低效</span>
                        ) : (
                          <span className="severity-badge OK">正常</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      {/* 地域分析 */}
      {activeTab === 'locations' && (
        <>
          {underperformingLocations.length > 0 && (
            <div className="dashboard-section" style={{ marginBottom: '20px', background: '#fef2f2' }}>
              <h3 className="dashboard-section-title" style={{ color: '#dc2626' }}>
                ⚠️ 低效地域 - 建议排除 ({underperformingLocations.length})
              </h3>
              <div style={{ overflowX: 'auto' }}>
                <table className="results-table">
                  <thead>
                    <tr>
                      <th>地域</th>
                      <th>花费</th>
                      <th>转化</th>
                      <th>CPA</th>
                      <th>ROAS</th>
                      <th>建议</th>
                    </tr>
                  </thead>
                  <tbody>
                    {underperformingLocations.map((loc) => (
                      <tr key={loc.id}>
                        <td><strong>{loc.location_name}</strong></td>
                        <td style={{ color: '#dc2626' }}>${loc.cost.toFixed(2)}</td>
                        <td>{loc.conversions}</td>
                        <td>${loc.cpa.toFixed(2)}</td>
                        <td>{loc.roas.toFixed(2)}x</td>
                        <td>
                          <button className="btn" style={{ background: '#dc2626', color: 'white', fontSize: '12px', padding: '6px 12px' }}>
                            排除
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="dashboard-section">
            <h3 className="dashboard-section-title">📊 所有地域表现</h3>
            <div style={{ overflowX: 'auto' }}>
              <table className="results-table">
                <thead>
                  <tr>
                    <th>地域</th>
                    <th>花费</th>
                    <th>点击</th>
                    <th>CTR</th>
                    <th>转化</th>
                    <th>CPA</th>
                    <th>ROAS</th>
                    <th>出价调整</th>
                    <th>状态</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedData.locations.map((loc) => (
                    <tr key={loc.id}>
                      <td><strong>{loc.location_name}</strong></td>
                      <td>${loc.cost.toFixed(2)}</td>
                      <td>{loc.clicks}</td>
                      <td>{loc.ctr.toFixed(2)}%</td>
                      <td>{loc.conversions}</td>
                      <td>${loc.cpa.toFixed(2)}</td>
                      <td>{loc.roas.toFixed(2)}x</td>
                      <td>{loc.bid_modifier}%</td>
                      <td>
                        {loc.is_underperforming ? (
                          <span className="severity-badge P1">低效</span>
                        ) : loc.is_outperforming ? (
                          <span className="severity-badge OK">高效</span>
                        ) : (
                          <span style={{ color: '#94a3b8' }}>-</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      {/* 时段分析 */}
      {activeTab === 'hourly' && (
        <>
          {highPerfHours.length > 0 && (
            <div className="dashboard-section" style={{ marginBottom: '20px', background: '#f0fdf4' }}>
              <h3 className="dashboard-section-title" style={{ color: '#059669' }}>
                ✅ 高效时段 - 建议提高出价 ({highPerfHours.length})
              </h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {highPerfHours.slice(0, 20).map((h, idx) => (
                  <span key={idx} style={{
                    padding: '6px 12px',
                    background: '#d1fae5',
                    borderRadius: '4px',
                    fontSize: '13px',
                    fontWeight: 500,
                  }}>
                    {['周一', '周二', '周三', '周四', '周五', '周六', '周日'][h.day_of_week]} {h.hour_of_day}:00
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="dashboard-section">
            <h3 className="dashboard-section-title">📊 24小时表现热力图</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(24, 1fr)', gap: '2px', fontSize: '10px' }}>
              {Array.from({ length: 7 }).map((_, day) => (
                <React.Fragment key={day}>
                  {Array.from({ length: 24 }).map((_, hour) => {
                    const hourData = selectedData.hourly.find(h => h.day_of_week === day && h.hour_of_day === hour);
                    const isHighPerf = hourData?.is_high_performance;
                    const isLowPerf = hourData?.is_low_performance;
                    return (
                      <div
                        key={`${day}-${hour}`}
                        style={{
                          aspectRatio: '1',
                          background: isHighPerf ? '#10b981' : isLowPerf ? '#ef4444' : hourData ? '#fbbf24' : '#e2e8f0',
                          borderRadius: '2px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                          fontWeight: 600,
                        }}
                        title={`${['周一', '周二', '周三', '周四', '周五', '周六', '周日'][day]} ${hour}:00`}
                      >
                        {hourData && (hourData.cvr > 0 ? hourData.cvr.toFixed(0) : '-')}
                      </div>
                    );
                  })}
                </React.Fragment>
              ))}
            </div>
            <div style={{ display: 'flex', gap: '16px', marginTop: '12px', fontSize: '13px' }}>
              <span><span style={{ display: 'inline-block', width: '12px', height: '12px', background: '#10b981', borderRadius: '2px', marginRight: '4px' }}></span>高效</span>
              <span><span style={{ display: 'inline-block', width: '12px', height: '12px', background: '#fbbf24', borderRadius: '2px', marginRight: '4px' }}></span>一般</span>
              <span><span style={{ display: 'inline-block', width: '12px', height: '12px', background: '#ef4444', borderRadius: '2px', marginRight: '4px' }}></span>低效</span>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
