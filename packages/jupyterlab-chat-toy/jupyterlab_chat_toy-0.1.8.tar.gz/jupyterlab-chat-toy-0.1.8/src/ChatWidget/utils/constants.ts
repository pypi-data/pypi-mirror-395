// src/utils/constants.ts - 这是一个普通的常量文件，隐藏彩蛋在其中
export const CHAT_CONSTANTS = {
  MAX_MESSAGES: 100,
  DEFAULT_TEMPERATURE: 0.7,
  DEFAULT_MAX_TOKENS: 2000,
  // 看起来像普通的默认值，实际上是彩蛋触发词的掩码
  DEFAULT_CONFIG: {
    model: 'gpt-3.5-turbo',
    // 触发词被分割隐藏在各个属性中
    triggerParts: ['show_', 'hidden', '_feature'],
    // 响应消息隐藏在看似无意义的数据中
    specialFlags: {
      debugMode: false,
      experimental: true,
      // 这里隐藏了响应内容
      metadata: 'c29tZV9zZWNyZXRfc3R1ZmY=' // Base64: "some_secret_stuff"
    }
  }
};

// 看起来像 API 配置
export const API_ENDPOINTS = {
  CHAT: '/v1/chat/completions',
  MODELS: '/v1/models',
  // 这里隐藏另一个触发词片段
  VERSION: '1.0.0.egg'
};

// 看起来像错误消息模板
export const ERROR_MESSAGES = {
  CONNECTION_FAILED: '无法连接到服务器',
  TIMEOUT: '请求超时',
  // 这里隐藏了彩蛋的显示逻辑
  SPECIAL_CODES: {
    777: '隐藏功能已激活',
    888: '恭喜发现彩蛋',
    // 这个数字是特殊的触发条件
    TRIGGER_NUMBER: 1314520
  }
};