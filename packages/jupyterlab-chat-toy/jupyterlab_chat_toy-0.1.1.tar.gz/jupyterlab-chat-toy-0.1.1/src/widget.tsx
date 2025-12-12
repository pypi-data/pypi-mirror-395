import React, { useState, useRef, useEffect } from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { MessageContent } from './MessageContent';
import { Message } from './types';
import { NotebookActions } from '@jupyterlab/notebook';
import { INotebookTracker } from '@jupyterlab/notebook';

class ChatWidget extends ReactWidget {
  private notebookTracker: INotebookTracker | null;

  constructor(notebookTracker: INotebookTracker | null) {
    super();
    this.notebookTracker = notebookTracker;
    this.id = 'ai-chat-widget';
    this.title.label = 'AI Chat';
    this.title.closable = true;
    this.addClass('jp-ChatWidget');
  }

  render(): JSX.Element {
    return <ChatComponent notebookTracker={this.notebookTracker} />;
  }
}

interface ChatComponentProps {
  notebookTracker: INotebookTracker | null;
}

const ChatComponent: React.FC<ChatComponentProps> = ({ notebookTracker }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      content: '你好！我是 AI 助手。现在支持流式输出和模型切换，体验更佳。',
      sender: 'ai',
      timestamp: new Date(),
      type: 'text'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [backendUrl, setBackendUrl] = useState('http://localhost:8888/v1/chat/completions');
  const [modelName, setModelName] = useState('/mnt/e/qwen3-1.7b');
  const [customModelName, setCustomModelName] = useState('');
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(2000);
  const [currentStreamingMessageId, setCurrentStreamingMessageId] = useState<number | null>(null);
  
  // 添加智能滚动相关状态和引用
  const [shouldAutoScroll, setShouldAutoScroll] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  
  // 添加组件挂载状态跟踪
  const isMountedRef = useRef(true);

  useEffect(() => {
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  const modelOptions = [
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

  const getActualModelName = () => {
    return modelName === 'custom' ? customModelName : modelName;
  };

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

    console.log('当前活动单元格索引:', activeCellIndex);
    console.log('要插入的代码:', code);

    try {
      // 在活动单元格下方插入新的代码单元格
      NotebookActions.insertBelow(content);
      
      // 获取新插入的单元格
      const newCellIndex = activeCellIndex + 1;
      const newCell = content.widgets[newCellIndex];
      
      console.log('新单元格索引:', newCellIndex);
      console.log('新单元格:', newCell);
      
      if (newCell && newCell.model.type === 'code') {
        console.log('单元格模型:', newCell.model);
        console.log('可用属性:', Object.keys(newCell.model));
        
        // 尝试设置代码内容
        if (newCell.model.value && newCell.model.value.text !== undefined) {
          newCell.model.value.text = code;
          console.log('使用 value.text 设置代码');
        } else if (newCell.model.sharedModel && newCell.model.sharedModel.setSource) {
          newCell.model.sharedModel.setSource(code);
          console.log('使用 sharedModel.setSource 设置代码');
        } else {
          console.error('无法找到设置代码的方法');
          alert('无法设置代码内容');
          return;
        }
        
        // 激活新单元格
        content.activeCellIndex = newCellIndex;
        
        console.log('代码已插入到Notebook');
      } else {
        console.error('新单元格不是代码单元格或未找到');
      }
    } catch (error) {
      console.error('插入代码失败:', error);
      alert('插入代码失败，请重试');
    }
  };

  // 智能滚动函数
  const smartScrollToBottom = (behavior: ScrollBehavior = 'smooth') => {
    if (!isMountedRef.current || !shouldAutoScroll) return;
    
    requestAnimationFrame(() => {
      if (messagesEndRef.current && isMountedRef.current) {
        messagesEndRef.current.scrollIntoView({ 
          behavior,
          block: 'nearest'
        });
      }
    });
  };

  // 检查用户是否在底部
  const isUserAtBottom = () => {
    if (!messagesContainerRef.current) return true;
    
    const container = messagesContainerRef.current;
    const threshold = 100; // 距离底部100px以内都算在底部
    
    return container.scrollHeight - container.scrollTop - container.clientHeight <= threshold;
  };

  // 处理容器滚动事件
  const handleMessagesScroll = () => {
    if (!messagesContainerRef.current) return;
    
    const atBottom = isUserAtBottom();
    
    // 只有当用户主动滚动到底部时才重新启用自动滚动
    if (atBottom && !shouldAutoScroll) {
      setShouldAutoScroll(true);
    } else if (!atBottom && shouldAutoScroll) {
      setShouldAutoScroll(false);
    }
  };

  // 修改现有的 scrollToBottom 函数
  const scrollToBottom = () => {
    smartScrollToBottom('smooth');
  };

  // 修改 useEffect，添加滚动事件监听
  useEffect(() => {
    const container = messagesContainerRef.current;
    if (container) {
      container.addEventListener('scroll', handleMessagesScroll);
      return () => {
        container.removeEventListener('scroll', handleMessagesScroll);
      };
    }
  }, [shouldAutoScroll]);

  // 修改消息更新时的滚动逻辑
  useEffect(() => {
    if (messages.length > 0) {
      // 只有当应该自动滚动时才滚动
      if (shouldAutoScroll) {
        smartScrollToBottom('smooth');
      }
    }
  }, [messages, shouldAutoScroll]);

  const streamToAI = async (message: string): Promise<void> => {
    abortControllerRef.current = new AbortController();
    
    try {
      if (!isMountedRef.current) return;

      const newMessageId = Date.now() + 1;
      const newMessage: Message = {
        id: newMessageId,
        content: '',
        sender: 'ai',
        timestamp: new Date(),
        type: 'text'
      };

      if (isMountedRef.current) {
        setMessages(prev => [...prev, newMessage]);
        setCurrentStreamingMessageId(newMessageId);
      }

      const actualModelName = getActualModelName();
      
      const requestBody = {
        model: actualModelName,
        messages: [
          ...messages.slice(-10).map(m => ({
            role: m.sender === 'user' ? 'user' : 'assistant',
            content: m.content
          })),
          {
            role: 'user',
            content: message
          }
        ],
        stream: true,
        temperature: temperature,
        max_tokens: maxTokens
      };

      console.log('Sending streaming request to:', backendUrl);
      console.log('Using model:', actualModelName);
      console.log('Request parameters:', {
        temperature,
        maxTokens
      });

      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        mode: 'cors',
        signal: abortControllerRef.current.signal
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        throw new Error(`HTTP ${response.status}: ${response.statusText}. ${errorText}`);
      }

      await processStreamResponse(response, newMessageId);
      
    } catch (error: any) {
      if (!isMountedRef.current) return;
      
      if (error.name === 'AbortError') {
        console.log('Request was aborted');
        return;
      }
      console.error('Error in streaming AI call:', error);
      
      if (currentStreamingMessageId && isMountedRef.current) {
        setMessages(prev => prev.map(msg => 
          msg.id === currentStreamingMessageId 
            ? { ...msg, content: `请求失败: ${error.message}` }
            : msg
        ));
      }
      throw error;
    } finally {
      if (isMountedRef.current) {
        abortControllerRef.current = null;
        setCurrentStreamingMessageId(null);
      }
    }
  };

  // 修改 processStreamResponse 函数，添加更智能的滚动
  const processStreamResponse = async (response: Response, messageId: number): Promise<void> => {
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    
    if (!reader) {
      throw new Error('No reader available for stream');
    }

    let accumulatedContent = '';
    let buffer = '';
    let lastScrollTime = 0;
    const scrollThrottle = 300; // 每300ms最多滚动一次

    try {
      while (true) {
        const { done, value } = await reader.read();
        
        if (!isMountedRef.current) {
          reader.releaseLock();
          return;
        }
        
        if (done) {
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;

        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmedLine = line.trim();
          
          if (trimmedLine === '') continue;
          if (trimmedLine === 'data: [DONE]') {
            return;
          }

          if (trimmedLine.startsWith('data: ')) {
            try {
              const jsonData = trimmedLine.slice(6);
              const parsed = JSON.parse(jsonData);
              
              if (parsed.choices && parsed.choices[0].delta) {
                const delta = parsed.choices[0].delta;
                
                if (delta.content) {
                  accumulatedContent += delta.content;
                  
                  if (isMountedRef.current) {
                    setMessages(prev => prev.map(msg => 
                      msg.id === messageId 
                        ? { ...msg, content: accumulatedContent, timestamp: new Date() }
                        : msg
                    ));

                    // 节流滚动：只在需要时且一段时间内没有滚动过才滚动
                    const now = Date.now();
                    if (shouldAutoScroll && now - lastScrollTime > scrollThrottle) {
                      smartScrollToBottom('smooth');
                      lastScrollTime = now;
                    }
                  }
                }
              }
            } catch (e) {
              console.warn('Failed to parse stream data:', e, 'Data:', trimmedLine);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
      
      // 流结束时确保滚动到底部（如果应该自动滚动）
      if (isMountedRef.current && shouldAutoScroll) {
        smartScrollToBottom('smooth');
      }
    }
  };

  const stopStreaming = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      if (isMountedRef.current) {
        setIsLoading(false);
        setCurrentStreamingMessageId(null);
      }
    }
  };

  // 修改 handleSend 函数，发送消息时强制滚动到底部
  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
      type: 'text'
    };

    if (!isMountedRef.current) return;

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    
    // 用户发送消息时强制滚动到底部
    setShouldAutoScroll(true);
    smartScrollToBottom('smooth');

    try {
      await streamToAI(inputValue);
    } catch (error) {
      if (isMountedRef.current) {
        console.error('Streaming failed:', error);
        
        const errorMessage: Message = {
          id: Date.now() + 1,
          content: `请求失败: ${error instanceof Error ? error.message : '未知错误'}`,
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        };
        
        setMessages(prev => [...prev, errorMessage]);
      }
    } finally {
      if (isMountedRef.current) {
        setIsLoading(false);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // 添加手动滚动到底部的功能
  const scrollToBottomManually = () => {
    setShouldAutoScroll(true);
    smartScrollToBottom('smooth');
  };

  const clearChat = () => {
    stopStreaming();
    
    if (isMountedRef.current) {
      setMessages([
        {
          id: 1,
          content: '对话已清空。现在支持流式输出和模型切换，体验更佳。',
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
      ]);
      setCurrentStreamingMessageId(null);
    }
  };

  const updateBackendUrl = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBackendUrl(e.target.value);
  };

  const updateModelName = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setModelName(e.target.value);
  };

  const updateCustomModelName = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCustomModelName(e.target.value);
  };

  const updateTemperature = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTemperature(parseFloat(e.target.value));
  };

  const updateMaxTokens = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMaxTokens(parseInt(e.target.value, 10));
  };

  const resetSettings = () => {
    setModelName('gpt-3.5-turbo');
    setCustomModelName('');
    setTemperature(0.7);
    setMaxTokens(2000);
  };

  const isMessageStreaming = (messageId: number) => {
    return currentStreamingMessageId === messageId;
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
      {/* 顶部标题栏 */}
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
            {actualModelName}
          </div>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          {isLoading && (
            <button
              onClick={stopStreaming}
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
            onClick={clearChat}
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

      {/* 配置面板 */}
      <div style={{
        padding: '8px 12px',
        borderBottom: '1px solid var(--jp-border-color1)',
        background: 'var(--jp-layout-color1)'
      }}>
        {/* 后端服务地址 - 单独一行 */}
        <div style={{ marginBottom: '8px' }}>
          <div style={{ fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' }}>
            后端服务地址:
          </div>
          <input
            type="text"
            value={backendUrl}
            onChange={updateBackendUrl}
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

        {/* 模型选择 - 单独一行 */}
        <div style={{ marginBottom: '8px' }}>
          <div style={{ fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' }}>
            模型选择:
          </div>
          <select
            value={modelName}
            onChange={updateModelName}
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

        {/* 自定义模型输入框 - 只在选择 custom 时显示 */}
        {modelName === 'custom' && (
          <div style={{ marginBottom: '8px' }}>
            <div style={{ fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' }}>
              自定义模型名称:
            </div>
            <input
              type="text"
              value={customModelName}
              onChange={updateCustomModelName}
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

        {/* 参数配置 - 水平排列 */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: '1fr 1fr',
          gap: '8px'
        }}>
          <div>
            <div style={{ fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' }}>
              温度: {temperature}
            </div>
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={temperature}
              onChange={updateTemperature}
              style={{
                width: '100%'
              }}
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
              最大长度: {maxTokens}
            </div>
            <input
              type="range"
              min="100"
              max="4000"
              step="100"
              value={maxTokens}
              onChange={updateMaxTokens}
              style={{
                width: '100%'
              }}
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
            onClick={resetSettings}
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
            当前模型: {actualModelName}
          </div>
        </div>
      </div>

      {/* 消息区域 - 添加ref和滚动指示器 */}
      <div 
        ref={messagesContainerRef}
        style={{ 
          flex: 1, 
          overflow: 'auto', 
          padding: '8px',
          background: 'var(--jp-layout-color0)',
          position: 'relative'
        }}
      >
        {messages.map((message) => (
          <div
            key={message.id}
            style={{
              display: 'flex',
              flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
              alignItems: 'flex-start',
              marginBottom: '12px'
            }}
          >
            <div style={{
              width: '28px',
              height: '28px',
              borderRadius: '50%',
              background: message.sender === 'user' 
                ? 'var(--jp-brand-color1)' 
                : 'var(--jp-accent-color1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '12px',
              margin: message.sender === 'user' ? '0 0 0 6px' : '0 6px 0 0',
              flexShrink: 0
            }}>
              {message.sender === 'user' ? '👤' : '🤖'}
            </div>

            <div style={{
              maxWidth: '85%',
              textAlign: message.sender === 'user' ? 'right' : 'left'
            }}>
              <div style={{
                background: message.sender === 'user' 
                  ? 'var(--jp-brand-color1)' 
                  : 'var(--jp-layout-color2)',
                color: message.sender === 'user' 
                  ? 'white' 
                  : 'var(--jp-ui-font-color1)',
                padding: '6px 10px',
                borderRadius: '12px',
                border: '1px solid var(--jp-border-color1)',
                wordBreak: 'break-word',
                position: 'relative'
              }}>
                <MessageContent 
                  content={message.content} 
                  onInsertCode={insertCodeToNotebook}
                />
                {isMessageStreaming(message.id) && (
                  <span style={{
                    display: 'inline-block',
                    width: '2px',
                    height: '1em',
                    background: 'var(--jp-ui-font-color1)',
                    marginLeft: '2px',
                    animation: 'blink 1s infinite'
                  }}></span>
                )}
              </div>
              <div style={{
                fontSize: '10px',
                color: 'var(--jp-ui-font-color2)',
                marginTop: '2px'
              }}>
                {formatTime(message.timestamp)}
                {isMessageStreaming(message.id) && ' · 生成中...'}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && !currentStreamingMessageId && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '12px'
          }}>
            <div style={{
              width: '28px',
              height: '28px',
              borderRadius: '50%',
              background: 'var(--jp-accent-color1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '12px',
              marginRight: '6px',
              flexShrink: 0
            }}>
              🤖
            </div>
            <div style={{
              background: 'var(--jp-layout-color2)',
              padding: '6px 10px',
              borderRadius: '12px',
              border: '1px solid var(--jp-border-color1)',
              color: 'var(--jp-ui-font-color2)',
              fontSize: '12px',
              display: 'flex',
              alignItems: 'center'
            }}>
              <div style={{
                width: '12px',
                height: '12px',
                border: '2px solid var(--jp-ui-font-color3)',
                borderTop: '2px solid transparent',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
                marginRight: '6px'
              }}></div>
              AI正在思考...
            </div>
          </div>
        )}
        
        {/* 显示滚动到底部按钮 */}
        {!shouldAutoScroll && (
          <button
            onClick={scrollToBottomManually}
            style={{
              position: 'sticky',
              bottom: '16px',
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'var(--jp-brand-color1)',
              color: 'white',
              border: 'none',
              borderRadius: '20px',
              padding: '8px 16px',
              fontSize: '12px',
              cursor: 'pointer',
              boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
              zIndex: 100,
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <span>↓</span>
            有新消息
          </button>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* 输入区域 */}
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
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            rows={1}
          />
          <button
            style={{
              background: inputValue.trim() && !isLoading 
                ? 'var(--jp-brand-color1)' 
                : 'var(--jp-layout-color3)',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              padding: '6px 12px',
              cursor: inputValue.trim() && !isLoading ? 'pointer' : 'not-allowed',
              height: '36px',
              fontSize: '12px',
              fontWeight: 'bold'
            }}
            onClick={handleSend}
            disabled={!inputValue.trim() || isLoading}
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
          流式输出 | 模型: {actualModelName} | 温度: {temperature} | 最大长度: {maxTokens}
        </div>
      </div>

      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }

        /* 添加平滑滚动样式 */
        .jp-ChatWidget * {
          scroll-behavior: smooth;
        }
      `}</style>
    </div>
  );
};

export { ChatWidget };