// @electron-gui/src/main/preload.ts

/**
 * The preload script runs before. It has access to web APIs
 * as well as Electron's renderer process modules and some
 * polyfilled Node.js functions.
 * 
 * In this file, you can expose chosen Electron APIs to the
 * renderer process in a controlled and secure way.
 */

const { contextBridge, ipcRenderer } = require('electron');

/**
 * Expose protected methods that allow the renderer process to use
 * the ipcRenderer without exposing the entire object.
 * 
 * This is a security best practice in Electron.
 */
contextBridge.exposeInMainWorld('electronAPI', {
  // Example of exposing a function to send data to the main process
  send: (channel: string, data: any) => {
    // Whitelist channels to prevent arbitrary IPC calls
    const validChannels = ['notify'];
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data);
    }
  },
  // Example of exposing a function to receive data from the main process
  receive: (channel: string, func: (...args: any[]) => void) => {
    const validChannels = ['my-custom-reply']; // Added new channel for AI responses
    if (validChannels.includes(channel)) {
      // Deliberately strip event as it includes `sender`
      ipcRenderer.on(channel, (event: any, ...args: any[]) => func(...args));
    }
  }
}); 