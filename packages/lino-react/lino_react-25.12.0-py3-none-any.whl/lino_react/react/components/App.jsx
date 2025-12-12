import "./custom_hooks";
import React from "react";
import PropTypes from "prop-types";
import * as constants from './constants';
import { setRpRefFactory, getSiteDataKey,
    pushExternalModules } from "./LinoUtils";
import { RegisterImportPool, getExReady, Component } from "./Base";

import(/* webpackChunkName: "AppCSS" */"./AppCSS");

let ex; const exModulePromises = ex = {
    rdc: import(/* webpackChunkName: "reactDom_App" */"react-dom/client"),
    rrd: import(/* webpackChunkName: "reactRouterDom_App" */"react-router-dom"),
    queryString: import(/* webpackChunkName: "queryString_App" */"query-string"),
    weakKey: import(/* webpackChunkName: "weakKey_App" */"weak-key"),
    ReconnectingWebSocket: import(/* webpackChunkName: "ReconnectingWebSocket_App" */"reconnecting-websocket"),
    prAPI: import(/* webpackChunkName: "prAPI_App" */"primereact/api"),
    prButton: import(/* webpackChunkName: "prButton_App" */"primereact/button"),
    prLocale: import(/* webpackChunkName: "prLocale_App" */"primelocale"),
    prToast: import(/* webpackChunkName: "prToast_App" */"primereact/toast"),
    nc: import(/* webpackChunkName: "NavigationControl_App" */"./NavigationControl"),
    sc: import(/* webpackChunkName: "SiteContext_App" */"./SiteContext"),
    i18n: import(/* webpackChunkName: "i18n_App" */"./i18n"),
};RegisterImportPool(exModulePromises);

/**
 *
 * Renders a HashRouter and renders the :js:class:`App` inside
 * upon when the HashRouter is available to the DOM.
 */
function LinoRouter(props) {
    const navigate = props.RRD.useNavigate();
    const location = props.RRD.useLocation();
    return <App navigate={navigate} location={location}/>
}

LinoRouter.propTypes = {
    RRD: PropTypes.shape({
        useNavigate: PropTypes.func.isRequired,
        useLocation: PropTypes.func.isRequired,
    }).isRequired,
};

export {LinoRouter};


/**
 * @typedef {Object} ServerErrorProps
 */
const ServerErrorProps = {}

/**
 * Component to render error message on status_code >= 500
 *
 * @param {ServerErrorProps} props
 */
function InternalServerError(props) {
    const localEx = getExReady(ex, ["prButton", "i18n"], (mods) => {
        mods.i18n = mods.i18n.default;
        return mods;
    });
    return !localEx.ready ? null : <div style={{textAlign: 'center'}}>
        <p>There was a problem on the server. If the problem persists, contact your site maintainer.</p>
        <localEx.prButton.Button label={localEx.i18n.t('Reinitialize')}
            onClick={() => window.location.reload()}/>
    </div>
}
export { InternalServerError }

InternalServerError.propTypes = ServerErrorProps;


/**
 *
 * The app class.
 *
 * Subclasses :class:`Component`
 *
 */
class App extends Component {
    static requiredModules = ["nc", "sc", "prToast", "ReconnectingWebSocket",
        "queryString", "i18n", "prAPI", "prLocale"];
    static iPool = ex;

    /** Keeps a reference to the singleton :js:class:`DialogFactory` instance. */
    dialogFactory = null;
    /** Keeps a reference to a `Toast <https://www.primefaces.org/primereact-v6/#/toast>`__ object. */
    toast = null;
    /** Keeps a reference to a :js:class:`Context` object (and is the :js:class:`RootURLContext` 's controller.) */
    URLContext = null;
    /**
     *
     */
    static propTypes = {
        location: PropTypes.object.isRequired,
        navigate: PropTypes.func.isRequired,
    }

    async prepare() {
        this.ex.queryString = this.ex.queryString.default;
        const { TransInit } = this.ex.i18n;
        this.ex.i18n = this.ex.i18n.default;
        const params = this.ex.queryString.parse(this.location.search.slice(1));
        const onTransInit = async (ti) => {
            if (params[constants.URL_PARAM_USER_LANGUAGE])
                ti.changeLanguage(params[constants.URL_PARAM_USER_LANGUAGE]);
            if (params[constants.URL_PARAM_SUBST_USER])
                await this.URLContext.history.replaceByType(
                    {[constants.URL_PARAM_SUBST_USER]: params[constants.URL_PARAM_SUBST_USER]},
                    constants.PARAM_TYPE_WINDOW, false, true);

            this.storageName = `lino-${window.Lino.site_name}-json-cache`;
            const request = window.indexedDB.open(this.storageName, 1);
            request.onsuccess = (event) => {
                this.cacheDB = event.target.result;
                this.setReady();
            }
            request.onupgradeneeded = (event) => {
                event.target.result.createObjectStore(this.storageName);
            }

            /**
             * CAUTION: Do NOT remove the translations below
             * Not useful at runtime, but they are put to the
             * *translation.json files and are used in other
             * translations.
             */
            this.ex.i18n.t("whiteSpace", " ");
            this.ex.i18n.t("colonSpaced", ":$t(whiteSpace)");
        }
        this.URLContext = new this.ex.nc.Context({APP: this,
            rs: params.rs,
            next: (ucc) => TransInit(ucc, onTransInit)});

        /**
         * Intentionally raised to override calling setReady for we do it
         * locally here on indexedDB open success!
         */
        throw 'Overriding call to: "App.setReady" (Intentionally raised, please ignore this error!)';
    }

    /**
     * @param {Object} [props] see: :js:attr:`propTypes`.
     */
    constructor(props) {
        super(props);
        this.location = props.location;
        this.navigate = props.navigate;
        /**
         * Keeps references to :js:class:`ActionHandler` (s).
         * (internally known as requesting_panel as rp(s))
         */
        this.rps = {};
        /** Current state of the :js:class:`App`. */
        this.state = {
            ...this.state,
            site_loading: true,
            site_data: null,
            menu_data: null,
            user_settings: null,

            WS: false, // Websocket status
            children: null,
        };

        this.data = {
            miStore: [],
            themeName: 'default', // `whitewall`, `default`

            selectedLanguage: null,
            scroll: {},
            scrollIndex: [],
            zoomHandles: [],
        }
        this.setRpRef = setRpRefFactory(this.rps);

        this.createAccount = this.createAccount.bind(this);
        this.fetch_user_settings = this.fetch_user_settings.bind(this);
        this.fetch_site_data = this.fetch_site_data.bind(this);
        // this.handleVerification = this.handleVerification.bind(this);
        this.handleZoom = this.handleZoom.bind(this);
        this.interceptBrowserBF = this.interceptBrowserBF.bind(this);
        this.interceptBrowserReload = this.interceptBrowserReload.bind(this);
        this.messageInterceptor = this.messageInterceptor.bind(this);
        this.onHrefClick = this.onHrefClick.bind(this);
        this.onMysettings = this.onMysettings.bind(this);
        this.onReady = this.onReady.bind(this);
        this.registerHandle = this.registerHandle.bind(this);
        this.unsetLoadMask = this.unsetLoadMask.bind(this);
        this.reset = this.reset.bind(this);
        this.setLoadMask = this.setLoadMask.bind(this);
        this.setServerError = this.setServerError.bind(this);
        this.unregisterHandle = this.unregisterHandle.bind(this);
        this.getSettings = this.getSettings.bind(this);
        this.setSettings = this.setSettings.bind(this);

        this.onSignOutIn = this.onSignOutIn.bind(this);
        // this.onSignIn = this.onSignIn.bind(this);

        this.runAction = this.runAction.bind(this);

        this.notification_web_socket = this.notification_web_socket.bind(this);
        this.push = this.push.bind(this);

        window.App = this;
    }

    /**
     * Does what componentDidMount does.
     */
    onReady() {
        this.setState({children: <this.ex.sc.LinoProgressBar loading={true}/>});
        this.reset();
        this.setTheme(this);
        window.addEventListener('message', this.messageInterceptor);
        window.addEventListener('click', this.onHrefClick);
        window.onbeforeunload = this.interceptBrowserReload;
        window.onpopstate = this.interceptBrowserBF;
    }

    componentWillUnmount() {
        this.cacheDB.close();
        window.removeEventListener('message', this.messageInterceptor);
        window.removeEventListener('click', this.onHrefClick);
    }

    /**
     * Executes when the browser's reload button is clicked.
     *
     * Used to check and prevent modified data loss.
     *
     * @param [event] `BeforeUnloadEvent <https://developer.mozilla.org/en-US/docs/Web/API/BeforeUnloadEvent>`__
     */
    interceptBrowserReload(event) {
        if (this.URLContext.isModified()) {
            event.preventDefault();
            event.returnValue = true;
        }
    }

    /**
     * Executes when the browser detect a change in the History state.
     *
     * Used to check and prevent modified data loss.
     *
     * @param [event] `PopStateEvent <https://developer.mozilla.org/en-US/docs/Web/API/PopStateEvent>`__
     */
    interceptBrowserBF(event) {
        const [pathname, search] = document.URL.split('#')[1].split('?'),
            params = this.ex.queryString.parse(search),
            { URLContext } = this;
        if (pathname === URLContext.value.path) return;
        if (URLContext.filled(params.rs)) {
            if (URLContext.history.has(params.rs))
                URLContext.history.load({rs: params.rs, lazy: true})
            else URLContext.history.pushPath({
                pathname: pathname, params: params, lazy: true});
        } else {
            params.rs = URLContext.newSlug();
            this.navigate(
                URLContext.makePath({path: pathname, ...params}),
                {replace: true})
            URLContext.history.pushPath({
                pathname: pathname, params: params, lazy: true});
        }
    }

    registerHandle(handleType, handle) {
        this.data[`${handleType}Handles`].push(handle);
    }

    unregisterHandle(handleType, handle) {
        let i = this.data[`${handleType}Handles`].indexOf(handle);
        if (i > -1) {
            this.data[`${handleType}Handles`].splice(i, 1);
        }
    }

    handleZoom() {
        if (!this.tbContainer) return;
        let tbBottom = this.tbContainer.getBoundingClientRect().bottom;
        function zoomFire(App) {
            if (!App.tbContainer) {
                clearInterval(App.state.zoomHandlerID);
                return;
            }
            let tbBottomCur = App.tbContainer.getBoundingClientRect().bottom;
            if (tbBottomCur == tbBottom) return;
            tbBottom = tbBottomCur;
            Object.values(App.data.zoomHandles).forEach(handle => handle());
        }
        this.state.zoomHandlerID = setInterval(zoomFire, 300, this);
    }

    onHrefClick(event) {
        if (event.ctrlKey
            && event.target.href && event.target.href.startsWith('javascript')) {
            event.preventDefault();
            let action_param = JSON.parse(event.target.href.split('runAction(')[1].slice(0, -1));
            Object.assign(action_param, {clickCatch: true});
            this.runAction(action_param);
        }
    }

    /**
     * Sets a input blocking load mask to the Window.
     */
    setLoadMask() {
        this.setState({loadMask: true});
        // if (document.activeElement.tagName !== 'body')
        //     this.activeElement = document.activeElement;
        // if (this.activeElement) this.activeElement.blur();
    }
    /**
     * Removes the load mask created by :js:meth:`~App.setLoadMask`.
     */
    unsetLoadMask() {
        this.setState({loadMask: false});
        // if (this.activeElement) this.activeElement.focus();
    }

    setTheme(app) {
        if (app.data.themeName === 'whitewall') {
            document.querySelector('body').classList.add('l-whitewall-body-container');
            this.setState({staticMenuInactive: true});
        }
    }

    messageInterceptor(e) {
        if (e.data === "ArrowsTaken" && !this.data.arrowsTaken)
            this.data.arrowsTaken = true;
        else if (e.data === "ArrowsReleased" && this.data.arrowsTaken)
            this.data.arrowsTaken = false;
    }

    updatePushSubscription(subscription) {
        if (this.state.site_data
            && this.state.site_data.use_push_api) {
            if (!subscription) {
                if ('serviceWorker' in navigator) {
                    navigator.serviceWorker.ready.then((reg) => {
                        reg.pushManager.getSubscription().then(sub => {
                            if (sub !== null) {
                                this.updatePushSubscription(sub);
                            }
                        });
                    });
                }
            }
            else {
                // let lang = document.documentElement.lang || document.documentElement.getAttribute('language');
                let ajax_query = {
                    lang: navigator.userLanguage || navigator.language,
                    userAgent: navigator.userAgent,
                    sub: JSON.stringify(subscription),
                }
                this.URLContext.actionHandler.silentFetch({path:
                    `pushsubscription?${this.ex.queryString.stringify(ajax_query)}`});
            }
        }
    }

    onMysettings(event) {
        let runable = {actorId: "users.Me", action_full_name: "users.Me.detail",
            [constants.URL_PARAM_SELECTED]: [this.state.user_settings.user_id]}
        if (event.ctrlKey) {
            runable.clickCatch = true;
        }
        this.runAction(runable);
    }

    onSignOutIn(event) {
        if (!this.state.user_settings.logged_in)
            this.runAction({
                actorId: "about.About",
                action_full_name: this.URLContext.actionHandler.findUniqueAction("sign_in").full_name})
        else {
            this.setLoadMask();
            this.URLContext.actionHandler.silentFetch({path:"auth"}).then(
                (resp) => {
                    this.webSocketBridge && this.webSocketBridge.close();
                    this.navigate('/');
                    this.reset()});
            this.unsetLoadMask();
        }
    }

    createAccount() {
        if (this.state.user_settings.logged_in) return
        this.runAction({actorId: "about.About", action_full_name: this.URLContext
            .actionHandler.findUniqueAction("create_account").full_name});
    }

    // handleVerification(action_name) {
    //     let pk = this.state.user_settings.user_id;
    //     this.data.user_state_change = true;
    //     this.runAction({actorId: "users.Me", action_full_name: action_name, [constants.URL_PARAM_SELECTED]: [pk]});
    // }

    addClass(element, className) {
        if (element.classList)
            element.classList.add(className);
        else
            element.className += ' ' + className;
    }

    removeClass(element, className) {
        if (element.classList)
            element.classList.remove(className);
        else
            element.className = element.className.replace(new RegExp('(^|\\b)' + className.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
    }

    isDesktop() {
        return window.innerWidth > 1024;
    }

    componentDidUpdate() {
        if (this.state.mobileMenuActive)
            this.addClass(document.body, 'body-overflow-hidden')
        else
            this.removeClass(document.body, 'body-overflow-hidden');
    }

    notification_web_socket(user_settings) {

        console.warn("NWS");
        if (!window.Lino || !window.Lino.useWebSockets) return;

        let {user_id} = user_settings || this.state.user_settings;

        if (this.webSocketBridge) {
            this.webSocketBridge.close();
            this.setState({WS: false});
        }

        this.webSocketBridge = new this.ex.ReconnectingWebSocket.default(
            (window.location.protocol === "https:" ? "wss" : "ws") + "://" + window.location.host + "/WS/",
            [], // protocalls, not needed
            {} //options, see https://www.npmjs.com/package/reconnecting-websocket
        );

        // Helpful debugging
        this.webSocketBridge.addEventListener(
            'close', (e) => this.setState({WS: false}));

        // this.webSocketBridge.connect();
        this.webSocketBridge.addEventListener(
            'open', () => this.setState({WS: true}));


        this.webSocketBridge.addEventListener('message', (e) => {

            let data = JSON.parse(e.data);
            console.log("Received message ", data);
            if (data.type === constants.WSM_TYPE.NOTIFICATION) {
                this.push(data)
            } else if (data.type === constants.WSM_TYPE.CHAT) {
                console.warn("CHAT features has been disabled!");
            } else if (data.type === constants.WSM_TYPE.LIVE_PANEL_UPDATE) {
                const { panels } = this.URLContext.globals;
                Object.keys(data.data).filter(ID => ID in panels)
                    .forEach(ID => panels[ID].liveUpdate(data.data[ID]));
            }
        });
    }

    pushPermission() {
        let onGranted = () => console.log("onGranted");
        let onDenied = () => console.log("onDenied");
        // Ask for permission if it's not already granted
        Push.Permission.request(onGranted, onDenied);
    }

    push(data) {
        let {body, subject, action_url} = data;
        this.pushPermission();
        try {
            Push.create(subject, {
                body: body,
                icon: '/static/img/lino-logo.png',
                onClick: function () {
                    window.open(action_url);
                }
            });
        }
        catch (err) {
            console.log(err.message);
        }

    }

    /**
     * Reset (as in reload) all content (children) of :js:class:`App`.
     *
     * When the :js:func:`~App.reset` is caused by a version mismatch
     * indexedDB and URI caches gets cleared.
     */
    reset(signIn=false) {
        let LinoProgressBar = this.ex.sc.LinoProgressBar;
        this.setState({
            site_loading: true,
            site_data: null,
            menu_data: null,
            user_settings: null,
            children: <LinoProgressBar loading={true}/>
        })
        this.fetch_user_settings(signIn);
    }

    /**
     * Fetches settings for the logged in user or substitue user or anonymous
     */
    fetch_user_settings(signIn=false) {
        let url = "user/settings/", qs = {};
        this.URLContext.actionHandler.commonParams(qs);
        this.URLContext.actionHandler.silentFetch({
            path: `${url}?${this.ex.queryString.stringify(qs)}`}
        ).then((data) => {
            if (signIn) {
                this.ex.i18n.changeLanguage(data.user_lang);
                /**
                * Call fetch_user_settings again with the new language preference
                */
                this.fetch_user_settings();
                return;
            }
            const { all } = this.ex.prLocale;
            if (Object.keys(all).includes(data.locale)) {
                this.ex.prAPI.addLocale(data.locale, all[data.locale]);
                this.ex.prAPI.locale(data.locale);
            }
            this.setState({
                user_settings: data,
                menu_data: this.createMenu(data.user_menu),
                settings_key: `settings_${data.site_name}`
            });

            this.notification_web_socket(data);
            this.fetch_site_data(data);
        });
    };

    /**
     * Fetches siteData for the given URI.
     *
     * @param {Object} [data] user_settings.
     */
    async fetch_site_data(data) {
        const key = getSiteDataKey(this.URLContext, data);
        const uri = data.site_data;
        const siteData = await this.URLContext.getSiteData(key, uri);
        this.setState({
            site_data: siteData,
            site_loading: false,
        });
        if (siteData.theme_name && siteData.theme_name !== this.data.themeName) {
            this.data.themeName = siteData.theme_name;
            this.setTheme(this);
        }
        this.updatePushSubscription();
        const RootURLContext = this.ex.sc.RootURLContext;
        this.setState({children: <RootURLContext APP={this}/>});
        if (this.state.zoomHandlerID) {
            clearInterval(this.state.zoomHandlerID);
            setTimeout(this.handleZoom, 1000);
        }
    };

    /**
     * When called, sets the :js:class:`App` children to :js:func:`InternalServerError`.
     */
    setServerError() {
        this.setState({children: <InternalServerError reset={this.reset}/>});
    }

    /**
     * Hook for handling hard-coded (in HTML) action.
     *
     * @param {Object} [kwargs] see type ArgsRunAction
     */
    runAction(kwargs) {
        let aH, rp = kwargs[constants.URL_PARAM_REQUESTING_PANEL];
        if (rp && !rp.includes('dashboard') && !rp.includes('dItems'))
            aH = this.rps[kwargs[constants.URL_PARAM_REQUESTING_PANEL]];
        if (!aH) aH = this.URLContext.actionHandler;
        aH.checkAndRunAction(kwargs);
    };

    /**
     * Converts and returns sitedata menu data as Primereact menu data
     * with command functions
     *
     * @param {Object} [layout] siteData.menu
     * @returns {Object} menuData
     **/
    createMenu(layout) {
        // let counter = 0;
        //
        // const convert = (mi) => {
        //     let menu;
        //     if (!mi.text) {
        //         menu = "is_a_seperator";
        //     } else {
        //         let id = counter.toString();
        //         id += "_" + mi.text.replace(' ', '_');
        //         counter += 1;
        //         menu = {id: id, label: mi.text, command: (event) => {
        //             eval(mi.handler)}}
        //     }
        //     if (mi.menu && mi.menu.items) {
        //         menu.items = mi.menu.items.map(convert);
        //         delete menu.command; // Only have command on submenu items,
        //     }
        //     return menu;
        // };
        // let result = layout.map(convert);
        // this.data.miStore = result;
        // return result
        let miStore = [];
        this.data.counter = [0];

        const convert = (mi, store) => {
            let menu, storeMenu = {};
            if (!mi.text) {
                menu = "is_a_seperator";
            } else {
                let id = this.data.counter[0].toString();
                id += "_" + mi.text;
                id = id.replaceAll(' ', '_');
                id = id.replaceAll("(", "_");
                id = id.replaceAll(")", "_");
                id = id.replaceAll(".", "_");
                this.data.counter[0] += 1;
                menu = {
                    id: "m" + id,
                    label: mi.text,
                    command: (event) => {
                        eval(mi.handler);
                    }
                }
            };
            if (typeof menu !== 'string') storeMenu.id = menu.id;
            if (mi.menu && mi.menu.items) {
                storeMenu.items= [];
                menu.items = mi.menu.items.map(mi => convert(mi, storeMenu.items));
                delete menu.command; // Only have command on submenu items,
            }
            if (Object.keys(storeMenu).length) store.push(storeMenu);
            return menu;
        };
        let result = layout.map(mi => convert(mi, miStore));
        if (this.data.counter) delete this.data.counter;
        this.data.miStore = miStore;
        return result
    }

    getSettings() {
        return window.localStorage.getObject(this.state.settings_key) || {};
    }

    setSettings(settings) {
        window.localStorage.setObject(this.state.settings_key,
            Object.assign(this.getSettings(), settings));
    }

    async reload() {
        await this.URLContext.iDBclear();
        window.localStorage.clear();
        window.location.reload();
    }

    render() {
        if (!this.state.ready) return null;
        return <React.Fragment>
            {this.state.loadMask && <this.ex.sc.LinoLoadMask/>}
            <this.ex.prToast.Toast ref={(el) => this.toast = el}/>

            {this.state.children}

            <div className="layout-mask"/>
            <iframe id="temp" name="temp" style={{display: "none"}}/>
            <this.ex.sc.DialogFactory ref={ref => this.dialogFactory = ref} APP={this}/>
        </React.Fragment>
    }
}
export {App};


export function Main(props) {
    const localEx = getExReady(ex, ["rrd"]);
    return !localEx.ready ? null : <localEx.rrd.HashRouter>
        <LinoRouter RRD={localEx.rrd}/>
    </localEx.rrd.HashRouter>
}


export async function render() {
    const rootElement = document.getElementById("root");
    if (rootElement) {
        // Populate LinoUtils with the modules it require.
        pushExternalModules(await ex.resolve(["queryString", "weakKey"]));

        // render app.
        const rdc = (await ex.resolve(["rdc"])).rdc;
        rdc.createRoot(rootElement).render(<Main/>);
    }
}
