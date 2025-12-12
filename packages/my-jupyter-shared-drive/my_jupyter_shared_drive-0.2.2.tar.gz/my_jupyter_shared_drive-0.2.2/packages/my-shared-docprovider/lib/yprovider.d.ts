import { IDocumentProvider } from '@jupyter/collaborative-drive';
import { User } from '@jupyterlab/services';
import { TranslationBundle } from '@jupyterlab/translation';
import { DocumentChange, YDocument } from '@jupyter/ydoc';
/**
 * A class to provide Yjs synchronization.
 */
export declare class MyProvider implements IDocumentProvider {
    /**
     * Construct a new MyProvider
     *
     * @param options The instantiation options for a MyProvider
     */
    constructor(options: MyProvider.IOptions);
    setSource(value: any): void;
    /**
     * Test whether the object has been disposed.
     */
    get isDisposed(): boolean;
    /**
     * A promise that resolves when the document provider is ready.
     */
    get ready(): Promise<void>;
    get contentType(): string;
    get format(): string;
    /**
     * Dispose of the resources held by the object.
     */
    dispose(): void;
    private _onUserChanged;
    private _awareness;
    private _contentType;
    private _format;
    private _isDisposed;
    private _ready;
    model: YDocument<DocumentChange>;
}
/**
 * A namespace for MyProvider statics.
 */
export declare namespace MyProvider {
    /**
     * The instantiation options for a MyProvider.
     */
    interface IOptions {
        /**
         * The document file path
         */
        path: string;
        /**
         * Content type
         */
        contentType: string;
        /**
         * The source format
         */
        format: string;
        /**
         * The shared model
         */
        model: YDocument<DocumentChange>;
        /**
         * The user data
         */
        user: User.IManager;
        /**
         * The jupyterlab translator
         */
        translator: TranslationBundle;
    }
}
