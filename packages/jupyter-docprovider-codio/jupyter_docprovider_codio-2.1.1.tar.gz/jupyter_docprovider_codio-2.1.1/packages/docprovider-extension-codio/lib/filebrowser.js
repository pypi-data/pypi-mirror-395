/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { IStatusBar } from '@jupyterlab/statusbar';
import { IEditorTracker, IEditorWidgetFactory } from '@jupyterlab/fileeditor';
import { ILoggerRegistry } from '@jupyterlab/logconsole';
import { INotebookTracker, INotebookWidgetFactory } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { YFile, YNotebook } from '@jupyter/ydoc';
import { ICollaborativeContentProvider, IGlobalAwareness } from '@jupyter/collaborative-drive';
import { TimelineWidget, RtcContentProvider } from 'docprovider-codio';
import { URLExt } from '@jupyterlab/coreutils';
import { loadCodioClient, getCodioProjectState } from './codio';
const DOCUMENT_TIMELINE_URL = 'api/collaboration/timeline';
const TWO_SESSIONS_WARNING = 'The file %1 has been opened with two different views. ' +
    'This is not supported. Please close this view; otherwise, ' +
    'some of your edits may not be saved properly.';
export const rtcContentProvider = {
    id: 'docprovider-extension-codio:content-provider',
    description: 'The RTC content provider',
    provides: ICollaborativeContentProvider,
    requires: [ITranslator],
    optional: [IGlobalAwareness, ISettingRegistry],
    activate: async (app, translator, globalAwareness, settingRegistry) => {
        const trans = translator.load('jupyter_collaboration');
        const defaultDrive = app.serviceManager.contents
            .defaultDrive;
        if (!defaultDrive) {
            throw Error('Cannot initialize content provider: default drive property not accessible on contents manager instance.');
        }
        const registry = defaultDrive.contentProviderRegistry;
        if (!registry) {
            throw Error('Cannot initialize content provider: no content provider registry.');
        }
        const docmanagerSettings = settingRegistry
            ? await settingRegistry.load('@jupyterlab/docmanager-extension:plugin')
            : null;
        const rtcContentProvider = new RtcContentProvider({
            apiEndpoint: '/api/contents',
            serverSettings: defaultDrive.serverSettings,
            user: app.serviceManager.user,
            trans,
            globalAwareness,
            docmanagerSettings
        });
        registry.register('rtc', rtcContentProvider);
        return rtcContentProvider;
    }
};
/**
 * Plugin to register the shared model factory for the content type 'file'.
 */
export const yfile = {
    id: 'docprovider-extension-codio:yfile',
    description: "Plugin to register the shared model factory for the content type 'file'",
    autoStart: true,
    requires: [ICollaborativeContentProvider, IEditorWidgetFactory],
    activate: (app, contentProvider, editorFactory) => {
        const yFileFactory = () => {
            return new YFile();
        };
        contentProvider.sharedModelFactory.registerDocumentFactory('file', yFileFactory);
        editorFactory.contentProviderId = 'rtc';
    }
};
/**
 * Plugin to register the shared model factory for the content type 'notebook'.
 */
export const ynotebook = {
    id: 'docprovider-extension-codio:ynotebook',
    description: "Plugin to register the shared model factory for the content type 'notebook'",
    autoStart: true,
    requires: [ICollaborativeContentProvider, INotebookWidgetFactory],
    optional: [ISettingRegistry],
    activate: (app, contentProvider, notebookFactory, settingRegistry) => {
        let disableDocumentWideUndoRedo = true;
        // Fetch settings if possible.
        if (settingRegistry) {
            settingRegistry
                .load('@jupyterlab/notebook-extension:tracker')
                .then(settings => {
                const updateSettings = (settings) => {
                    var _a;
                    const enableDocWideUndo = settings === null || settings === void 0 ? void 0 : settings.get('experimentalEnableDocumentWideUndoRedo').composite;
                    disableDocumentWideUndoRedo = (_a = !enableDocWideUndo) !== null && _a !== void 0 ? _a : true;
                };
                updateSettings(settings);
                settings.changed.connect((settings) => updateSettings(settings));
            });
        }
        const yNotebookFactory = () => {
            return new YNotebook({
                disableDocumentWideUndoRedo
            });
        };
        contentProvider.sharedModelFactory.registerDocumentFactory('notebook', yNotebookFactory);
        notebookFactory.contentProviderId = 'rtc';
    }
};
/**
 * A plugin to add a timeline slider status item to the status bar.
 */
// 
export const statusBarTimeline = {
    id: 'docprovider-extension-codio:statusBarTimeline',
    description: 'Plugin to add a timeline slider to the status bar',
    autoStart: true,
    requires: [IStatusBar, ICollaborativeContentProvider, IDocumentManager],
    activate: async (app, statusBar, contentProvider, docManager) => {
        try {
            await loadCodioClient("https://codio.com/ext/iframe/base/static/codio-client.js");
            const codioProjectState = await getCodioProjectState();
            let sliderItem = null;
            let timelineWidget = null;
            const updateTimelineForDocument = async (documentPath, documentId) => {
                var _a;
                if (!documentId) {
                    return;
                }
                // Dispose of the previous timelineWidget if it exists
                if (timelineWidget) {
                    timelineWidget.dispose();
                    timelineWidget = null;
                }
                const [format, type] = documentId.split(':');
                const provider = contentProvider.providers.get(`${format}:${type}:${documentPath}`);
                if (!provider) {
                    // this can happen for documents which are not provisioned with RTC
                    return;
                }
                const forkProvider = provider;
                const fullPath = URLExt.join(app.serviceManager.serverSettings.baseUrl, DOCUMENT_TIMELINE_URL, documentPath);
                let docIsReadonly = false;
                const shellWidget = app.shell.currentWidget;
                if (shellWidget) {
                    const docContext = docManager.contextForWidget(shellWidget);
                    if (docContext) {
                        docIsReadonly = ((_a = docContext.contentsModel) === null || _a === void 0 ? void 0 : _a.writable) !== true;
                    }
                }
                timelineWidget = new TimelineWidget(fullPath, forkProvider, forkProvider.contentType, forkProvider.format, DOCUMENT_TIMELINE_URL, codioProjectState && codioProjectState.complete, docIsReadonly);
                const elt = document.getElementById('jp-slider-status-bar');
                if (elt && !timelineWidget.isAttached) {
                    Widget.attach(timelineWidget, elt);
                }
            };
            if (app.shell.currentChanged) {
                app.shell.currentChanged.connect(async (_, args) => {
                    const currentWidget = args.newValue;
                    if (timelineWidget) {
                        // Dispose of the timelineWidget when the document is closed
                        timelineWidget.dispose();
                        timelineWidget = null;
                    }
                    if (currentWidget && 'context' in currentWidget) {
                        await currentWidget.context.ready;
                        await updateTimelineForDocument(currentWidget.context.path, currentWidget.context.model.sharedModel.getState('document_id'));
                    }
                });
            }
            if (statusBar) {
                if (!sliderItem) {
                    sliderItem = new Widget();
                    sliderItem.addClass('jp-StatusBar-GroupItem');
                    sliderItem.addClass('jp-mod-highlighted');
                    sliderItem.id = 'jp-slider-status-bar';
                    statusBar.registerStatusItem('jp-slider-status-bar', {
                        item: sliderItem,
                        align: 'left',
                        rank: 4,
                        isActive: () => {
                            var _a, _b;
                            const currentWidget = app.shell
                                .currentWidget;
                            return ((_b = (_a = currentWidget === null || currentWidget === void 0 ? void 0 : currentWidget.context) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.collaborative) || false;
                        }
                    });
                }
            }
        }
        catch (error) {
            console.error('Failed to activate statusBarTimeline plugin:', error);
        }
    }
};
/**
 * The default collaborative drive provider.
 */
export const logger = {
    id: 'docprovider-extension-codio:logger',
    description: 'A logging plugin for debugging purposes.',
    autoStart: true,
    optional: [ILoggerRegistry, IEditorTracker, INotebookTracker, ITranslator],
    activate: (app, loggerRegistry, fileTracker, nbTracker, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : nullTranslator).load('jupyter_collaboration');
        const schemaID = 'https://schema.jupyter.org/jupyter_collaboration/session/v1';
        if (!loggerRegistry) {
            app.serviceManager.events.stream.connect((_, emission) => {
                var _a, _b;
                if (emission.schema_id === schemaID) {
                    console.debug(`[${emission.room}(${emission.path})] ${(_a = emission.action) !== null && _a !== void 0 ? _a : ''}: ${(_b = emission.msg) !== null && _b !== void 0 ? _b : ''}`);
                    if (emission.level === 'WARNING') {
                        showDialog({
                            title: trans.__('Warning'),
                            body: trans.__(TWO_SESSIONS_WARNING, emission.path),
                            buttons: [Dialog.okButton()]
                        });
                    }
                }
            });
            return;
        }
        const loggers = new Map();
        const addLogger = (sender, document) => {
            const logger = loggerRegistry.getLogger(document.context.path);
            loggers.set(document.context.localPath, logger);
            document.disposed.connect(document => {
                loggers.delete(document.context.localPath);
            });
        };
        if (fileTracker) {
            fileTracker.widgetAdded.connect(addLogger);
        }
        if (nbTracker) {
            nbTracker.widgetAdded.connect(addLogger);
        }
        void (async () => {
            var _a, _b;
            const { events } = app.serviceManager;
            for await (const emission of events.stream) {
                if (emission.schema_id === schemaID) {
                    const logger = loggers.get(emission.path);
                    logger === null || logger === void 0 ? void 0 : logger.log({
                        type: 'text',
                        level: emission.level.toLowerCase(),
                        data: `[${emission.room}] ${(_a = emission.action) !== null && _a !== void 0 ? _a : ''}: ${(_b = emission.msg) !== null && _b !== void 0 ? _b : ''}`
                    });
                    if (emission.level === 'WARNING') {
                        showDialog({
                            title: trans.__('Warning'),
                            body: trans.__(TWO_SESSIONS_WARNING, emission.path),
                            buttons: [Dialog.warnButton({ label: trans.__('Ok') })]
                        });
                    }
                }
            }
        })();
    }
};
