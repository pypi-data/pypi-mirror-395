import { JupyterFrontEnd } from '@jupyterlab/application';
import { ISignal } from '@lumino/signaling';
import { TranslationBundle } from '@jupyterlab/translation';
import { Contents, IContentProvider, User } from '@jupyterlab/services';
import { IDocumentProvider, ISharedModelFactory } from '@jupyter/collaborative-drive';
declare namespace RtcContentProvider {
    interface IOptions {
        currentDrive: Contents.IDrive;
        user: User.IManager;
        trans: TranslationBundle;
    }
}
export declare class RtcContentProvider implements IContentProvider {
    /**
     * Construct a new drive object.
     *
     * @param user - The user manager to add the identity to the awareness of documents.
     */
    constructor(app: JupyterFrontEnd, options: RtcContentProvider.IOptions);
    /**
     * SharedModel factory for the content provider.
     */
    readonly sharedModelFactory: ISharedModelFactory;
    get providers(): Map<string, IDocumentProvider>;
    /**
     * Get a file or directory.
     *
     * @param localPath: The path to the file.
     *
     * @param options: The options used to fetch the file.
     *
     * @returns A promise which resolves with the file content.
     *
     * Uses the [Jupyter Notebook API](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyter/notebook/master/notebook/services/api/api.yaml#!/contents) and validates the response model.
     */
    get(localPath: string, options?: Contents.IFetchOptions): Promise<Contents.IModel>;
    listCheckpoints(path: string): Promise<Contents.ICheckpointModel[]>;
    createCheckpoint(path: string): Promise<Contents.ICheckpointModel>;
    rename(oldLocalPath: string, newLocalPath: string): Promise<Contents.IModel>;
    delete(localPath: string): Promise<void>;
    newUntitled(options?: Contents.ICreateOptions): Promise<Contents.IModel>;
    /**
     * Save a file.
     *
     * @param localPath - The desired file path.
     *
     * @param options - Optional overrides to the model.
     *
     * @returns A promise which resolves with the file content model when the
     *   file is saved.
     */
    save(localPath: string, options?: Partial<Contents.IModel> & Contents.IContentProvisionOptions): Promise<Contents.IModel>;
    /**
     * A signal emitted when a file operation takes place.
     */
    get fileChanged(): ISignal<this, Contents.IChangedArgs>;
    private _onCreate;
    private _currentDrive;
    private _app;
    private _user;
    private _trans;
    private _providers;
    private _ydriveFileChanged;
    private _saveLock;
}
export {};
