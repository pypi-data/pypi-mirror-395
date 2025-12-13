import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILayoutRestorer
} from '@jupyterlab/application';
import {
  ICommandPalette,
  WidgetTracker
} from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { INotebookTracker } from '@jupyterlab/notebook';
import { Widget } from '@lumino/widgets';
import { chatIcon } from './icons';
import { ChatWidget } from './widget';

/**
 * The command IDs used by the chat plugin.
 */
namespace CommandIDs {
  export const open = 'jupyterlab-chat:open';
}

/**
 * Initialization data for the jupyterlab-chat extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-chat:plugin',
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker],
  optional: [ILauncher, ILayoutRestorer, ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    notebookTracker: INotebookTracker,
    launcher: ILauncher | null,
    restorer: ILayoutRestorer | null,
    settingRegistry: ISettingRegistry | null
  ) => {
    const { commands, shell } = app;
    
    // Create a widget tracker for the left sidebar
    const tracker = new WidgetTracker<Widget>({
      namespace: 'jupyterlab-chat-sidebar'
    });

    // Create the chat widget
    let chatWidget: ChatWidget | null = null;

    // Add command to open chat in sidebar
    commands.addCommand(CommandIDs.open, {
      label: 'AI Chat',
      caption: 'Open AI Chat Interface in Sidebar',
      icon: chatIcon,
      execute: () => {
        if (!chatWidget || chatWidget.isDisposed) {
          // Create the chat widget if it doesn't exist
          chatWidget = new ChatWidget(notebookTracker);
          chatWidget.id = 'jupyterlab-chat-sidebar';
          chatWidget.title.label = 'AI Chat';
          chatWidget.title.closable = true;
          chatWidget.title.icon = chatIcon;

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

export default plugin;