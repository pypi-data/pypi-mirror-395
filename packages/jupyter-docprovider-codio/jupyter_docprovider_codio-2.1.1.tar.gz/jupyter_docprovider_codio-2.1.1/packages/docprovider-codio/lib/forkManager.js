/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
import { URLExt } from '@jupyterlab/coreutils';
import { Signal } from '@lumino/signaling';
import { requestAPI, ROOM_FORK_URL } from './requests';
export const JUPYTER_COLLABORATION_FORK_EVENTS_URI = 'https://schema.jupyter.org/jupyter_collaboration/fork/v1';
export class ForkManager {
    constructor(options) {
        this._disposed = false;
        this._forkAddedSignal = new Signal(this);
        this._forkDeletedSignal = new Signal(this);
        const { contentProvider, eventManager } = options;
        this._contentProvider = contentProvider;
        this._eventManager = eventManager;
        this._eventManager.stream.connect(this._handleEvent, this);
    }
    get isDisposed() {
        return this._disposed;
    }
    get forkAdded() {
        return this._forkAddedSignal;
    }
    get forkDeleted() {
        return this._forkDeletedSignal;
    }
    dispose() {
        var _a;
        if (this._disposed) {
            return;
        }
        (_a = this._eventManager) === null || _a === void 0 ? void 0 : _a.stream.disconnect(this._handleEvent);
        this._disposed = true;
    }
    async createFork(options) {
        const { rootId, title, description, synchronize } = options;
        const init = {
            method: 'PUT',
            body: JSON.stringify({ title, description, synchronize })
        };
        const url = URLExt.join(ROOM_FORK_URL, rootId);
        const response = await requestAPI(url, init);
        return response;
    }
    async getAllForks(rootId) {
        const url = URLExt.join(ROOM_FORK_URL, rootId);
        const init = { method: 'GET' };
        const response = await requestAPI(url, init);
        return response;
    }
    async deleteFork(options) {
        const { forkId, merge } = options;
        const url = URLExt.join(ROOM_FORK_URL, forkId);
        const query = URLExt.objectToQueryString({ merge });
        const init = { method: 'DELETE' };
        await requestAPI(`${url}${query}`, init);
    }
    getProvider(options) {
        const { documentPath, format, type } = options;
        const contentProvider = this._contentProvider;
        if (contentProvider) {
            const docPath = documentPath;
            const provider = contentProvider.providers.get(`${format}:${type}:${docPath}`);
            return provider;
        }
        return;
    }
    _handleEvent(_, emission) {
        if (emission.schema_id === JUPYTER_COLLABORATION_FORK_EVENTS_URI) {
            switch (emission.action) {
                case 'create': {
                    this._forkAddedSignal.emit(emission);
                    break;
                }
                case 'delete': {
                    this._forkDeletedSignal.emit(emission);
                    break;
                }
                default:
                    break;
            }
        }
    }
}
