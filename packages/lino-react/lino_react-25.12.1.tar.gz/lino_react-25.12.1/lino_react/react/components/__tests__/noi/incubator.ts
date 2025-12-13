import * as t from '../../types';
import * as constants from "../../constants";
import { setTimeout } from "timers/promises";

describe("noi/incubator.ts", () => {
    it.skip("placeholder", async () => {});

    let page;

    beforeAll(async () => {
        page = await globalThis.__BROWSER_GLOBAL__.newPage();
        // page.on("console", message => console.log(message.text()));
        await global.wait.runserverInit();
        await page.setDefaultNavigationTimeout(0);
    });

    beforeEach(async () => {
        await page.goto(global.SERVER_URL);
        await page.waitForNetworkIdle();
        await global.signIn(page);
    });

    afterAll(async () => {
        await page.close();
    });
});
