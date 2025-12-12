/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
import { PromiseDelegate } from '@lumino/coreutils';
import { Signal } from '@lumino/signaling';
/**
 * A class to provide Yjs synchronization.
 */
export class MyProvider {
    /**
     * Construct a new MyProvider
     *
     * @param options The instantiation options for a MyProvider
     */
    constructor(options) {
        this._ready = new PromiseDelegate();
        this._isDisposed = false;
        this._contentType = options.contentType;
        this._format = options.format;
        this._awareness = options.model.awareness;
        this.model = options.model;
        const user = options.user;
        user.ready
            .then(() => {
            this._onUserChanged(user);
        })
            .catch(e => console.error(e));
        user.userChanged.connect(this._onUserChanged, this);
    }
    setSource(value) {
        this.model.setSource(value);
        this._ready.resolve();
    }
    /**
     * Test whether the object has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A promise that resolves when the document provider is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    get contentType() {
        return this._contentType;
    }
    get format() {
        return this._format;
    }
    /**
     * Dispose of the resources held by the object.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        Signal.clearData(this);
    }
    _onUserChanged(user) {
        this._awareness.setLocalStateField('user', user.identity);
    }
}
