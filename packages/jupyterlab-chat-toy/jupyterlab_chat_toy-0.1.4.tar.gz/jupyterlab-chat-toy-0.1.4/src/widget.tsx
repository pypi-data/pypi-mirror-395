// widget.tsx
import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { ChatComponent } from './ChatWidget/ChatComponent';

class ChatWidget extends ReactWidget {
  private notebookTracker: INotebookTracker | null;

  constructor(notebookTracker: INotebookTracker | null) {
    super();
    this.notebookTracker = notebookTracker;
    this.id = 'ai-chat-widget';
    this.title.label = 'AI Chat';
    this.title.closable = true;
    this.addClass('jp-ChatWidget');
  }

  render(): JSX.Element {
    return <ChatComponent notebookTracker={this.notebookTracker} />;
  }
}

export { ChatWidget };