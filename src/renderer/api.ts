// @electron-gui/src/renderer/api.ts

/**
 * This file defines the shape of the API that is exposed from the
 * preload script to the renderer process.
 * It's used to provide type safety for the `window.electronAPI` object.
 */
export interface IElectronAPI {
    send: (channel: string, data?: any) => void;
    receive: (channel: string, func: (...args: any[]) => void) => void;
}

// Extend the global Window interface
declare global {
    interface Window {
        electronAPI: IElectronAPI;
    }
} 