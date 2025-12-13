// src/utils/errorAnalyzer.ts
import { INotebookTracker } from '@jupyterlab/notebook';
import { CellError } from '../types';

// JupyterLab 3.x 的输出类型
interface NotebookOutput {
  output_type: string;
  ename?: string;
  evalue?: string;
  traceback?: string[];
  name?: string;
  text?: string | string[];
  data?: {
    [key: string]: any;
  };
  metadata?: {
    [key: string]: any;
  };
}

// 安全地处理 outputs，确保它是数组
const safeGetOutputs = (cellModel: any): NotebookOutput[] => {
  if (!cellModel || typeof cellModel !== 'object') {
    return [];
  }
  
  const outputs = cellModel.outputs;
  
  // 如果 outputs 不存在或为 null/undefined，返回空数组
  if (!outputs) {
    return [];
  }
  
  // 如果已经是数组，直接返回
  if (Array.isArray(outputs)) {
    return outputs as NotebookOutput[];
  }
  
  // 尝试转换非数组对象为数组
  try {
    // 如果 outputs 有 toArray 方法（某些 Jupyter 版本）
    if (typeof outputs.toArray === 'function') {
      const arr = outputs.toArray();
      return Array.isArray(arr) ? arr : [];
    }
    
    // 如果 outputs 是类似数组的对象（有 length 属性）
    if (outputs.length !== undefined) {
      return Array.from(outputs);
    }
    
    // 如果 outputs 是单个对象，包装成数组
    if (typeof outputs === 'object') {
      return [outputs as NotebookOutput];
    }
  } catch (error) {
    console.error('Failed to convert outputs to array:', error);
  }
  
  return [];
};

// 获取当前活动单元格的错误信息 - 兼容 JupyterLab 3.2.9
export const getCurrentCellErrors = (notebookTracker: INotebookTracker | null): CellError[] | null => {
  if (!notebookTracker) {
    console.warn('Notebook tracker not available');
    return null;
  }

  const current = notebookTracker.currentWidget;
  if (!current) {
    console.warn('No active notebook found');
    return null;
  }

  const { content } = current;
  const activeCell = content.activeCell;
  
  if (!activeCell) {
    console.warn('No active cell found');
    return null;
  }

  const cellModel = activeCell.model as any;
  
  // 使用安全的 outputs 获取方法
  const outputs = safeGetOutputs(cellModel);
  
  console.log('Cell outputs:', outputs); // 调试信息
  
  if (outputs.length === 0) {
    return null;
  }

  const errors: CellError[] = [];

  outputs.forEach((output: NotebookOutput) => {
    try {
      // 处理错误输出
      if (output.output_type === 'error') {
        const error: CellError = {
          ename: output.ename || 'UnknownError',
          evalue: output.evalue || 'Unknown error occurred',
          traceback: output.traceback || []
        };
        errors.push(error);
      }
      
      // 检查流输出中的错误
      if (output.output_type === 'stream' && output.name === 'stderr') {
        let errorText = '';
        
        if (Array.isArray(output.text)) {
          errorText = output.text.join('');
        } else if (typeof output.text === 'string') {
          errorText = output.text;
        }
        
        if (errorText.trim()) {
          errors.push({
            ename: 'StreamError',
            evalue: errorText.trim(),
            traceback: []
          });
        }
      }
      
      // 检查 display_data 中的错误
      if (output.output_type === 'display_data' && output.data) {
        const textData = output.data['text/plain'] || output.data['text/html'];
        if (typeof textData === 'string' && (textData.includes('Error') || textData.includes('Exception'))) {
          errors.push({
            ename: 'DisplayError',
            evalue: textData.substring(0, 500), // 限制长度
            traceback: []
          });
        }
      }
    } catch (error) {
      console.warn('Error processing cell output:', error, output);
    }
  });

  return errors.length > 0 ? errors : null;
};

// 获取当前单元格的代码内容 - 兼容 JupyterLab 3.2.9
export const getCurrentCellCode = (notebookTracker: INotebookTracker | null): string | null => {
  if (!notebookTracker) return null;
  
  const current = notebookTracker.currentWidget;
  if (!current) return null;
  
  const activeCell = current.content.activeCell;
  if (!activeCell || activeCell.model.type !== 'code') return null;
  
  const cellModel = activeCell.model as any;
  
  let code = '';
  
  try {
    // 方法1: value.text（旧版本）
    if (cellModel.value && cellModel.value.text !== undefined) {
      code = cellModel.value.text;
    } 
    // 方法2: sharedModel.getSource() 或 sharedModel.source
    else if (cellModel.sharedModel) {
      if (typeof cellModel.sharedModel.getSource === 'function') {
        code = cellModel.sharedModel.getSource();
      } else if (cellModel.sharedModel.source !== undefined) {
        code = cellModel.sharedModel.source;
      }
    }
    // 方法3: 直接访问 source 属性
    else if (cellModel.source !== undefined) {
      code = typeof cellModel.source === 'string' ? cellModel.source : '';
    }
    // 方法4: 尝试其他可能的属性
    else if (cellModel.getSource && typeof cellModel.getSource === 'function') {
      code = cellModel.getSource();
    }
  } catch (error) {
    console.warn('Error getting cell code:', error);
  }
  
  return code || null;
};

// 构建错误分析提示词
export const buildErrorAnalysisPrompt = (
  error: CellError, 
  userContext?: string,
  code?: string
): string => {
  let prompt = `请帮我分析并解决以下Python代码错误：\n\n`;
  
  prompt += `错误类型：${error.ename}\n`;
  prompt += `错误信息：${error.evalue}\n\n`;
  
  if (error.traceback && error.traceback.length > 0) {
    prompt += `堆栈跟踪（最近的部分）：\n`;
    const recentTraceback = error.traceback.slice(-3);
    recentTraceback.forEach(line => {
      prompt += `${line}\n`;
    });
    prompt += '\n';
  }
  
  if (code) {
    prompt += `相关代码：\n\`\`\`python\n${code}\n\`\`\`\n\n`;
  }
  
  if (userContext) {
    prompt += `额外上下文：${userContext}\n\n`;
  }
  
  prompt += `请按以下格式回答：
1. 错误原因分析
2. 解决方案（步骤清晰）
3. 修复后的代码示例（如果有）
4. 预防类似错误的建议

如果错误信息不足，请告诉我需要哪些额外信息来进一步分析。`;
  
  return prompt;
};

// 处理 /fix 命令
export const handleFixCommand = (
  notebookTracker: INotebookTracker | null,
  userInput: string
): { 
  shouldContinue: boolean; 
  analysisPrompt?: string; 
  error?: string;
} => {
  console.log('handleFixCommand called with input:', userInput); // 调试信息
  
  if (!userInput.trim().startsWith('/fix')) {
    return { shouldContinue: true };
  }
  
  // 获取额外上下文（/fix 后面的内容）
  const context = userInput.trim().substring(4).trim();
  
  // 检查是否有活动的 notebook
  if (!notebookTracker || !notebookTracker.currentWidget) {
    return { 
      shouldContinue: false, 
      error: '没有活动的Notebook。请先打开一个Notebook文件。'
    };
  }
  
  const current = notebookTracker.currentWidget;
  
  // 检查是否有活动的单元格
  if (!current.content.activeCell) {
    return { 
      shouldContinue: false, 
      error: '没有活动的单元格。请先点击一个代码单元格。'
    };
  }
  
  // 检查是否是代码单元格
  if (current.content.activeCell.model.type !== 'code') {
    return { 
      shouldContinue: false, 
      error: '当前单元格不是代码单元格。请选择一个代码单元格。'
    };
  }
  
  // 获取当前单元格的错误
  const errors = getCurrentCellErrors(notebookTracker);
  
  console.log('Found errors:', errors); // 调试信息
  
  if (!errors || errors.length === 0) {
    // 尝试获取代码内容，看看是否有代码
    const code = getCurrentCellCode(notebookTracker);
    if (code) {
      // 即使没有错误，用户也可能想分析代码
      const analysisPrompt = `请帮我分析以下Python代码，看看是否有潜在问题或改进建议：\n\n\`\`\`python\n${code}\n\`\`\`\n\n${context ? `额外上下文：${context}\n\n` : ''}请提供代码分析和改进建议。`;
      
      return {
        shouldContinue: false,
        analysisPrompt
      };
    }
    
    return { 
      shouldContinue: false, 
      error: '当前活动单元格没有错误信息。请先执行包含错误的代码单元格，并确保它处于活动状态。'
    };
  }
  
  // 使用第一个错误进行分析
  const primaryError = errors[0];
  const code = getCurrentCellCode(notebookTracker);
  
  // 构建分析提示词
  const analysisPrompt = buildErrorAnalysisPrompt(primaryError, context, code);
  
  return {
    shouldContinue: false,
    analysisPrompt
  };
};

// 添加一个辅助函数来检查是否支持错误检测
export const isErrorDetectionSupported = (notebookTracker: INotebookTracker | null): boolean => {
  if (!notebookTracker) return false;
  
  try {
    const current = notebookTracker.currentWidget;
    if (!current) return true; // 没有活动的notebook不代表不支持
    
    const activeCell = current.content.activeCell;
    if (!activeCell) return true;
    
    const cellModel = activeCell.model as any;
    
    // 尝试访问模型属性，但不要抛出错误
    if (cellModel.outputs !== undefined) {
      // 检查是否可迭代
      const outputs = cellModel.outputs;
      return outputs !== null && (Array.isArray(outputs) || 
             typeof outputs === 'object' && outputs.length !== undefined);
    }
    
    return false;
  } catch (error) {
    console.warn('Error detection compatibility check failed:', error);
    return false;
  }
};

// 添加调试函数，帮助了解单元格结构
export const debugCellStructure = (notebookTracker: INotebookTracker | null): any => {
  if (!notebookTracker || !notebookTracker.currentWidget) return null;
  
  const current = notebookTracker.currentWidget;
  if (!current.content.activeCell) return null;
  
  const cellModel = current.content.activeCell.model as any;
  
  // 返回单元格模型的结构信息（不包含实际内容）
  return {
    type: cellModel.type,
    hasOutputs: cellModel.outputs !== undefined,
    outputsType: typeof cellModel.outputs,
    outputsIsArray: Array.isArray(cellModel.outputs),
    outputsLength: cellModel.outputs ? (Array.isArray(cellModel.outputs) ? cellModel.outputs.length : 'not an array') : 0,
    hasValue: cellModel.value !== undefined,
    hasSharedModel: cellModel.sharedModel !== undefined,
    hasSource: cellModel.source !== undefined,
    keys: Object.keys(cellModel).filter(key => !key.startsWith('_'))
  };
};