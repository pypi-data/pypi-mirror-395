"use strict";
(self["webpackChunkjupyterlab_chat_toy"] = self["webpackChunkjupyterlab_chat_toy"] || []).push([["lib_index_js"],{

/***/ "./lib/MessageContent.js":
/*!*******************************!*\
  !*** ./lib/MessageContent.js ***!
  \*******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MessageContent = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const MessageContent = ({ content, onInsertCode }) => {
    const handleInsertCode = (code, language) => {
        if (onInsertCode) {
            onInsertCode(code, language);
        }
    };
    // 渲染代码块
    const renderCodeBlock = (codeContent, language = 'text') => {
        return (react_1.default.createElement("div", { style: {
                position: 'relative',
                margin: '8px 0'
            } },
            onInsertCode && (react_1.default.createElement("button", { onClick: () => handleInsertCode(codeContent, language), style: {
                    position: 'absolute',
                    top: '4px',
                    right: '4px',
                    background: 'var(--jp-brand-color1)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '3px',
                    padding: '2px 6px',
                    fontSize: '10px',
                    cursor: 'pointer',
                    zIndex: 10
                }, title: "\u63D2\u5165\u5230Jupyter\u5355\u5143\u683C" }, "\u63D2\u5165\u4EE3\u7801")),
            react_1.default.createElement("pre", { style: {
                    background: 'var(--jp-code-cell-background)',
                    border: '1px solid var(--jp-border-color1)',
                    borderRadius: '4px',
                    padding: '8px',
                    overflowX: 'auto',
                    fontFamily: 'var(--jp-code-font-family)',
                    fontSize: 'var(--jp-code-font-size)',
                    lineHeight: 'var(--jp-code-line-height)',
                    margin: 0
                } },
                react_1.default.createElement("code", { style: {
                        color: 'var(--jp-content-font-color1)',
                        display: 'block'
                    } }, codeContent))));
    };
    // 渲染表格
    const renderTable = (tableContent) => {
        const lines = tableContent.split('\n').filter(line => line.trim());
        if (lines.length < 2)
            return null;
        try {
            const headers = lines[0]
                .split('|')
                .filter(cell => cell.trim() !== '')
                .map(header => header.trim());
            const rows = lines.slice(2) // 跳过表头和分隔线
                .map(line => line.split('|')
                .filter(cell => cell.trim() !== '')
                .map(cell => cell.trim()))
                .filter(row => row.length > 0);
            return (react_1.default.createElement("div", { style: {
                    overflowX: 'auto',
                    margin: '12px 0'
                } },
                react_1.default.createElement("table", { style: {
                        borderCollapse: 'collapse',
                        width: '100%',
                        minWidth: '400px',
                        border: '1px solid var(--jp-border-color1)',
                        fontSize: '12px'
                    } },
                    react_1.default.createElement("thead", null,
                        react_1.default.createElement("tr", { style: { backgroundColor: 'var(--jp-layout-color2)' } }, headers.map((header, index) => (react_1.default.createElement("th", { key: index, style: {
                                border: '1px solid var(--jp-border-color1)',
                                padding: '8px 12px',
                                textAlign: 'left',
                                fontWeight: 'bold'
                            } }, header))))),
                    react_1.default.createElement("tbody", null, rows.map((row, rowIndex) => (react_1.default.createElement("tr", { key: rowIndex, style: {
                            borderBottom: '1px solid var(--jp-border-color2)'
                        } }, row.map((cell, cellIndex) => (react_1.default.createElement("td", { key: cellIndex, style: {
                            border: '1px solid var(--jp-border-color1)',
                            padding: '8px 12px',
                            textAlign: 'left'
                        } }, cell))))))))));
        }
        catch (error) {
            console.error('表格渲染错误:', error);
            return react_1.default.createElement("div", { style: { whiteSpace: 'pre-wrap' } }, tableContent);
        }
    };
    // 主渲染函数
    const renderContent = () => {
        if (!content)
            return null;
        try {
            // 分割代码块和普通文本
            const parts = content.split(/(```[\s\S]*?```)/g);
            return parts.map((part, index) => {
                // 代码块
                if (part.startsWith('```') && part.endsWith('```')) {
                    const codeMatch = part.match(/```(\w+)?\n?([\s\S]*?)```/);
                    if (codeMatch) {
                        const language = codeMatch[1] || 'text';
                        const codeContent = codeMatch[2].trim();
                        return react_1.default.createElement("div", { key: index }, renderCodeBlock(codeContent, language));
                    }
                }
                // 表格检测
                const tableMatch = part.match(/(\|[^\n]+\|\r?\n\|[-:\s|]+\|\r?\n(?:\|[^\n]+\|\r?\n)*)/);
                if (tableMatch) {
                    return react_1.default.createElement("div", { key: index }, renderTable(tableMatch[0]));
                }
                // 普通文本
                return (react_1.default.createElement("div", { key: index, style: {
                        lineHeight: '1.5',
                        margin: '4px 0',
                        whiteSpace: 'pre-wrap'
                    } }, part));
            });
        }
        catch (error) {
            console.error('内容渲染错误:', error);
            return react_1.default.createElement("div", { style: { whiteSpace: 'pre-wrap' } }, content);
        }
    };
    return (react_1.default.createElement("div", { style: {
            lineHeight: '1.5',
            fontSize: '13px',
            fontFamily: 'var(--jp-ui-font-family)'
        } }, renderContent()));
};
exports.MessageContent = MessageContent;


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.chatIcon = void 0;
const ui_components_1 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
// 简单的聊天图标 SVG
const chatIconSvg = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
</svg>
`;
exports.chatIcon = new ui_components_1.LabIcon({
    name: 'jupyterlab-chat:chat',
    svgstr: chatIconSvg
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
const application_1 = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const launcher_1 = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
const settingregistry_1 = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
const notebook_1 = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
const icons_1 = __webpack_require__(/*! ./icons */ "./lib/icons.js");
const widget_1 = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/**
 * The command IDs used by the chat plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'jupyterlab-chat:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the jupyterlab-chat extension.
 */
const plugin = {
    id: 'jupyterlab-chat:plugin',
    autoStart: true,
    requires: [apputils_1.ICommandPalette, notebook_1.INotebookTracker],
    optional: [launcher_1.ILauncher, application_1.ILayoutRestorer, settingregistry_1.ISettingRegistry],
    activate: (app, palette, notebookTracker, launcher, restorer, settingRegistry) => {
        const { commands, shell } = app;
        // Create a widget tracker for the left sidebar
        const tracker = new apputils_1.WidgetTracker({
            namespace: 'jupyterlab-chat-sidebar'
        });
        // Create the chat widget
        let chatWidget = null;
        // Add command to open chat in sidebar
        commands.addCommand(CommandIDs.open, {
            label: 'AI Chat',
            caption: 'Open AI Chat Interface in Sidebar',
            icon: icons_1.chatIcon,
            execute: () => {
                if (!chatWidget || chatWidget.isDisposed) {
                    // Create the chat widget if it doesn't exist
                    chatWidget = new widget_1.ChatWidget(notebookTracker);
                    chatWidget.id = 'jupyterlab-chat-sidebar';
                    chatWidget.title.label = 'AI Chat';
                    chatWidget.title.closable = true;
                    chatWidget.title.icon = icons_1.chatIcon;
                    // Add to tracker
                    tracker.add(chatWidget);
                    // Add to left sidebar
                    shell.add(chatWidget, 'left', { rank: 800 });
                }
                // Activate the widget
                shell.activateById(chatWidget.id);
            }
        });
        // Add to command palette
        palette.addItem({
            command: CommandIDs.open,
            category: 'AI'
        });
        // Add to launcher if available
        if (launcher) {
            launcher.add({
                command: CommandIDs.open,
                category: 'AI'
            });
        }
        // Restore widget state if restorer is available
        if (restorer) {
            restorer.restore(tracker, {
                command: CommandIDs.open,
                name: () => 'jupyterlab-chat-sidebar'
            });
        }
        // Load settings if available
        if (settingRegistry) {
            Promise.all([settingRegistry.load(plugin.id), app.restored])
                .then(([settings]) => {
                console.log('jupyterlab-chat settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.warn('Failed to load settings for jupyterlab-chat, using defaults.', reason);
            });
        }
    }
};
exports["default"] = plugin;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ChatWidget = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const MessageContent_1 = __webpack_require__(/*! ./MessageContent */ "./lib/MessageContent.js");
const notebook_1 = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
class ChatWidget extends apputils_1.ReactWidget {
    constructor(notebookTracker) {
        super();
        this.notebookTracker = notebookTracker;
        this.id = 'ai-chat-widget';
        this.title.label = 'AI Chat';
        this.title.closable = true;
        this.addClass('jp-ChatWidget');
    }
    render() {
        return react_1.default.createElement(ChatComponent, { notebookTracker: this.notebookTracker });
    }
}
exports.ChatWidget = ChatWidget;
const ChatComponent = ({ notebookTracker }) => {
    const [messages, setMessages] = react_1.useState([
        {
            id: 1,
            content: '你好！我是 AI 助手。现在支持流式输出和模型切换，体验更佳。',
            sender: 'ai',
            timestamp: new Date(),
            type: 'text'
        }
    ]);
    const [inputValue, setInputValue] = react_1.useState('');
    const [isLoading, setIsLoading] = react_1.useState(false);
    const [backendUrl, setBackendUrl] = react_1.useState('http://localhost:8888/v1/chat/completions');
    const [modelName, setModelName] = react_1.useState('/mnt/e/qwen3-1.7b');
    const [customModelName, setCustomModelName] = react_1.useState('');
    const [temperature, setTemperature] = react_1.useState(0.7);
    const [maxTokens, setMaxTokens] = react_1.useState(2000);
    const [currentStreamingMessageId, setCurrentStreamingMessageId] = react_1.useState(null);
    // 添加智能滚动相关状态和引用
    const [shouldAutoScroll, setShouldAutoScroll] = react_1.useState(true);
    const messagesEndRef = react_1.useRef(null);
    const messagesContainerRef = react_1.useRef(null);
    const abortControllerRef = react_1.useRef(null);
    // 添加组件挂载状态跟踪
    const isMountedRef = react_1.useRef(true);
    react_1.useEffect(() => {
        return () => {
            isMountedRef.current = false;
        };
    }, []);
    const modelOptions = [
        { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
        { value: 'gpt-4', label: 'GPT-4' },
        { value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
        { value: 'claude-3-sonnet', label: 'Claude 3 Sonnet' },
        { value: 'claude-3-opus', label: 'Claude 3 Opus' },
        { value: 'llama-2-7b', label: 'Llama 2 7B' },
        { value: 'llama-2-13b', label: 'Llama 2 13B' },
        { value: 'llama-2-70b', label: 'Llama 2 70B' },
        { value: 'custom', label: '自定义模型' }
    ];
    const getActualModelName = () => {
        return modelName === 'custom' ? customModelName : modelName;
    };
    const insertCodeToNotebook = (code, language) => {
        if (!notebookTracker) {
            console.error('Notebook tracker not available');
            alert('错误：未找到活动的Notebook');
            return;
        }
        const current = notebookTracker.currentWidget;
        if (!current) {
            alert('错误：请先打开一个Notebook');
            return;
        }
        const { content } = current;
        const { activeCellIndex } = content;
        console.log('当前活动单元格索引:', activeCellIndex);
        console.log('要插入的代码:', code);
        try {
            // 在活动单元格下方插入新的代码单元格
            notebook_1.NotebookActions.insertBelow(content);
            // 获取新插入的单元格
            const newCellIndex = activeCellIndex + 1;
            const newCell = content.widgets[newCellIndex];
            console.log('新单元格索引:', newCellIndex);
            console.log('新单元格:', newCell);
            if (newCell && newCell.model.type === 'code') {
                console.log('单元格模型:', newCell.model);
                console.log('可用属性:', Object.keys(newCell.model));
                // 尝试设置代码内容
                if (newCell.model.value && newCell.model.value.text !== undefined) {
                    newCell.model.value.text = code;
                    console.log('使用 value.text 设置代码');
                }
                else if (newCell.model.sharedModel && newCell.model.sharedModel.setSource) {
                    newCell.model.sharedModel.setSource(code);
                    console.log('使用 sharedModel.setSource 设置代码');
                }
                else {
                    console.error('无法找到设置代码的方法');
                    alert('无法设置代码内容');
                    return;
                }
                // 激活新单元格
                content.activeCellIndex = newCellIndex;
                console.log('代码已插入到Notebook');
            }
            else {
                console.error('新单元格不是代码单元格或未找到');
            }
        }
        catch (error) {
            console.error('插入代码失败:', error);
            alert('插入代码失败，请重试');
        }
    };
    // 智能滚动函数
    const smartScrollToBottom = (behavior = 'smooth') => {
        if (!isMountedRef.current || !shouldAutoScroll)
            return;
        requestAnimationFrame(() => {
            if (messagesEndRef.current && isMountedRef.current) {
                messagesEndRef.current.scrollIntoView({
                    behavior,
                    block: 'nearest'
                });
            }
        });
    };
    // 检查用户是否在底部
    const isUserAtBottom = () => {
        if (!messagesContainerRef.current)
            return true;
        const container = messagesContainerRef.current;
        const threshold = 100; // 距离底部100px以内都算在底部
        return container.scrollHeight - container.scrollTop - container.clientHeight <= threshold;
    };
    // 处理容器滚动事件
    const handleMessagesScroll = () => {
        if (!messagesContainerRef.current)
            return;
        const atBottom = isUserAtBottom();
        // 只有当用户主动滚动到底部时才重新启用自动滚动
        if (atBottom && !shouldAutoScroll) {
            setShouldAutoScroll(true);
        }
        else if (!atBottom && shouldAutoScroll) {
            setShouldAutoScroll(false);
        }
    };
    // 修改现有的 scrollToBottom 函数
    const scrollToBottom = () => {
        smartScrollToBottom('smooth');
    };
    // 修改 useEffect，添加滚动事件监听
    react_1.useEffect(() => {
        const container = messagesContainerRef.current;
        if (container) {
            container.addEventListener('scroll', handleMessagesScroll);
            return () => {
                container.removeEventListener('scroll', handleMessagesScroll);
            };
        }
    }, [shouldAutoScroll]);
    // 修改消息更新时的滚动逻辑
    react_1.useEffect(() => {
        if (messages.length > 0) {
            // 只有当应该自动滚动时才滚动
            if (shouldAutoScroll) {
                smartScrollToBottom('smooth');
            }
        }
    }, [messages, shouldAutoScroll]);
    const streamToAI = async (message) => {
        abortControllerRef.current = new AbortController();
        try {
            if (!isMountedRef.current)
                return;
            const newMessageId = Date.now() + 1;
            const newMessage = {
                id: newMessageId,
                content: '',
                sender: 'ai',
                timestamp: new Date(),
                type: 'text'
            };
            if (isMountedRef.current) {
                setMessages(prev => [...prev, newMessage]);
                setCurrentStreamingMessageId(newMessageId);
            }
            const actualModelName = getActualModelName();
            const requestBody = {
                model: actualModelName,
                messages: [
                    ...messages.slice(-10).map(m => ({
                        role: m.sender === 'user' ? 'user' : 'assistant',
                        content: m.content
                    })),
                    {
                        role: 'user',
                        content: message
                    }
                ],
                stream: true,
                temperature: temperature,
                max_tokens: maxTokens
            };
            console.log('Sending streaming request to:', backendUrl);
            console.log('Using model:', actualModelName);
            console.log('Request parameters:', {
                temperature,
                maxTokens
            });
            const response = await fetch(backendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
                mode: 'cors',
                signal: abortControllerRef.current.signal
            });
            console.log('Response status:', response.status);
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`HTTP ${response.status}: ${response.statusText}. ${errorText}`);
            }
            await processStreamResponse(response, newMessageId);
        }
        catch (error) {
            if (!isMountedRef.current)
                return;
            if (error.name === 'AbortError') {
                console.log('Request was aborted');
                return;
            }
            console.error('Error in streaming AI call:', error);
            if (currentStreamingMessageId && isMountedRef.current) {
                setMessages(prev => prev.map(msg => msg.id === currentStreamingMessageId
                    ? { ...msg, content: `请求失败: ${error.message}` }
                    : msg));
            }
            throw error;
        }
        finally {
            if (isMountedRef.current) {
                abortControllerRef.current = null;
                setCurrentStreamingMessageId(null);
            }
        }
    };
    // 修改 processStreamResponse 函数，添加更智能的滚动
    const processStreamResponse = async (response, messageId) => {
        var _a;
        const reader = (_a = response.body) === null || _a === void 0 ? void 0 : _a.getReader();
        const decoder = new TextDecoder();
        if (!reader) {
            throw new Error('No reader available for stream');
        }
        let accumulatedContent = '';
        let buffer = '';
        let lastScrollTime = 0;
        const scrollThrottle = 300; // 每300ms最多滚动一次
        try {
            while (true) {
                const { done, value } = await reader.read();
                if (!isMountedRef.current) {
                    reader.releaseLock();
                    return;
                }
                if (done) {
                    break;
                }
                const chunk = decoder.decode(value, { stream: true });
                buffer += chunk;
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';
                for (const line of lines) {
                    const trimmedLine = line.trim();
                    if (trimmedLine === '')
                        continue;
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
                                    if (isMountedRef.current) {
                                        setMessages(prev => prev.map(msg => msg.id === messageId
                                            ? { ...msg, content: accumulatedContent, timestamp: new Date() }
                                            : msg));
                                        // 节流滚动：只在需要时且一段时间内没有滚动过才滚动
                                        const now = Date.now();
                                        if (shouldAutoScroll && now - lastScrollTime > scrollThrottle) {
                                            smartScrollToBottom('smooth');
                                            lastScrollTime = now;
                                        }
                                    }
                                }
                            }
                        }
                        catch (e) {
                            console.warn('Failed to parse stream data:', e, 'Data:', trimmedLine);
                        }
                    }
                }
            }
        }
        finally {
            reader.releaseLock();
            // 流结束时确保滚动到底部（如果应该自动滚动）
            if (isMountedRef.current && shouldAutoScroll) {
                smartScrollToBottom('smooth');
            }
        }
    };
    const stopStreaming = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            if (isMountedRef.current) {
                setIsLoading(false);
                setCurrentStreamingMessageId(null);
            }
        }
    };
    // 修改 handleSend 函数，发送消息时强制滚动到底部
    const handleSend = async () => {
        if (!inputValue.trim() || isLoading)
            return;
        const userMessage = {
            id: Date.now(),
            content: inputValue,
            sender: 'user',
            timestamp: new Date(),
            type: 'text'
        };
        if (!isMountedRef.current)
            return;
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);
        // 用户发送消息时强制滚动到底部
        setShouldAutoScroll(true);
        smartScrollToBottom('smooth');
        try {
            await streamToAI(inputValue);
        }
        catch (error) {
            if (isMountedRef.current) {
                console.error('Streaming failed:', error);
                const errorMessage = {
                    id: Date.now() + 1,
                    content: `请求失败: ${error instanceof Error ? error.message : '未知错误'}`,
                    sender: 'ai',
                    timestamp: new Date(),
                    type: 'text'
                };
                setMessages(prev => [...prev, errorMessage]);
            }
        }
        finally {
            if (isMountedRef.current) {
                setIsLoading(false);
            }
        }
    };
    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };
    const formatTime = (date) => {
        return date.toLocaleTimeString('zh-CN', {
            hour: '2-digit',
            minute: '2-digit'
        });
    };
    // 添加手动滚动到底部的功能
    const scrollToBottomManually = () => {
        setShouldAutoScroll(true);
        smartScrollToBottom('smooth');
    };
    const clearChat = () => {
        stopStreaming();
        if (isMountedRef.current) {
            setMessages([
                {
                    id: 1,
                    content: '对话已清空。现在支持流式输出和模型切换，体验更佳。',
                    sender: 'ai',
                    timestamp: new Date(),
                    type: 'text'
                }
            ]);
            setCurrentStreamingMessageId(null);
        }
    };
    const updateBackendUrl = (e) => {
        setBackendUrl(e.target.value);
    };
    const updateModelName = (e) => {
        setModelName(e.target.value);
    };
    const updateCustomModelName = (e) => {
        setCustomModelName(e.target.value);
    };
    const updateTemperature = (e) => {
        setTemperature(parseFloat(e.target.value));
    };
    const updateMaxTokens = (e) => {
        setMaxTokens(parseInt(e.target.value, 10));
    };
    const resetSettings = () => {
        setModelName('gpt-3.5-turbo');
        setCustomModelName('');
        setTemperature(0.7);
        setMaxTokens(2000);
    };
    const isMessageStreaming = (messageId) => {
        return currentStreamingMessageId === messageId;
    };
    const actualModelName = getActualModelName();
    return (react_1.default.createElement("div", { style: {
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            fontFamily: 'var(--jp-ui-font-family)',
            fontSize: 'var(--jp-ui-font-size1)',
            background: 'var(--jp-layout-color0)'
        } },
        react_1.default.createElement("div", { style: {
                background: 'var(--jp-brand-color1)',
                color: 'white',
                padding: '8px 12px',
                display: 'flex',
                alignItems: 'center',
                borderBottom: '1px solid var(--jp-border-color1)',
                justifyContent: 'space-between'
            } },
            react_1.default.createElement("div", { style: { display: 'flex', alignItems: 'center' } },
                react_1.default.createElement("span", { style: { fontWeight: 'bold', fontSize: '14px', marginRight: '8px' } }, "\uD83E\uDD16 AI \u804A\u5929 (\u6D41\u5F0F\u8F93\u51FA)"),
                react_1.default.createElement("div", { style: {
                        background: 'rgba(255,255,255,0.2)',
                        padding: '2px 6px',
                        borderRadius: '8px',
                        fontSize: '11px',
                    } }, actualModelName)),
            react_1.default.createElement("div", { style: { display: 'flex', gap: '8px' } },
                isLoading && (react_1.default.createElement("button", { onClick: stopStreaming, style: {
                        background: 'rgba(255,255,255,0.2)',
                        border: '1px solid rgba(255,255,255,0.3)',
                        color: 'white',
                        borderRadius: '4px',
                        padding: '2px 6px',
                        fontSize: '11px',
                        cursor: 'pointer'
                    }, title: "\u505C\u6B62\u751F\u6210" }, "\u505C\u6B62")),
                react_1.default.createElement("button", { onClick: clearChat, style: {
                        background: 'transparent',
                        border: '1px solid rgba(255,255,255,0.3)',
                        color: 'white',
                        borderRadius: '4px',
                        padding: '2px 6px',
                        fontSize: '11px',
                        cursor: 'pointer'
                    }, title: "\u6E05\u7A7A\u5BF9\u8BDD" }, "\u6E05\u7A7A"))),
        react_1.default.createElement("div", { style: {
                padding: '8px 12px',
                borderBottom: '1px solid var(--jp-border-color1)',
                background: 'var(--jp-layout-color1)'
            } },
            react_1.default.createElement("div", { style: { marginBottom: '8px' } },
                react_1.default.createElement("div", { style: { fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' } }, "\u540E\u7AEF\u670D\u52A1\u5730\u5740:"),
                react_1.default.createElement("input", { type: "text", value: backendUrl, onChange: updateBackendUrl, style: {
                        width: '100%',
                        padding: '4px 8px',
                        border: '1px solid var(--jp-border-color1)',
                        borderRadius: '4px',
                        fontSize: '12px',
                        background: 'var(--jp-input-background)',
                        color: 'var(--jp-ui-font-color1)'
                    }, placeholder: "\u8F93\u5165\u540E\u7AEF\u670D\u52A1 URL" })),
            react_1.default.createElement("div", { style: { marginBottom: '8px' } },
                react_1.default.createElement("div", { style: { fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' } }, "\u6A21\u578B\u9009\u62E9:"),
                react_1.default.createElement("select", { value: modelName, onChange: updateModelName, style: {
                        width: '100%',
                        padding: '4px 8px',
                        border: '1px solid var(--jp-border-color1)',
                        borderRadius: '4px',
                        fontSize: '12px',
                        background: 'var(--jp-input-background)',
                        color: 'var(--jp-ui-font-color1)'
                    } }, modelOptions.map(option => (react_1.default.createElement("option", { key: option.value, value: option.value }, option.label))))),
            modelName === 'custom' && (react_1.default.createElement("div", { style: { marginBottom: '8px' } },
                react_1.default.createElement("div", { style: { fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' } }, "\u81EA\u5B9A\u4E49\u6A21\u578B\u540D\u79F0:"),
                react_1.default.createElement("input", { type: "text", value: customModelName, onChange: updateCustomModelName, style: {
                        width: '100%',
                        padding: '4px 8px',
                        border: '1px solid var(--jp-border-color1)',
                        borderRadius: '4px',
                        fontSize: '12px',
                        background: 'var(--jp-input-background)',
                        color: 'var(--jp-ui-font-color1)'
                    }, placeholder: "\u8F93\u5165\u81EA\u5B9A\u4E49\u6A21\u578B\u540D\u79F0" }))),
            react_1.default.createElement("div", { style: {
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: '8px'
                } },
                react_1.default.createElement("div", null,
                    react_1.default.createElement("div", { style: { fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' } },
                        "\u6E29\u5EA6: ",
                        temperature),
                    react_1.default.createElement("input", { type: "range", min: "0", max: "2", step: "0.1", value: temperature, onChange: updateTemperature, style: {
                            width: '100%'
                        } }),
                    react_1.default.createElement("div", { style: {
                            fontSize: '10px',
                            color: 'var(--jp-ui-font-color2)',
                            display: 'flex',
                            justifyContent: 'space-between'
                        } },
                        react_1.default.createElement("span", null, "\u7CBE\u786E"),
                        react_1.default.createElement("span", null, "\u5E73\u8861"),
                        react_1.default.createElement("span", null, "\u521B\u610F"))),
                react_1.default.createElement("div", null,
                    react_1.default.createElement("div", { style: { fontSize: '12px', marginBottom: '4px', color: 'var(--jp-ui-font-color2)' } },
                        "\u6700\u5927\u957F\u5EA6: ",
                        maxTokens),
                    react_1.default.createElement("input", { type: "range", min: "100", max: "4000", step: "100", value: maxTokens, onChange: updateMaxTokens, style: {
                            width: '100%'
                        } }),
                    react_1.default.createElement("div", { style: {
                            fontSize: '10px',
                            color: 'var(--jp-ui-font-color2)',
                            display: 'flex',
                            justifyContent: 'space-between'
                        } },
                        react_1.default.createElement("span", null, "\u7B80\u6D01"),
                        react_1.default.createElement("span", null, "\u9002\u4E2D"),
                        react_1.default.createElement("span", null, "\u8BE6\u7EC6")))),
            react_1.default.createElement("div", { style: {
                    display: 'flex',
                    justifyContent: 'space-between',
                    marginTop: '8px'
                } },
                react_1.default.createElement("button", { onClick: resetSettings, style: {
                        background: 'transparent',
                        border: '1px solid var(--jp-border-color1)',
                        color: 'var(--jp-ui-font-color2)',
                        borderRadius: '4px',
                        padding: '2px 8px',
                        fontSize: '10px',
                        cursor: 'pointer'
                    } }, "\u91CD\u7F6E\u8BBE\u7F6E"),
                react_1.default.createElement("div", { style: { fontSize: '10px', color: 'var(--jp-ui-font-color2)' } },
                    "\u5F53\u524D\u6A21\u578B: ",
                    actualModelName))),
        react_1.default.createElement("div", { ref: messagesContainerRef, style: {
                flex: 1,
                overflow: 'auto',
                padding: '8px',
                background: 'var(--jp-layout-color0)',
                position: 'relative'
            } },
            messages.map((message) => (react_1.default.createElement("div", { key: message.id, style: {
                    display: 'flex',
                    flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
                    alignItems: 'flex-start',
                    marginBottom: '12px'
                } },
                react_1.default.createElement("div", { style: {
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
                    } }, message.sender === 'user' ? '👤' : '🤖'),
                react_1.default.createElement("div", { style: {
                        maxWidth: '85%',
                        textAlign: message.sender === 'user' ? 'right' : 'left'
                    } },
                    react_1.default.createElement("div", { style: {
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
                        } },
                        react_1.default.createElement(MessageContent_1.MessageContent, { content: message.content, onInsertCode: insertCodeToNotebook }),
                        isMessageStreaming(message.id) && (react_1.default.createElement("span", { style: {
                                display: 'inline-block',
                                width: '2px',
                                height: '1em',
                                background: 'var(--jp-ui-font-color1)',
                                marginLeft: '2px',
                                animation: 'blink 1s infinite'
                            } }))),
                    react_1.default.createElement("div", { style: {
                            fontSize: '10px',
                            color: 'var(--jp-ui-font-color2)',
                            marginTop: '2px'
                        } },
                        formatTime(message.timestamp),
                        isMessageStreaming(message.id) && ' · 生成中...'))))),
            isLoading && !currentStreamingMessageId && (react_1.default.createElement("div", { style: {
                    display: 'flex',
                    alignItems: 'center',
                    marginBottom: '12px'
                } },
                react_1.default.createElement("div", { style: {
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
                    } }, "\uD83E\uDD16"),
                react_1.default.createElement("div", { style: {
                        background: 'var(--jp-layout-color2)',
                        padding: '6px 10px',
                        borderRadius: '12px',
                        border: '1px solid var(--jp-border-color1)',
                        color: 'var(--jp-ui-font-color2)',
                        fontSize: '12px',
                        display: 'flex',
                        alignItems: 'center'
                    } },
                    react_1.default.createElement("div", { style: {
                            width: '12px',
                            height: '12px',
                            border: '2px solid var(--jp-ui-font-color3)',
                            borderTop: '2px solid transparent',
                            borderRadius: '50%',
                            animation: 'spin 1s linear infinite',
                            marginRight: '6px'
                        } }),
                    "AI\u6B63\u5728\u601D\u8003..."))),
            !shouldAutoScroll && (react_1.default.createElement("button", { onClick: scrollToBottomManually, style: {
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
                } },
                react_1.default.createElement("span", null, "\u2193"),
                "\u6709\u65B0\u6D88\u606F")),
            react_1.default.createElement("div", { ref: messagesEndRef })),
        react_1.default.createElement("div", { style: {
                borderTop: '1px solid var(--jp-border-color1)',
                padding: '10px',
                background: 'var(--jp-layout-color1)'
            } },
            react_1.default.createElement("div", { style: {
                    display: 'flex',
                    alignItems: 'flex-end',
                    gap: '6px'
                } },
                react_1.default.createElement("textarea", { style: {
                        flex: 1,
                        minHeight: '36px',
                        maxHeight: '100px',
                        padding: '6px 10px',
                        border: '1px solid var(--jp-border-color1)',
                        borderRadius: '4px',
                        background: 'var(--jp-input-background)',
                        color: 'var(--jp-ui-font-color1)',
                        fontFamily: 'inherit',
                        fontSize: '13px',
                        resize: 'vertical',
                        outline: 'none'
                    }, placeholder: "\u8F93\u5165\u4F60\u7684\u95EE\u9898...", value: inputValue, onChange: (e) => setInputValue(e.target.value), onKeyPress: handleKeyPress, disabled: isLoading, rows: 1 }),
                react_1.default.createElement("button", { style: {
                        background: inputValue.trim() && !isLoading
                            ? 'var(--jp-brand-color1)'
                            : 'var(--jp-layout-color3)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        padding: '6px 12px',
                        cursor: inputValue.trim() && !isLoading ? 'pointer' : 'not-allowed',
                        height: '36px',
                        fontSize: '12px',
                        fontWeight: 'bold'
                    }, onClick: handleSend, disabled: !inputValue.trim() || isLoading }, isLoading ? '生成中...' : '发送')),
            react_1.default.createElement("div", { style: {
                    fontSize: '10px',
                    color: 'var(--jp-ui-font-color2)',
                    marginTop: '4px',
                    textAlign: 'center'
                } },
                "\u6D41\u5F0F\u8F93\u51FA | \u6A21\u578B: ",
                actualModelName,
                " | \u6E29\u5EA6: ",
                temperature,
                " | \u6700\u5927\u957F\u5EA6: ",
                maxTokens)),
        react_1.default.createElement("style", null, `
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }

        /* 添加平滑滚动样式 */
        .jp-ChatWidget * {
          scroll-behavior: smooth;
        }
      `)));
};


/***/ })

}]);
//# sourceMappingURL=lib_index_js.3ab462d70b21b4a48771.js.map