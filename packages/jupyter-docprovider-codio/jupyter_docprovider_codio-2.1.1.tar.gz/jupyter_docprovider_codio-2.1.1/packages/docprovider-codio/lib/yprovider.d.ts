import { IDocumentProvider } from '@jupyter/collaborative-drive';
import { User } from '@jupyterlab/services';
import { TranslationBundle } from '@jupyterlab/translation';
import { DocumentChange, YDocument } from '@jupyter/ydoc';
import { WebsocketProvider as YWebsocketProvider } from 'y-websocket';
import { IForkProvider } from './ydrive';
/**
 * A class to provide Yjs synchronization over WebSocket.
 *
 * We specify custom messages that the server can interpret. For reference please look in yjs_ws_server.
 *
 */
export declare class WebSocketProvider implements IDocumentProvider, IForkProvider {
    /**
     * Construct a new WebSocketProvider
     *
     * @param options The instantiation options for a WebSocketProvider
     */
    constructor(options: WebSocketProvider.IOptions);
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
    reconnect(): Promise<void>;
    private _connect;
    connectToForkDoc(forkRoomId: string, sessionId: string): Promise<void>;
    get wsProvider(): YWebsocketProvider | null;
    private _disconnect;
    private _onUserChanged;
    private _onConnectionClosed;
    private _onSync;
    private _awareness;
    private _contentType;
    private _format;
    private _isDisposed;
    private _path;
    private _ready;
    private _serverUrl;
    private _sharedModel;
    private _yWebsocketProvider;
    private _trans;
}
/**
 * A namespace for WebSocketProvider statics.
 */
export declare namespace WebSocketProvider {
    /**
     * The instantiation options for a WebSocketProvider.
     */
    interface IOptions {
        /**
         * The server URL
         */
        url: string;
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
