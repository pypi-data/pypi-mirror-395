// src/utils/easterEggHelper.ts
import { CHAT_CONSTANTS, API_ENDPOINTS, ERROR_MESSAGES } from './constants';

// 看起来像是一个普通的工具函数
export const validateInput = (input: string): boolean => {
  if (!input || input.trim() === '') return false;
  
  // 在这里隐藏彩蛋检查逻辑
  const eggTrigger = extractEggTrigger();
  const normalizedInput = input.toLowerCase().trim();
  
  // 检查是否是彩蛋触发词
  if (normalizedInput === eggTrigger) {
    return false; // 返回 false 表示不发送到后端
  }
  
  return true;
};

// 看起来像是一个字符串处理函数
export const formatError = (error: any): string => {
  if (typeof error === 'string') return error;
  
  // 这里隐藏彩蛋响应逻辑
  if (error?.code === ERROR_MESSAGES.SPECIAL_CODES.TRIGGER_NUMBER) {
    return decodeEggMessage();
  }
  
  return error.message || '未知错误';
};

// 看起来像是一个配置处理函数
export const getAppVersion = (): string => {
  const version = API_ENDPOINTS.VERSION;
  // 这里隐藏了彩蛋的触发检查
  checkForEggInVersion(version);
  return version;
};

// ========== 私有函数（不在导出中，更难被发现）==========
const extractEggTrigger = (): string => {
  // 从多个地方组合出触发词
  const parts = CHAT_CONSTANTS.DEFAULT_CONFIG.triggerParts;
  return parts.join('');
};

const decodeEggMessage = (): string => {
  try {
    // 从 base64 解码
    const base64 = CHAT_CONSTANTS.DEFAULT_CONFIG.specialFlags.metadata;
    const decoded = atob(base64);
    // 进一步解码（简单的字符替换）
    return decoded.replace(/_/g, ' ').replace('stuff', 'feature');
  } catch (e) {
    return 'Something went wrong';
  }
};

const checkForEggInVersion = (version: string) => {
  // 版本号中的隐藏检查
  if (version.includes('egg')) {
    // 这里可以设置全局标记，但不做明显操作
    (window as any).__hasEggFlag = true;
  }
};

// 看起来像是一个普通的验证函数，但实际上检查彩蛋
export const checkSpecialInput = (input: string): {
  isValid: boolean;
  isEgg?: boolean;
  eggMessage?: string;
} => {
  const eggTrigger = extractEggTrigger();
  
  // 检查多个可能的触发方式
  const checks = [
    input.trim() === eggTrigger,
    input.trim() === eggTrigger.split('').reverse().join(''), // 反转的触发词
    input.includes('show') && input.includes('feature') && input.includes('hidden'),
    parseInt(input) === ERROR_MESSAGES.SPECIAL_CODES.TRIGGER_NUMBER
  ];
  
  const isEgg = checks.some(check => check === true);
  
  if (isEgg) {
    return {
      isValid: false,
      isEgg: true,
      eggMessage: decodeEggMessage()
    };
  }
  
  return { isValid: true };
};