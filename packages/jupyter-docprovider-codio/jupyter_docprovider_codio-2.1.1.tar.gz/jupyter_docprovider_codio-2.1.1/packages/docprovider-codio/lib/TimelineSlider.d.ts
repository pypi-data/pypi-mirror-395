import { ReactWidget } from '@jupyterlab/apputils';
import { IForkProvider } from './ydrive';
export declare class TimelineWidget extends ReactWidget {
    private apiURL;
    private provider;
    private contentType;
    private format;
    private documentTimelineUrl;
    private projectIsComplete;
    private docIsReadonly;
    constructor(apiURL: string, provider: IForkProvider, contentType: string, format: string, documentTimelineUrl: string, projectIsComplete: boolean, docIsReadonly: boolean);
    render(): JSX.Element;
    updateContent(apiURL: string, provider: IForkProvider): void;
}
