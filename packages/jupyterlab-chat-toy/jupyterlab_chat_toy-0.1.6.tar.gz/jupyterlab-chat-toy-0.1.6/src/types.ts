export interface Message {
  id: number;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  type: 'text' | 'code' | 'image';
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  currentStreamingMessage: Message | null;
  error?: string;
}

export interface AIRequest {
  model: string;
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  stream: boolean;
  temperature?: number;
  max_tokens?: number;
}

export interface AIStreamChunk {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    delta: {
      role?: string;
      content?: string;
    };
    finish_reason: string | null;
  }>;
}

// 在 types.ts 中，确保有 CellError 和 ErrorAnalysisRequest 类型
export interface CellError {
  ename: string;  // 错误类型
  evalue: string; // 错误信息
  traceback?: string[]; // 堆栈跟踪
}

export interface ErrorAnalysisRequest {
  error: CellError;
  context?: string; // 用户提供的额外上下文
  code?: string;    // 相关代码（可选）
}

