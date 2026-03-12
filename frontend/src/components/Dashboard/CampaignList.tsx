import React from 'react';
import type { Campaign } from '../../api/client';
import './CampaignList.css';

interface CampaignListProps {
  campaigns: Campaign[];
  selectedIds: string[];
  onSelect: (id: string) => void;
  onSelectAll: () => void;
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'ENABLED': return '#22c55e';
    case 'PAUSED': return '#f59e0b';
    case 'REMOVED': return '#ef4444';
    default: return '#94a3b8';
  }
};

const getBiddingLabel = (type: string) => {
  const labels: Record<string, string> = {
    'TARGET_CPA': 'tCPA',
    'TARGET_ROAS': 'tROAS',
    'MAXIMIZE_CONVERSIONS': 'Max Conv',
    'MAXIMIZE_CONVERSION_VALUE': 'Max Value',
    'MANUAL_CPC': 'Manual',
  };
  return labels[type] || type;
};

export const CampaignList: React.FC<CampaignListProps> = ({
  campaigns,
  selectedIds,
  onSelect,
  onSelectAll,
}) => {
  const allSelected = campaigns.length > 0 && selectedIds.length === campaigns.length;

  return (
    <div className="campaign-list">
      <div className="campaign-list-header">
        <label className="campaign-checkbox">
          <input
            type="checkbox"
            checked={allSelected}
            onChange={onSelectAll}
          />
          <span>全选 ({selectedIds.length}/{campaigns.length})</span>
        </label>
      </div>
      <div className="campaign-chips">
        {campaigns.map((campaign) => (
          <div
            key={campaign.id}
            className={`campaign-chip ${selectedIds.includes(campaign.id) ? 'selected' : ''}`}
            onClick={() => onSelect(campaign.id)}
          >
            <span
              className="status-dot"
              style={{ backgroundColor: getStatusColor(campaign.status) }}
            />
            <span className="campaign-name">{campaign.name}</span>
            <span className="bidding-type">{getBiddingLabel(campaign.bidding_strategy_type)}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
