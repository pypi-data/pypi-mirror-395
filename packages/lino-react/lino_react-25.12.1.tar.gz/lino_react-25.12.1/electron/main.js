const { app, dialog, BrowserWindow } = require('electron');
const { Updater } = require('./updateProvider');
const log = require('electron-log');
const path = require('node:path');
const fs = require('node:fs');
const os = require('node:os');

fs.writeFileSync('dummy.json', JSON.stringify(process.env))


log.transports.file.level = process.env.LOG_LEVEL || 'info';
log.info(`App starting on ${process.platform} ...`);

log.debug("resources path:", process.resourcesPath);

const loadConfig = () => {
    let defaultConfFile = path.join(os.homedir(), '.config/lino-react/default.json'),
        confFile = app.commandLine.getSwitchValue('config'), customConfig = false;
    if (confFile) {
        if (confFile.startsWith('~/'))
            confFile = path.join(os.homedir(), confFile.slice(2));
        customConfig = true;
    } else confFile = defaultConfFile;
    log.debug("Config file:", confFile);
    if (!fs.existsSync(confFile)) {
        if (customConfig) {
            log.error("Config file not found:", confFile);
            process.exit(1);
        }
        const confResFile = path.join(process.resourcesPath, "default-config.json");
        if (!fs.existsSync(confResFile)) {
            log.error("No configuration available. Please throw away this app.");
            process.exit(1);
        }
        fs.mkdirSync(path.dirname(defaultConfFile), {recursive: true});
        fs.writeFileSync(defaultConfFile, fs.readFileSync(confResFile), {flush: true});
    }
    app.config = {};
    if (customConfig) Object.assign(app.config, JSON.parse(fs.readFileSync(defaultConfFile)));
    Object.assign(app.config, JSON.parse(fs.readFileSync(confFile)));
    log.debug("Configuration:", app.config);
}

loadConfig();

const createWindow = () => {
    const continue_ = dialog.showMessageBoxSync({
        message: "Warning! Dragons larking, avoid us?",
        buttons: ["Yes", "No"]

    });
    if (!continue_) process.exit(1);
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
        }
    });

    win.loadURL(process.env.SITE_URL || app.config.SITE_URL || "http://127.0.0.1:8000");
}

app.whenReady().then(() => {
    createWindow();
});

app.on('ready', () => {
    new Updater();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
