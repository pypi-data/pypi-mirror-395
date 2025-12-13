// Header.tsx
import React from 'react';
import { HeaderProps } from './types';

export const Header: React.FC<HeaderProps> = ({ 
  modelName, 
  isLoading, 
  onStop, 
  onClear,
  onToggleConfig,
  isConfigVisible 
}) => {
  return (
    <div style={{
      background: 'var(--jp-brand-color1)',
      color: 'white',
      padding: '8px 12px',
      display: 'flex',
      alignItems: 'center',
      borderBottom: '1px solid var(--jp-border-color1)',
      justifyContent: 'space-between'
    }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <span style={{ fontWeight: 'bold', fontSize: '14px', marginRight: '8px' }}>
          🤖 AI 聊天 (流式输出)
        </span>
        <div style={{ 
          background: 'rgba(255,255,255,0.2)',
          padding: '2px 6px',
          borderRadius: '8px',
          fontSize: '11px',
        }}>
          {modelName}
        </div>
      </div>
      <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
        {/* 配置面板切换按钮 */}
        <button
          onClick={onToggleConfig}
          style={{
            background: isConfigVisible ? 'rgba(255,255,255,0.3)' : 'transparent',
            border: '1px solid rgba(255,255,255,0.3)',
            color: 'white',
            borderRadius: '4px',
            padding: '2px 6px',
            fontSize: '11px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '4px'
          }}
          title={isConfigVisible ? '隐藏配置' : '显示配置'}
        >
          <span style={{ fontSize: '10px' }}>
            {isConfigVisible ? '▲' : '▼'}
          </span>
          配置
        </button>
        
        {isLoading && (
          <button
            onClick={onStop}
            style={{
              background: 'rgba(255,255,255,0.2)',
              border: '1px solid rgba(255,255,255,0.3)',
              color: 'white',
              borderRadius: '4px',
              padding: '2px 6px',
              fontSize: '11px',
              cursor: 'pointer'
            }}
            title="停止生成"
          >
            停止
          </button>
        )}
        <button
          onClick={onClear}
          style={{
            background: 'transparent',
            border: '1px solid rgba(255,255,255,0.3)',
            color: 'white',
            borderRadius: '4px',
            padding: '2px 6px',
            fontSize: '11px',
            cursor: 'pointer'
          }}
          title="清空对话"
        >
          清空
        </button>
      </div>
    </div>
  );
};