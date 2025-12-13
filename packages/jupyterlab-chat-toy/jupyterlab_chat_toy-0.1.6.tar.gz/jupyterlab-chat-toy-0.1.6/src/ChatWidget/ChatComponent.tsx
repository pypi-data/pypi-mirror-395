// ChatComponent.tsx
import React, { useState, useEffect } from 'react';
import { NotebookActions } from '@jupyterlab/notebook';
import { INotebookTracker } from '@jupyterlab/notebook';
import { Header } from './Header';
import { ConfigPanel } from './ConfigPanel';
import { MessageList } from './MessageList';
import { InputArea } from './InputArea';
import { useChat } from './hooks/useChat';
import { useStreaming } from './hooks/useStreaming';
import { useScroll } from './hooks/useScroll';
import { ChatComponentProps, ModelOption } from './types';
// 导入错误分析工具，改名为 handleFixCommand
import { handleFixCommand, isErrorDetectionSupported } from '../utils/errorAnalyzer';

const MODEL_OPTIONS: ModelOption[] = [
  { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
  { value: 'gpt-4', label: 'GPT-4' },
  { value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
  { value: 'claude-3-sonnet', label: 'Claude 3 Sonnet' },
  { value: 'claude-3-opus', label: 'Claude 3 Opus' },
  { value: 'llama-2-7b', label: 'Llama 2 7B' },
  { value: 'llama-2-13b', label: 'Llama 2 13B' },
  { value: 'llama-2-70b', label: 'Llama 2 70B' },
  { value: 'custom', label: '自定义模型' }
];

const ChatComponent: React.FC<ChatComponentProps> = ({ notebookTracker }) => {
  const [inputValue, setInputValue] = useState('');
  const [isConfigVisible, setIsConfigVisible] = useState(true);
  const [errorDetectionSupported, setErrorDetectionSupported] = useState(true);
  
  // 使用自定义hooks
  const { 
    messages, 
    config, 
    addMessage, 
    updateMessage, 
    clearMessages, 
    updateConfig, 
    resetConfig,
    getActualModelName 
  } = useChat();
  
  const { 
    isLoading, 
    currentStreamingMessageId, 
    streamToAI, 
    stopStreaming, 
    setIsLoading 
  } = useStreaming();
  
  const { 
    shouldAutoScroll, 
    messagesEndRef, 
    messagesContainerRef, 
    smartScrollToBottom, 
    scrollToBottomManually 
  } = useScroll();

  // 检查错误检测功能是否支持
  useEffect(() => {
    const supported = isErrorDetectionSupported(notebookTracker);
    setErrorDetectionSupported(supported);
    
    if (!supported) {
      console.warn('错误检测功能在当前JupyterLab版本中可能不可用');
    }
  }, [notebookTracker]);

  // 切换配置面板显示
  const toggleConfigPanel = () => {
    setIsConfigVisible(prev => !prev);
  };

  // 插入代码到Notebook
  const insertCodeToNotebook = (code: string, language: string) => {
    if (!notebookTracker) {
      console.error('Notebook tracker not available');
      alert('错误：未找到活动的Notebook');
      return;
    }

    const current = notebookTracker.currentWidget;
    if (!current) {
      alert('错误：请先打开一个Notebook');
      return;
    }

    const { content } = current;
    const { activeCellIndex } = content;

    try {
      NotebookActions.insertBelow(content);
      
      const newCellIndex = activeCellIndex + 1;
      const newCell = content.widgets[newCellIndex];
      
      if (newCell && newCell.model.type === 'code') {
        const cellModel = newCell.model as any;
        
        if (cellModel.value && cellModel.value.text !== undefined) {
          cellModel.value.text = code;
        } else if (cellModel.sharedModel) {
          if (typeof cellModel.sharedModel.setSource === 'function') {
            cellModel.sharedModel.setSource(code);
          } else if (cellModel.sharedModel.source !== undefined) {
            cellModel.sharedModel.source = code;
          } else {
            alert('无法设置代码内容：sharedModel 格式不支持');
            return;
          }
        } else if (cellModel.source !== undefined) {
          cellModel.source = code;
        } else {
          alert('无法设置代码内容：不支持的单元格模型');
          return;
        }
        
        content.activeCellIndex = newCellIndex;
      }
    } catch (error) {
      console.error('插入代码失败:', error);
      alert('插入代码失败，请重试');
    }
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // 检查是否是 /help 命令
    if (inputValue.trim() === '/help') {
      showHelpMessage();
      setInputValue('');
      return;
    }

    // 检查是否是 /fix 命令
    if (inputValue.trim().startsWith('/fix')) {
      if (!errorDetectionSupported) {
        const errorMessage = {
          id: Date.now(),
          content: '⚠️ 错误检测功能在当前JupyterLab版本中不可用。请升级到最新版本或使用其他方法分析错误。',
          sender: 'ai' as const,
          timestamp: new Date(),
          type: 'text' as const
        };
        addMessage(errorMessage);
        setInputValue('');
        smartScrollToBottom('smooth');
        return;
      }
      
      const fixResult = handleFixCommand(notebookTracker, inputValue);
      
      if (!fixResult.shouldContinue) {
        // 如果是 /fix 命令但处理失败（如没有错误）
        if (fixResult.error) {
          const errorMessage = {
            id: Date.now(),
            content: fixResult.error,
            sender: 'ai' as const,
            timestamp: new Date(),
            type: 'text' as const
          };
          addMessage(errorMessage);
          setInputValue('');
          smartScrollToBottom('smooth');
          return;
        }
        
        // 如果有分析提示词，直接发送给大模型
        if (fixResult.analysisPrompt) {
          // 添加用户消息（显示原始命令）
          const userMessage = {
            id: Date.now(),
            content: inputValue,
            sender: 'user' as const,
            timestamp: new Date(),
            type: 'text' as const
          };
          addMessage(userMessage);
          
          setInputValue('');
          setIsLoading(true);
          smartScrollToBottom('smooth');
          
          try {
            // 使用分析提示词发送给大模型
            await streamToAI({
              message: fixResult.analysisPrompt,
              messages: [...messages, userMessage],
              config,
              onNewMessage: addMessage,
              onUpdateMessage: updateMessage,
              onStreamingStart: (messageId) => {
                // 可以根据需要处理流式开始
              },
              onStreamingEnd: () => {
                // 流式结束处理
              },
              onError: (error) => {
                const errorMessage = {
                  id: Date.now() + 1,
                  content: `请求失败: ${error instanceof Error ? error.message : '未知错误'}`,
                  sender: 'ai' as const,
                  timestamp: new Date(),
                  type: 'text' as const
                };
                addMessage(errorMessage);
              }
            });
          } catch (error) {
            console.error('Streaming failed:', error);
          } finally {
            setIsLoading(false);
          }
          return;
        }
      }
    }

    // 普通消息处理
    const userMessage = {
      id: Date.now(),
      content: inputValue,
      sender: 'user' as const,
      timestamp: new Date(),
      type: 'text' as const
    };

    addMessage(userMessage);
    setInputValue('');
    setIsLoading(true);
    
    // 用户发送消息时强制滚动到底部
    smartScrollToBottom('smooth');

    try {
      await streamToAI({
        message: inputValue,
        messages: [...messages, userMessage],
        config,
        onNewMessage: addMessage,
        onUpdateMessage: updateMessage,
        onStreamingStart: (messageId) => {
          // 可以根据需要处理流式开始
        },
        onStreamingEnd: () => {
          // 流式结束处理
        },
        onError: (error) => {
          const errorMessage = {
            id: Date.now() + 1,
            content: `请求失败: ${error instanceof Error ? error.message : '未知错误'}`,
            sender: 'ai' as const,
            timestamp: new Date(),
            type: 'text' as const
          };
          addMessage(errorMessage);
        }
      });
    } catch (error) {
      console.error('Streaming failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClearChat = () => {
    stopStreaming();
    clearMessages();
  };

  // 显示帮助信息
  const showHelpMessage = () => {
    let helpContent = `🛠️ **可用命令**

\`/fix\` - 分析并修复当前活动单元格的错误
   用法: \`/fix [额外描述]\`
   示例: \`/fix 这个函数为什么报错？\`
   
\`/help\` - 显示帮助信息`;

    // 根据是否支持错误检测调整帮助信息
    if (!errorDetectionSupported) {
      helpContent += `

⚠️ **注意**: 错误修复功能(\`/fix\`)在当前JupyterLab版本中可能不可用。
   请确保：
   1. 你使用的是 JupyterLab 3.2.9 或更高版本
   2. 代码单元格已执行并产生了错误
   3. 包含错误的单元格处于活动状态`;
    } else {
      helpContent += `

**错误修复功能说明**：
1. 确保你已经执行了包含错误的代码单元格
2. 将光标放在有错误的单元格上
3. 输入 \`/fix\` 命令获取错误分析和修复方案
4. 可以在命令后添加额外描述，如 \`/fix 这个数据处理的错误怎么解决？\``;
    }

    helpContent += `

💡 提示：当你在输入框中输入 \`/\` 时，会显示命令提示。`;

    const helpMessage = {
      id: Date.now(),
      content: helpContent,
      sender: 'ai' as const,
      timestamp: new Date(),
      type: 'text' as const
    };
    addMessage(helpMessage);
    smartScrollToBottom('smooth');
  };

  // 添加快捷命令提示
  const [showCommandHint, setShowCommandHint] = useState(false);

  // 监听输入变化，显示命令提示
  useEffect(() => {
    if (inputValue.trim() === '/') {
      setShowCommandHint(true);
    } else if (inputValue.trim().startsWith('/fix')) {
      setShowCommandHint(false);
    } else {
      setShowCommandHint(false);
    }
  }, [inputValue]);

  const actualModelName = getActualModelName();

  return (
    <div style={{ 
      height: '100%', 
      display: 'flex', 
      flexDirection: 'column',
      fontFamily: 'var(--jp-ui-font-family)',
      fontSize: 'var(--jp-ui-font-size1)',
      background: 'var(--jp-layout-color0)',
      position: 'relative'
    }}>
      <Header
        modelName={actualModelName}
        isLoading={isLoading}
        onStop={stopStreaming}
        onClear={handleClearChat}
        onToggleConfig={toggleConfigPanel}
        isConfigVisible={isConfigVisible}
      />
      
      <ConfigPanel
        config={config}
        modelOptions={MODEL_OPTIONS}
        onConfigChange={updateConfig}
        onReset={resetConfig}
        isVisible={isConfigVisible}
        onToggleVisibility={toggleConfigPanel}
      />
      
      <MessageList
        messages={messages}
        isLoading={isLoading}
        currentStreamingMessageId={currentStreamingMessageId}
        onInsertCode={insertCodeToNotebook}
        onScrollToBottom={scrollToBottomManually}
        shouldAutoScroll={shouldAutoScroll}
        messagesEndRef={messagesEndRef}
        messagesContainerRef={messagesContainerRef}
      />
      
      {/* 命令提示 */}
      {showCommandHint && (
        <div style={{
          position: 'absolute',
          bottom: '80px',
          left: '10px',
          right: '10px',
          background: 'var(--jp-layout-color1)',
          border: '1px solid var(--jp-border-color1)',
          borderRadius: '6px',
          padding: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
          zIndex: 100,
          fontSize: '12px'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '4px'
          }}>
            <span style={{ fontWeight: 'bold', color: 'var(--jp-ui-font-color1)' }}>
              可用命令
            </span>
            <button
              onClick={() => setShowCommandHint(false)}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--jp-ui-font-color2)',
                cursor: 'pointer',
                fontSize: '12px'
              }}
            >
              ✕
            </button>
          </div>
          <div style={{ 
            display: 'flex', 
            flexDirection: 'column',
            gap: '4px'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '4px',
              borderRadius: '4px',
              background: errorDetectionSupported ? 'var(--jp-layout-color2)' : 'var(--jp-layout-color3)',
              cursor: errorDetectionSupported ? 'pointer' : 'not-allowed',
              opacity: errorDetectionSupported ? 1 : 0.6
            }}
            onClick={() => {
              if (errorDetectionSupported) {
                setInputValue('/fix ');
                setShowCommandHint(false);
              }
            }}
            title={errorDetectionSupported ? '' : '错误检测功能不可用'}
            >
              <code style={{
                background: errorDetectionSupported ? 'var(--jp-brand-color1)' : 'var(--jp-ui-font-color3)',
                color: 'white',
                padding: '2px 6px',
                borderRadius: '4px',
                fontSize: '11px'
              }}>/fix</code>
              <div style={{ flex: 1 }}>
                <div style={{ color: 'var(--jp-ui-font-color1)' }}>
                  分析并修复当前单元格的错误
                </div>
                {!errorDetectionSupported && (
                  <div style={{ 
                    fontSize: '10px', 
                    color: 'var(--jp-ui-font-color3)',
                    marginTop: '2px'
                  }}>
                    当前版本不可用
                  </div>
                )}
              </div>
            </div>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '4px',
              borderRadius: '4px',
              background: 'var(--jp-layout-color2)',
              cursor: 'pointer'
            }}
            onClick={() => {
              setInputValue('/help');
              setShowCommandHint(false);
            }}
            >
              <code style={{
                background: 'var(--jp-accent-color1)',
                color: 'white',
                padding: '2px 6px',
                borderRadius: '4px',
                fontSize: '11px'
              }}>/help</code>
              <span style={{ color: 'var(--jp-ui-font-color1)' }}>
                显示帮助信息
              </span>
            </div>
          </div>
        </div>
      )}
      
      <InputArea
        value={inputValue}
        isLoading={isLoading}
        modelName={actualModelName}
        temperature={config.temperature}
        maxTokens={config.maxTokens}
        onChange={setInputValue}
        onSend={handleSend}
        onKeyPress={handleKeyPress}
      />

      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }

        @keyframes slideDown {
          from {
            opacity: 0;
            max-height: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            max-height: 300px;
            transform: translateY(0);
          }
        }

        .jp-ChatWidget * {
          scroll-behavior: smooth;
        }
      `}</style>
    </div>
  );
};

export { ChatComponent };