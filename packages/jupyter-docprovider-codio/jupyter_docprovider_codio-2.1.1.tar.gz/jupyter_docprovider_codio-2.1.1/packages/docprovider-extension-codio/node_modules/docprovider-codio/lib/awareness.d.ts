import { User } from '@jupyterlab/services';
import { IDisposable } from '@lumino/disposable';
import { IAwareness } from '@jupyter/ydoc';
import { WebsocketProvider } from 'y-websocket';
export interface IContent {
    type: string;
    body: string;
}
/**
 * A class to provide Yjs synchronization over WebSocket.
 *
 * We specify custom messages that the server can interpret. For reference please look in yjs_ws_server.
 *
 */
export declare class WebSocketAwarenessProvider extends WebsocketProvider implements IDisposable {
    /**
     * Construct a new WebSocketAwarenessProvider
     *
     * @param options The instantiation options for a WebSocketAwarenessProvider
     */
    constructor(options: WebSocketAwarenessProvider.IOptions);
    get isDisposed(): boolean;
    dispose(): void;
    private _onUserChanged;
    private _isDisposed;
    private _user;
    private _awareness;
}
/**
 * A namespace for WebSocketAwarenessProvider statics.
 */
export declare namespace WebSocketAwarenessProvider {
    /**
     * The instantiation options for a WebSocketAwarenessProvider.
     */
    interface IOptions {
        /**
         * The server URL
         */
        url: string;
        /**
         * The room ID
         */
        roomID: string;
        /**
         * The awareness object
         */
        awareness: IAwareness;
        /**
         * The user data
         */
        user: User.IManager;
    }
}
