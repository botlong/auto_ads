import React from 'react';
import type { WorkstreamResult } from '../../api/client';

interface WorkstreamCardProps {
  workstream: WorkstreamResult;
  isActive: boolean;
  onClick: () => void;
}

export const WorkstreamCard: React.FC<WorkstreamCardProps> = ({
  workstream,
  isActive,
  onClick,
}) => {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'P1':
        return '#dc2626';
      case 'P2':
        return '#d97706';
      default:
        return '#059669';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return '✅';
      case 'PARTIAL':
        return '⚠️';
      case 'SKIPPED':
        return '⏭️';
      default:
        return '⏳';
    }
  };

  return (
    <div
      className={`workstream-card ${isActive ? 'active' : ''}`}
      onClick={onClick}
      style={{
        padding: '16px',
        borderRadius: '8px',
        border: isActive ? '2px solid #3b82f6' : '1px solid #e2e8f0',
        background: isActive ? '#f0f9ff' : 'white',
        cursor: 'pointer',
        transition: 'all 0.2s',
      }}
    >
      <div className="workstream-header" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontWeight: 600, fontSize: '14px' }}>
          {getStatusIcon(workstream.status)} {workstream.workstream_id}
        </span>
        <span
          style={{
            padding: '2px 8px',
            borderRadius: '4px',
            background: getPriorityColor(workstream.priority) + '20',
            color: getPriorityColor(workstream.priority),
            fontSize: '11px',
            fontWeight: 600,
          }}
        >
          {workstream.priority}
        </span>
      </div>
      <div className="workstream-name" style={{ fontWeight: 600, marginBottom: '4px' }}>
        {workstream.workstream_name}
      </div>
      <div className="workstream-desc" style={{ fontSize: '12px', color: '#64748b', marginBottom: '12px' }}>
        {workstream.description}
      </div>
      <div className="workstream-stats" style={{ display: 'flex', gap: '12px', fontSize: '12px' }}>
        <span style={{ color: '#dc2626' }}>{workstream.issues_found} 问题</span>
        <span style={{ color: '#3b82f6' }}>{workstream.actions_recommended} 操作</span>
        {workstream.estimated_savings > 0 && (
          <span style={{ color: '#059669' }}>省 ${workstream.estimated_savings.toFixed(0)}</span>
        )}
      </div>
    </div>
  );
};
