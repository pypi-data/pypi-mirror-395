/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
import { WebsocketProvider } from 'y-websocket';
/**
 * A class to provide Yjs synchronization over WebSocket.
 *
 * We specify custom messages that the server can interpret. For reference please look in yjs_ws_server.
 *
 */
export class WebSocketAwarenessProvider extends WebsocketProvider {
    /**
     * Construct a new WebSocketAwarenessProvider
     *
     * @param options The instantiation options for a WebSocketAwarenessProvider
     */
    constructor(options) {
        super(options.url, options.roomID, options.awareness.doc, {
            awareness: options.awareness
        });
        this._isDisposed = false;
        this._awareness = options.awareness;
        this._user = options.user;
        this._user.ready
            .then(() => this._onUserChanged(this._user))
            .catch(e => console.error(e));
        this._user.userChanged.connect(this._onUserChanged, this);
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._user.userChanged.disconnect(this._onUserChanged, this);
        this._isDisposed = true;
        this.destroy();
    }
    _onUserChanged(user) {
        this._awareness.setLocalStateField('user', user.identity);
    }
}
