// InputArea.tsx
import React from 'react';
import { InputAreaProps } from './types';

export const InputArea: React.FC<InputAreaProps> = ({
  value,
  isLoading,
  modelName,
  temperature,
  maxTokens,
  onChange,
  onSend,
  onKeyPress
}) => {
  return (
    <div style={{
      borderTop: '1px solid var(--jp-border-color1)',
      padding: '10px',
      background: 'var(--jp-layout-color1)'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'flex-end',
        gap: '6px'
      }}>
        <textarea
          style={{
            flex: 1,
            minHeight: '36px',
            maxHeight: '100px',
            padding: '6px 10px',
            border: '1px solid var(--jp-border-color1)',
            borderRadius: '4px',
            background: 'var(--jp-input-background)',
            color: 'var(--jp-ui-font-color1)',
            fontFamily: 'inherit',
            fontSize: '13px',
            resize: 'vertical',
            outline: 'none'
          }}
          placeholder="输入你的问题..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyPress={onKeyPress}
          disabled={isLoading}
          rows={1}
        />
        <button
          style={{
            background: value.trim() && !isLoading 
              ? 'var(--jp-brand-color1)' 
              : 'var(--jp-layout-color3)',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            padding: '6px 12px',
            cursor: value.trim() && !isLoading ? 'pointer' : 'not-allowed',
            height: '36px',
            fontSize: '12px',
            fontWeight: 'bold'
          }}
          onClick={onSend}
          disabled={!value.trim() || isLoading}
        >
          {isLoading ? '生成中...' : '发送'}
        </button>
      </div>
      <div style={{
        fontSize: '10px',
        color: 'var(--jp-ui-font-color2)',
        marginTop: '4px',
        textAlign: 'center'
      }}>
        流式输出 | 模型: {modelName} | 温度: {temperature} | 最大长度: {maxTokens}
      </div>
    </div>
  );
};