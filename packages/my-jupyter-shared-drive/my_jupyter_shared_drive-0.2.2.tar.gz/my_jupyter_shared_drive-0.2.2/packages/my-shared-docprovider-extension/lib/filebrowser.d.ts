import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ICollaborativeContentProvider } from '@jupyter/collaborative-drive';
/**
 * The shared drive provider.
 */
export declare const rtcContentProvider: JupyterFrontEndPlugin<ICollaborativeContentProvider>;
/**
 * Plugin to register the shared model factory for the content type 'file'.
 */
export declare const yfile: JupyterFrontEndPlugin<void>;
/**
 * Plugin to register the shared model factory for the content type 'notebook'.
 */
export declare const ynotebook: JupyterFrontEndPlugin<void>;
