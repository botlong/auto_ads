import React from 'react';
import type { FeedABTest } from '../../api/client';

interface FeedTestPanelProps {
  tests: FeedABTest[];
}

export const FeedTestPanel: React.FC<FeedTestPanelProps> = ({ tests }) => {
  const getElementLabel = (type: string) => {
    const labels: Record<string, string> = {
      'TITLE': '标题',
      'IMAGE': '图片',
      'DESCRIPTION': '描述',
      'PRICE': '价格',
    };
    return labels[type] || type;
  };

  return (
    <div className="panel-content">
      <h4>🛍️ Feed 元素 A/B 测试 (S083)</h4>
      <p className="panel-description">
        电商商品 Feed 元素优化测试
      </p>

      {tests.length > 0 ? (
        <div className="feed-test-list">
          {tests.map((test, idx) => (
            <div key={idx} className="feed-test-card">
              <div className="feed-test-header">
                <div className="feed-product-info">
                  <h5>{test.product_name}</h5>
                  <span className="element-type">{getElementLabel(test.element_type)}</span>
                </div>
                {test.winner && (
                  <div className="winner-badge">
                    🏆 胜出版本: {test.winner}
                  </div>
                )}
              </div>

              <div className="variant-comparison">
                <div className="variant-box">
                  <div className="variant-title">版本 A</div>
                  <div className="variant-content">{test.variant_a}</div>
                  <div className="variant-stats">
                    <div>展示: {test.variant_a_impressions.toLocaleString()}</div>
                    <div>点击: {test.variant_a_clicks}</div>
                    <div>转化: {test.variant_a_conversions}</div>
                    <div>CTR: {test.variant_a_ctr}%</div>
                  </div>
                </div>

                <div className="vs-indicator">VS</div>

                <div className="variant-box winner">
                  <div className="variant-title">版本 B</div>
                  <div className="variant-content">{test.variant_b}</div>
                  <div className="variant-stats">
                    <div>展示: {test.variant_b_impressions.toLocaleString()}</div>
                    <div>点击: {test.variant_b_clicks}</div>
                    <div>转化: {test.variant_b_conversions}</div>
                    <div>CTR: {test.variant_b_ctr}%</div>
                  </div>
                </div>
              </div>

              {test.lift_percentage > 0 && (
                <div className="lift-indicator">
                  提升幅度: <strong>+{test.lift_percentage}%</strong>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">暂无 Feed A/B 测试数据</div>
      )}
    </div>
  );
};
