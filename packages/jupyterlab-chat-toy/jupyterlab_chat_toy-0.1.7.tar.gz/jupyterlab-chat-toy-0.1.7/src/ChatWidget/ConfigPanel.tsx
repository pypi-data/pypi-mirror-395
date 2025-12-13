// ConfigPanel.tsx
import React from 'react';
import { ConfigPanelProps, ModelOption } from './types';

export const ConfigPanel: React.FC<ConfigPanelProps> = ({ 
  config, 
  modelOptions, 
  onConfigChange, 
  onReset,
  isVisible,
  onToggleVisibility 
}) => {
  const handleBackendUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onConfigChange({ backendUrl: e.target.value });
  };

  const handleModelNameChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onConfigChange({ modelName: e.target.value });
  };

  const handleCustomModelNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onConfigChange({ customModelName: e.target.value });
  };

  const handleTemperatureChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onConfigChange({ temperature: parseFloat(e.target.value) });
  };

  const handleMaxTokensChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onConfigChange({ maxTokens: parseInt(e.target.value, 10) });
  };

  const getActualModelName = () => {
    return config.modelName === 'custom' ? config.customModelName : config.modelName;
  };

  // 如果没有显示，只显示一个最小化的面板
  if (!isVisible) {
    return (
      <div style={{
        padding: '4px 12px',
        borderBottom: '1px solid var(--jp-border-color1)',
        background: 'var(--jp-layout-color1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        cursor: 'pointer'
      }}
      onClick={onToggleVisibility}
      title="点击展开配置面板"
      >
        <div style={{ 
          fontSize: '11px', 
          color: 'var(--jp-ui-font-color2)',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <span style={{ fontSize: '10px' }}>▼</span>
          <span>配置面板已隐藏</span>
        </div>
        <div style={{ 
          fontSize: '10px', 
          color: 'var(--jp-ui-font-color2)',
          background: 'var(--jp-layout-color2)',
          padding: '2px 6px',
          borderRadius: '10px'
        }}>
          {getActualModelName()} | T:{config.temperature} | L:{config.maxTokens}
        </div>
      </div>
    );
  }

  return (
    <div style={{
      padding: '8px 12px',
      borderBottom: '1px solid var(--jp-border-color1)',
      background: 'var(--jp-layout-color1)',
      animation: 'slideDown 0.2s ease-out'
    }}>
      {/* 面板标题栏 */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '8px',
        paddingBottom: '4px',
        borderBottom: '1px solid var(--jp-border-color2)'
      }}>
        <div style={{ 
          fontSize: '11px', 
          color: 'var(--jp-ui-font-color1)',
          fontWeight: 'bold'
        }}>
          模型配置
        </div>
        <button
          onClick={onToggleVisibility}
          style={{
            background: 'transparent',
            border: '1px solid var(--jp-border-color2)',
            color: 'var(--jp-ui-font-color2)',
            borderRadius: '4px',
            padding: '1px 6px',
            fontSize: '9px',
            cursor: 'pointer'
          }}
          title="隐藏配置面板"
        >
          隐藏 ▲
        </button>
      </div>

      {/* 后端服务地址 */}
      <div style={{ marginBottom: '8px' }}>
        <div style={{ fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' }}>
          后端服务地址:
        </div>
        <input
          type="text"
          value={config.backendUrl}
          onChange={handleBackendUrlChange}
          style={{
            width: '100%',
            padding: '4px 8px',
            border: '1px solid var(--jp-border-color1)',
            borderRadius: '4px',
            fontSize: '12px',
            background: 'var(--jp-input-background)',
            color: 'var(--jp-ui-font-color1)'
          }}
          placeholder="输入后端服务 URL"
        />
      </div>

      {/* 模型选择 */}
      <div style={{ marginBottom: '8px' }}>
        <div style={{ fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' }}>
          模型选择:
        </div>
        <select
          value={config.modelName}
          onChange={handleModelNameChange}
          style={{
            width: '100%',
            padding: '4px 8px',
            border: '1px solid var(--jp-border-color1)',
            borderRadius: '4px',
            fontSize: '12px',
            background: 'var(--jp-input-background)',
            color: 'var(--jp-ui-font-color1)'
          }}
        >
          {modelOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      {/* 自定义模型输入框 */}
      {config.modelName === 'custom' && (
        <div style={{ marginBottom: '8px' }}>
          <div style={{ fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' }}>
            自定义模型名称:
          </div>
          <input
            type="text"
            value={config.customModelName}
            onChange={handleCustomModelNameChange}
            style={{
              width: '100%',
              padding: '4px 8px',
              border: '1px solid var(--jp-border-color1)',
              borderRadius: '4px',
              fontSize: '12px',
              background: 'var(--jp-input-background)',
              color: 'var(--jp-ui-font-color1)'
            }}
            placeholder="输入自定义模型名称"
          />
        </div>
      )}

      {/* 参数配置 */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: '1fr 1fr',
        gap: '8px'
      }}>
        <div>
          <div style={{ fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' }}>
            温度: {config.temperature}
          </div>
          <input
            type="range"
            min="0"
            max="2"
            step="0.1"
            value={config.temperature}
            onChange={handleTemperatureChange}
            style={{ width: '100%' }}
          />
          <div style={{ 
            fontSize: '10px', 
            color: 'var(--jp-ui-font-color2)',
            display: 'flex',
            justifyContent: 'space-between'
          }}>
            <span>精确</span>
            <span>平衡</span>
            <span>创意</span>
          </div>
        </div>
        
        <div>
          <div style={{ fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' }}>
            最大长度: {config.maxTokens}
          </div>
          <input
            type="range"
            min="100"
            max="4000"
            step="100"
            value={config.maxTokens}
            onChange={handleMaxTokensChange}
            style={{ width: '100%' }}
          />
          <div style={{ 
            fontSize: '10px', 
            color: 'var(--jp-ui-font-color2)',
            display: 'flex',
            justifyContent: 'space-between'
          }}>
            <span>简洁</span>
            <span>适中</span>
            <span>详细</span>
          </div>
        </div>
      </div>

      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between',
        marginTop: '8px'
      }}>
        <button
          onClick={onReset}
          style={{
            background: 'transparent',
            border: '1px solid var(--jp-border-color1)',
            color: 'var(--jp-ui-font-color2)',
            borderRadius: '4px',
            padding: '2px 8px',
            fontSize: '10px',
            cursor: 'pointer'
          }}
        >
          重置设置
        </button>
        <div style={{ fontSize: '10px', color: 'var(--jp-ui-font-color2)' }}>
          当前模型: {getActualModelName()}
        </div>
      </div>
    </div>
  );
};