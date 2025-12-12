import React from 'react';
import '../style/slider.css';
import { IForkProvider } from './ydrive';
type Props = {
    apiURL: string;
    provider: IForkProvider;
    contentType: string;
    format: string;
    documentTimelineUrl: string;
    projectIsComplete: boolean;
    docIsReadonly: boolean;
};
export declare const TimelineSliderComponent: React.FC<Props>;
export {};
