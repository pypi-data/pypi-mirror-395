const {mkdir, writeFile} = require('fs').promises;
const {spawn} = require('child_process');
const os = require('os');
const path = require('path');
const puppeteer = require('puppeteer');

const DIR = path.join(os.tmpdir(), 'jest_puppeteer_global_setup');

module.exports = async (globalConfig, projectConfig) => {
    let browser;
    if (process.getuid() == 0) {
        browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
            protocolTimeout: 120000,
        });
    } else {
        browser = await puppeteer.launch({headless: false});
        // browser = await puppeteer.launch();
    }

    globalThis.__BROWSER_GLOBAL__ = browser;

    await mkdir(DIR, {recursive: true});
    await writeFile(path.join(DIR, 'wsEndpoint'), browser.wsEndpoint());

    const mpy = path.resolve(__dirname).split(path.sep).slice(0, -3)
        .join(path.sep) + `/puppeteers/${process.env.BASE_SITE}/manage.py`;
    globalThis.__SERVER_PROCESS__ = spawn(
        "python",
        [mpy, "runserver", "127.0.0.1:3000"],
        {stdio: 'ignore'}
    );
}
