/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
import { ReactWidget } from '@jupyterlab/apputils';
import { TimelineSliderComponent } from './component';
import * as React from 'react';
export class TimelineWidget extends ReactWidget {
    constructor(apiURL, provider, contentType, format, documentTimelineUrl, projectIsComplete, docIsReadonly) {
        super();
        this.apiURL = apiURL;
        this.provider = provider;
        this.contentType = contentType;
        this.format = format;
        this.documentTimelineUrl = documentTimelineUrl;
        this.projectIsComplete = projectIsComplete;
        this.docIsReadonly = docIsReadonly;
        this.addClass('jp-timelineSliderWrapper');
    }
    render() {
        return (React.createElement(TimelineSliderComponent, { key: this.apiURL, apiURL: this.apiURL, provider: this.provider, contentType: this.contentType, format: this.format, documentTimelineUrl: this.documentTimelineUrl, projectIsComplete: this.projectIsComplete, docIsReadonly: this.docIsReadonly }));
    }
    updateContent(apiURL, provider) {
        this.apiURL = apiURL;
        this.provider = provider;
        this.contentType = this.provider.contentType;
        this.format = this.provider.format;
        this.update();
    }
}
