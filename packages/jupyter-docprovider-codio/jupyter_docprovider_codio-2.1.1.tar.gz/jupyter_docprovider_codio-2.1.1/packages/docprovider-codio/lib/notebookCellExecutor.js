/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { nullTranslator } from '@jupyterlab/translation';
/**
 * Notebook cell executor posting a request to the server for execution.
 */
export class NotebookCellServerExecutor {
    /**
     * Constructor
     *
     * @param options Constructor options; the contents manager, the collaborative drive and optionally the server settings.
     */
    constructor(options) {
        var _a;
        this._serverSettings =
            (_a = options.serverSettings) !== null && _a !== void 0 ? _a : ServerConnection.makeSettings();
    }
    /**
     * Execute a given cell of the notebook.
     *
     * @param options Execution options
     * @returns Execution success status
     */
    async runCell({ cell, notebook, notebookConfig, onCellExecuted, onCellExecutionScheduled, sessionContext, sessionDialogs, translator }) {
        var _a, _b, _c;
        translator = translator !== null && translator !== void 0 ? translator : nullTranslator;
        const trans = translator.load('jupyterlab');
        switch (cell.model.type) {
            case 'markdown':
                cell.rendered = true;
                cell.inputHidden = false;
                onCellExecuted({ cell, success: true });
                break;
            case 'code':
                if (sessionContext) {
                    if (sessionContext.isTerminating) {
                        await showDialog({
                            title: trans.__('Kernel Terminating'),
                            body: trans.__('The kernel for %1 appears to be terminating. You can not run any cell for now.', (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.path),
                            buttons: [Dialog.okButton()]
                        });
                        break;
                    }
                    if (sessionContext.pendingInput) {
                        await showDialog({
                            title: trans.__('Cell not executed due to pending input'),
                            body: trans.__('The cell has not been executed to avoid kernel deadlock as there is another pending input! Submit your pending input and try again.'),
                            buttons: [Dialog.okButton()]
                        });
                        return false;
                    }
                    if (sessionContext.hasNoKernel) {
                        const shouldSelect = await sessionContext.startKernel();
                        if (shouldSelect && sessionDialogs) {
                            await sessionDialogs.selectKernel(sessionContext);
                        }
                    }
                    if (sessionContext.hasNoKernel) {
                        cell.model.sharedModel.transact(() => {
                            cell.model.clearExecution();
                        });
                        return true;
                    }
                    const kernelId = (_c = (_b = sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.id;
                    const apiURL = URLExt.join(this._serverSettings.baseUrl, `api/kernels/${kernelId}/execute`);
                    const cellId = cell.model.sharedModel.getId();
                    const documentId = notebook.sharedModel.getState('document_id');
                    const init = {
                        method: 'POST',
                        body: JSON.stringify({ cell_id: cellId, document_id: documentId })
                    };
                    onCellExecutionScheduled({ cell });
                    let success = false;
                    try {
                        // FIXME quid of deletedCells and timing record
                        const response = await ServerConnection.makeRequest(apiURL, init, this._serverSettings);
                        success = response.ok;
                    }
                    catch (error) {
                        onCellExecuted({
                            cell,
                            success: false
                        });
                        if (cell.isDisposed) {
                            return false;
                        }
                        else {
                            throw error;
                        }
                    }
                    onCellExecuted({ cell, success });
                    return true;
                }
                cell.model.sharedModel.transact(() => {
                    cell.model.clearExecution();
                }, false);
                break;
            default:
                break;
        }
        return Promise.resolve(true);
    }
}
