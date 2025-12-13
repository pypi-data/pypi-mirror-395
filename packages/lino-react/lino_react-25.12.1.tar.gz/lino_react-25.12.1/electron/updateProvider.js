const { Provider, DebUpdater, DOWNLOAD_PROGRESS } = require('electron-updater');
const log = require('electron-log');
const { ElectronHttpExecutor } = require("electron-updater/out/electronHttpExecutor");
const { getFileList } = require("electron-updater/out/providers/Provider");
const { newUrlFromBase } = require("electron-updater/out/util");

const fs = require('fs');
const { chmod, mkdir, unlink, rename } = require('fs-extra');
const path = require('node:path');

const DownloadedUpdateHelper_1 = require("electron-updater/out/DownloadedUpdateHelper");
const builder_util_runtime_1 = require("builder-util-runtime");

const UPDATE_SERVER_URL = "http://127.0.0.1:1337";


class UpdateProvider extends Provider {

    constructor(...options) {
        super(...options);
        this.executor = new ElectronHttpExecutor();
    }

    async getLatestVersion() {
        let v = JSON.parse(await this.httpRequest(new URL(`${UPDATE_SERVER_URL}/versions/sorted`))).items[0];
        return {
            version: v.name,
            files: [
                {
                    url: `${UPDATE_SERVER_URL}/download/${v.name}/linux_64`,
                    size: v.assets[0].size,
                    // sha512: v.assets[0].hash,
                }
            ]
        }
    }

    resolveFiles(updateInfo) {
        const baseUrl = new URL(UPDATE_SERVER_URL);
        const files = getFileList(updateInfo);
        const result = files.map(fileInfo => ({
            url: (0, newUrlFromBase)(fileInfo.url, baseUrl),
            info: fileInfo}));
        const packages = updateInfo.packages;
        const packageInfo = packages == null ? null : packages[process.arch] || packages.ia32;
        if (packageInfo != null) {
            result[0].packageInfo = {
                ...packageInfo,
                path: (0, newUrlFromBase)(packageInfo.path, baseUrl).href,
            };
        }
        return result;
    }
}


class DebUpdaterExtended extends DebUpdater {
    async executeDownload(taskOptions) {
        const fileInfo = taskOptions.fileInfo;
        const downloadOptions = {
            headers: taskOptions.downloadUpdateOptions.requestHeaders,
            cancellationToken: taskOptions.downloadUpdateOptions.cancellationToken,
            sha2: fileInfo.info.sha2,
            sha512: fileInfo.info.sha512,
        };
        if (this.listenerCount(DOWNLOAD_PROGRESS) > 0) {
            downloadOptions.onProgress = it => this.emit(DOWNLOAD_PROGRESS, it);
        }
        const updateInfo = taskOptions.downloadUpdateOptions.updateInfoAndProvider.info;
        const version = updateInfo.version;
        const packageInfo = fileInfo.packageInfo;
        function getCacheUpdateFileName() {
            return updateInfo.version;
        }
        const downloadedUpdateHelper = await this.getOrCreateDownloadHelper();
        const cacheDir = downloadedUpdateHelper.cacheDirForPendingUpdate;
        await (0, mkdir)(cacheDir, { recursive: true });
        const updateFileName = getCacheUpdateFileName();
        let updateFile = path.join(cacheDir, updateFileName);
        const packageFile = packageInfo == null ? null : path.join(cacheDir, `package-${version}${path.extname(packageInfo.path) || ".7z"}`);
        const done = async (isSaveCache) => {
            await downloadedUpdateHelper.setDownloadedFile(updateFile, packageFile, updateInfo, fileInfo, updateFileName, isSaveCache);
            const doneEvent = {...updateInfo, downloadedFile: updateFile};
            if (taskOptions.done) {
                await taskOptions.done(doneEvent);
            } else {
                this.dispatchUpdateDownloaded(doneEvent);
                this.addQuitHandler();
            }
            return packageFile == null ? [updateFile] : [updateFile, packageFile];
        };
        const log = this._logger;
        const cachedUpdateFile = await downloadedUpdateHelper.validateDownloadedPath(updateFile, updateInfo, fileInfo, log);
        if (cachedUpdateFile != null) {
            updateFile = cachedUpdateFile;
            return await done(false);
        }
        const removeFileIfAny = async () => {
            await downloadedUpdateHelper.clear().catch(() => {
                // ignore
            });
            return await (0, unlink)(updateFile).catch(() => {
                // ignore
            });
        };
        const tempUpdateFile = await (0, DownloadedUpdateHelper_1.createTempUpdateFile)(`temp-${updateFileName}`, cacheDir, log);
        try {
            await taskOptions.task(tempUpdateFile, downloadOptions, packageFile, removeFileIfAny);
            await (0, rename)(tempUpdateFile, updateFile);
        }
        catch (e) {
            await removeFileIfAny();
            if (e instanceof builder_util_runtime_1.CancellationError) {
                log.info("cancelled");
                this.emit("update-cancelled", updateInfo);
            }
            throw e;
        }
        log.info(`New version ${version} has been downloaded to ${updateFile}`);
        return await done(true);
    }
}

class Updater {
    constructor() {
        const options = {
            provider: 'custom',
            updateProvider: UpdateProvider,
            isUseMultipleRangeRequest: true
        }
        const autoUpdater = new DebUpdaterExtended(options);
        autoUpdater.forceDevUpdateConfig = true;
        autoUpdater.disableDifferentialDownload = true;
        autoUpdater.logger = log;
        autoUpdater.logger.transports.file.level = process.env.LOG_LEVEL || 'info';
        autoUpdater.checkForUpdatesAndNotify({
            title: "New update available",
            body: "blu blu blu"
        });
    }
}

module.exports = {Updater, UPDATE_SERVER_URL}
