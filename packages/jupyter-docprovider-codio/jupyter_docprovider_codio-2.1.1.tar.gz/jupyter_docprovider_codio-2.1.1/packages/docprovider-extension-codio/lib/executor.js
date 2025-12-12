// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module docprovider-extension-codio
 */
import { NotebookCellServerExecutor } from 'docprovider-codio';
import { PageConfig } from '@jupyterlab/coreutils';
import { INotebookCellExecutor, runCell } from '@jupyterlab/notebook';
export const notebookCellExecutor = {
    id: 'docprovider-extension-codio:notebook-cell-executor',
    description: 'Add notebook cell executor that uses REST API instead of kernel protocol over WebSocket.',
    autoStart: true,
    provides: INotebookCellExecutor,
    activate: (app) => {
        if (PageConfig.getOption('serverSideExecution') === 'true') {
            return new NotebookCellServerExecutor({
                serverSettings: app.serviceManager.serverSettings
            });
        }
        return Object.freeze({ runCell });
    }
};
