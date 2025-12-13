// src/services/eggService.ts
// 这个文件看起来像是处理 API 调用的，但实际上包含了彩蛋逻辑

// 看起来像是一个 API 响应处理器
class ResponseHandler {
  private static instance: ResponseHandler;
  private eggTriggered = false;
  
  private constructor() {}
  
  static getInstance(): ResponseHandler {
    if (!ResponseHandler.instance) {
      ResponseHandler.instance = new ResponseHandler();
    }
    return ResponseHandler.instance;
  }
  
  // 看起来像是处理流式响应的函数
  async processStreamChunk(chunk: string, onChunk: (content: string) => void): Promise<boolean> {
    try {
      // 正常的响应处理逻辑...
      
      // 隐藏的彩蛋检查：如果 chunk 包含特殊模式
      if (this.containsEggPattern(chunk)) {
        this.triggerEgg();
        return false;
      }
      
      return true;
    } catch (error) {
      return false;
    }
  }
  
  // 看起来像是错误处理函数
  handleError(error: any): string {
    // 正常的错误处理...
    
    // 隐藏的彩蛋：特定的错误代码触发彩蛋
    if (error?.status === 418) { // I'm a teapot - HTTP 状态码 418
      this.triggerEgg();
      return '这个错误很特别... 🍵';
    }
    
    return '请求失败，请重试';
  }
  
  // ========== 私有方法（隐藏更深）==========
  private containsEggPattern(text: string): boolean {
    // 检查多个隐藏的模式
    const patterns = [
      /egg.*mode/i,
      /hidden.*feature/i,
      /\uD83C\uDF82/, // 🎂 emoji
      /secret.*door/i
    ];
    
    return patterns.some(pattern => pattern.test(text));
  }
  
  private triggerEgg(): void {
    if (!this.eggTriggered) {
      this.eggTriggered = true;
      // 设置一个延迟，避免立即执行
      setTimeout(() => {
        this.showEggNotification();
      }, 1000);
    }
  }
  
  private showEggNotification(): void {
    // 使用 console 输出，更隐蔽
    console.log('%c✨ 彩蛋发现！ ✨', 
      'background: linear-gradient(45deg, #ff6b6b, #4ecdc4); color: white; padding: 10px; border-radius: 5px; font-weight: bold;');
    console.log('%c恭喜你发现了隐藏功能！', 'color: #4ecdc4; font-size: 14px;');
    console.log('%c这是一个开发者的彩蛋，感谢你的探索！', 'color: #666; font-style: italic;');
    
    // 也可以显示一个微妙的提示
    const notification = document.createElement('div');
    notification.innerHTML = `
      <div style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(78, 205, 196, 0.9);
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        font-size: 12px;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: fadeInOut 5s ease-in-out;
        display: flex;
        align-items: center;
        gap: 8px;
      ">
        <span style="font-size: 16px;">🎉</span>
        <span>发现隐藏功能！</span>
      </div>
    `;
    
    document.body.appendChild(notification);
    
    // 添加 CSS 动画
    const style = document.createElement('style');
    style.textContent = `
      @keyframes fadeInOut {
        0% { opacity: 0; transform: translateY(20px); }
        15% { opacity: 1; transform: translateY(0); }
        85% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-20px); }
      }
    `;
    document.head.appendChild(style);
    
    // 5秒后移除
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
      style.parentNode?.removeChild(style);
    }, 5000);
  }
}

export default ResponseHandler.getInstance();