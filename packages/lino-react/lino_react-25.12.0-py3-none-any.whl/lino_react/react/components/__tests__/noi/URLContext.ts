import * as t from '../../types';
import * as constants from "../../constants";
import { setTimeout } from "timers/promises";

describe("noi/URLContext.ts", () => {
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

    it("Multi row selected delete", async () => {
        await page.evaluate(() => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/tickets/AllTickets"
            });
        });
        await page.waitForNetworkIdle();

        const newTickets = [];

        await createTicket("test ticket 1");

        var {rowPK, headerTitle} = await pkAndTitle();
        expect(headerTitle).toEqual(`All tickets » #${rowPK} (test ticket 1)`);

        newTickets.push(rowPK);

        await createTicket("test ticket 2");

        var {rowPK, headerTitle} = await pkAndTitle();
        expect(headerTitle).toEqual(`All tickets » #${rowPK} (test ticket 2)`);

        newTickets.push(rowPK);

        await page.evaluate((sr, c) => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/tickets/AllTickets",
                params: {
                    [c.URL_PARAM_SELECTED]: sr,
                    [c.URL_PARAM_DISPLAY_MODE]: c.DISPLAY_MODE_TABLE,
                },
            });
        }, newTickets, constants);
        await page.waitForNetworkIdle();

        await page.keyboard.press("Delete");
        await page.locator("button>span ::-p-text(Yes)").click();
        await page.waitForNetworkIdle();

        const selected = await page.evaluate(() => {
            return window.App.URLContext.value.sr;
        });
        expect(selected).toEqual([]);
        const dialogs = await page.evaluate(() => {
            const dF = window.App.dialogFactory;
            return dF.state.children.size + dF.state.callbacks.size;
        });
        expect(dialogs).toEqual(0);
    });

    it("test insert window footer on dashboard", async () => {
        // await page.waitForSelector("div.dashboard-item>h2::-p-text(My Tickets)");
        // const mas = await page.$("div.dashboard-item>h2::-p-text(My Tickets)");
        await page.waitForSelector("div.dashboard-item>h2::-p-text(Tickets to work)");
        const mas = await page.$("div.dashboard-item>h2::-p-text(Tickets to work)");
        await mas.scrollIntoView();
        const insertButton = await mas.$("a.pi-plus-circle");
        await mas.dispose();
        await insertButton.click();
        await insertButton.dispose();
        await page.waitForSelector("div.l-bbar");
        const bbar = await page.$("div.l-bbar");
        const buttonCount = await (await bbar.getProperty("childElementCount")).jsonValue();
        expect(buttonCount).toEqual(1);

        const createButton = await bbar.$("button>span");
        await bbar.dispose();
        const text = await (await createButton.getProperty("textContent")).jsonValue();
        await createButton.dispose();
        expect(text).toEqual("Create");
    });

    it("delayed value component in grid, while changing 'row count' via QuickSearch",
    async () => {
        await page.evaluate(() => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/groups/Groups"
            });
        });
        await page.waitForNetworkIdle();

        const qf = await page.$("input.l-grid-quickfilter");
        await qf.type("pr");
        await page.waitForNetworkIdle();

        const root = await page.$("div#root");
        const elemCount = await (await root.getProperty("childElementCount")).jsonValue();

        expect(elemCount).toBeGreaterThan(0);

        await qf.dispose();
        await root.dispose()
    });

    it("test choices view on an action window", async () => {
        await page.evaluate((c) => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/tickets/AllTickets",
                params: {[c.URL_PARAM_DISPLAY_MODE]: c.DISPLAY_MODE_TABLE}
            });
        }, constants);
        await page.waitForNetworkIdle();

        await page.evaluate(() => {
            const ftid = window.App.URLContext.dataContext.mutableContext.pks[0];
            window.App.URLContext.history.replace({sr: [ftid]});
        });

        await page.locator('span ::-p-text(⚭)').click();
        await page.waitForNetworkIdle();
        await page.waitForSelector("label ::-p-text(into...)");
        await page.keyboard.type("gone");
        await page.waitForNetworkIdle();
        await page.waitForSelector(".p-autocomplete-items");
        const items = await page.$(".p-autocomplete-items");
        const itemCount = await (await items.getProperty("childElementCount")).jsonValue();
        expect(itemCount).toBeGreaterThan(0);

        await items.dispose();

        await page.evaluate((t) => {
            (Object.values(window.App.URLContext.children)[0] as t.NavigationContext)
                .actionHandler.clearMod();
        }, t);
        await page.locator(".p-dialog-header-close").click();
        await global.waitToMeet(page, () => {
            if (window.App.URLContext.children.length) return false;
            return true;
        });
    });

    it("test choices view on an insert action", async () => {
        await page.evaluate(() => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/tickets/AllTickets"
            });
        });
        await page.waitForNetworkIdle();

        await page.keyboard.press("Insert");
        await page.waitForNetworkIdle();

        await page.waitForSelector("label ::-p-text(Summary)");

        await page.keyboard.type("test");

        await page.evaluate((t) => {
            (Object.values(window.App.URLContext.children)[0] as t.NavigationContext)
                .dataContext.refStore.Leaves.order.focus();
        }, t);
        await page.keyboard.type("a");

        await page.waitForSelector(".p-autocomplete-items");
        const items = await page.$(".p-autocomplete-items");
        const itemCount = await (await items.getProperty("childElementCount")).jsonValue();
        expect(itemCount).toBe(1);

        const item = await items.$("div");
        const subscription = await (await item.getProperty("textContent")).jsonValue();

        expect(subscription).toBe("SLA 3/2024 (aab)");

        await item.dispose();
        await items.dispose();

        await page.evaluate((t) => {
            (Object.values(window.App.URLContext.children)[0] as t.NavigationContext)
                .actionHandler.clearMod();
        }, t);
        await page.locator(".p-dialog-header-close").click();
        await global.waitToMeet(page, () => {
            if (window.App.URLContext.children.length) return false;
            return true;
        });
    });

    it("trading.InvoicesByJournal workflow button", async () => {
        await page.evaluate(() => {
             window.App.state.menu_data.filter(
                 md => md.label === 'Sales'
             )[0].items.filter(
                 md => md.label === 'Sales invoices (SLS)'
             )[0].command();
        });
        await page.waitForNetworkIdle();

        const invoice_id = await page.evaluate(() => {
            return window.App.URLContext.dataContext.mutableContext.rows[0][
                window.App.URLContext.static.actorData.pk_index
            ];
        });

        await page.evaluate((pk) => {
            window.App.URLContext.actionHandler.singleRow({}, pk);
        }, invoice_id);
        await page.waitForNetworkIdle();

        await page.evaluate((pk) => {
            const { actionHandler } = window.App.URLContext;
            const action = actionHandler.findUniqueAction("wf2");
            actionHandler.runAction({actorId: "trading.InvoicesByJournal",
                                     action_full_name: action.full_name, sr: pk});
        }, invoice_id)
        await page.waitForNetworkIdle();

        // const clone = await page.evaluate(() => {
        //     return window.App.URLContext.actionHandler.parser.stringify({
        //         clone: {
        //             params: {path: "/api/trading/InvoicesByJournal/86", mk: 1, mt: 66},
        //             runnable: {actorId: "trading.InvoicesByJournal", action_full_name: "wf2", sr: 86},
        //         }
        //     }, true);
        // });
        // await page.goBack();  // Otherwise, browser doesn't load the hash content from the following goto.
        // // 127.0.0.1:8000/#/api/trading/InvoicesByJournal/86?clone=JSON%3A%3A%3A%7B%22params%22%3A%7B%22path%22%3A%22%2Fapi%2Ftrading%2FInvoicesByJournal%2F86%22%2C%22mk%22%3A1%2C%22mt%22%3A72%7D%2C%22runnable%22%3A%7B%22actorId%22%3A%22trading.InvoicesByJournal%22%2C%22an%22%3A%22wf2%22%2C%22sr%22%3A86%7D%7D
        // await page.goto(`${global.SERVER_URL}/#/api/trading/InvoicesByJournal/86?${clone}`);
        // await page.waitForNetworkIdle();

        let wfState;
        wfState = await page.evaluate(() => {
            return window.App.URLContext.dataContext.mutableContext.data.workflow_buttons;
        });
        expect(wfState).toContain("<b>Draft</b>");
        await page.evaluate((pk) => {
            const { actionHandler } = window.App.URLContext;
            const action = actionHandler.findUniqueAction("wf1");
            actionHandler.runAction({actorId: "trading.InvoicesByJournal",
                                     action_full_name: action.full_name, sr: pk});
        }, invoice_id);
        await page.waitForNetworkIdle();
        wfState = await page.evaluate(() => {
            return window.App.URLContext.dataContext.mutableContext.data.workflow_buttons;
        });
        expect(wfState).toContain("<b>Registered</b>");
    });

    it("test grid_put", async () => {
        await page.evaluate((c) => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/tickets/AllTickets",
                params: {[c.URL_PARAM_DISPLAY_MODE]: c.DISPLAY_MODE_TABLE}
            });
        }, constants);
        await page.waitForNetworkIdle();

        let firstSummary = await page.$(".l-grid-col-summary");
        await firstSummary.click();
        await firstSummary.waitForSelector('input');
        let input = await firstSummary.$('input');
        const oldSummary = await (await input.getProperty('value')).jsonValue();
        await input.dispose();

        const inputText = "Nothing important to say!";

        await firstSummary.type(inputText);
        await page.keyboard.press("Enter");
        await page.waitForNetworkIdle();
        await firstSummary.dispose();
        await setTimeout(500);

        const ctxBackupSummary = await page.evaluate(() => {
            const sIndex = window.App.URLContext.static.actorData.col
                .filter(col => col.name === "summary")[0].fields_index;
            return window.App.URLContext.dataContext.contextBackup.rows[0][sIndex];
        });

        expect(ctxBackupSummary).toEqual(inputText);

        firstSummary = await page.$(".l-grid-col-summary");
        await firstSummary.click();
        await firstSummary.waitForSelector('input');

        input = await firstSummary.$("input");
        const newSummary = await (await input.getProperty('value')).jsonValue();
        await input.dispose();

        expect(newSummary).toBe(inputText);

        await firstSummary.type(oldSummary);
        await page.keyboard.press("Enter");
        await page.waitForNetworkIdle();

        await firstSummary.dispose();
    });

    it("TicketsByParent ticket.description open in own window", async () => {
        await page.evaluate((c) => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/tickets/AllTickets",
                params: {[c.URL_PARAM_LIMIT]: 100}
            })
        }, constants);
        await page.waitForNetworkIdle();


        const rows = await page.evaluate(() => {
            return window.App.URLContext.dataContext.mutableContext.rows;
        });

        for (var i = 0; i < rows.length; i++) {
            const row = rows[i];
            await page.evaluate((pk) => {
                window.App.URLContext.history.pushPath({
                    pathname: `/api/tickets/AllTickets/${pk}`,
                    params: {tab: 2}
                });
            }, row.id);
            await page.waitForNetworkIdle();

            const childRows = await page.evaluate((t) => {
                return (Object.values(window.App.URLContext.children)[0] as t.NavigationContext)
                    .dataContext.mutableContext.rows;
            }, t);
            if (childRows.length) {
                await page.evaluate((pk) => {
                    (Object.values(window.App.URLContext.children)[0] as t.NavigationContext)
                        .actionHandler.singleRow({}, pk, window.App.URLContext);
                }, childRows[0].id);
                await page.waitForNetworkIdle();
                break;
            }
        }

        await page.evaluate(() => {
            window.App.URLContext.history.replace({tab: 1});
        });

        await page.locator('span ::-p-text(⏏)').click();
        await page.waitForNetworkIdle();

        const success = await page.evaluate(() => {
            return window.App.URLContext.dataContext.mutableContext.success;
        })
        expect(success).toBe(true);

        const master_key = await page.evaluate((c) => {
            return window.App.URLContext.value[c.URL_PARAM_MASTER_PK];
        }, constants);
        expect(typeof master_key).toEqual("number");

        const master_type = await page.evaluate((c) => {
            return window.App.URLContext.value[c.URL_PARAM_MASTER_TYPE];
        }, constants);
        expect(typeof master_type).toEqual("number");

        const contextType = await page.evaluate(() => {
            return window.App.URLContext.contextType;
        });
        expect(contextType).toEqual(constants.CONTEXT_TYPE_TEXT_FIELD);
    });

    const typeToElement = async (text, label, input_dep) => {
        await page.waitForSelector(label);
        let elementLabel = await page.$(label);
        let elementParent = await elementLabel.getProperty("parentElement");
        let elementInput = await elementParent.$(input_dep);
        await elementInput.click();
        await elementInput.type(text);
        await elementLabel.dispose();
        await elementParent.dispose();
        await elementInput.dispose();
    };

    const createTicket = async (summary) => {
        await page.keyboard.press("Insert");
        await page.waitForNetworkIdle();

        await typeToElement(summary, "label ::-p-text(Summary)", ".l-card>input");

        await page.locator("button>span ::-p-text(Create)").click();
        await page.waitForNetworkIdle();
    };

    const pkAndTitle = async () => {
        let rowPK = await page.evaluate(() => {
            return window.App.URLContext.value.pk;
        });
        await page.waitForSelector(".l-detail-header>span");
        let detailHeader = await page.$(".l-detail-header>span");
        let headerTitle = await (await detailHeader.getProperty("textContent")).jsonValue();
        await detailHeader.dispose();
        return {rowPK, headerTitle}
    }

    it("Enter/Return key on a ChoiceList inside insert window must not submit the dialog", async () => {
        await page.evaluate(() => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/contacts/Persons"
            })
        })
        await page.waitForNetworkIdle();

        await page.keyboard.press("Insert");
        await page.waitForNetworkIdle();

        await typeToElement("John", "label::-p-text(First name)", "input");
        await page.keyboard.press("Tab");
        await page.keyboard.type("Doe");
        await page.keyboard.press("Tab");
        await page.keyboard.press("ArrowDown");
        await page.keyboard.press("ArrowDown");
        await page.keyboard.press("Enter");

        const childCount = await page.evaluate(() => {
            return Object.values(window.App.URLContext.children).length;
        });

        expect(childCount).toBe(1);

        const actionFullName = await page.evaluate(() => {
            const insertCtx = Object.values(window.App.URLContext.children)[0];
            return (insertCtx as t.NavigationContext).value.action_full_name;
        });

        expect(actionFullName.endsWith(".insert")).toBe(true);

        await page.evaluate(() => {
            (Object.values(window.App.URLContext.children)[0] as t.NavigationContext).actionHandler.clearMod();
        });
    });


    it("Eject button on CommentsByRFC body", async () => {
        await page.evaluate(() => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/tickets/AllTickets/1"
            });
        });
        await page.waitForNetworkIdle();

        const getSlaveHtml = async () => {
            return await page.evaluate(() => {
                return window.App.URLContext.dataContext.refStore
                    .slaveLeaves["comments.CommentsByRFC"].state.value;
            });
        }

        let html = await getSlaveHtml();
        if (html === '<div class="htmlText"></div>') {
            await page.locator("button>span.pi-angle-double-left").click();
            await page.waitForNetworkIdle();

            html = await getSlaveHtml();
        }

        while (html === '<div class="htmlText"></div>') {
            await page.locator("button>span.pi-angle-right").click();
            await page.waitForNetworkIdle();

            html = await getSlaveHtml();
        }

        await page.waitForSelector("div.p-panel-header>span::-p-text(Comments)");
        const headerTitle = await page.$("div.p-panel-header>span::-p-text(Comments)");
        const header = await headerTitle.getProperty("parentElement");
        await headerTitle.dispose();
        const eject = await header.$("::-p-text(⏏)");
        await header.dispose();
        await eject.click();
        await eject.dispose();
        await page.waitForNetworkIdle();

        const url = await page.evaluate(() => window.location.href);
        expect(url).toContain("/api/comments/CommentsByRFC");
    });

    it("insert (twice), merge, and delete", async () => {
        await page.evaluate(() => {
            window.App.URLContext.history.pushPath({
                pathname: "/api/tickets/AllTickets"
            });
        });
        await page.waitForNetworkIdle();

        const initRowCount = await page.evaluate(() => {
            return window.App.URLContext.dataContext.mutableContext.count;
        });

        let t1 = "test ticket 1";

        await createTicket(t1);

        var {rowPK, headerTitle} = await pkAndTitle();
        expect(headerTitle).toEqual(`All tickets » #${rowPK} (test ticket 1)`);

        await createTicket("test ticket 2");

        var {rowPK, headerTitle} = await pkAndTitle();
        expect(headerTitle).toEqual(`All tickets » #${rowPK} (test ticket 2)`);

        await page.reload();
        await page.waitForNetworkIdle();

        await page.locator("button>span ::-p-text(⚭)").click();
        await page.waitForNetworkIdle();
        await typeToElement(t1, "label ::-p-text(into...)", ".l-card>span>input");
        await page.waitForNetworkIdle();
        await page.waitForSelector(".p-autocomplete-items");
        const items = await page.$(".p-autocomplete-items");
        const item = await items.$("div");
        await item.click();

        await items.dispose();
        await item.dispose();

        await page.locator("button>span ::-p-text(OK)").click();
        await page.locator("button>span ::-p-text(Yes)").click();
        await page.waitForNetworkIdle();

        var {rowPK, headerTitle} = await pkAndTitle();
        expect(headerTitle).toEqual(`All tickets » #${rowPK} (test ticket 1)`);

        await page.reload();
        await page.waitForNetworkIdle();

        await page.locator("button.l-button-delete_selected").click();
        await page.locator("button>span ::-p-text(Yes)").click();
        await page.waitForNetworkIdle();

        var {rowPK, headerTitle} = await pkAndTitle();
        expect(headerTitle).toEqual("All tickets");

        const endRowCount = await page.evaluate(() => {
            return window.App.URLContext.dataContext.mutableContext.count;
        });

        expect(initRowCount).toEqual(endRowCount);
    });
});
