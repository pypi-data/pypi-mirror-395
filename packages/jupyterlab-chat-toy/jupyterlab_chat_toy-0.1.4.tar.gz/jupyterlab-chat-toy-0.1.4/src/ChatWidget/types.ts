// types.ts
import { INotebookTracker } from '@jupyterlab/notebook';

export interface Message {
  id: number;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  type: 'text' | 'code';
  language?: string;
}

export interface ModelOption {
  value: string;
  label: string;
}

export interface ChatConfig {
  backendUrl: string;
  modelName: string;
  customModelName: string;
  temperature: number;
  maxTokens: number;
}

export interface ChatComponentProps {
  notebookTracker: INotebookTracker | null;
}

export interface HeaderProps {
  modelName: string;
  isLoading: boolean;
  onStop: () => void;
  onClear: () => void;
}

export interface ConfigPanelProps {
  config: ChatConfig;
  modelOptions: ModelOption[];
  onConfigChange: (config: Partial<ChatConfig>) => void;
  onReset: () => void;
}

export interface MessageItemProps {
  message: Message;
  isStreaming: boolean;
  onInsertCode: (code: string, language: string) => void;
}

export interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
  currentStreamingMessageId: number | null;
  onInsertCode: (code: string, language: string) => void;
  onScrollToBottom: () => void;
  shouldAutoScroll: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement>;
  messagesContainerRef: React.RefObject<HTMLDivElement>;
}

export interface InputAreaProps {
  value: string;
  isLoading: boolean;
  modelName: string;
  temperature: number;
  maxTokens: number;
  onChange: (value: string) => void;
  onSend: () => void;
  onKeyPress: (e: React.KeyboardEvent) => void;
}

export interface StreamingParams {
  message: string;
  messages: Message[];
  config: ChatConfig;
  onNewMessage: (message: Message) => void;
  onUpdateMessage: (messageId: number, content: string) => void;
  onStreamingStart: (messageId: number) => void;
  onStreamingEnd: () => void;
  onError: (error: Error) => void;
}

export interface ConfigPanelProps {
  config: ChatConfig;
  modelOptions: ModelOption[];
  onConfigChange: (config: Partial<ChatConfig>) => void;
  onReset: () => void;
  isVisible: boolean; // 新增：控制面板是否可见
  onToggleVisibility: () => void; // 新增：切换可见性回调
}

export interface HeaderProps {
  modelName: string;
  isLoading: boolean;
  onStop: () => void;
  onClear: () => void;
  onToggleConfig: () => void; // 新增：切换配置面板回调
  isConfigVisible: boolean; // 新增：配置面板是否可见
}