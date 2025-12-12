/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
import { IEditorWidgetFactory } from '@jupyterlab/fileeditor';
import { INotebookWidgetFactory } from '@jupyterlab/notebook';
import { RtcContentProvider } from '@jupyter/my-shared-docprovider';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { YFile, YNotebook } from '@jupyter/ydoc';
import { ICollaborativeContentProvider } from '@jupyter/collaborative-drive';
/**
 * The shared drive provider.
 */
export const rtcContentProvider = {
    id: '@jupyter/docprovider-extension:content-provider',
    description: 'The RTC content provider',
    provides: ICollaborativeContentProvider,
    optional: [ITranslator],
    activate: (app, translator) => {
        translator = translator !== null && translator !== void 0 ? translator : nullTranslator;
        const trans = translator.load('my-jupyter-shared-drive');
        const defaultDrive = app.serviceManager.contents
            .defaultDrive;
        if (!defaultDrive) {
            throw Error('Cannot initialize content provider: default drive property not accessible on contents manager instance.');
        }
        const registry = defaultDrive.contentProviderRegistry;
        if (!registry) {
            throw Error('Cannot initialize content provider: no content provider registry.');
        }
        const rtcContentProvider = new RtcContentProvider(app, {
            currentDrive: defaultDrive,
            user: app.serviceManager.user,
            trans
        });
        registry.register('rtc', rtcContentProvider);
        return rtcContentProvider;
    }
};
/**
 * Plugin to register the shared model factory for the content type 'file'.
 */
export const yfile = {
    id: '@jupyter/my-shared-docprovider-extension:yfile',
    description: "Plugin to register the shared model factory for the content type 'file'",
    autoStart: true,
    requires: [ICollaborativeContentProvider, IEditorWidgetFactory],
    optional: [],
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
    id: '@jupyter/my-shared-docprovider-extension:ynotebook',
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
