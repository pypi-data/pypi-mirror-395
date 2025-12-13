import * as constants from '../../constants';

describe("noi/cloneUI.ts", () => {
    let page;

    beforeAll(async () => {
        page = await globalThis.__BROWSER_GLOBAL__.newPage();
        await global.wait.runserverInit();
        await page.setDefaultNavigationTimeout(0);
    });

    it("clone tickets.AllTickets", async () => {
        await page.goto(global.SERVER_URL);
        await global.signIn(page);
        await page.evaluate(() => {
            window.App.URLContext.history.pushPath({pathname: "/api/tickets/AllTickets"})
        });
        await page.waitForNetworkIdle();
        await global.wait.parserReady(page);
        await global.waitToMeet(page, (): boolean => {
            let { URLContext } = window.App;
            if (!URLContext.root.state.initialized) return false;
            if (!URLContext.filled(URLContext.dataContext)) return false;
            if (!URLContext.filled(URLContext.dataContext.mutableContext.rows)) return false;
            return true;
        });

        await page.evaluate((constants) => {
            window.App.URLContext.history.replaceState({
                [constants.URL_PARAM_LIMIT]: 25,
                [constants.URL_PARAM_DISPLAY_MODE]: constants.DISPLAY_MODE_CARDS,
            });
        }, constants);
        await page.waitForNetworkIdle();

        await global.waitToMeet(page, (): boolean => {
            let { URLContext } = window.App;
            if (!URLContext.dataContext) return false;
            if (URLContext.dataContext.root.state.loading) return false;
            return true;
        });

        const [clone, cloneSTR] = await page.evaluate(constants => {
            let {actionHandler} = window.App.URLContext,
                c = actionHandler.cloneState(constants.CLONE_LEVEL_DATA);
            return [c, actionHandler.parser.stringify(
                actionHandler.ex._.cloneDeep(c), true)];
        }, constants);

        const strRevert = await page.evaluate((cloneSTR) => {
            return window.App.URLContext.actionHandler.parseClone(cloneSTR);
        }, cloneSTR);

        expect(clone).toEqual(strRevert);
    });

    afterAll(async () => {
        await page.close();
    })
});
