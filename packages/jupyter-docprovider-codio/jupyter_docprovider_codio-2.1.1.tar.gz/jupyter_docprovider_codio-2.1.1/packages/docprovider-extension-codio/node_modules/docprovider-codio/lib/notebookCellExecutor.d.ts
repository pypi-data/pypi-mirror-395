import { INotebookCellExecutor } from '@jupyterlab/notebook';
import { ServerConnection } from '@jupyterlab/services';
/**
 * Notebook cell executor posting a request to the server for execution.
 */
export declare class NotebookCellServerExecutor implements INotebookCellExecutor {
    private _serverSettings;
    /**
     * Constructor
     *
     * @param options Constructor options; the contents manager, the collaborative drive and optionally the server settings.
     */
    constructor(options: {
        serverSettings?: ServerConnection.ISettings;
    });
    /**
     * Execute a given cell of the notebook.
     *
     * @param options Execution options
     * @returns Execution success status
     */
    runCell({ cell, notebook, notebookConfig, onCellExecuted, onCellExecutionScheduled, sessionContext, sessionDialogs, translator }: INotebookCellExecutor.IRunCellOptions): Promise<boolean>;
}
