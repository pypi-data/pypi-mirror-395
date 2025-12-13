export const name = "LinoToolbar";
import './LinoToolbar.css';

import React from "react";
import PropTypes from "prop-types";
import * as constants from './constants';
import { RegisterImportPool, getExReady, Component, URLContextType } from "./Base";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    AbortController: import(/* webpackChunkName: "AbortController_LinoToolbar" */"abort-controller"),
    prButton: import(/* webpackChunkName: "prButton_LinoToolbar" */"primereact/button"),
    prInputText: import(/* webpackChunkName: "prInputText_LinoToolbar" */"primereact/inputtext"),
    prOverlayPanel: import(/* webpackChunkName: "prOverlayPanel_LinoToolbar" */"primereact/overlaypanel"),
    prMultiSelect: import(/* webpackChunkName: "prMultiSelect_LinoToolbar" */"primereact/multiselect"),
    prSelectButton: import(/* webpackChunkName: "prSelectButton_LinoToolbar" */"primereact/selectbutton"),
    prSplitButton: import(/* webpackChunkName: "prSplitButton_LinoToolbar" */"primereact/splitbutton"),
    prToggleButton: import(/* webpackChunkName: "prToggleButton_LinoToolbar" */"primereact/togglebutton"),
    u: import(/* webpackChunkName: "LinoUtils_LinoToolbar" */"./LinoUtils"),
    bb: import(/* webpackChunkName: "LinoBbar_LinoToolbar" */"./LinoBbar"),
    lm: import(/* webpackChunkName: "LinoBbar_LinoToolbar" */"./LoadingMask"),
    ac: import(/* webpackChunkName: "AutoComplete_LinoToolbar" */"./AutoComplete"),
    tbc: import(/* webpackChunkName: "ToolbarComponents_LinoToolbar" */"./ToolbarComponents"),
    i18n: import(/* webpackChunkName: "i18n_LinoToolbar" */"./i18n"),
};RegisterImportPool(ex);


// Also used in LinoBody. TODO: rename LayoutButton to DisplayModeSelector
export function LayoutButton() {
    const context = React.useContext(URLContextType);
    const localEx = getExReady(ex, ["prSelectButton", "u", "i18n"], (mods) => {
        mods.i18n = mods.i18n.default;
    });
    const c = context.controller;

    const onLayoutButtonClick = React.useCallback((layout, e) => {
        const checkAndDo = (callback) => {
            if (!c.isModified()) {callback()} else {
                c.actionHandler.discardModDConfirm({agree: callback})
            }
        }
        let action;
        switch (layout) {
            case constants.DISPLAY_MODE_DETAIL: {
                if (c.contextType === constants.CONTEXT_TYPE_SINGLE_ROW)
                    return;
                if (context[constants.URL_PARAM_SELECTED].length === 0) {
                    let pk, row = c.dataContext.mutableContext.rows[0];
                    if (row) {
                        if (Object.prototype.hasOwnProperty.call(row, 'id')) pk = row.id
                        else if (typeof row === 'object') {
                            pk = row[c.static.actorData.pk_index];
                        } else pk = null;
                    }
                    if (!c.filled(pk)) {
                        if (pk === undefined) console.warn("actorData.pk_index is undefined, cannot resolve pk!");
                        if (pk === null) console.warn("cannot open detail on a phantom row!");
                        c.history.replaceState({hasDetail: false});
                    } else checkAndDo(() => c.actionHandler.singleRow(e, pk));
                } else checkAndDo(() => c.actionHandler.singleRow(
                        e, context[constants.URL_PARAM_SELECTED][0]));
                break;
            }
            case 'external': {
                const params = {};
                if ([constants.DISPLAY_MODE_HTML, constants.DISPLAY_MODE_SUMMARY]
                    .includes(context[constants.URL_PARAM_DISPLAY_MODE])
                ) Object.assign(params, {
                    [constants.URL_PARAM_DISPLAY_MODE]: constants.DISPLAY_MODE_TABLE});
                checkAndDo(() => c.actionHandler.copyContext(c.APP.URLContext, params));
                break;
            }
            case constants.DISPLAY_MODE_HTML:
            case constants.DISPLAY_MODE_SUMMARY:
            case constants.DISPLAY_MODE_TABLE:
            case constants.DISPLAY_MODE_CARDS:
            case constants.DISPLAY_MODE_LIST:
            case constants.DISPLAY_MODE_GALLERY:
            case constants.DISPLAY_MODE_STORY:
            case constants.DISPLAY_MODE_TILES: {
                const values = {[constants.URL_PARAM_DISPLAY_MODE]: layout};
                if (!action) {
                    action = c.contextType === constants.CONTEXT_TYPE_SINGLE_ROW
                        ? c.actionHandler.multiRow : c.history.replace;
                }
                checkAndDo(() => action(values));
            }
        }
    });

    const [options, setOptions] = React.useState([]);
    React.useEffect(() => {
        if (!localEx.ready) return;
        const ad = c.static.actorData;
        const opt = [];
        opt.push({icon: "pi-table", help: localEx.i18n.t("Table view"),
            value: constants.DISPLAY_MODE_TABLE});
        if (context.hasDetail) opt.push({icon: "pi-file-o",
            help: localEx.i18n.t("Detail view"),
            value: constants.DISPLAY_MODE_DETAIL});
        if (ad.available_display_modes.includes(constants.DISPLAY_MODE_HTML))
          opt.push({icon: "pi-arrows-h", help: localEx.i18n.t("Simple table view"),
            value: constants.DISPLAY_MODE_HTML});
        if (ad.available_display_modes.includes(constants.DISPLAY_MODE_LIST))
          opt.push({icon: "pi-bars",
            help: localEx.i18n.t("List view"),
            value: constants.DISPLAY_MODE_LIST});
        if (ad.available_display_modes.includes(constants.DISPLAY_MODE_SUMMARY))
          opt.push({icon: "pi-ellipsis-h", help: localEx.i18n.t("Summary view"),
            value: constants.DISPLAY_MODE_SUMMARY});
        if (ad.available_display_modes.includes(constants.DISPLAY_MODE_TILES))
          opt.push({icon: "pi-microsoft", help: localEx.i18n.t("Tiles view"),
            value: constants.DISPLAY_MODE_TILES});
        if (ad.available_display_modes.includes(constants.DISPLAY_MODE_STORY))
          opt.push({icon: "pi-map", help: localEx.i18n.t("Story view"),
            value: constants.DISPLAY_MODE_STORY});
        // if (ad.contain_media) opt.push({icon: "pi-clone",
        if (ad.available_display_modes.includes(constants.DISPLAY_MODE_GALLERY))
          opt.push({icon: "pi-clone",
            help: localEx.i18n.t("Gallery view"),
            value: constants.DISPLAY_MODE_GALLERY});
        // if (ad.card_layout)
        if (ad.available_display_modes.includes(constants.DISPLAY_MODE_CARDS))
          opt.push({icon: "pi-th-large",
            help: localEx.i18n.t("Card view"),
            value: constants.DISPLAY_MODE_CARDS});
        // if (c.isSlave && ad.editable) opt.push({
        if (c.isSlave) opt.push({
            icon: "pi-eject", help: localEx.i18n.t("Expand this panel to own window"),
            value: "external"});
        setOptions(opt);
    }, [localEx.ready, context.hasDetail]);
    // if (localEx.ready && options.length == 0) console.warn("Oops, no options in DisplayModeSelector");

    return !localEx.ready ? null : <localEx.prSelectButton.SelectButton
        itemTemplate={option => (
            <i title={option.help} className={"pi " + option.icon}></i>)}
        onChange={e => onLayoutButtonClick(e.value, e)}
        options={options}
        style={{float: "right"}}
        value={context[constants.URL_PARAM_DISPLAY_MODE]}/>
}


export class LinoToolbar extends Component {
    static requiredModules = ["AbortController", "prButton", "prInputText",
        "prOverlayPanel", "prMultiSelect", "prSplitButton", "prToggleButton",
        "bb", "lm", "u", "ac", "i18n", "tbc"];
    static iPool = ex;
    static contextType = URLContextType;

    static propTypes = {
        side: PropTypes.bool,
        parent: PropTypes.object.isRequired,
        query: PropTypes.string,
    };
    static defaultProps = {
        side: false,
    };

    async prepare() {
        await super.prepare();
        this.ex.i18n = this.ex.i18n.default;
    }

    constructor(props) {
        super(props);
        this.state = {...this.state, query: props.query || "", key: "whatev"};

        this.renderActionBar = this.renderActionBar.bind(this);
        this.renderDataViewSortButton = this.renderDataViewSortButton.bind(this);
        this.renderDetailNavigator = this.renderDetailNavigator.bind(this);
        this.renderEditorButton = this.renderEditorButton.bind(this);
        this.renderParamValueControls = this.renderParamValueControls.bind(this);
        this.renderQuickFilter = this.renderQuickFilter.bind(this);
        this.renderToggle_colControls = this.renderToggle_colControls.bind(this);
    }

    onReady() {
        this.controller = new this.ex.AbortController.default();
    }

    renderActionBar(onSide, nonCollapsibles) {
        const ad = this.context.controller.static.actorData;
        const { APP } = this.context.controller;
        return <this.ex.bb.LinoBbar
            onSide={onSide}
            nonCollapsibles={nonCollapsibles}
            action_full_name={this.context[constants.URL_PARAM_DISPLAY_MODE] === constants.DISPLAY_MODE_DETAIL
                ? ad.default_action.endsWith('.show') // TODO: remove dependecy to 'show'
                ? ad.default_action : ad.detail_action
                : ad.grid_action || APP.state.site_data.common_actions.show_table}/>
    }

    renderDataViewSortButton() {
        if (this.context[constants.URL_PARAM_DISPLAY_MODE] === constants.DISPLAY_MODE_DETAIL) return;
        let ad = this.context.controller.static.actorData;
        const model = ad.col.map((col) => ({
            label: col.name,
            value: String(col.fields_index),
            command: ((e) => {
                let sortField = parseInt(e.item.value);
                this.context.controller.history.replace({
                    // [constants.URL_PARAM_SORT]: this.context.showableColumns.get(sortField),
                    [constants.URL_PARAM_SORT]: ad.col.filter(c => c.fields_index === sortField)[0].name,
                    [constants.URL_PARAM_SORTDIR]: "DESC",
                    sortField: sortField,
                    sortOrder: 1});
            }),
        }));
        return <this.ex.prSplitButton.SplitButton
            icon={
                this.context.sortOrder === 0 ? "pi pi-sort-alt" :
                this.context.sortOrder === 1 ? "pi pi-sort-amount-up" :
                "pi pi-sort-amount-down"
            }
            label={this.ex.i18n.t("Sort by {{value}}",  // 20240930: removed "$t(colonSpaced)"
                {value: this.context[constants.URL_PARAM_SORT] || ""})}
            model={model}
            onClick={() => {
                let sortOrder = this.context.sortOrder === 1 ? -1 : 1;
                this.context.controller.history.replace({
                    [constants.URL_PARAM_SORTDIR]: sortOrder === 1 ? "DESC" : "ASC",
                    sortOrder: sortOrder});
            }}
            style={{verticalAlign: "bottom"}}/>
    }

    renderDetailNavigator() {
        if (this.context[constants.URL_PARAM_DISPLAY_MODE] !== constants.DISPLAY_MODE_DETAIL) return null;
        let navinfo = this.context.controller.dataContext.mutableContext.navinfo,
            loading = this.props.parent.state.loading;
        const checkAndPush = (what) => {
            this.props.parent.LinoDetail.navigate(what);
        }
        return navinfo && <React.Fragment>
            <this.ex.prButton.Button
                disabled={loading || navinfo.prev === null}
                className="l-nav-first" icon="pi pi-angle-double-left"
                onClick={() => checkAndPush('first')}/>
            <this.ex.prButton.Button
                disabled={loading || navinfo.prev === null}
                className="l-nav-prev" icon="pi pi-angle-left"
                onClick={() => checkAndPush('prev')}/>
            <this.ex.prButton.Button
                disabled={loading || navinfo.next === null}
                className="l-nav-next" icon="pi pi-angle-right"
                onClick={() => checkAndPush('next')}/>
            <this.ex.prButton.Button
                disabled={loading || navinfo.next === null}
                className="l-nav-last" icon="pi pi-angle-double-right"
                onClick={() => checkAndPush('last')}/>
        </React.Fragment>
    }

    renderEditorButton() {
        let c = this.context.controller, ad = c.static.actorData;
        if (
            this.context[constants.URL_PARAM_DISPLAY_MODE] !== constants.DISPLAY_MODE_DETAIL
            || !ad.editable || ad.edit_safe
            || c.dataContext.contextBackup.disable_editing
        ) return null
        return <this.ex.prToggleButton.ToggleButton
            checked={!this.context.editing_mode}
            className="l-bbar-editor-button"
            onChange={() => {
                this.ex.u.toggleEditingMode(this.context);
            }}
            onLabel=""
            offLabel=""
            offIcon="pi pi-times"
            onIcon="pi pi-pencil"
            tooltip={this.context.editing_mode ?
                this.ex.i18n.t("Cancel") : this.ex.i18n.t("Edit")}
            tooltipOptions={{position : "bottom"}}/>
    }

    renderParamValueControls() {
        return <this.ex.tbc.ParamsPanelControl />;
        // const c = this.context.controller;
        // return c.static.actorData.params_layout
        //     && c.contextType == constants.CONTEXT_TYPE_MULTI_ROW
        //     && c.APP.state.site_data.data_exporter
        //     && <React.Fragment>
        //     <this.ex.prButton.Button
        //         className="l-button-pv_control"
        //         icon="pi pi-sliders-h"
        //         onClick={() => {
        //             c.history.replace(
        //                 {pvPVisible: !this.context.pvPVisible});
        //         }}
        //         tooltip={this.context.pvPVisible ?
        //             this.ex.i18n.t("Hide parameters panel") :
        //             this.ex.i18n.t("Show parameters panel")}
        //         tooltipOptions={{position : "bottom"}}/>
        //     {Object.keys(this.context[constants.URL_PARAM_PARAM_VALUES] || {}).length !== 0 && <this.ex.prButton.Button
        //         icon={"pi pi-times-circle"}
        //         onClick={() => {
        //             c.dataContext.updateState({param_values: {
        //                 ...c.dataContext.contextBackup.param_values}});
        //             c.history.replace({pv: []});
        //         }}
        //         tooltip={this.ex.i18n.t("Clear and set the parameter values to default")}
        //         tooltipOptions={{position: "bottom"}}/>
        //     }
        // </React.Fragment>
    }

    renderQuickFilter(wide) {
        return <span onKeyDown={e => {
                if (e.code === "Delete") e.stopPropagation();
            }}>
            {this.context[constants.URL_PARAM_DISPLAY_MODE] === constants.DISPLAY_MODE_DETAIL
                ? <this.ex.ac.QuickFilter urlParams={this.context} wide={!!wide}/>
                : <this.ex.prInputText.InputText
                    className="l-grid-quickfilter"
                    onChange={(e) => {
                        let v = e.target.value;
                        this.setState({query: v});
                        this.props.parent.quickFilter({query: v});
                    }}
                    placeholder={this.ex.i18n.t("Quick search")}
                    ref={(ref) => {
                        if (ref &&
                            this.context.controller.globals.currentInputWindowType === constants.WINDOW_TYPE_UNKNOWN &&
                            this.context.controller.globals.currentInputIndex === 0
                        ) {
                            ref.focus();
                        }
                    }}
                    style={{
                        width: wide ? "100%" : undefined,
                        marginRight: wide ? "1ch" : undefined,
                        marginLeft: wide ? "1ch" : undefined
                    }}
                    value={this.state.query}/>
            }
        </span>
    }

    renderToggle_colControls() {
        if (this.context[constants.URL_PARAM_DISPLAY_MODE] !== constants.DISPLAY_MODE_TABLE)
            return null;

        return <React.Fragment>
            <this.ex.prButton.Button
                icon={"pi pi-list"}
                onClick={(e) => this.col_selector_op.toggle(e)}
                tooltip={this.ex.i18n.t("Configure visibility of the grid columns")}
                tooltipOptions={{position: "bottom"}}/>
            <this.ex.prOverlayPanel.OverlayPanel
                onHide={() => this.col_selector.hide()}
                onShow={() => this.col_selector.show()}
                ref={ref => this.col_selector_op = ref}>
                <this.ex.prMultiSelect.MultiSelect
                    display="chip"
                    filter={true}
                    onChange={(e) => {
                        let showableColumns = new Map();
                        e.value.forEach((fields_index) => {
                            showableColumns.set(
                                fields_index,
                                this.context.controller.static.actorData.col.find(
                                    col => col.fields_index === fields_index
                                ).name
                            );
                        });

                        this.context.controller.history.replace({
                            showableColumns: showableColumns});
                        this.props.parent.GridElement.set_cols();
                    }}
                    onHide={() => this.col_selector_op.hide()}
                    options={this.context.controller.static.actorData.col.map(
                        (col) => {
                            return {
                                label: col.name,
                                value: col.fields_index,
                            }
                        }
                    )}
                    panelStyle={{
                        zIndex: "99999",
                        height: "auto",
                        width: "auto",
                        position: "absolute",
                    }}
                    ref={ref => this.col_selector = ref}
                    style={{maxWidth: "90vw"}}
                    value={Array.from(this.context.showableColumns.keys())}/>
            </this.ex.prOverlayPanel.OverlayPanel>
        </React.Fragment>
    }

    render() {
        if (!this.state.ready) return null;
        let ad = this.context.controller.static.actorData;
        return <React.Fragment key={this.state.key}>
            {this.context.toolbarState == constants.TOOLBAR_STATE_VISIBLE ? <React.Fragment>
                <div className={"table-header"}>
                    <div
                        className="l-bbar-left"
                        style={{background: "transparent"}}>
                        {!ad.hide_navigator
                            && <React.Fragment>
                                {this.renderQuickFilter()}
                                {
                                    this.renderParamValueControls()
                                }
                                {this.context[constants.URL_PARAM_DISPLAY_MODE] !== constants.DISPLAY_MODE_TABLE
                                    ? this.renderDataViewSortButton()
                                    : this.renderToggle_colControls()}
                                {this.renderDetailNavigator()}
                            </React.Fragment>
                        }
                        {this.renderActionBar(false)}
                        {this.renderEditorButton()}
                    </div>
                    <LayoutButton/>
                </div>
            </React.Fragment>
            : this.props.side ? <React.Fragment>
                {!ad.hide_navigator && <React.Fragment>
                    {this.renderDetailNavigator()}
                    {this.context[constants.URL_PARAM_DISPLAY_MODE] === constants.DISPLAY_MODE_TABLE
                        && this.renderToggle_colControls()}
                </React.Fragment>}
                {this.renderActionBar(true)}
                {this.renderEditorButton()}
            </React.Fragment>
            : !ad.hide_top_toolbar
                && this.context.toolbarState == constants.TOOLBAR_STATE_PARTIALLY_VISIBLE
                && <React.Fragment>
                <div className={"table-header"}>
                    <div
                        className="l-bbar-left"
                        style={{background: "transparent"}}>
                        {!ad.hide_navigator && <React.Fragment>
                            {this.renderQuickFilter()}
                            {
                                this.renderParamValueControls()
                            }
                            {this.context[constants.URL_PARAM_DISPLAY_MODE] !== constants.DISPLAY_MODE_TABLE
                                && this.renderDataViewSortButton()}
                        </React.Fragment>}
                        {this.renderActionBar(false, true)}
                    </div>
                    <LayoutButton/>
                </div>
            </React.Fragment>}

            {!this.props.side
                && <this.ex.lm.LinoProgressBar loading={this.props.parent.state.loading}/>}
        </React.Fragment>
    }
}
