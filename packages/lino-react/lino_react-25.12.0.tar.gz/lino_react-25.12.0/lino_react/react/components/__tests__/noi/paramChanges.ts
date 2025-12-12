import * as constants from '../../constants';
import * as t from '../../types';
import { setTimeout } from "timers/promises";

describe("noi/paramChanges.ts", () => {
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

    it("test working session play at todo list of other users ticket.",
    async () => {
        await page.evaluate(() => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/tickets/MyTicketsToWork"
            });
        });
        await page.waitForNetworkIdle();

        await page.locator(".l-button-pv_control").click();
        await page.waitForSelector("div.l-component>label ::-p-text(Assigned to)");
        const atLabel = await page.$("div.l-component>label ::-p-text(Assigned to)");
        const atParent = await atLabel.getProperty("parentElement");
        const atInput = await atParent.$("div.l-card>span>input");
        await atInput.click({clickCount: 3})
        await atInput.type("Jean");
        await page.waitForNetworkIdle();

        await atLabel.dispose();
        await atParent.dispose();
        await atInput.dispose();

        await page.waitForSelector(".p-autocomplete-items");
        const items = await page.$(".p-autocomplete-items");
        const item = await items.$("div ::-p-text(Jean)");

        await items.dispose();
        await item.click();
        await item.dispose();
        await page.waitForNetworkIdle();

        await page.reload();
        await page.waitForNetworkIdle();

        await page.locator("div.l-grid>div>p.clearfix>a").click();
        await page.waitForNetworkIdle();

        const workflowPlayStop = async () => {
            await page.waitForSelector("div.l-component>label ::-p-text(Workflow)");
            const workflowLabel = await page.$("div.l-component>label ::-p-text(Workflow)");
            const workflowParent = await workflowLabel.getProperty("parentElement");
            const playStop = await workflowParent.$("div>span>a"); // ::-p-text( ▶ )");
            await workflowLabel.dispose();
            await workflowParent.dispose();
            return playStop;
        }

        const playStopCycle = async (playOrStop) => {
            let playStop = await workflowPlayStop();
            let text_playStop = await (await playStop.getProperty("textContent")).jsonValue();

            expect(text_playStop).toEqual(playOrStop);

            await playStop.click();
            await playStop.dispose();
            await page.waitForNetworkIdle();
        }

        await playStopCycle(" ▶ ");
        await playStopCycle(" ■ ");
    });

    it("test #5792", async () => {
        await page.evaluate(() => {
            window.App.URLContext.history.pushPath({pathname: "/api/tickets/MyTicketsToWork"})
        });
        // await global.wait.dataLoadDone(page);
        await page.waitForNetworkIdle();
        await page.evaluate((c) => {
            window.App.URLContext.actionHandler.update({values: {
                assigned_toHidden: 6
            }, windowType: c.WINDOW_TYPE_PARAMS})
        }, constants);
        await page.waitForNetworkIdle();

        await page.reload();
        await page.waitForNetworkIdle();

        await page.waitForSelector("div.l-detail-header>span");
        let header = await page.$("div.l-detail-header>span");
        let headerText = await (await header.getProperty("textContent")).jsonValue();

        expect(headerText).toBe("Tickets to work (Assigned to Luc)")

        await header.dispose();

        // await global.waitToMeet(page, () => {
        //     let t = document.querySelector('div.l-detail-header>span').textContent;
        //     // console.log(t);
        //     return t === "Tickets to work (Assigned to Luc)";
        // });
        await page.locator('div.l-grid>div>p.clearfix>a').click();
        await page.waitForNetworkIdle();

        header = await page.$("div.l-detail-header>span");
        headerText = await (await header.getProperty("textContent")).jsonValue();

        expect(headerText).toBe("Tickets to work (Assigned to Luc) » #10 (Where can I find a Foo when bazing Bazes?)");
        header.dispose();

        // await global.waitToMeet(page, () => {
        //     const header = document.querySelector('div.l-detail-header>span');
        //     if (!header) return false;
        //     let t = header.textContent;
        //     // console.log(t)
        //     return t === "Tickets to work (Assigned to Luc) » #101 (Foo never bars)";
        // })

        const commentsValue = await page.evaluate(() => window.App.URLContext
            .dataContext.refStore.slaveLeaves["comments.CommentsByRFC"].state.value);

        expect(commentsValue).not.toBe(null);
    });
})
