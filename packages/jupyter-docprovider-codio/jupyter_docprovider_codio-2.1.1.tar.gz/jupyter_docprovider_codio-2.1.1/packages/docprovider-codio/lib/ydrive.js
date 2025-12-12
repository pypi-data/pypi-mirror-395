// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { PageConfig, URLExt } from '@jupyterlab/coreutils';
import { RestContentProvider } from '@jupyterlab/services';
import { PromiseDelegate } from '@lumino/coreutils';
import { Signal } from '@lumino/signaling';
import { WebSocketProvider } from './yprovider';
import * as decoding from 'lib0/decoding';
import * as encoding from 'lib0/encoding';
const DISABLE_RTC = PageConfig.getOption('disableRTC') === 'true' ? true : false;
const RAW_MESSAGE_TYPE = 2;
/**
 * The url for the default drive service.
 */
const DOCUMENT_PROVIDER_URL = 'api/collaboration/room';
export class RtcContentProvider extends RestContentProvider {
    constructor(options) {
        super(options);
        this._onCreate = (options, sharedModel) => {
            var _a, _b, _c, _d, _e, _f;
            if (typeof options.format !== 'string') {
                return;
            }
            // Set initial autosave value, used to determine backend autosave (default: true)
            const autosave = (_c = (_b = (_a = this._docmanagerSettings) === null || _a === void 0 ? void 0 : _a.composite) === null || _b === void 0 ? void 0 : _b['autosave']) !== null && _c !== void 0 ? _c : true;
            sharedModel.awareness.setLocalStateField('autosave', autosave);
            // Watch for changes in settings
            (_d = this._docmanagerSettings) === null || _d === void 0 ? void 0 : _d.changed.connect(() => {
                var _a, _b, _c;
                const newAutosave = (_c = (_b = (_a = this._docmanagerSettings) === null || _a === void 0 ? void 0 : _a.composite) === null || _b === void 0 ? void 0 : _b['autosave']) !== null && _c !== void 0 ? _c : true;
                sharedModel.awareness.setLocalStateField('autosave', newAutosave);
            });
            try {
                const provider = new WebSocketProvider({
                    url: URLExt.join(this._serverSettings.wsUrl, DOCUMENT_PROVIDER_URL),
                    path: options.path,
                    format: options.format,
                    contentType: options.contentType,
                    model: sharedModel,
                    user: this._user,
                    translator: this._trans
                });
                // Add the document path in the list of opened ones for this user.
                const state = ((_e = this._globalAwareness) === null || _e === void 0 ? void 0 : _e.getLocalState()) || {};
                const documents = state.documents || [];
                if (!documents.includes(options.path)) {
                    documents.push(options.path);
                    (_f = this._globalAwareness) === null || _f === void 0 ? void 0 : _f.setLocalStateField('documents', documents);
                }
                const key = `${options.format}:${options.contentType}:${options.path}`;
                this._providers.set(key, provider);
                sharedModel.changed.connect(async (_, change) => {
                    var _a;
                    if (!change.stateChange) {
                        return;
                    }
                    const hashChanges = change.stateChange.filter(change => change.name === 'hash');
                    if (hashChanges.length === 0) {
                        return;
                    }
                    if (hashChanges.length > 1) {
                        console.error('Unexpected multiple changes to hash value in a single transaction');
                    }
                    const hashChange = hashChanges[0];
                    // A change in hash signifies that a save occurred on the server-side
                    // (e.g. a collaborator performed the save) - we want to notify the
                    // observers about this change so that they can store the new hash value.
                    const newPath = (_a = sharedModel.state.path) !== null && _a !== void 0 ? _a : options.path;
                    const model = await this.get(newPath, { content: false });
                    this._ydriveFileChanged.emit({
                        type: 'save',
                        newValue: { ...model, hash: hashChange.newValue },
                        // we do not have the old model because it was discarded when server made the change,
                        // we only have the old hash here (which may be empty if the file was newly created!)
                        oldValue: { hash: hashChange.oldValue }
                    });
                });
                sharedModel.disposed.connect(() => {
                    var _a, _b;
                    const provider = this._providers.get(key);
                    if (provider) {
                        provider.dispose();
                        this._providers.delete(key);
                    }
                    // Remove the document path from the list of opened ones for this user.
                    const state = ((_a = this._globalAwareness) === null || _a === void 0 ? void 0 : _a.getLocalState()) || {};
                    const documents = state.documents || [];
                    const index = documents.indexOf(options.path);
                    if (index > -1) {
                        documents.splice(index, 1);
                    }
                    (_b = this._globalAwareness) === null || _b === void 0 ? void 0 : _b.setLocalStateField('documents', documents);
                });
            }
            catch (error) {
                // Falling back to the contents API if opening the websocket failed
                //  This may happen if the shared document is not a YDocument.
                console.error(`Failed to open websocket connection for ${options.path}.\n:${error}`);
            }
        };
        this._saveCounter = 0;
        this._ydriveFileChanged = new Signal(this);
        this._user = options.user;
        this._trans = options.trans;
        this._globalAwareness = options.globalAwareness;
        this._serverSettings = options.serverSettings;
        this.sharedModelFactory = new SharedModelFactory(this._onCreate);
        this._providers = new Map();
        this._docmanagerSettings = options.docmanagerSettings;
    }
    get providers() {
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
     */
    async get(localPath, options) {
        if (options && options.format && options.type) {
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._providers.get(key);
            if (provider) {
                // If the document doesn't exist, `super.get` will reject with an
                // error and the provider will never be resolved.
                // Use `Promise.all` to reject as soon as possible. The Context will
                // show a dialog to the user.
                const [model] = await Promise.all([
                    super.get(localPath, { ...options, content: false }),
                    provider.ready
                ]);
                // The server doesn't return a model with a format when content is false,
                // so set it back.
                return { ...model, format: options.format };
            }
        }
        return super.get(localPath, options);
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
    async save(localPath, options = {}) {
        var _a;
        // Check that there is a provider - it won't e.g. if the document model is not collaborative.
        if (options.format && options.type) {
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._providers.get(key);
            const saveId = ++this._saveCounter;
            if (provider) {
                const ws = (_a = provider.wsProvider) === null || _a === void 0 ? void 0 : _a.ws;
                if (ws) {
                    const delegate = new PromiseDelegate();
                    const handler = (event) => {
                        const data = new Uint8Array(event.data);
                        const decoder = decoding.createDecoder(data);
                        try {
                            const messageType = decoding.readVarUint(decoder);
                            if (messageType !== RAW_MESSAGE_TYPE) {
                                return;
                            }
                        }
                        catch (_a) {
                            return;
                        }
                        const rawReply = decoding.readVarString(decoder);
                        let reply = null;
                        try {
                            reply = JSON.parse(rawReply);
                        }
                        catch (e) {
                            console.debug('The raw reply received was not a JSON reply');
                        }
                        if (reply &&
                            reply['type'] === 'save' &&
                            reply['responseTo'] === saveId) {
                            if (reply.status === 'success') {
                                delegate.resolve();
                            }
                            else if (reply.status === 'failed') {
                                delegate.reject('Saving failed');
                            }
                            else if (reply.status === 'skipped') {
                                delegate.reject('Saving already in progress');
                            }
                            else {
                                delegate.reject('Unrecognised save reply status');
                            }
                        }
                    };
                    ws.addEventListener('message', handler);
                    const encoder = encoding.createEncoder();
                    encoding.writeVarUint(encoder, RAW_MESSAGE_TYPE);
                    encoding.writeVarString(encoder, 'save');
                    encoding.writeVarUint(encoder, saveId);
                    const saveMessage = encoding.toUint8Array(encoder);
                    ws.send(saveMessage);
                    await delegate.promise;
                    ws.removeEventListener('message', handler);
                }
                const fetchOptions = {
                    type: options.type,
                    format: options.format,
                    content: false
                };
                return this.get(localPath, fetchOptions);
            }
        }
        return super.save(localPath, options);
    }
    /**
     * A signal emitted when a file operation takes place.
     */
    get fileChanged() {
        return this._ydriveFileChanged;
    }
}
/**
 * Yjs sharedModel factory for real-time collaboration.
 */
class SharedModelFactory {
    /**
     * Shared model factory constructor
     *
     * @param _onCreate Callback on new document model creation
     */
    constructor(_onCreate) {
        this._onCreate = _onCreate;
        /**
         * Whether the IDrive supports real-time collaboration or not.
         */
        this.collaborative = !DISABLE_RTC;
        this.documentFactories = new Map();
    }
    /**
     * Register a SharedDocumentFactory.
     *
     * @param type Document type
     * @param factory Document factory
     */
    registerDocumentFactory(type, factory) {
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
    createNew(options) {
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
            const factory = this.documentFactories.get(options.contentType);
            const sharedModel = factory(options);
            this._onCreate(options, sharedModel);
            return sharedModel;
        }
        return;
    }
}
