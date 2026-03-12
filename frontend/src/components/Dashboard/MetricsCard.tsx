import React from 'react';
import './Dashboard.css';

interface MetricsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  icon?: string;
  color?: 'blue' | 'green' | 'orange' | 'red' | 'purple';
}

const colorMap = {
  blue: { bg: '#e3f2fd', text: '#1976d2' },
  green: { bg: '#e8f5e9', text: '#388e3c' },
  orange: { bg: '#fff3e0', text: '#f57c00' },
  red: { bg: '#ffebee', text: '#d32f2f' },
  purple: { bg: '#f3e5f5', text: '#7b1fa2' },
};

export const MetricsCard: React.FC<MetricsCardProps> = ({
  title,
  value,
  subtitle,
  trend,
  trendValue,
  color = 'blue',
}) => {
  const colors = colorMap[color];

  return (
    <div className="metrics-card" style={{ borderLeft: `4px solid ${colors.text}` }}>
      <div className="metrics-card-header">
        <span className="metrics-card-title">{title}</span>
        <div
          className="metrics-card-icon"
          style={{ backgroundColor: colors.bg, color: colors.text }}
        >
          {title.charAt(0)}
        </div>
      </div>
      <div className="metrics-card-value" style={{ color: colors.text }}>
        {value}
      </div>
      {subtitle && <div className="metrics-card-subtitle">{subtitle}</div>}
      {trend && (
        <div className={`metrics-card-trend ${trend}`}>
          {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'} {trendValue}
        </div>
      )}
    </div>
  );
};
