declare global {
    interface Window {
        codio: any;
    }
}
export declare const deferred: () => {
    resolve: any;
    reject: any;
    promise: Promise<unknown>;
};
export declare const codioClientLoadDeferred: {
    resolve: any;
    reject: any;
    promise: Promise<unknown>;
};
export declare const loadCodioClient: (codioClientUrl?: string) => Promise<void>;
export declare const sendErrorEvent: (message: string, context: any) => Promise<void>;
export declare const getCodioProjectState: () => Promise<unknown>;
