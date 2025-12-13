import * as t from '../../types';
import * as constants from "../../constants";
import { setTimeout } from "timers/promises";
import queryString from 'query-string';


describe("avanti/URLContext.ts", () => {
    let page;

    beforeAll(async () => {
        page = await globalThis.__BROWSER_GLOBAL__.newPage();
        // page.on("console", message => console.log(message.text()));
        await global.wait.runserverInit();
        await page.setDefaultNavigationTimeout(0);

        await page.goto(global.SERVER_URL);
        await page.waitForNetworkIdle();
        await global.signIn(page);
    })

    it("test [Read eID card] action", async () => {
        const postURL = `${global.SERVER_URL}/api/avanti/Clients`;
        let requestData, responseData;

        await page.setRequestInterception(true);
        page.on('request', async request => {
            if (request.isInterceptResolutionHandled()) return;
            request.continue();
            if (request.url() === postURL)
                requestData = queryString.parse(request.postData());
        });
        page.on('response', async response => {
            if (response.url() === postURL)
                responseData = await response.json();
        });

        await page.evaluate(() => {
            const { actionHandler } = window.App.URLContext;
            const action = actionHandler.findUniqueAction("find_by_beid");
            actionHandler.runAction({actorId: "avanti.Clients", action_full_name: action.full_name});
        });
        await page.waitForNetworkIdle();

        expect(requestData).not.toBe(undefined);
        expect(responseData).not.toBe(undefined);

        expect(requestData.an).toEqual("find_by_beid");
        expect(responseData).toEqual({
            alert: "Error", message: "Abandoned after 15 seconds",
            success: false});
    });

    afterAll(async () => {
        await page.close();
    });
});
