import { ICollaborativeContentProvider } from '@jupyter/collaborative-drive';
import { Event } from '@jupyterlab/services';
import { ISignal } from '@lumino/signaling';
import { IAllForksResponse, IForkChangedEvent, IForkCreationResponse, IForkManager } from './tokens';
import { IForkProvider } from './ydrive';
export declare const JUPYTER_COLLABORATION_FORK_EVENTS_URI = "https://schema.jupyter.org/jupyter_collaboration/fork/v1";
export declare class ForkManager implements IForkManager {
    constructor(options: ForkManager.IOptions);
    get isDisposed(): boolean;
    get forkAdded(): ISignal<ForkManager, IForkChangedEvent>;
    get forkDeleted(): ISignal<ForkManager, IForkChangedEvent>;
    dispose(): void;
    createFork(options: {
        rootId: string;
        synchronize: boolean;
        title?: string;
        description?: string;
    }): Promise<IForkCreationResponse | undefined>;
    getAllForks(rootId: string): Promise<IAllForksResponse>;
    deleteFork(options: {
        forkId: string;
        merge: boolean;
    }): Promise<void>;
    getProvider(options: {
        documentPath: string;
        format: string;
        type: string;
    }): IForkProvider | undefined;
    private _handleEvent;
    private _disposed;
    private _contentProvider;
    private _eventManager;
    private _forkAddedSignal;
    private _forkDeletedSignal;
}
export declare namespace ForkManager {
    interface IOptions {
        contentProvider: ICollaborativeContentProvider;
        eventManager: Event.IManager;
    }
}
