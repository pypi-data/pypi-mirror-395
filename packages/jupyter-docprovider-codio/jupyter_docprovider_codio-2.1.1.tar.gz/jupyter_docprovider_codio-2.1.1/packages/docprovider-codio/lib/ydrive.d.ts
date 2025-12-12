import { TranslationBundle } from '@jupyterlab/translation';
import { Contents, IContentProvider, RestContentProvider, User } from '@jupyterlab/services';
import { ISignal } from '@lumino/signaling';
import { IDocumentProvider, ISharedModelFactory } from '@jupyter/collaborative-drive';
import { Awareness } from 'y-protocols/awareness';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
export interface IForkProvider {
    connectToForkDoc: (forkRoomId: string, sessionId: string) => Promise<void>;
    reconnect: () => Promise<void>;
    contentType: string;
    format: string;
}
declare namespace RtcContentProvider {
    interface IOptions extends RestContentProvider.IOptions {
        user: User.IManager;
        trans: TranslationBundle;
        globalAwareness: Awareness | null;
        docmanagerSettings: ISettingRegistry.ISettings | null;
    }
}
export declare class RtcContentProvider extends RestContentProvider implements IContentProvider {
    constructor(options: RtcContentProvider.IOptions);
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
     */
    get(localPath: string, options?: Contents.IFetchOptions): Promise<Contents.IModel>;
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
    save(localPath: string, options?: Partial<Contents.IModel>): Promise<Contents.IModel>;
    /**
     * A signal emitted when a file operation takes place.
     */
    get fileChanged(): ISignal<this, Contents.IChangedArgs>;
    private _onCreate;
    private _user;
    private _saveCounter;
    private _trans;
    private _globalAwareness;
    private _providers;
    private _ydriveFileChanged;
    private _serverSettings;
    private _docmanagerSettings;
}
export {};
