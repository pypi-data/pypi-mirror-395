import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ICollaborativeContentProvider } from '@jupyter/collaborative-drive';
export declare const rtcContentProvider: JupyterFrontEndPlugin<ICollaborativeContentProvider>;
/**
 * Plugin to register the shared model factory for the content type 'file'.
 */
export declare const yfile: JupyterFrontEndPlugin<void>;
/**
 * Plugin to register the shared model factory for the content type 'notebook'.
 */
export declare const ynotebook: JupyterFrontEndPlugin<void>;
/**
 * A plugin to add a timeline slider status item to the status bar.
 */
export declare const statusBarTimeline: JupyterFrontEndPlugin<void>;
/**
 * The default collaborative drive provider.
 */
export declare const logger: JupyterFrontEndPlugin<void>;
