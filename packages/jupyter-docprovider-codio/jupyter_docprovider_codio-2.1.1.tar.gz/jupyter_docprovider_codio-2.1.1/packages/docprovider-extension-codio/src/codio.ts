/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

declare global {
  interface Window {
      codio: any;
  }
}

export const deferred = () => {
  let resolve: any;
  let reject: any;
  const promise = new Promise((resolveF, rejectF) => {
    resolve = resolveF;
    reject = rejectF;
  });
  return { resolve, reject, promise };
};

export const codioClientLoadDeferred = deferred();
const loadJS = (url: string, onLoad: any, location: any) => {
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

export const loadCodioClient = async (codioClientUrl?: string) => {
  // do not double load
  if (window.codio) {
    codioClientLoadDeferred.resolve();
    return
  }
  if (!codioClientUrl) {
    codioClientUrl = 'https://codio.com/ext/iframe/base/static/codio-client.js';
  }
  loadJS(codioClientUrl, onLoadCodioClient, document.body);
  await codioClientLoadDeferred.promise
}

export const sendErrorEvent = async function (message: string, context: any) {
  try {
    console.log('[docprovider-extension] codio sendErrorEvent', message, context)
    await window.codio?.loaded()
    window.codio?.event('error', {
      message: message,
      context: context
    })
  } catch (e) {
    console.log('[docprovider-extension] sendErrorEvent', e)
  }
}

export const getCodioProjectState = async () => {
  if (!window.codio) {
    return false
  }

  const p = new Promise((resolve, reject) => {
    window.codio.subscribe('projectState', async (data: any) => {
      resolve(data)
    })
    setTimeout(() => {
      resolve({})
    }, 10 * 1000)
  })

  window.codio?.setLoaded()
  await window.codio.loaded()

  return p
}
