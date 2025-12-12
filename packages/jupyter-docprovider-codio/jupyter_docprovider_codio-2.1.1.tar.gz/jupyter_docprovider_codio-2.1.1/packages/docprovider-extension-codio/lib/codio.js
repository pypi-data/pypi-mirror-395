/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
export const deferred = () => {
    let resolve;
    let reject;
    const promise = new Promise((resolveF, rejectF) => {
        resolve = resolveF;
        reject = rejectF;
    });
    return { resolve, reject, promise };
};
export const codioClientLoadDeferred = deferred();
const loadJS = (url, onLoad, location) => {
    //url is URL of external file, onLoad is the code
    //to be called from the file, location is the location to
    //insert the <script> element
    console.log('[docprovider-extension] loadCodio from url', url);
    const scriptTag = document.createElement('script');
    scriptTag.src = url;
    scriptTag.onload = onLoad;
    scriptTag.onerror = (...args) => {
        console.log('[docprovider-extension] loading script error', args);
        codioClientLoadDeferred.reject(args);
    };
    location.appendChild(scriptTag);
};
const onLoadCodioClient = function () {
    // window.onload event already finished when this code executes. manually set loaded state.
    codioClientLoadDeferred.resolve();
    console.log('[docprovider-extension] codio client loaded');
};
export const loadCodioClient = async (codioClientUrl) => {
    // do not double load
    if (window.codio) {
        codioClientLoadDeferred.resolve();
        return;
    }
    if (!codioClientUrl) {
        codioClientUrl = 'https://codio.com/ext/iframe/base/static/codio-client.js';
    }
    loadJS(codioClientUrl, onLoadCodioClient, document.body);
    await codioClientLoadDeferred.promise;
};
export const sendErrorEvent = async function (message, context) {
    var _a, _b;
    try {
        console.log('[docprovider-extension] codio sendErrorEvent', message, context);
        await ((_a = window.codio) === null || _a === void 0 ? void 0 : _a.loaded());
        (_b = window.codio) === null || _b === void 0 ? void 0 : _b.event('error', {
            message: message,
            context: context
        });
    }
    catch (e) {
        console.log('[docprovider-extension] sendErrorEvent', e);
    }
};
export const getCodioProjectState = async () => {
    var _a;
    if (!window.codio) {
        return false;
    }
    const p = new Promise((resolve, reject) => {
        window.codio.subscribe('projectState', async (data) => {
            resolve(data);
        });
        setTimeout(() => {
            resolve({});
        }, 10 * 1000);
    });
    (_a = window.codio) === null || _a === void 0 ? void 0 : _a.setLoaded();
    await window.codio.loaded();
    return p;
};
