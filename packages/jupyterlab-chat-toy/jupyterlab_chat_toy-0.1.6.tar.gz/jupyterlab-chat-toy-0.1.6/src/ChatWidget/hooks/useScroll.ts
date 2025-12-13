// hooks/useScroll.ts
import { useState, useRef, useEffect, useCallback } from 'react';

export const useScroll = () => {
  const [shouldAutoScroll, setShouldAutoScroll] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const isMountedRef = useRef(true);

  useEffect(() => {
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  const isUserAtBottom = useCallback(() => {
    if (!messagesContainerRef.current) return true;
    
    const container = messagesContainerRef.current;
    const threshold = 100;
    
    return container.scrollHeight - container.scrollTop - container.clientHeight <= threshold;
  }, []);

  const smartScrollToBottom = useCallback((behavior: ScrollBehavior = 'smooth') => {
    if (!isMountedRef.current || !shouldAutoScroll) return;
    
    requestAnimationFrame(() => {
      if (messagesEndRef.current && isMountedRef.current) {
        messagesEndRef.current.scrollIntoView({ 
          behavior,
          block: 'nearest'
        });
      }
    });
  }, [shouldAutoScroll]);

  const handleMessagesScroll = useCallback(() => {
    if (!messagesContainerRef.current) return;
    
    const atBottom = isUserAtBottom();
    
    if (atBottom && !shouldAutoScroll) {
      setShouldAutoScroll(true);
    } else if (!atBottom && shouldAutoScroll) {
      setShouldAutoScroll(false);
    }
  }, [shouldAutoScroll, isUserAtBottom]);

  useEffect(() => {
    const container = messagesContainerRef.current;
    if (container) {
      container.addEventListener('scroll', handleMessagesScroll);
      return () => {
        container.removeEventListener('scroll', handleMessagesScroll);
      };
    }
  }, [handleMessagesScroll]);

  const scrollToBottomManually = () => {
    setShouldAutoScroll(true);
    smartScrollToBottom('smooth');
  };

  return {
    shouldAutoScroll,
    messagesEndRef,
    messagesContainerRef,
    smartScrollToBottom,
    scrollToBottomManually,
    handleMessagesScroll
  };
};