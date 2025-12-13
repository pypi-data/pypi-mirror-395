import '@testing-library/jest-dom';
import path from 'path';
import { setTimeout } from "timers/promises";
import { get } from 'http';
import * as t from "../components/types";

type condition = () => boolean;

global.SERVER_PATH = "127.0.0.1:3000";
global.SERVER_URL = `http://${global.SERVER_PATH}`;
global.WAIT_TIMEOUT = 20000;

global.waitToMeet = async (page, fn: condition, ...args) => {
    const initTime: number = Date.now();
    while ((Date.now() - initTime) < global.WAIT_TIMEOUT) {
        if (await page.evaluate(fn, ...args)) return;
        await setTimeout(300);
    }

    let err = Error("Could not satisfy condition");
    throw err;
}

global.wait = {
    actionHandlerReady: async (page) => {
        await global.waitToMeet(page, () => (
            window.App.hasOwnProperty('URLContext') &&
            window.App.URLContext.hasOwnProperty('actionHandler') &&
            window.App.URLContext.actionHandler.ready));
    },
    parserReady: async (page) => {
        await global.wait.actionHandlerReady(page);
        await global.waitToMeet(page,
            () => window.App.URLContext.actionHandler.parser.ready);
    },
    dataContextReady: async (page) => {
        await global.wait.parserReady(page);
        await global.waitToMeet(page, () => {
            return (window.App.URLContext.hasOwnProperty('dataContext') &&
                window.App.URLContext.dataContext.ready)
        })
    },
    dataLoadDone: async (page) => {
        await global.wait.dataContextReady(page);
        await global.waitToMeet(page, () => {
            // return true;
            return window.App.URLContext.dataContext.mutableContext.success;
        });
    },
    runserverInit: async () => {
        // process.stdout.write("===========================\n");
        const oto = global.WAIT_TIMEOUT;
        global.WAIT_TIMEOUT = 30000;

        let ok = false;
        const initTime = Date.now();
        while ((Date.now() - initTime) < global.WAIT_TIMEOUT) {
            if (await new Promise((resolve) => {
                get(global.SERVER_URL, (res) => {
                    // process.stdout.write(`${res.statusCode}\n!!!!!!\n`);
                    ok = res.statusCode === 200;
                    resolve(ok);
                    // resolve(res.statusCode === 200);
                }).on('error', (e) => {
                    resolve(false);
                })
            }).then(r => r))
                break;
            await setTimeout(300);
        }
        if (!ok) throw "runserver failed!";
        // process.stdout.write("===========================\n");
        global.WAIT_TIMEOUT = oto;
    },
}

global.signIn = async (page) => {
    await global.wait.dataContextReady(page);
    if (await page.evaluate(() => window.App.state.user_settings.logged_in))
        return;
    await page.evaluate(() => {
        const { actionHandler } = window.App.URLContext;
        const action = actionHandler.findUniqueAction("sign_in");
        actionHandler.runAction({actorId: "about.About", action_full_name: action.full_name});
    });
    await global.waitToMeet(page, (): boolean => {
        let { URLContext } = window.App;
        let childContext: t.NavigationContext = Object.values(URLContext.children)[0];
        if (!URLContext.filled(childContext)) return false;
        if (!URLContext.filled(childContext.dataContext)) return false;
        if (!URLContext.filled(childContext.dataContext.mutableContext.data)) return false;
        return true;
    });
    await page.evaluate(() => {
        let context: t.NavigationContext = Object.values(window.App.URLContext.children)[0];
        Object.assign(context.dataContext.mutableContext.data, {
            username: 'robin', password: '1234'});
    });
    await page.evaluate(() => {
        (Object.values(window.App.URLContext.children)[0] as t.NavigationContext).dataContext.root.ok();
    });
    await page.waitForNetworkIdle();
    await global.waitToMeet(page, (): boolean => {
        let { URLContext, state } = window.App;
        if (Object.values(URLContext.children).length) return false;
        if (!URLContext.filled(state.user_settings)) return false;
        if (!URLContext.filled(state.site_data)) return false;
        return state.user_settings.logged_in;
    });
    await global.wait.dataContextReady(page);
}

// page.on("console", message => console.log(message.text()));
// page.on('console', async (msg) => {
//     const msgArgs = msg.args();
//     for (let i = 0; i < msgArgs.length; ++i) {
//         console.log(await msgArgs[i].jsonValue());
//     }
// });
