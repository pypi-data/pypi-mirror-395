/**
 * @module NavigationControl
 * Copyright 2023-2024 Rumma & Ko Ltd
 * License: GNU Affero General Public License v3 (see file COPYING for details)
 */

export const name = "NavigationControl";

import * as constants from './constants';
import { RegisterImportPool, DynDep } from './Base';

import { ActionHandler } from './ActionHandler';

export const ROUTES = {
    home: "/",
    actor: "/api/:packId/:actorId/:pk?/:fieldName?",
}

const ContextGlobals = {};
const Lino = window.Lino;
const exModulePromises = RegisterImportPool({
    u: import(
        /* webpackChunkName: "LinoUtils_NavigationControl" */"./LinoUtils"),
    queryString: import(
        /* webpackChunkName: "queryString_NavigationControl" */"query-string"),
    rrd: import(
        /* webpackChunkName: "reactRouterDom_NavigationControl" */"react-router-dom"),
    _: import(
        /* webpackChunkName: "lodash_NavigationControl" */"lodash"),
    i18n: import(/* webpackChunkName: "i18n_NavigationControl" */"./i18n"),
});

/**
 * @typedef {Object} ContextParams
 * @property APP the singleton instance of :js:class:`App`.
 * @property {Object} value the default value of the :js:attr:`URLContextBase.Context`.
 * @property root the :term:`react component` whose children are subject to this :js:class:`Context`.
 * @property {Function} callback to run after :js:meth:`Context.onReady`.
 */
/**
 * Controller for all navigation features.
 */
export class Context extends DynDep {
    static requiredModules = ["u", "queryString", "rrd", "_", "i18n"];
    static iPool = exModulePromises;

    async prepare() {
        await super.prepare();
        this.ex._ = this.ex._.default;
        const i18n = this.ex.i18n.default;
        this.mentionValues = {
            "@": [{ value: i18n.t("Mention @People") }],
            "#": [{ value: i18n.t("Tag #content") }]
        }
    }

    /** Computes the site wide static parameters. */
    computeGlobals() {
        this.globals = ContextGlobals;
        if (ContextGlobals.hasOwnProperty('isMobile')) return;
        ContextGlobals.isMobile = this.ex.u.isMobile();
        ContextGlobals.currentInputWindowType = constants.WINDOW_TYPE_UNKNOWN;
        ContextGlobals.currentInputRowIndex = 0;
        ContextGlobals.currentInputIndex = 0;
        ContextGlobals.panels = {};
        this.localStorageSize();
    }
    // constructor(APP, value, root) {
    /**
     * @param {ContextParams}
     */
    onReady({APP, rs, slave = false, root, next}) {
        this.computeGlobals = this.computeGlobals.bind(this);
        /** The singleton instance of :js:class:`App`. */
        this.APP = APP;
        /** Current value / state. */
        this.value = {};
        this.paramNames = [];
        /** The :term:`react component` whose children are subject to :js:attr:`Context.value`. */
        this.root = root;
        /** [boolean = true] specifies whether this is a controller for a NON-:js:class:`RootURLContext` :term:`react component` */
        this.isSlave = slave;
        /** Pointer to parent :js:class:`Context` for a NON-:js:class:`RootURLContext` :term:`react component` */
        this.parent = null;
        /** Keeps references to the children :js:class:`Context` (s) */
        this.children = {};
        this.delegate = {};

        this.static = {actorData: null};

        this.addDelegate = this.addDelegate.bind(this);
        this.actorDependentParams = this.actorDependentParams.bind(this);
        this.assertAndReflect = this.assertAndReflect.bind(this);
        this.attachDataContext = this.attachDataContext.bind(this);
        this.basicContext = basicContext.bind(this);
        this.build = this.build.bind(this);
        this.buildURLContext = buildURLContext.bind(this);
        this.computeDefaults = this.computeDefaults.bind(this);
        this.copy = this.copy.bind(this);
        this.getActorData = this.getActorData.bind(this);
        this.isModified = this.isModified.bind(this);
        this.newSlug = this.newSlug.bind(this);
        this.onLeafMount = this.ex.u.debounce(this.onLeafMount.bind(this), 300);
        this.paramChange_Action = this.paramChange_Action.bind(this);
        this.pushStatus = this.pushStatus.bind(this);
        this.reflect = this.reflect.bind(this);
        this.removeDelegate = this.removeDelegate.bind(this);
        this.setActionHandler = this.setActionHandler.bind(this);
        this.setContextType = this.setContextType.bind(this);
        this.setParent = this.setParent.bind(this);
        this.setRoot = this.setRoot.bind(this);
        this.storeDetaultInitialize = this.storeDetaultInitialize.bind(this);

        /** An instance of :js:class:`ActionHandler` */
        this.actionHandler = new ActionHandler({context: this, next: (aH) => {
            /** An instance of :js:class:`History`. */
            this.history = new History(this, rs);
            this.computeGlobals();
            this.createGettersSG();
            if (!ContextGlobals.hasOwnProperty('currentInputAHRefName'))
                ContextGlobals.currentInputAHRefName = aH.refName;
            next(this);
        }});
    }

    onLeafMount = () => {
        if (this.contextType === constants.CONTEXT_TYPE_ACTION) {
            Object.values(this.dataContext.refStore.Leaves).sort((a, b) => {
                if (a.props.leafIndex < b.props.leafIndex &&
                    a.hasOwnProperty('focus') && !a.disabled())
                    return -1
                else if (a.props.leafIndex > b.props.leafIndex &&
                    b.hasOwnProperty('focus') && !b.disabled()
                ) return 1
                else return 0;
            })[0].focus();
        }
    }

    matchActorPath(path) {
        return this.ex.rrd.matchPath(ROUTES.actor, path);
    }

    setActorData = (actorData) => {
        if (!actorData) return;
        if (this.static.actorData)
            delete ContextGlobals.panels[this.static.actorData.id];
        this.static.actorData = actorData;
        ContextGlobals.panels[this.static.actorData.id] = this.root;
    }

    localStorageSize() {
        if (!ContextGlobals.localStorageTotal) {
            for (var i = 0, data = "1".repeat(10000); ; i++) {
                try {
                    window.localStorage.setItem("ONES", data);
                    data = data + "1".repeat(100000);
                } catch(e) {
                    ContextGlobals.localStorageTotal = Math.round((JSON.stringify(window.localStorage).length/1024)*2);
                    window.localStorage.removeItem("ONES");
                    break;
                }
            }
            ContextGlobals.localStorageFreeThreshold = Math.round(ContextGlobals.localStorageTotal * 0.2);
        }
        ContextGlobals.localStorageUsed = Math.round((JSON.stringify(window.localStorage).length/1024)*2);
        ContextGlobals.localStorageAvailable = ContextGlobals.localStorageTotal - ContextGlobals.localStorageUsed;
        return {total: ContextGlobals.localStorageTotal, used: ContextGlobals.localStorageUsed,
            free: ContextGlobals.localStorageAvailable, threshold: ContextGlobals.localStorageFreeThreshold};
    }

    addDelegate(id, delegate) {
        this.delegate[id] = delegate;
    }

    attachDataContext = (dataContext) => this.dataContext = dataContext;

    /**
    * WARNING: Never call this from child URLContext component.
     * Should only be called from RootURLContext.
     */
    async build(callback) {
        let up = await this.buildURLContext(this.APP.location.pathname);
        let searchParams = this.actionHandler.parser.parse(this.APP.location.search);

        if (searchParams.clone) {
            const clone = searchParams.clone;
            this.clone = clone;
            if (clone.windowGlobals)
                await this.history.replaceByType(clone.windowGlobals,
                    constants.PARAM_TYPE_WINDOW, false, true);
            if (clone.children) this.copyChildClones(clone.children);
            searchParams = clone.params;
        }

        const rs = (searchParams && searchParams.rs) || up.params.rs;
        if (rs && this.history.has(rs))
            Object.assign(up.params, this.history.getState(rs));
        Object.assign(up.params, searchParams);

        if (callback) callback(up)
        else return up;
    }

    copyChildClones(children) {
        children.forEach(obj => Object.keys(obj).forEach(
            actorID => this.static[actorID] = obj[actorID]));
    }

    disabled(name) {
        return this.contextType === constants.CONTEXT_TYPE_SINGLE_ROW && (
            this.dataContext.mutableContext.data && (
                this.dataContext.mutableContext.data.disabled_fields[name] || false
            )
        );
    }

    getSiteData = async (key, url) => {
        return await this.getIDBData(key, url);
    }

    getActorData = async (actorID) => {
        return await this.getIDBData(
            this.getActorKey(actorID), this.getActorURL(actorID));
    }

    getActorKey = (actorID) => {
        let userSettings = this.APP.state.user_settings;
        return `ActorData_${userSettings.su_user_type || userSettings.user_type
            }_${this.APP.data.selectedLanguage || userSettings.site_lang}_${
            userSettings.site_name}_${actorID}`
    }

    getActorURL = (actorID) => {
        let userSettings = this.APP.state.user_settings,
            url = "/media/cache/json/",
            no_user = this.APP.state.site_data.no_user_model;
        if (no_user) {
            url += `Lino_${actorID}_${
                this.APP.data.selectedLanguage || userSettings.site_lang}.json`;
        } else {
            url += `Lino_${actorID}_${
                userSettings.su_user_type || userSettings.user_type}_${
                    this.APP.data.selectedLanguage || userSettings.site_lang}.json`;
        }
        return url;
    }

    iDBOStore = () => {
        return this.APP.cacheDB.transaction(this.APP.storageName, 'readwrite')
            .objectStore(this.APP.storageName);
    }

    iDBTransactionRequest = (type, ...args) => this.iDBOStore()[type](...args);

    iDBTransactionResult = async (type, ...args) => {
        let tr = this.iDBTransactionRequest(type, ...args);
        return await new Promise((resolve) => {
            tr.onsuccess = (e) => resolve(tr.result);
        }).then(r => r);
    }

    iDBclear = async () => await this.iDBTransactionResult('clear');
    iDBdelete = async (key) => await this.iDBTransactionResult('delete', key);
    iDBget = async (key) => await this.iDBTransactionResult('get', key);
    iDBput = async (item, key) => await this.iDBTransactionResult('put', item, key);

    getIDBData = async (key, url) => {
        let data = await this.iDBget(key);

        const fetchActorData = async () => {
            data = await this.actionHandler.silentFetch({
                path: url + `?v=${Math.round(Math.random() * 1000000).toString()}`
            });
            if (Lino[constants.URL_PARAM_LINO_VERSION] < data[constants.URL_PARAM_LINO_VERSION]) {
                this.APP.reload();
                return data;
            }
            if (Lino[constants.URL_PARAM_LINO_VERSION] !== data[constants.URL_PARAM_LINO_VERSION])
                throw new Error(`Invalid lv marks. RUN "pm buildcache" and restart the server.`);
            await this.iDBput(data, key);
            return data;
        }

        if (data) {
            if (Lino[constants.URL_PARAM_LINO_VERSION] === data[constants.URL_PARAM_LINO_VERSION])
                return data
            else if (Lino[constants.URL_PARAM_LINO_VERSION] < data[constants.URL_PARAM_LINO_VERSION]){
                this.APP.reload();
                return data;
            } else return await fetchActorData();
        } else {
            return await fetchActorData();
        }
    }

    computeDefaults(bodyWidthInCh, actorData, paramStore, actorMain) {
        let display_mode = this.ex.u.getDisplayMode(actorData, bodyWidthInCh);
        if (actorMain) {
            paramStore.toolbarState = actorData.hide_top_toolbar
                ? constants.TOOLBAR_STATE_HIDDEN
                : this.globals.isMobile
                    ? constants.TOOLBAR_STATE_PARTIALLY_VISIBLE
                    : constants.TOOLBAR_STATE_VISIBLE;
        }
        paramStore.pvPVisible = !actorData.params_panel_hidden;
        let allowedDataDM = actorData.available_display_modes;
        // console.warn("20241018 computeDefaults", actorData.id, display_mode, bodyWidthInCh, allowedDataDM);
        // console.warn("20241018 is this true?", allowedDataDM.includes(display_mode));
        paramStore[constants.URL_PARAM_DISPLAY_MODE] = (
            actorData.default_action.endsWith(".show")
            || (paramStore.pk !== undefined && actorData.col !== undefined)
                ? constants.DISPLAY_MODE_DETAIL
                : allowedDataDM.includes(display_mode)
                      ? display_mode
                      : constants.DISPLAY_MODE_TABLE);

        // let allowedDataDM = [
        //     constants.DISPLAY_MODE_LIST,
        //     constants.DISPLAY_MODE_CARDS,
        //     constants.DISPLAY_MODE_STORY,
        // ]
        // if (this.isSlave) allowedDataDM = allowedDataDM.concat([
        //     constants.DISPLAY_MODE_HTML,
        //     constants.DISPLAY_MODE_SUMMARY,
        // ]);

        // paramStore[constants.URL_PARAM_DISPLAY_MODE] = (
        //     actorData.default_action === "show"
        //     || (paramStore.pk !== undefined && actorData.col !== undefined)
        //         ? constants.DISPLAY_MODE_DETAIL
        //         : actorData.contain_media
        //             ? constants.DISPLAY_MODE_GALLERY
        //             : allowedDataDM.includes(display_mode)
        //                 ? display_mode
        //                 : constants.DISPLAY_MODE_TABLE
        // );
        paramStore[constants.URL_PARAM_WINDOW_TYPE] = constants.DM_WT_MAP[
            paramStore[constants.URL_PARAM_DISPLAY_MODE]];
        if (actorData.default_action === "show") paramStore.pk = -99998;

        /**
        * context.showableColumns
        * ***********************
        *
        * struct: Map
        *     - key: col.fields_index
        *       value: col.name
        *
        **/
        paramStore.showableColumns = new Map();
        paramStore.rowReorder = false;
        actorData.col && actorData.col.filter(col => !col.hidden)
        .forEach((col, i) => {
            paramStore.showableColumns.set(col.fields_index, col.name);
        });

        if (actorData.col) {
            const dndreorder = actorData.col.filter(col => col.name === 'dndreorder');
            if (dndreorder.length) paramStore.rowReorder = true;
        }

        if (
            this.filled(paramStore.pk)
            && (this.value.actorId !== paramStore.actorId ||
                this.value.packId !== paramStore.packId ||
                !this.filled(this.value.pk))
        ) {
            paramStore.detailNav = new Map();
            if (!paramStore.rs) paramStore.rs = this.newSlug();
            paramStore.detailNav.set(paramStore.pk, paramStore.rs);
        } else if (this.filled(paramStore.pk))
            paramStore.detailNav = this.value.detailNav;
    }

    copy() {
        const _copy = (o) => {
            let val = o;
            if (o instanceof Map) {
                val = new Map();
                for (const [key, value] of o) val.set(key, _copy(value));
            }
            else if (Array.isArray(o)) {
                val = [];
                o.forEach(item => val.push(_copy(item)));
            } else if (o instanceof Object) {
                val = {}
                Object.keys(o).forEach(key => val[key] = _copy(o[key]));
            }
            return val;
        }
        const clone = {};
        this.paramNames.forEach(name => clone[name] = _copy(this.value[name]));
        return clone;
    }

    isModified() {
        if (this.void) return false;
        if (!this.dataContext) return false;
        if (this.dataContext.isModified()) return true;
        for (const variable of Object.values(this.children))
            if (variable.isModified()) return true;
        return false;
    }

    makePath(ctx) {
        return `${ctx.path}?${this.ex.queryString.default.stringify({
            rs: ctx.rs, mk: ctx.mk, mt: ctx.mt
        })}`;
    }

    newSlug = () => {
        let s = Math.round(Math.random() * 1000000000);
        if (s in localStorage) return this.newSlug();
        return s;
    }

    /**
     * Used in LinoBody.getSnapshotBeforeUpdate
     * @returns oneOf([render, reload, refresh]) as action to execute
     */
    paramChange_Action(newContext, oldContext) {
        let snapshot = {};
        if (
            newContext.noreload && !oldContext.noreload
        ) snapshot.render = true
        else if (
            oldContext[constants.URL_PARAM_DISPLAY_MODE] !== newContext[constants.URL_PARAM_DISPLAY_MODE] ||
            oldContext.path !== newContext.path
        ) snapshot.reload = true
        else if (
            oldContext[constants.URL_PARAM_START] !== newContext[constants.URL_PARAM_START] ||
            oldContext[constants.URL_PARAM_LIMIT] !== newContext[constants.URL_PARAM_LIMIT] ||
            oldContext[constants.URL_PARAM_MASTER_PK] !== newContext[constants.URL_PARAM_MASTER_PK] ||
            oldContext[constants.URL_PARAM_MASTER_TYPE] !== newContext[constants.URL_PARAM_MASTER_TYPE] ||
            oldContext[constants.URL_PARAM_SORT] !== newContext[constants.URL_PARAM_SORT] ||
            oldContext[constants.URL_PARAM_SORTDIR] !== newContext[constants.URL_PARAM_SORTDIR] ||
            oldContext[constants.URL_PARAM_FILTER] !== newContext[constants.URL_PARAM_FILTER] ||
            !this.ex._.isEqual(oldContext[constants.URL_PARAM_PARAM_VALUES], newContext[constants.URL_PARAM_PARAM_VALUES]) ||
            !this.ex._.isEqual(oldContext[constants.URL_PARAM_GRIDFILTER], newContext[constants.URL_PARAM_GRIDFILTER])
        ) snapshot.refresh = true;
        return snapshot;
    }

    pushStatus(status, ctx, actorData) {
        actorData = actorData || this.static.actorData;
        if (this.filled(status.base_params)) {
            if (this.filled(status.base_params.mk)) ctx.mk = status.base_params.mk;
            if (this.filled(status.base_params.mt)) ctx.mt = status.base_params.mt;
        }
        if (actorData && this.filled(status.param_values)) {
            ctx[constants.URL_PARAM_PARAM_VALUES] = this.ex.u.pvObj2array(
                status.param_values, actorData.params_fields)
        }
        if (this.filled(status.record_id)) ctx[constants.URL_PARAM_SELECTED] = [parseInt(status.record_id)];
        if (this.filled(status.data)) Object.assign(ctx, status.data);
        if (this.filled(status.clickCatch)) ctx.clickCatch = status.clickCatch;
        return ctx;
    }

    filled(pointer) {
        return ![null, undefined, ""].includes(pointer);
    }

    actorDependentParams(params, actorData) {
        params.hasDetail = !!actorData.detail_action;
    }

    /**
    * @param {boolean} [lazy] `true` means the path is already in the router path!
    **/
    assertAndReflect({lazy, actorData, params}) {
        // console.warn("20241010 assertAndReflect", params, actorData);
        const reflect = async () => {
            await this.root.iSetState({initialized: false});
            this.setActorData(actorData);
            await this.reflect({params, param_type: constants.PARAM_TYPE_VIEW,
                clean: true, browserPush: !lazy});
        }
        if (!this.isModified()) {reflect()} else {
            if (lazy) window.history.pushState(null, null,
                `/#${this.value.path}?rs=${this.value.rs}`);
            this.actionHandler.discardModDConfirm({agree: e => {
                    if (lazy) window.history.go(-1)
                    else reflect();
                }, disagree: e => {
                    // this.history.state = this.value;
                },
            });
        }
    }

    createGettersSG() {
        this.paramNames.push(...constants.SITE_GLOBALS_KEYS);
        constants.SITE_GLOBALS_KEYS.forEach((name, i) => Object.defineProperty(
            this.value, name, {get: () => (
                this.history.getState(constants.PARAM_TYPE_GLOBAL)[name])}));

    }

    defined = (key) => this.paramNames.includes(key);
    fillPlaceHolder = (param_type, key, value) => {
        if (this.defined(key))
            this.history.state.value[param_type][key] = value
        else this.value[key] = value;
    }
    createGetters({params, param_type=constants.PARAM_TYPE_VIEW}) {
        const define = (name, pt) => {
            this.paramNames.push(name);
            Object.defineProperty(this.value, name, {
                get: () => this.history.state.value[pt][name]
            });
        };
        if (param_type === constants.PARAM_TYPE_IMPLICIT) {
            Object.keys(params).forEach((pt, i) => {
                if (pt === constants.PARAM_TYPE_GLOBAL) return;
                Object.keys(params[pt]).forEach((key, i) => {
                    if (!this.defined(key)) define(key, pt);
                });
            });
        } else {
            Object.keys(params).forEach((key, i) => {
                if (!this.defined(key)) define(key, param_type);
            });
        }
    }

    shallowCopy(obj) {
        const clone = Object.create(Object.getPrototypeOf(obj));
        const descriptors = Object.getOwnPropertyDescriptors(obj);
        Object.defineProperties(clone, descriptors);
        return clone;
    }

    async reflect({params, browserPush = false, rebuild = false, silent = false,
        param_type = constants.PARAM_TYPE_VIEW, clean = false
    }) {
        // console.warn("20241010 reflect", params, param_type, clean);
        if (clean) {
            this.history.state.value[constants.PARAM_TYPE_VIEW] = {};
            this.paramNames = [];
            this.value = {};
            this.createGettersSG();
            this.createGetters({params: this.history.state.value,
                param_type: constants.PARAM_TYPE_IMPLICIT});
        }
        if (rebuild) this.value = this.shallowCopy(this.value);
        this.value.controller = this;
        if (param_type === constants.PARAM_TYPE_IMPLICIT)
            for (var pt in Object.keys(params))
                await this.history.state.update(params[pt], pt);
        else await this.history.state.update(params, param_type);
        this.createGetters({params, param_type});
        if (!this.isSlave && browserPush)
            this.APP.navigate(this.makePath(this.value));
        if (!silent) await this.root.iSetState(
            {context: this.value, hasActor: this.value.hasActor,
                initialized: true});
    }

    removeDelegate(id) {
        delete this.delegate[id];
    }

    setActionHandler = (actionHandler) => this.actionHandler = actionHandler;

    setContextType = (contextType) => this.contextType = contextType;

    setParent(controller) {
        if (this.parent) delete this.parent.children[this.actionHandler.refName];
        this.parent = controller;
        controller.children[this.actionHandler.refName] = this;
    }

    setRoot = (ref) => {this.root = ref};

    storeDetaultInitialize(paramStore) {
        if (this.isSlave) paramStore.wid = this.parent.value.wid;
        paramStore.sortField = null;
        paramStore.sortOrder = 0;
        paramStore.pvPVisible = false;
        paramStore[constants.URL_PARAM_SELECTED] = [];
        paramStore.gridFilters = new Map();
        paramStore.filter = [];
    }
}

async function basicContext(path, callback) {
    const { sanitize } = this.actionHandler.parser;
    let params = {path: path}, actorData;
    this.storeDetaultInitialize(params);
    let match = this.ex.rrd.matchPath(ROUTES.actor, path);
    Object.assign(params, match.params);
    params.pk = this.filled(params.pk) ? sanitize(params.pk) : undefined;
    actorData = await this.getActorData(`${params.packId}.${params.actorId}`);
    this.actorDependentParams(params, actorData);
    if (callback) callback({params, actorData})
    else return {params, actorData};
}

async function buildURLContext(path, callback) {
    const { sanitize } = this.actionHandler.parser;
    let siteData = this.APP.state.site_data, params = {
        editing_mode: false,
        hasActor: path !== "/",
        path: path
    }, actorData = null;
    this.storeDetaultInitialize(params);
    if (params.hasActor) {
        let match = this.ex.rrd.matchPath(ROUTES.actor, path);
        if (!match) {
            if (path !== "/") throw new Error(`InvalidRouterPath: ${path}`);
            params.packId = "system"
            params.actorId = "Dashboard"
        } else {
            Object.assign(params, match.params);
        }
        params.pk = this.filled(params.pk) ? sanitize(params.pk) : undefined;
        actorData = await this.getActorData(`${params.packId}.${params.actorId}`);
        if (!match) {
            params.window_layout = siteData.choicelists['system.DashboardLayouts'].find(
                dl => dl.value === (this.APP.state.user_settings.dashboard_layout || "default")
            ).window_layout;
        } else {
            params.window_layout = actorData.window_layout;
        }
        this.actorDependentParams(params, actorData);
        this.computeDefaults(
            this.root.contextEntry.offsetWidth / this.root.chInPx.offsetWidth,
            actorData, params, true);
        this.ex.u.fillParamDefaults(params, actorData);
    }
    if (callback) {
        callback({params, actorData});
    } else return {params, actorData};
}


class State {
    /**
     * @typedef {Object} state
     * @property {Object} [PARAM_TYPE_VIEW]
     * @property {Object} [PARAM_TYPE_WINDOW]
     *
     * @param {state} state
     */
    constructor({history, rs}) {
        const { context, getState } = history, state = {};
        this.history = history;
        this.context = context;

        const globals_latest = getState(constants.PARAM_TYPE_GLOBAL);

        if (!context.isSlave && !context.filled(rs)) rs = context.newSlug();

        state[constants.PARAM_TYPE_VIEW] = {rs: rs};
        if (context.filled(rs) && history.has(rs))
            state[constants.PARAM_TYPE_VIEW] = getState(rs);

        state[constants.PARAM_TYPE_WINDOW] = {};
        if (context.isSlave)
            state[constants.PARAM_TYPE_WINDOW] = context.APP.URLContext
                .history.state.value[constants.PARAM_TYPE_WINDOW]
        else if (context.filled(state[constants.PARAM_TYPE_VIEW].wid)
            && history.has(state[constants.PARAM_TYPE_VIEW].wid)
        ) state[constants.PARAM_TYPE_WINDOW] = getState(
            state[constants.PARAM_TYPE_VIEW].wid)
        else if (context.filled(globals_latest.latestWID)
            && history.has(globals_latest.latestWID)
        ) state[constants.PARAM_TYPE_WINDOW] = getState(
            globals_latest.latestWID);

        context.createGetters({
            params: state, param_type: constants.PARAM_TYPE_IMPLICIT});
        this.value = state;
    }

    async update(params, param_type=constants.PARAM_TYPE_VIEW) {
        const {context, history, value} = this;
        const G = history.getState(constants.PARAM_TYPE_GLOBAL),
            W = value[constants.PARAM_TYPE_WINDOW],
            V = value[constants.PARAM_TYPE_VIEW];

        if (param_type === constants.PARAM_TYPE_GLOBAL) {
            history.putState(constants.PARAM_TYPE_GLOBAL,
                Object.assign(G, params));
            return;
        }

        Object.assign(value[param_type], params);

        let key = V.rs;
        if (param_type === constants.PARAM_TYPE_WINDOW) {
            if (!context.filled(V.wid)) await history.replaceByType(
                {wid: context.newSlug()},
                constants.PARAM_TYPE_VIEW, false, true);
            key = V.wid
        } else if (param_type !== constants.PARAM_TYPE_VIEW)
            throw new Error(`Invalid parameter type: ${param_type}`)
        else if (context.isSlave) key = history.slaveContextStoreKey();

        await this.update({latestWID: V.wid}, constants.PARAM_TYPE_GLOBAL);
        let rsOrder = history.stateStore.getObject('rsOrder');
        if (history.has(key)) {
            rsOrder = rsOrder.filter(k => key !== k);
            rsOrder.push(key);
            history.stateStore.setObject("rsOrder", rsOrder);
            history.putState(key, value[param_type]);
            return;
        }

        const checkAndFree = () => {
            const {free, threshold} = context.localStorageSize();
            if (free < threshold) {
                history.stateStore.removeItem(rsOrder.shift());
                checkAndFree();
            }
        }
        checkAndFree();
        rsOrder.push(key);
        history.putState(key, value[param_type]);
        history.stateStore.setObject('rsOrder', rsOrder);
    }
}


class History {
    state = null

    constructor(context, rs) {
        this.stateStore = window.localStorage
        this.context = context;

        this.has = this.has.bind(this);
        this.load = this.load.bind(this);
        this.popFromStore = this.popFromStore.bind(this);
        this.push = this.push.bind(this);
        this.pushLazy = this.pushLazy.bind(this);
        this.pushPath = this.pushPath.bind(this);
        this.replace = this.replace.bind(this);

        if (!('isMobile' in ContextGlobals)) this.prepare();
        this.state = new State({history: this, rs});
    }

    prepare = () => {
        if (!this.has('rsOrder')) localStorage.setItem('rsOrder', "[]");
        if (!this.has(constants.PARAM_TYPE_GLOBAL))
            localStorage.setItem(constants.PARAM_TYPE_GLOBAL, "{}");
    }
    has = (rs) => (rs in this.stateStore);
    load = async ({rs, lazy=false}) => {
        const params = this.popFromStore(rs);
        const actorData = params.hasActor ? await this.context.getActorData(
            `${params.packId}.${params.actorId}`) : null;
        await this.context.root.iSetState({initialized: false});
        this.context.assertAndReflect({lazy, actorData, params});
    }
    popFromStore = (rs) => {
        const value = this.getState(rs);
        this.state.value[constants.PARAM_TYPE_VIEW] = value;
        return value;
    }

    push({params, actorData}) {
        // console.warn("20241010 push 1", params, actorData);
        const current = this.state.value[constants.PARAM_TYPE_VIEW];
        if (params.path === current.path &&
            params[constants.URL_PARAM_MASTER_PK] === current[constants.URL_PARAM_MASTER_PK] &&
            params[constants.URL_PARAM_MASTER_TYPE] === current[constants.URL_PARAM_MASTER_TYPE]
        ) throw new Error("Action not allowed, does not have any effect on router path!");
        if (!params.rs) params.rs = this.context.newSlug();
        if (!params.wid) params.wid = current.wid || this.context.newSlug();
        if (params.clickCatch) {
            window.open(`#${this.context.makePath(params)}`);
            return;
        }
        // console.warn("20241010 push 2", params, actorData);
        this.context.assertAndReflect({lazy: false, actorData, params});
    }

    pushLazy({params, actorData}) {
        this.context.assertAndReflect({lazy: true, actorData, params});
    }

    async pushPath({pathname, params, lazy=false} = {}, status) {
        let up = await this.context.buildURLContext(pathname);
        // console.warn("20241010 pushPath up.actorData=", up.actorData);
        if (status) up.params = this.context.pushStatus(status, up.params, up.actorData);
        Object.assign(up.params, params);
        // console.warn("20241010 pushPath up.params=", up.params);
        if (lazy) this.pushLazy(up)
        else this.push(up);
    }

    replaceStateByType = async (params, param_type) => (
        await this.replaceByType(params, param_type, true));
    replace = async (params) => await this.replaceByType(params, constants.PARAM_TYPE_VIEW);
    replaceState = async (params) => (
        await this.replaceStateByType(params, constants.PARAM_TYPE_VIEW));
    async replaceByType(params, param_type, rebuild=false, silent = false) {
        if (param_type === constants.PARAM_TYPE_VIEW &&
            this.context.value.noreload && !params.noreload
        ) params.noreload = false;
        await this.context.reflect({params, param_type, rebuild, silent});
    }
    hardReplace = async (params) => {
        await this.replaceState(params);
        this.context.root.setState({key: this.context.newSlug()});
    }

    contextStoreKey = () => (this.context.isSlave ? this.slaveContextStoreKey()
                                                  : this.context.value.rs);

    slaveContextStoreKey = (suffix = "") => {
        suffix = "_" + this.context.static.actorData.id + suffix;
        const p = this.context.parent;
        if (!p.value.rs)
            return p.history.slaveContextStoreKey(suffix);
        return p.value.rs.toString() + suffix;
    }

    putState = (key, state) => this.stateStore.setObject(key, this.context
        .actionHandler.parser.sanitizeObjectUnparse(
            this.context.ex._.cloneDeep(state)));
    getState = (key) => this.context.actionHandler.parser.sanitizeParse(
        this.stateStore.getObject(key));
}


/**
 * Attaches another root to the Context.
 * Should NOT be able to modify the context but just only reflect
 * the changes in the context.
 * May also have it's own context items which extends or overrides the
 * original context.
 *
 * Creates Getter(s) for all the items in the original context.
 */
export class Delegate {
    constructor(root, context) {
        this.createProperty = this.createProperty.bind(this);

        this.id = context.newSlug();
        this.context = context;
        context.addDelegate(this.id, this);
        this.root = root;
        this._values = {}
        this.value = {}

        Object.keys(context.value).forEach(item => this.createProperty(item));

        this.unset = this.unset.bind(this);
    }

    createProperty(name) {
        Object.defineProperty(
            this.value, name, {
                get: () => {
                    if (this._values.hasOwnProperty(name))
                        return this._values[name]
                    else return this.context.value[name];
                },
                set: (value) => {
                    this._values[name] = value;
                }
            });
    }

    unset() {
        this.context.removeDelegate(this.id);
    }
}
