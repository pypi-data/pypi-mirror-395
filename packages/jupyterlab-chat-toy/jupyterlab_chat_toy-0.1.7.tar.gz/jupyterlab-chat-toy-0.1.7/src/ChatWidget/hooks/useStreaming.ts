// hooks/useStreaming.ts
import { useState, useRef } from 'react';
import { StreamingParams } from '../types';

export const useStreaming = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [currentStreamingMessageId, setCurrentStreamingMessageId] = useState<number | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const processStreamResponse = async (
    response: Response, 
    messageId: number,
    onUpdateMessage: (messageId: number, content: string) => void
  ): Promise<void> => {
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    
    if (!reader) {
      throw new Error('No reader available for stream');
    }

    let accumulatedContent = '';
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        
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
                  onUpdateMessage(messageId, accumulatedContent);
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
    }
  };

  const streamToAI = async (params: StreamingParams): Promise<void> => {
    abortControllerRef.current = new AbortController();
    
    try {
      setIsLoading(true);

      const newMessageId = Date.now() + 1;
      params.onNewMessage({
        id: newMessageId,
        content: '',
        sender: 'ai',
        timestamp: new Date(),
        type: 'text'
      });
      
      setCurrentStreamingMessageId(newMessageId);

      const actualModelName = params.config.modelName === 'custom' 
        ? params.config.customModelName 
        : params.config.modelName;
      
      const requestBody = {
        model: actualModelName,
        messages: [
          ...params.messages.slice(-10).map(m => ({
            role: m.sender === 'user' ? 'user' : 'assistant',
            content: m.content
          })),
          {
            role: 'user',
            content: params.message
          }
        ],
        stream: true,
        temperature: params.config.temperature,
        max_tokens: params.config.maxTokens
      };

      const response = await fetch(params.config.backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        mode: 'cors',
        signal: abortControllerRef.current.signal
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${response.statusText}. ${errorText}`);
      }

      await processStreamResponse(response, newMessageId, params.onUpdateMessage);
      
    } catch (error: any) {
      if (error.name === 'AbortError') {
        console.log('Request was aborted');
        return;
      }
      console.error('Error in streaming AI call:', error);
      params.onError(error);
    } finally {
      abortControllerRef.current = null;
      setCurrentStreamingMessageId(null);
      setIsLoading(false);
    }
  };

  const stopStreaming = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  };

  return {
    isLoading,
    currentStreamingMessageId,
    streamToAI,
    stopStreaming,
    setIsLoading
  };
};