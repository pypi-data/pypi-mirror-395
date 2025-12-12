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
  const [isConfigVisible, setIsConfigVisible] = useState(true); // 新增：控制配置面板显示
  
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
        if (newCell.model.value && newCell.model.value.text !== undefined) {
          newCell.model.value.text = code;
        } else if (newCell.model.sharedModel && newCell.model.sharedModel.setSource) {
          newCell.model.sharedModel.setSource(code);
        } else {
          alert('无法设置代码内容');
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

  const actualModelName = getActualModelName();

  return (
    <div style={{ 
      height: '100%', 
      display: 'flex', 
      flexDirection: 'column',
      fontFamily: 'var(--jp-ui-font-family)',
      fontSize: 'var(--jp-ui-font-size1)',
      background: 'var(--jp-layout-color0)'
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