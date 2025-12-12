export const name = "LinoBody";

import "./LinoBody.css";

import React from "react";
import PropTypes from "prop-types";
import * as constants from './constants';

import { RegisterImportPool, Component, URLContextType } from "./Base";

import { LinoDetail } from "./LinoDetail";
import { GridElement } from "./GridElement";
import { LinoCards, LinoGalleria } from "./LinoDataView";
import { LinoPaginator } from "./LinoPaginator";
import { LinoParamsPanel } from "./LinoParamsPanel";
import { LinoToolbar, LayoutButton } from "./LinoToolbar";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    _: import(/* webpackChunkName: "lodash_LinoBody" */"lodash"),
    AbortController: import(/* webpackChunkName: "AbortController_LinoBody" */"abort-controller"),
    classNames: import(/* webpackChunkName: "classNames_LinoBody" */"classnames"),
    i18n: import(/* webpackChunkName: "i18n_LinoBody" */"./i18n"),
    le: import(/* webpackChunkName: "LinoEditor_LinoBody" */"./LinoEditor"),
    prButton: import(/* webpackChunkName: "prButton_LinoBody" */"primereact/button"),
    sc: import(/* webpackChunkName: "SiteContext_LinoBody" */"./SiteContext"),
    u: import(/* webpackChunkName: "LinoUtils_LinoBody" */"./LinoUtils"),
    tbc: import(/* webpackChunkName: "LinoUtils_LinoBody" */"./ToolbarComponents"),
};RegisterImportPool(ex);


export class LinoBody extends Component {
    static requiredModules = ["_", "AbortController", "classNames", "prButton",
        "u", "sc", "i18n", "le", "tbc"];
    static iPool = ex;

    static contextType = URLContextType;

    static propTypes = {
        actorData: PropTypes.object.isRequired,
        inDetail: PropTypes.bool
    };

    static defaultProps = {inDetail: false}

    constructor(props) {
        super(props);
        this.state = {
            ...this.state,
            context: {success: false},
            loading: true,
        }
        this.data = {urlParams: null};

        this.get_current_grid_config = this.get_current_grid_config.bind(this);
        this.messageInterceptor = this.messageInterceptor.bind(this);
        this.registerScroll = this.registerScroll.bind(this);
        this.onKeyDown = this.onKeyDown.bind(this);
    }

    async prepare() {
        this.quickFilter = this.ex.u.debounce(this.quickFilter.bind(this), 300);
        this.ex._ = this.ex._.default;
        this.ex.i18n = this.ex.i18n.default;
        let c = this.context.controller;
        this.data.urlParams = !c.static.actorData.use_detail_params_value
            ? c.copy() : c.APP.URLContext.copy();
        this.DataContext = new this.ex.sc.DataContext(
            {root: this, context: {success: false}, next: (dc) => {
                this.state.context = dc.mutableContext;
                c.attachDataContext(dc);
                this.controller = new this.ex.AbortController.default();
                if (c.clone) {
                    if (c.clone.mutableData) {
                        dc.set(c.clone.immutableData, false);
                        dc.updateState(c.clone.mutableData);

                        // DISPLAY_MODE_DETAIL is unique to SingleRow.
                        c.setContextType(c.filled(this.context.fieldName)
                            ? constants.CONTEXT_TYPE_TEXT_FIELD : this.context[
                            constants.URL_PARAM_DISPLAY_MODE] === constants.DISPLAY_MODE_DETAIL
                            ? constants.CONTEXT_TYPE_SINGLE_ROW : constants.CONTEXT_TYPE_MULTI_ROW);
                        this.setState({loading: false});
                        this.context.controller.history.replace({});
                    } else {
                        c.actionHandler.load();
                    }

                    if (c.clone.runnable)
                        c.actionHandler.runAction(c.clone.runnable);

                    delete c.clone;
                } else c.actionHandler.load();
                window.addEventListener("keydown", this.onKeyDown);
                window.addEventListener("message", this.messageInterceptor);
                if (!this.props.inDetail) {
                    window.addEventListener("scroll", this.registerScroll);
                    let p = this.context.controller.APP.location.pathname,
                        arr = window.App.data.scrollIndex,
                        i = arr.indexOf(p);
                    if (i >= 0) {
                        arr.pop(i);
                    } else if (arr.length >= 99) {
                        arr.pop(0);
                        delete window.App.data.scroll[p];
                    };
                    arr.push(p);
                }
            }});
    }

    registerScroll(event) {
        if (this.firstScrollIngonred) {
            window.App.data.scroll[this.context.controller.APP.location.pathname] = Object.assign(
            {}, {scrollX: window.scrollX, scrollY: window.scrollY});
        }
        else {
            this.firstScrollIngonred = true;
        }
    }

    getSnapshotBeforeUpdate(prevProps, prevState) {
        let newContext = this.context;

        if (newContext.controller.static.actorData.use_detail_params_value)
            newContext = newContext.controller.APP.URLContext.value;

        let snapshot = this.context.controller.paramChange_Action(
            newContext, this.data.urlParams);

        if (Object.keys(snapshot).length) {
            this.data.urlParams = newContext.controller.copy();
            return snapshot;
        }
        return null
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (snapshot === null) return
        else if (snapshot.reload) this.context.controller.actionHandler.reload()
        else if (snapshot.refresh) this.context.controller.actionHandler.refresh()
        else if (snapshot.render) this.setState({loading: false});
    }

    componentWillUnmount() {
        if (this.controller) this.controller.abort();
        window.removeEventListener("keydown", this.onKeyDown);
        window.removeEventListener("message", this.messageInterceptor);
        if (!this.props.inDetail) {
            window.removeEventListener("scroll", this.registerScroll);
        }
    }

    messageInterceptor(event) {
    }

    onKeyDown(event) {
        const ad = this.props.actorData;
        const aH = this.context.controller.actionHandler;
        const stopPrevent = () => {
            event.preventDefault(); event.stopPropagation()}
        if (event.code === "Delete" && !this.context.editing_mode) {
            stopPrevent();
            if (this.context[constants.URL_PARAM_SELECTED].length) {
              aH.runAction({action_full_name: ad.delete_action, actorId: ad.id});
            }
        } else if (event.key === "Insert" && !this.props.inDetail && !event.shiftKey
            && !event.ctrlKey && !event.altKey && !this.data.editing_mode) {
            stopPrevent();
            aH.runAction({action_full_name: ad.insert_action, actorId: ad.id,
                pollContext: true});
        } else if (ad.hasOwnProperty('hotkeys')
            && (event.ctrlKey || event.shiftKey || event.altKey ||
            // range keyCode includes function buttons F1, F2, ... F12
            (event.keyCode >= 112 && event.keyCode <= 123))
        ) {
            if (!this.context[constants.URL_PARAM_SELECTED].length) return
            ad.hotkeys.forEach(action => {
                if (event.ctrlKey === action.ctrl && event.shiftKey === action.shift
                    && event.altKey === action.alt && event.code === action.code) {
                    stopPrevent();
                    aH.runAction({action_full_name: action.ba, actorId: ad.id, pollContext: true});
                }
            });
        }
    }

    async quickFilter(values) {
        const c = this.context.controller;

        const oldQuery = c.filled(this.context[constants.URL_PARAM_FILTER]);
        const sort = c.filled(this.context[constants.URL_PARAM_SORT]);
        const gridFilter = c.actionHandler.getGridFilters();

        await c.history.replace(
            {[constants.URL_PARAM_FILTER]: values.query});

        if (this.context.rowReorder && !sort && !gridFilter.length && (
            !oldQuery || !c.filled(values.query)
        )) this.GridElement.set_cols();
    }

    get_current_grid_config(ajax_args) {
        let columns = [],
            widths = [],
            hiddens = [];
        if (this.GridElement) {
            let labels = Array.from(this.GridElement.dataTable.getTable()
                    .querySelectorAll('.col-header-label')),
                dt_cols = labels.map(label => parseInt(label
                    .getAttribute("value"))).map(
                        fields_index => this.props.actorData.col.find(
                            col => col.fields_index === fields_index)),
                doc_cols = labels.map(label => label.closest('th'));
            dt_cols.forEach((col, i) => {
                columns.push(col.name);
                widths.push(Math.floor(doc_cols[i].getBoundingClientRect().width));
                hiddens.push(false);
            });
        }
        ajax_args[constants.URL_PARAM_COLUMNS] = columns;
        ajax_args[constants.URL_PARAM_HIDDENS] = hiddens;
        ajax_args[constants.URL_PARAM_WIDTHS] = widths;
        return ajax_args;
    }

    // renderParamValueControls() {
    //     const {controller} = this.context;
    //     if (this.context[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TEXT)
    //         return null;
    //     return controller.static.actorData.params_layout && <React.Fragment>
    //         <this.ex.prButton.Button
    //             className="l-button-pv_control"
    //             icon={"pi pi-sliders-h"}
    //             onClick={(e) => {
    //                 controller.history.replace(
    //                     {pvPVisible: !this.context.pvPVisible});
    //             }}
    //             style={{float: 'right', background: "#6c8999"}}
    //             tooltip={this.context.pvPVisible ?
    //                 this.ex.i18n.t("Hide parameters panel") :
    //                 this.ex.i18n.t("Show parameters panel")}
    //             tooltipOptions={{position : "left"}}/>
    //         {Object.keys(this.context[constants.URL_PARAM_PARAM_VALUES] || {}).length !== 0 && <this.ex.prButton.Button
    //             icon={"pi pi-times-circle"}
    //             onClick={() => {
    //                 let c = controller;
    //                 c.dataContext.updateState({param_values: {
    //                     ...c.dataContext.contextBackup.param_values}});
    //                 c.history.replace({pv: []});
    //             }}
    //             style={{float: 'right', background: "#6c8999"}}
    //             tooltip={this.ex.i18n.t("Clear and set the parameter values to default")}
    //             tooltipOptions={{position: "left"}}/>
    //         }
    //     </React.Fragment>
    // }

    renderHeader() {
        let header = <React.Fragment>
            <span dangerouslySetInnerHTML={{__html: this.state.context.title
                || this.props.actorData.label || "\u00a0" }}></span>
            {!this.props.inDetail
                ? this.context.controller.globals.isMobile
                    ? <div
                        style={{
                            position: 'fixed',
                            right: '0px',
                            top: '50%',
                            transform: 'translate(0, -50%)',
                            maxWidth: '40px',
                            background: '#2255AA40',
                            borderRadius: '3px',
                            zIndex: 999999
                        }}>
                        <LinoToolbar
                            ref={ref => this.sideToolbar = ref}
                            query={this.context.query} parent={this} side={true}/>
                    </div>
                    : <>
                        {this.context[constants.URL_PARAM_WINDOW_TYPE] !== constants.WINDOW_TYPE_TEXT
                        && <this.ex.prButton.Button
                            icon={
                                this.context.toolbarState == constants.TOOLBAR_STATE_HIDDEN
                                    ? "pi pi-caret-up"
                                    : this.context.toolbarState == constants.TOOLBAR_STATE_VISIBLE
                                        ? "pi pi-caret-down"
                                        : "pi pi-ellipsis-h"
                            }
                            label=""
                            onClick={e => {
                                this.context.controller.history.replace({
                                    toolbarState: this.ex.u.getNextToolbarState(this.context.toolbarState)
                                });
                            }}
                            style={{float: 'right', background: "#6c8999"}}/>}
                        <this.ex.prButton.Button
                            icon="pi pi-link"
                            label=""
                            onClick={e => {
                                const c = this.context.controller;
                                const ah = c.actionHandler;
                                const clone = ah.cloneState({
                                    flags: constants.FLAG_CLONE_UI | constants.FLAG_CLONE_URL,
                                    recursive: true});
                                const link = `${location.origin}/#${c.APP.location.pathname}?${ah.parser.stringify({clone, ...clone.windowGlobals}, true)}`;
                                navigator.clipboard.writeText(link);
                                c.APP.toast.show({
                                    severity: "success",
                                    summary: this.ex.i18n.t("Link copied to clipboard"),
                                    detail: link
                                });
                            }}
                            style={{float: 'right', background: "#6c8999"}}
                            tooltip={this.ex.i18n.t("Copy permalink")}
                            tooltipOptions={{position: "left"}}/>
                        {/* {this.renderParamValueControls()} */}
                    </>
                : <span style={{float: "right"}}>
                    {this.props.actorData.enable_slave_params && <this.ex.tbc.ParamsPanelControl />}
                    <LayoutButton/>
                </span>
            }
        </React.Fragment>

        return this.props.inDetail ? <div className="p-panel p-component">
                <div className="l-detail-header p-panel-header">
                    {header}
                </div>
            </div>
            : <div className="l-detail-header">{header}</div>
    }

    render() {
        if (!this.state.ready) return null;
        if (
            !this.data.urlParams
            // || (
            //     this.props.actorData.hide_if_empty
            //     && this.props.inDetail
            //     // && (this.data.rows === undefined || this.data.rows.length === 0)
            //     && this.data.rows.length === 0
            // )
        ) return null;

        // let paginator = <React.Fragment></React.Fragment>
        let paginator = <LinoPaginator
            parent={this}
            ref={el => this.paginator = el}
            slider={true}
            rowsPerPage={this.context[constants.URL_PARAM_LIMIT]}/>;

        let displayMode = this.state.displayMode,
            ppos = displayMode && this.props.actorData.params_panel_pos;

        return <React.Fragment>
            {this.renderHeader()}
            <this.ex.sc.DataContext.Context.Provider value={this.state.context}>
                {!this.state.context.success
                ? <div dangerouslySetInnerHTML={{__html: this.state.context.message}}/>
                : this.context.controller.filled(this.context.fieldName)
                ? <this.ex.le.LinoEditor elem={{
                    name: this.context.fieldName, field_options: {format: this.state.context.format}
                }} tabIndex={0} urlParams={this.context}/>
                : <>
                    {this.props.inDetail && this.props.actorData.enable_slave_params && <LinoParamsPanel/>}
                    {!this.props.inDetail && <div className="l-header">
                        {ppos === "top" && <LinoParamsPanel/>}
                        <LinoToolbar
                            ref={ref => this.toolbar = ref}
                            query={this.context.query} parent={this}/>
                        {ppos === "bottom" && <LinoParamsPanel/>}
                    </div>}
                    <div className={this.ex.classNames.default("", {["l-params-panel-" + ppos]: ["left", "right"].includes(ppos)})}>
                        {["left", "right"].includes(ppos) && !this.props.inDetail && <LinoParamsPanel/>}
                        <div className="l-grid">
                            {displayMode === constants.DISPLAY_MODE_DETAIL ?
                                <LinoDetail
                                    editing_mode={this.context.editing_mode}
                                    parent={this}
                                    ref={ref => this.LinoDetail = ref}
                                    urlParams={this.context}
                                    window_layout={this.context.window_layout}/>
                                : <React.Fragment>
                                    {this.context.controller.APP.state.site_data.top_paginator && paginator}
                                    {[constants.DISPLAY_MODE_STORY, constants.DISPLAY_MODE_LIST, constants.DISPLAY_MODE_TILES,
                                        constants.DISPLAY_MODE_SUMMARY, constants.DISPLAY_MODE_HTML].includes(displayMode)
                                        ? <div dangerouslySetInnerHTML={{__html: this.state.context.html_text}}/>
                                        : constants.DISPLAY_MODE_TABLE === displayMode
                                            ? <GridElement
                                                loading={this.state.loading}
                                                parent={this}
                                                ref={ref => this.GridElement = ref}
                                                urlParams={this.context}/>
                                            : constants.DISPLAY_MODE_CARDS === displayMode
                                                ? <LinoCards urlParams={this.context}/>
                                                : constants.DISPLAY_MODE_GALLERY === displayMode
                                                    && <LinoGalleria urlParams={this.context}/>
                                    }
                                    {!this.context.controller.APP.state.site_data.top_paginator && paginator}
                                </React.Fragment>
                            }
                        </div>
                    </div>
                </>}
            </this.ex.sc.DataContext.Context.Provider>
        </React.Fragment>
    }
}
