export const name = "SiteContext";

import React from "react";
import PropTypes from "prop-types";
import * as constants from './constants';
import { RegisterImportPool, getExReady, Component, DynDep,
    URLContextType, DataContextType } from "./Base";

export { LoadingMask, LinoProgressBar, LinoLoadMask} from "./LoadingMask";
export { DialogFactory } from "./LinoDialog";

import { AppMenu } from "./AppMenu";
import { AppTopbar } from "./AppTopbar";

let ex; const exModulePromises = ex = {
    rrd: import(/* webpackChunkName: "reactRouterDom_SiteContext" */"react-router-dom"),
    classNames: import(/* webpackChunkName: "classNames_SiteContext" */"classnames"),
    _: import(/* webpackChunkName: "lodash_SiteContext" */"lodash"),
    prScrollPanel: import(/* webpackChunkName: "prScrollPanel_SiteContext" */"primereact/scrollpanel"),
    u: import(/* webpackChunkName: "LinoUtils_SiteContext" */"./LinoUtils"),
    DashboardItems: import(/* webpackChunkName: "DashboardItems_SiteContext" */"./DashboardItems"),
    nc: import(/* webpackChunkName: "NavigationControl_SiteContext" */"./NavigationControl"),
    lb: import(/* webpackChunkName: "LinoBody_SiteContext" */"./LinoBody"),
    reactI18n: import(/* webpackChunkName: "reactI18n_SiteContext" */"react-i18next"),
};RegisterImportPool(ex);


function MainLayout(props) {
    const { URLContext } = props.APP;
    let [layoutMode, setLayoutMode] = React.useState("static"),
        [layoutColorMode, setLayoutColorMode] = React.useState("dark");

    const localEx = getExReady(ex, ["prScrollPanel", "classNames"], (mods) => {
        mods.classNames = mods.classNames.default;
        mods.ScrollPanel = mods.prScrollPanel.ScrollPanel;
    });
    props.APP.location = props.RRD.useLocation();
    return !localEx.ready || !props.tReady ? null : <div
        className={localEx.classNames('layout-wrapper', {
            'layout-overlay': layoutMode === 'overlay',
            'layout-static': layoutMode === 'static',
            'layout-static-sidebar-inactive': URLContext.value.staticMenuInactive && layoutMode === 'static',
            'layout-overlay-sidebar-active': URLContext.value.overlayMenuActive && layoutMode === 'overlay',
            'layout-mobile-sidebar-active': URLContext.value.mobileMenuActive,
            // 'whitewall-layout-wrapper': this.data.themeName === 'whitewall',
        })}
        ref={el => props.APP.topDiv = el}>
        <AppTopbar
            onToggleMenu={event => {
                URLContext.history.replaceByType({
                    staticMenuInactive: !URLContext.value.staticMenuInactive,
                    overlayMenuActive: !URLContext.value.overlayMenuActive,
                    mobileMenuActive: !URLContext.value.mobileMenuActive,
                },
                constants.PARAM_TYPE_WINDOW);
                if (event) event.preventDefault();
            }}
            URLContext={props.APP.URLContext}
            WS={props.APP.state.WS}
            useChat={false}/>
        <div
            className={localEx.classNames("layout-sidebar", {'layout-sidebar-dark': layoutColorMode === 'dark'})}>
            <localEx.ScrollPanel style={{height: '100%'}}>
                <div className="layout-sidebar-scroll-content">
                    <AppMenu
                        model={props.APP.state.menu_data}
                        onMenuItemClick={event => {
                            if (!event.item.items) {
                                setOverlayMenuActive(false);
                                setMobileMenuActive(false);
                            }
                        }}/>
                </div>
            </localEx.ScrollPanel>
        </div>
        {props.children}
    </div>
}

class URLContextBase extends Component {
    static iPool = ex;
    static Context = URLContextType;

    constructor(props) {
        super(props);

        this.state = {
            ...this.state,
            initialized: false}
    }

    liveUpdate = (params) => {
        if (this.props.summary) {
            this.props.summary.liveUpdate(params);
            return;
        }
        const {mk, mt, controller} = this.state.context;
        const pk = controller.dataContext.mutableContext.id;

        if (controller.contextType === constants.CONTEXT_TYPE_SINGLE_ROW &&
            params.pk !== pk) return;

        if (params[constants.URL_PARAM_MASTER_PK] === null ||
            (params[constants.URL_PARAM_MASTER_PK] === mk &&
                params[constants.URL_PARAM_MASTER_TYPE] === mt)
        ) controller.actionHandler.refresh();
    }

    componentWillUnmount() {
        if (this.state.context === null) return;
        let c = this.state.context.controller;
        if (c.isSlave)
            delete c.parent.children[c.actionHandler.refName];
        delete c.APP.rps[c.actionHandler.refName];
    }
}

export class URLContext extends URLContextBase {
    static requiredModules = ["nc"];
    static propTypes = {
        children: (props, ...args) => {
            if (props.getChildren === null)
                return PropTypes.element.isRequired(props, ...args);
        },
        getChildren: (props, ...args) => {
            if (props.children === null)
                return PropTypes.func.isRequired(props, ...args);
        },
        inherit: PropTypes.bool,
        params: PropTypes.object,
        parentContext: PropTypes.object.isRequired,
        path: (props, ... args) => {
            if (!props.inherit)
                return PropTypes.string.isRequired(props, ...args);
        },
        simple: PropTypes.bool,
        status: PropTypes.object,
        onContextReady: PropTypes.func.isRequired,
        summary: PropTypes.object,
    }

    static defaultProps = {
        children: null,
        getChildren: null,
        inherit: false,
        params: {},
        simple: true,
        status: {},
        onContextReady: (context) => null,
        summary: null,
    }

    constructor(props) {
        super(props);
        this.state = {...this.state, context: null, key: "slave_context"}
    }

    onReady() {
        let pc = this.props.parentContext;
        const path = this.props.inherit ? pc.value.path : this.props.path;
        const m = pc.matchActorPath(path);
        const actorID = `${m.params.packId}.${m.params.actorId}`;
        const clone = pc.static[actorID];
        const next = (c) => {
            const contextHandler = async ({params, actorData}) => {
                c.setActorData(actorData);
                const storeKey = c.history.slaveContextStoreKey();
                Object.assign(params, c.history.getState(storeKey) || {});
                Object.assign(params, this.props.params);
                c.pushStatus(this.props.status, params, actorData);
                if (clone) {
                    c.clone = clone;
                    Object.assign(params, clone.params);
                    if (clone.children) c.copyChildClones(clone.children);
                    delete pc.static[actorID];
                }
                await c.history.replace(params);
                this.props.onContextReady(c.value);
            }
            c.setRoot(this);
            c.setParent(pc);
            if (this.props.inherit) {
                const params = c.history.getState(pc.history.contextStoreKey());
                contextHandler({params, actorData: pc.static.actorData});
            } else {
                if (this.props.simple) c.basicContext(this.props.path, contextHandler)
                else c.buildURLContext(this.props.path, contextHandler);
            }
        }
        new this.ex.nc.Context({APP: pc.APP, slave: true, next: next});
    }

    render() {
        let child = this.state.initialized ? <URLContext.Context.Provider value={this.state.context} key={this.state.key}>
                {this.props.children ? this.props.children
                    : this.props.getChildren(this.state.context)}
            </URLContext.Context.Provider>
            : null;
        return this.props.simple
            ? child
            : <div ref={el => this.contextEntry = el}>
                {child}
                <div ref={el => this.chInPx = el} style={{width: "1ch", visibility: "hidden"}}></div>
            </div>
    }
}

export class RootURLContext extends URLContextBase {
    static requiredModules = ["DashboardItems", "lb", "rrd", "reactI18n"];

    static propTypes = {
        APP: PropTypes.object.isRequired,
    }

    async prepare() {
        await super.prepare();
        this.MainLayout = this.ex.reactI18n.withTranslation()(MainLayout);
    }

    constructor(props) {
        super(props);
        this.state = {
            ...this.state,
            context: props.APP.URLContext.value,
            hasActor: null,
        }
        this.state.context.controller.setRoot(this);

        this.onChInPxRef = this.onChInPxRef.bind(this);
    }

    onChInPxRef(ref) {
        this.chInPx = ref;
        if (ref) {
            let c = this.state.context.controller;
            c.attachDataContext(
                new DataContext({root: this, context: {success: false},
                    next: () => c.build(({params, actorData}) => {
                        c.setActorData(actorData);
                        if (!c.filled(params.rs)) params.rs = c.value.rs;
                        c.APP.navigate(c.makePath(params), {replace: true});
                        c.history.replace(params);
                        if (!params.hasActor && c.clone) {
                            if (c.clone.runnable)
                                c.actionHandler.runAction(c.clone.runnable);
                            delete c.clone;
                        }
                    })}));
        }
    }

    render() {
        if (!this.state.ready) return null;
        return <this.MainLayout APP={this.props.APP} RRD={this.ex.rrd}>
            <div className="layout-main" ref={el => this.contextEntry = el}>
                {this.state.initialized &&
                    <URLContextBase.Context.Provider value={this.state.context}>
                        <div ref={ref => this.errorSpace = ref}></div>
                        {this.state.hasActor ?
                            <this.ex.lb.LinoBody key={this.state.context.rs} actorData={this.state.context.controller.static.actorData}/>
                            : <this.ex.DashboardItems.DashboardItems
                                ref={(el) => { this.props.APP.dashboard = el; this.props.APP.setRpRef(el, "dItems")}}
                                APP={this.props.APP}/>
                        }
                    </URLContextBase.Context.Provider>
                }
                <div ref={this.onChInPxRef} style={{width: "1ch", height: "1ex", visibility: "hidden"}}></div>
            </div>
        </this.MainLayout>
    }
}


export class DataContext extends DynDep {
    static requiredModules = ["u", "_"];
    static iPool = ex;
    static Context = DataContextType;
    async prepare() {this.ex._ = this.ex._.default}
    onReady({root, context = {}, next}) {
        this.root = root;

        this.refStore = {Leaves: {}, slaveLeaves: {}, virtualLeaves: {}}

        this.backupContext = this.backupContext.bind(this);
        this.clearMod = this.clearMod.bind(this);
        this.isModified = this.isModified.bind(this);
        this.prepContext = this.prepContext.bind(this);
        this.set = this.set.bind(this);
        this.setLeafRef = this.setLeafRef.bind(this);
        this.update = this.update.bind(this);
        this.updateState = this.updateState.bind(this);

        this.set(context, true);
        next(this);
    }

    prepContext(context) {
        context.UploadHandlerEvent = null;
        /**
        * context.modifiedRows
        * ********************
        * Used in Multirow context;
        *
        * struct: Object
        *     key: rowIndex
        *     value:
        *         struct: Array
        *             - col.fields_index
        **/
        context.modifiedRows = {}
        /**
        * context.modified
        * ****************
        * Used in single row context;
        *
        * struct: Array[elem.name]
        **/
        context.modified = []
        if (context.rows) {
            let lmt = this.root.context[constants.URL_PARAM_LIMIT];
            context.pks = context.rows.map(row => row[this.root.context.controller.static.actorData.pk_index]);
            for (var i = 0; i < context.rows.length; i++) context.modifiedRows[i] = [];
            context.pageCount = Math.floor(context.count / lmt);
        }
        return context;
    }

    backupContext(context) {
        this.contextBackup = this.ex._.cloneDeep(context);
    }

    clearMod() {
        this.mutableContext.UploadHandlerEvent = null;
        this.mutableContext.modified = [];
        if (this.mutableContext.rows)
            for (var i = 0; i < this.mutableContext.rows.length; i++)
                this.mutableContext.modifiedRows[i] = [];
        // Object.assign(this.mutableContext, this.ex._.cloneDeep(this.contextBackup));
        this.set(this.ex._.cloneDeep(this.contextBackup));
    }

    /**
    * @param {number | "detail" | undefined} row;  Either a rowIndex or constants.DISPLAY_MODE_DETAIL or undefined
    */
    isModified(row) {
        if (this.mutableContext.UploadHandlerEvent !== null) return true;
        if (row !== undefined) {
            if (this.ex.u.isNaN(parseInt(row))) return this.mutableContext.modified.length > 0
            else return this.mutableContext.modifiedRows[row].length > 0;
        }
        if (this.mutableContext.modified.length) return true;
        for (const variable of Object.values(this.mutableContext.modifiedRows))
            if (variable.length) return true;
        return false;
    }

    saveUploadHandlerEvent = (customizedEvent) => {
        this.mutableContext.UploadHandlerEvent = customizedEvent;
    }

    set(context, skipUpdate, extraStates = {}, callback = () => null) {
        this.backupContext(context);
        this.mutableContext = this.prepContext(context);
        if (!skipUpdate) {
            this.root.setState({
                context: this.mutableContext,
                displayMode: this.root.context[constants.URL_PARAM_DISPLAY_MODE],
                ...extraStates
            });
        }
        callback(this.mutableContext);
    }

    setLeafRef({name, ref, type, input}) {
        this.refStore[type + "Leaves"][name] = ref;
    }

    update(values = {}) {
        Object.assign(this.mutableContext, values);
        this.root.setState({context: this.mutableContext});
    }

    updateState(values, extraStates={}) {
        this.mutableContext = Object.assign({}, this.mutableContext, values);
        this.root.setState({context: this.mutableContext, ...extraStates});
    }
}
