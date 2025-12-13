import * as t from '../../types';

describe("noi/integrity.ts", () => {
    let page;

    beforeAll(async () => {
        page = await globalThis.__BROWSER_GLOBAL__.newPage();
        // page.on("console", message => console.log(message.text()));
        await global.wait.runserverInit();
        await page.setDefaultNavigationTimeout(0);
    });

    it("load landing page", async () => {
        await page.goto(global.SERVER_URL);
    });

    it("sign in ok", async () => {
        await page.goto(global.SERVER_URL);
        await page.waitForNetworkIdle();
        await global.signIn(page);
        const logged_in = await page.evaluate(() => {
            return window.App.state.user_settings.logged_in;
        });
        expect(logged_in).toBe(true);
    });

    afterAll(async () => {
        await page.close();
    })
});
