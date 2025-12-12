import { Contents } from '@jupyterlab/services';
export declare const ROOM_FORK_URL = "api/collaboration/fork";
/**
 * Document session model
 */
export interface ISessionModel {
    /**
     * Document format; 'text', 'base64',...
     */
    format: Contents.FileFormat;
    /**
     * Document type
     */
    type: Contents.ContentType;
    /**
     * File unique identifier
     */
    fileId: string;
    /**
     * Server session identifier
     */
    sessionId: string;
}
/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
export declare function requestAPI<T = any>(endPoint?: string, init?: RequestInit): Promise<T>;
export declare function requestDocSession(format: string, type: string, path: string): Promise<ISessionModel>;
export declare function requestDocumentTimeline(format: string, type: string, path: string): Promise<any>;
export declare function requestUndoRedo(roomid: string, action: 'undo' | 'redo' | 'restore', steps: number, forkRoom: string): Promise<any>;
