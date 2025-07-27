// @electron-gui/main.ts

// strategy: This is the main Electron process. We're setting up the fundamental window and app lifecycle here.

import { app, BrowserWindow, ipcMain } from 'electron';
import { fileURLToPath } from 'url';
import * as path from 'path';

// ES Module equivalent for __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function startWindow() {
    const window = new BrowserWindow({
        width: 999,
        height: 666,
        autoHideMenuBar: true, // <-- Add this line to hide the menu bar
        // transparent: true, // Enable window transparency
        // frame: false,      // Disable window frame
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'), // Correctly resolved path
            nodeIntegration: false, // <-- Crucial: Set this to false; otherwise, your system may be vulnerable to attacks from external sources.
            contextIsolation: true, // <-- Crucial: Set this to true; otherwise, your program may 'mess' with electron's internal functions.
        },
    });

    // Load the index.html of the start window.
    if (app.isPackaged) {
        window.loadFile(path.join(__dirname, '../../dist/renderer/index.html'));
    } else {
        window.loadURL('http://localhost:5173');
    }

    // Open the DevTools.
    window.webContents.openDevTools();
}

// When Electron is ready, create the window.
app.whenReady().then(() => {
    startWindow();

    // Listen for the 'notify' message from the renderer process
    ipcMain.on('notify', (event, message) => {
        console.log(`Notification from renderer: ${message}`);
    });

  app.on('activate', () => {
    // On macOS, it's common to re-create a window in the app when
    // the dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) {
        startWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
