// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import { JupyterFrontEnd } from '@jupyterlab/application';
import { ISignal, Signal } from '@lumino/signaling';
import { TranslationBundle } from '@jupyterlab/translation';
import {
  Contents,
  IContentProvider,
  SharedDocumentFactory,
  User
} from '@jupyterlab/services';

import { DocumentChange, ISharedDocument, YDocument } from '@jupyter/ydoc';

import { MyProvider } from './yprovider';
import {
  IDocumentProvider,
  ISharedModelFactory
} from '@jupyter/collaborative-drive';

namespace RtcContentProvider {
  export interface IOptions {
    currentDrive: Contents.IDrive;
    user: User.IManager;
    trans: TranslationBundle;
  }
}

export class RtcContentProvider implements IContentProvider {
  /**
   * Construct a new drive object.
   *
   * @param user - The user manager to add the identity to the awareness of documents.
   */
  constructor(app: JupyterFrontEnd, options: RtcContentProvider.IOptions) {
    this._app = app;
    this._user = options.user;
    this._trans = options.trans;
    this._currentDrive = options.currentDrive;
    this._providers = new Map<string, MyProvider>();
    this.sharedModelFactory = new SharedModelFactory(this._onCreate);
    this._saveLock = new AsyncLock();
  }

  /**
   * SharedModel factory for the content provider.
   */
  readonly sharedModelFactory: ISharedModelFactory;

  get providers(): Map<string, IDocumentProvider> {
    return this._providers;
  }

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
  async get(
    localPath: string,
    options?: Contents.IFetchOptions
  ): Promise<Contents.IModel> {
    if (options && options.format && options.type) {
      const key = `${options.format}:${options.type}:${localPath}`;
      const provider = this._providers.get(key);

      if (provider) {
        // If the document doesn't exist, `super.get` will reject with an
        // error and the provider will never be resolved.
        // Use `Promise.all` to reject as soon as possible. The Context will
        // show a dialog to the user.
        const [model] = await Promise.all([
          this._currentDrive.get(localPath, {
            ...options,
            content: false,
            contentProviderId: undefined
          }),
          provider.ready
        ]);
        // The server doesn't return a model with a format when content is false,
        // so set it back.
        return { ...model, format: options.format };
      }
    }

    return await this._currentDrive.get(localPath, {
      ...options,
      contentProviderId: undefined
    });
  }

  async listCheckpoints(path: string): Promise<Contents.ICheckpointModel[]> {
    return [];
  }

  async createCheckpoint(path: string): Promise<Contents.ICheckpointModel> {
    return { id: '', last_modified: '' };
  }

  async rename(
    oldLocalPath: string,
    newLocalPath: string
  ): Promise<Contents.IModel> {
    return await this._app.serviceManager.contents.rename(
      oldLocalPath,
      newLocalPath
    );
  }

  async delete(localPath: string): Promise<void> {
    return await this._app.serviceManager.contents.delete(localPath);
  }

  async newUntitled(
    options?: Contents.ICreateOptions
  ): Promise<Contents.IModel> {
    return await this._app.serviceManager.contents.newUntitled(options);
  }

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
  async save(
    localPath: string,
    options: Partial<Contents.IModel> & Contents.IContentProvisionOptions = {}
  ): Promise<Contents.IModel> {
    // Check that there is a provider - it won't e.g. if the document model is not collaborative.
    if (options.format && options.type) {
      const key = `${options.format}:${options.type}:${localPath}`;
      const provider = this._providers.get(key);

      if (provider) {
        // Save is done from the backend
        const fetchOptions: Contents.IFetchOptions = {
          type: options.type,
          format: options.format,
          content: false
        };
        return this.get(localPath, fetchOptions);
      }
    }

    return await this._currentDrive.save(localPath, {
      ...options,
      contentProviderId: undefined
    });
  }

  /**
   * A signal emitted when a file operation takes place.
   */
  get fileChanged(): ISignal<this, Contents.IChangedArgs> {
    return this._ydriveFileChanged;
  }

  private _onCreate = (
    options: Contents.ISharedFactoryOptions
  ): YDocument<DocumentChange> => {
    if (typeof options.format !== 'string') {
      const factory = (
        this.sharedModelFactory as SharedModelFactory
      ).documentFactories.get(options.contentType)!;
      const sharedModel = factory(options);
      return sharedModel;
    }

    const key = `${options.format}:${options.contentType}:${options.path}`;

    // Check if shared model alread exists.
    const _provider = this._providers.get(key);
    if (_provider) {
      return _provider.model;
    }

    const factory = (
      this.sharedModelFactory as SharedModelFactory
    ).documentFactories.get(options.contentType)!;
    const sharedModel = factory(options);
    sharedModel.changed.connect((_: any, event: any) => {
      if (!event.stateChange) {
        sharedModel.ystate.set('dirty', false);
      }
    });

    const provider = new MyProvider({
      path: options.path,
      format: options.format,
      contentType: options.contentType,
      model: sharedModel,
      user: this._user,
      translator: this._trans
    });

    this._providers.set(key, provider);

    this._app.serviceManager.contents
      .get(options.path, {
        type: options.contentType,
        format: options.format,
        content: true
      })
      .then(model => {
        let content = model.content;
        if (model.format === 'base64') {
          content = atob(content);
        } else if (options.format === 'text' && model.format === 'json') {
          content = JSON.stringify(content);
        } else if (options.format === 'json' && model.format === 'text') {
          content = JSON.parse(content);
        }
        provider.setSource(content);
      });

    sharedModel.ydoc.on('update', (update, origin) => {
      if (origin === this) {
        return;
      }
      this._saveLock.promise.then(() => {
        this._saveLock.enable();
        let content = sharedModel.getSource();
        sharedModel.ydoc.transact(() => {
          sharedModel.ystate.set('dirty', false);
        }, this);
        if (options.format === 'text' && typeof content === 'object') {
          content = JSON.stringify(content);
        }
        this._app.serviceManager.contents
          .save(options.path, {
            content,
            format: options.format,
            type: options.contentType
          })
          .then(() => {
            this._saveLock.disable();
          });
      });
    });

    sharedModel.disposed.connect(() => {
      const provider = this._providers.get(key);
      if (provider) {
        provider.dispose();
        this._providers.delete(key);
      }
    });

    return sharedModel;
  };

  private _currentDrive: Contents.IDrive;
  private _app: JupyterFrontEnd;
  private _user: User.IManager;
  private _trans: TranslationBundle;
  private _providers: Map<string, MyProvider>;
  private _ydriveFileChanged = new Signal<this, Contents.IChangedArgs>(this);
  private _saveLock: AsyncLock;
}

/**
 * Yjs sharedModel factory for real-time collaboration.
 */
class SharedModelFactory implements ISharedModelFactory {
  documentFactories: Map<Contents.ContentType, SharedDocumentFactory>;

  /**
   * Shared model factory constructor
   *
   * @param _onCreate Callback on new document model creation
   */
  constructor(
    private _onCreate: (
      options: Contents.ISharedFactoryOptions
    ) => YDocument<DocumentChange>
  ) {
    this.documentFactories = new Map();
  }

  /**
   * Whether the IDrive supports real-time collaboration or not.
   */
  readonly collaborative = true;

  /**
   * Register a SharedDocumentFactory.
   *
   * @param type Document type
   * @param factory Document factory
   */
  registerDocumentFactory(
    type: Contents.ContentType,
    factory: SharedDocumentFactory
  ) {
    if (this.documentFactories.has(type)) {
      throw new Error(`The content type ${type} already exists`);
    }
    this.documentFactories.set(type, factory);
  }

  /**
   * Create a new `ISharedDocument` instance.
   *
   * It should return `undefined` if the factory is not able to create a `ISharedDocument`.
   */
  createNew(
    options: Contents.ISharedFactoryOptions
  ): ISharedDocument | undefined {
    if (typeof options.format !== 'string') {
      console.warn(`Only defined format are supported; got ${options.format}.`);
      return;
    }

    if (!this.collaborative || !options.collaborative) {
      // Bail if the document model does not support collaboration
      // the `sharedModel` will be the default one.
      return;
    }

    if (this.documentFactories.has(options.contentType)) {
      const sharedModel = this._onCreate(options);
      return sharedModel;
    }

    return;
  }
}

class AsyncLock {
  constructor() {
    this.disable = () => {};
    this.promise = Promise.resolve();
  }

  enable() {
    this.promise = new Promise(resolve => (this.disable = resolve));
  }

  disable: any;
  promise: Promise<void>;
}
