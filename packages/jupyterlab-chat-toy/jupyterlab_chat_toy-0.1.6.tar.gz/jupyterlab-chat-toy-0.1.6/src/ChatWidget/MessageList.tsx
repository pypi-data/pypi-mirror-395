// MessageList.tsx
import React from 'react';
import { MessageListProps } from './types';
import { MessageItem } from './MessageItem';

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isLoading,
  currentStreamingMessageId,
  onInsertCode,
  onScrollToBottom,
  shouldAutoScroll,
  messagesEndRef,
  messagesContainerRef
}) => {
  return (
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
        <MessageItem
          key={message.id}
          message={message}
          isStreaming={currentStreamingMessageId === message.id}
          onInsertCode={onInsertCode}
        />
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
          onClick={onScrollToBottom}
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
  );
};