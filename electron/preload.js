const { contextBridge, ipcRenderer } = require('electron');
const os = require('os');
const path = require('path');

contextBridge.exposeInMainWorld('tojoAPI', {
  // --- Message / Backend Communication ---
  sendMessage: (message) => ipcRenderer.invoke('send-message', message),
  onBackendMessage: (callback) => {
    ipcRenderer.on('backend-message', (_event, data) => callback(data));
  },
  onBackendStatus: (callback) => {
    ipcRenderer.on('backend-status', (_event, status) => callback(status));
  },

  // --- File / Folder Dialogs ---
  selectFile: (options) => ipcRenderer.invoke('dialog-open-file', options),
  selectFolder: () => ipcRenderer.invoke('dialog-open-folder'),
  selectSaveFile: (options) => ipcRenderer.invoke('dialog-save-file', options),

  // --- System Info ---
  getSystemInfo: () => ({
    platform: process.platform,
    arch: process.arch,
    hostname: os.hostname(),
    username: os.userInfo().username,
    homeDir: os.homedir(),
    cpus: os.cpus().length,
    totalMemory: Math.round(os.totalmem() / (1024 * 1024 * 1024)) + ' GB',
    nodeVersion: process.versions.node,
    electronVersion: process.versions.electron,
    chromeVersion: process.versions.chrome,
  }),

  // --- App Control ---
  minimizeWindow: () => ipcRenderer.send('window-minimize'),
  maximizeWindow: () => ipcRenderer.send('window-maximize'),
  closeWindow: () => ipcRenderer.send('window-close'),

  // --- OpenClaw Status ---
  getOpenClawStatus: () => ipcRenderer.invoke('openclaw-status'),
});
