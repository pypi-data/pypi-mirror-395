// hooks/useChat.ts
import { useState, useRef } from 'react';
import { Message, ChatConfig } from '../types';

export const useChat = (initialConfig?: Partial<ChatConfig>) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      content: '你好！我是 AI 助手。现在支持流式输出和模型切换，体验更佳。',
      sender: 'ai',
      timestamp: new Date(),
      type: 'text'
    }
  ]);
  
  const [config, setConfig] = useState<ChatConfig>({
    backendUrl: 'http://localhost:8888/v1/chat/completions',
    modelName: 'gpt-3.5-turbo',
    customModelName: '',
    temperature: 0.7,
    maxTokens: 2000,
    ...initialConfig
  });

  const addMessage = (message: Message) => {
    setMessages(prev => [...prev, message]);
  };

  const updateMessage = (messageId: number, content: string) => {
    setMessages(prev => prev.map(msg => 
      msg.id === messageId 
        ? { ...msg, content, timestamp: new Date() }
        : msg
    ));
  };

  const clearMessages = () => {
    setMessages([
      {
        id: 1,
        content: '对话已清空。现在支持流式输出和模型切换，体验更佳。',
        sender: 'ai',
        timestamp: new Date(),
        type: 'text'
      }
    ]);
  };

  const updateConfigPartial = (newConfig: Partial<ChatConfig>) => {
    setConfig(prev => ({ ...prev, ...newConfig }));
  };

  const resetConfig = () => {
    setConfig({
      backendUrl: 'http://localhost:8888/v1/chat/completions',
      modelName: 'gpt-3.5-turbo',
      customModelName: '',
      temperature: 0.7,
      maxTokens: 2000,
      ...initialConfig
    });
  };

  const getActualModelName = () => {
    return config.modelName === 'custom' ? config.customModelName : config.modelName;
  };

  return {
    messages,
    config,
    addMessage,
    updateMessage,
    clearMessages,
    updateConfig: updateConfigPartial,
    resetConfig,
    getActualModelName
  };
};