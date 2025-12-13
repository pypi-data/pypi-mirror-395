import React from 'react';

interface MessageContentProps {
  content: string;
  onInsertCode?: (code: string, language: string) => void;
}

export const MessageContent: React.FC<MessageContentProps> = ({ 
  content, 
  onInsertCode 
}) => {
  const handleInsertCode = (code: string, language: string) => {
    if (onInsertCode) {
      onInsertCode(code, language);
    }
  };

  // 渲染代码块
  const renderCodeBlock = (codeContent: string, language: string = 'text') => {
    return (
      <div style={{
        position: 'relative',
        margin: '8px 0'
      }}>
        {onInsertCode && (
          <button
            onClick={() => handleInsertCode(codeContent, language)}
            style={{
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
            }}
            title="插入到Jupyter单元格"
          >
            插入代码
          </button>
        )}
        <pre style={{
          background: 'var(--jp-code-cell-background)',
          border: '1px solid var(--jp-border-color1)',
          borderRadius: '4px',
          padding: '8px',
          overflowX: 'auto',
          fontFamily: 'var(--jp-code-font-family)',
          fontSize: 'var(--jp-code-font-size)',
          lineHeight: 'var(--jp-code-line-height)',
          margin: 0
        }}>
          <code style={{
            color: 'var(--jp-content-font-color1)',
            display: 'block'
          }}>
            {codeContent}
          </code>
        </pre>
      </div>
    );
  };

  // 渲染表格
  const renderTable = (tableContent: string) => {
    const lines = tableContent.split('\n').filter(line => line.trim());
    if (lines.length < 2) return null;

    try {
      const headers = lines[0]
        .split('|')
        .filter(cell => cell.trim() !== '')
        .map(header => header.trim());

      const rows = lines.slice(2) // 跳过表头和分隔线
        .map(line => 
          line.split('|')
            .filter(cell => cell.trim() !== '')
            .map(cell => cell.trim())
        )
        .filter(row => row.length > 0);

      return (
        <div style={{ 
          overflowX: 'auto', 
          margin: '12px 0'
        }}>
          <table style={{
            borderCollapse: 'collapse',
            width: '100%',
            minWidth: '400px',
            border: '1px solid var(--jp-border-color1)',
            fontSize: '12px'
          }}>
            <thead>
              <tr style={{ backgroundColor: 'var(--jp-layout-color2)' }}>
                {headers.map((header, index) => (
                  <th key={index} style={{
                    border: '1px solid var(--jp-border-color1)',
                    padding: '8px 12px',
                    textAlign: 'left',
                    fontWeight: 'bold'
                  }}>
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, rowIndex) => (
                <tr key={rowIndex} style={{
                  borderBottom: '1px solid var(--jp-border-color2)'
                }}>
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex} style={{
                      border: '1px solid var(--jp-border-color1)',
                      padding: '8px 12px',
                      textAlign: 'left'
                    }}>
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    } catch (error) {
      console.error('表格渲染错误:', error);
      return <div style={{ whiteSpace: 'pre-wrap' }}>{tableContent}</div>;
    }
  };

  // 主渲染函数
  const renderContent = () => {
    if (!content) return null;

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
            return <div key={index}>{renderCodeBlock(codeContent, language)}</div>;
          }
        }
        
        // 表格检测
        const tableMatch = part.match(/(\|[^\n]+\|\r?\n\|[-:\s|]+\|\r?\n(?:\|[^\n]+\|\r?\n)*)/);
        if (tableMatch) {
          return <div key={index}>{renderTable(tableMatch[0])}</div>;
        }
        
        // 普通文本
        return (
          <div 
            key={index}
            style={{ 
              lineHeight: '1.5',
              margin: '4px 0',
              whiteSpace: 'pre-wrap'
            }}
          >
            {part}
          </div>
        );
      });
    } catch (error) {
      console.error('内容渲染错误:', error);
      return <div style={{ whiteSpace: 'pre-wrap' }}>{content}</div>;
    }
  };

  return (
    <div style={{ 
      lineHeight: '1.5',
      fontSize: '13px',
      fontFamily: 'var(--jp-ui-font-family)'
    }}>
      {renderContent()}
    </div>
  );
};