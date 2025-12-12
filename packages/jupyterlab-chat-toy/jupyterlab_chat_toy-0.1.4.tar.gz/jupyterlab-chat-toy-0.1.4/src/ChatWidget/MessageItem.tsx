// MessageItem.tsx
import React from 'react';
import { MessageItemProps } from './types';
import { MessageContent } from './MessageContent';

export const MessageItem: React.FC<MessageItemProps> = ({ 
  message, 
  isStreaming, 
  onInsertCode 
}) => {
  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
      alignItems: 'flex-start',
      marginBottom: '12px'
    }}>
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
            onInsertCode={onInsertCode}
          />
          {isStreaming && (
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
          {isStreaming && ' · 生成中...'}
        </div>
      </div>
    </div>
  );
};