/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
import { ICollaborativeContentProvider } from '@jupyter/collaborative-drive';
import { ForkManager, IForkManagerToken } from 'docprovider-codio';
export const forkManagerPlugin = {
    id: 'docprovider-extension-codio:forkManager',
    autoStart: true,
    requires: [ICollaborativeContentProvider],
    provides: IForkManagerToken,
    activate: (app, contentProvider) => {
        const eventManager = app.serviceManager.events;
        const manager = new ForkManager({ contentProvider, eventManager });
        return manager;
    }
};
