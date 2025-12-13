export const name = "GridElement";
import "./GridElement.css"

import React from "react";
import PropTypes from "prop-types";
import * as constants from './constants';

import { RegisterImportPool, Component, URLContextType, DataContextType } from "./Base";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    _: import(/* webpackChunkName: "lodash_GridElement" */"lodash"),
    // AbortController: import(/* webpackChunkName: "AbortController_GridElement" */"abort-controller"),
    prButton: import(/* webpackChunkName: "prButton_GridElement" */"primereact/button"),
    prColumn: import(/* webpackChunkName: "prColumn_GridElement" */"primereact/column"),
    prTriStateCheckbox: import(/* webpackChunkName: "prTriStateCheckbox_GridElement" */"primereact/tristatecheckbox"),
    prDataTable: import(/* webpackChunkName: "prDataTable_GridElement" */"primereact/datatable"),
    prInputNumber: import(/* webpackChunkName: "prInputNumber_GridElement" */"primereact/inputnumber"),
    prInputText: import(/* webpackChunkName: "prInputText_GridElement" */"primereact/inputtext"),
    prMultiSelect: import(/* webpackChunkName: "prMultiSelect_GridElement" */"primereact/multiselect"),
    prOverlayPanel: import(/* webpackChunkName: "prOverlayPanel_GridElement" */"primereact/overlaypanel"),
    prSelectButton: import(/* webpackChunkName: "prSelectButton_GridElement" */"primereact/selectbutton"),
    u: import(/* webpackChunkName: "LinoComponents_GridElement" */"./LinoUtils"),
    lc: import(/* webpackChunkName: "LinoComponents_GridElement" */"./LinoComponents"),
    dt: import(/* webpackChunkName: "datetime_GridElement" */"./datetime"),
    i18n: import(/* webpackChunkName: "i18n_GridElement" */"./i18n"),
};RegisterImportPool(ex);


class DragAndDrop extends React.Component {
    static propTypes = {
        rowData: PropTypes.array.isRequired,
        upc: PropTypes.object.isRequired,
        column: PropTypes.object.isRequired,
        children: PropTypes.node.isRequired,
    }
    constructor(props) {
        super(props);

        this.dragStart = this.dragStart.bind(this);
        this.drop = this.drop.bind(this);
    }

    dragOver(e) {
        e.preventDefault();
    }

    dragStart(e) {
        let t = e.target, pk;
        if (t.nodeName === 'A') t = e.target.querySelector('div');
        pk = t.attributes.pk.value;
        e.dataTransfer.setData('pk', pk);
    }

    drop(e) {
        const { rowData, upc, column } = this.props;
        const pk = e.dataTransfer.getData("pk");
        const start_date = rowData.filter(cell => (
                upc.filled(cell) && typeof cell === 'object' && cell.meta))[0]
                  .calDates[parseInt(column.field)];
        upc.actionHandler.runAction({
            actorId: 'cal.Events', [constants.URL_PARAM_SELECTED]: [pk],
            action_full_name: upc.actionHandler.findUniqueAction('drag_drop').full_name,
            status: {data: {start_date: start_date}}});
    }

    render() {
        return <div
            draggable={true}
            onDragOver={this.dragOver}
            onDragStart={this.dragStart}
            onDrop={this.drop}>
            {this.props.children}
        </div>
    }
}


class GridFilter extends Component {
    static requiredModules = ["u", "_", "prTriStateCheckbox", "prInputNumber",
        "prInputText", "prMultiSelect", "prSelectButton", "dt"];
    static iPool = ex;

    static propTypes = {
        col: PropTypes.object.isRequired,
        ge: PropTypes.object,
        style: PropTypes.object.isRequired,
    }
    static defaultProps = {
        style: {}
    }
    static contextType = URLContextType;

    async prepare() {
        this.ex._ = this.ex._.default;
    }

    constructor(props) {
        super(props);
        this.state = {
            ...this.state,
            filter: null,
            value: null,
            comparison: "exact",
        }
        this.comparisonSelect = this.comparisonSelect.bind(this);
    }

    onReady() {
        this.pushFilter = this.ex.u.debounce(this.pushFilter.bind(this), 300);
        let col = this.props.col,
            ft = this.context.gridFilters.get(col.fields_index) || {
                field: col.name,
                type: col.filter.type,
                value: "",
            };
        if (["numeric", "date"].includes(ft.type) && ft.comparison === undefined)
            ft.comparison = this.state.comparison;
        this.context.gridFilters.set(col.fields_index, ft);
        this.setState({
            filter: ft, value: ft.value,
            comparison: ft.comparison || this.state.comparison});
    }

    comparisonSelect(pushValue) {
        return <this.ex.prSelectButton.SelectButton
            onChange={e => pushValue({comparison: e.value})}
            optionLabel="label"
            options={[
                {label: "<", value: "lt"},
                {label: "==", value: "exact"},
                {label: ">", value: "gt"},
            ]}
            optionValue="value"
            style={{textAlign: "center"}}
            value={this.state.comparison}/>
    }

    pushFilter(values) {
        const c = this.context.controller;

        const noSort = !c.filled(this.context[constants.URL_PARAM_SORT]);
        const oldFilters = this.ex._.cloneDeep(c.actionHandler.getGridFilters());

        Object.assign(this.state.filter, values);

        const fts = c.actionHandler.getGridFilters();

        if (this.context.rowReorder
            && !c.filled(c.value[constants.URL_PARAM_FILTER]) && noSort
            && (!oldFilters.length || !fts.length)) this.props.ge.set_cols();

        c.history.replace({
            [constants.URL_PARAM_GRIDFILTER]: this.ex._.cloneDeep(fts)});
    }

    render() {
        if (!this.state.ready) return null;
        if (this.state.filter === null) return null;
        let {col} = this.props, el,
            op = this.props.ge.filterPanels[col.fields_index];
        const pushValue = (v) => {this.setState(v);this.pushFilter(v)};
        if (col.filter.type === "list") el = <this.ex.prMultiSelect.MultiSelect
            onChange={e => pushValue({value: e.target.value})}
            options={col.filter.options}
            value={this.state.value}/>
        else if (col.filter.type === "string") el = <this.ex.prInputText.InputText
            value={this.state.value}
            onChange={e => pushValue({value: e.target.value})}/>
        else if (col.filter.type === "numeric") el = <React.Fragment>
            <this.ex.prInputNumber.InputNumber
                value={this.state.value}
                onChange={e => pushValue({value: e.value})}/>
            {this.comparisonSelect(pushValue)}
        </React.Fragment>
        else if (col.filter.type === 'boolean') {
            el = <this.ex.prTriStateCheckbox.TriStateCheckbox
                onChange={e => pushValue({value: e.value})}
                value={this.state.value}/>
        } else if (col.filter.type === 'date') el = <React.Fragment>
            <this.ex.dt.DateFilter
                elem={col}
                parent={this}
                urlParams={this.context}/>
            {this.comparisonSelect(pushValue)}
            </React.Fragment>
        else throw "NotImplementedError"
        return <div style={this.props.style} onKeyDown={e => {
            if (e.code === "Escape" && op) {
                e.stopPropagation();
                e.preventDefault();
                op.hide();
            }
        }}>{el}</div>
    }
}


export class GridElement extends Component {
    static requiredModules = ["prButton", "prColumn", "prDataTable",
        "prOverlayPanel", "lc", "u", "i18n"];
    static iPool = ex;

    static contextType = DataContextType;

    static propTypes = {
        loading: PropTypes.bool.isRequired,
        parent: PropTypes.object.isRequired,
        urlParams: PropTypes.object.isRequired,
    }

    async prepare() {
        await super.prepare();
        this.ex.i18n = this.ex.i18n.default;
    }

    constructor(props) {
        super(props);
        this.state = {
            ...this.state,
            columns: null,
            loading: props.loading,
            scrollHeight: "",
        };
        this.data = {shiftIndex: null};
        this.filterPanels = {};

        this.arrowSelect = this.arrowSelect.bind(this);
        this.columnEditor = this.columnEditor.bind(this);
        this.columnTemplate = this.columnTemplate.bind(this);
        this.demandsFromChildren = this.demandsFromChildren.bind(this);
        this.handleZoom = this.handleZoom.bind(this);
        this.keyPaginator = this.keyPaginator.bind(this);
        this.loadSelectedRows = this.loadSelectedRows.bind(this);
        this.onBeforeEditorHide = this.onBeforeEditorHide.bind(this);
        this.onBeforeEditorShow = this.onBeforeEditorShow.bind(this);
        this.onCancel = this.onCancel.bind(this);
        this.onColReorder = this.onColReorder.bind(this);
        this.onEditorInit = this.onEditorInit.bind(this);
        this.onTableRef = this.onTableRef.bind(this);
        this.editorKeyDown = this.editorKeyDown.bind(this);
        this.onCellEditComplete = this.onCellEditComplete.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.rowReorder = this.rowReorder.bind(this);
        this.set_cols = this.set_cols.bind(this);
        this.showDetail = this.showDetail.bind(this);
    }

    onReady() {
        this.set_cols();
        if (this.props.parent.props.inDetail) {
            window.postMessage('GridMount', "*");
        } else {
            window.addEventListener('keydown', this.arrowSelect);
            window.addEventListener('keydown', this.loadSelectedRows);
            window.addEventListener('keydown', this.keyPaginator);
        }
        window.App.registerHandle("zoom", this.handleZoom);
    }

    onTableRef(ref) {
        this.dataTable = ref;
        if (ref) {
            if (!this.props.parent.props.inDetail) {
                this.setScrollHeight();
            }
        }
    }

    setScrollHeight() {
        let p = this.props.parent, n = 0,
            rect = this.dataTable.getElement().getBoundingClientRect();
        if (p.paginator && p.paginator.container) {
            let pRect = p.paginator.container.getBoundingClientRect();
            if (pRect.top > rect.top) {
                n = pRect.height;
            }
        }
        let h = Math.round(window.innerHeight - n - rect.top).toString() + "px";
        if (this.state.scrollHeight !== h) this.setState({scrollHeight: h});
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    getSnapshotBeforeUpdate(prevProps, _prevState) {
        if (!this.state.ready) return null;
        let snapshot = {};
        if (
            prevProps.urlParams !== this.props.urlParams ||
            this.props.loading !== prevProps.loading
        ) {
            snapshot.render = true;
        }
        if (Object.keys(snapshot).length) return snapshot
        return null
    }

    componentDidUpdate(_prevProps, _prevState, snapshot) {
        if (snapshot === null) return;
        this.setState({loading: this.props.loading});
    }

    componentWillUnmount() {
        if (!this.props.parent.props.inDetail && this.state.ready) {
            window.removeEventListener('keydown', this.arrowSelect);
            window.removeEventListener('keydown', this.loadSelectedRows);
            window.removeEventListener('keydown', this.keyPaginator);
        }
        window.App.unregisterHandle("zoom", this.handleZoom);
        const c = this.props.urlParams.controller;
        if (c.APP.URLContext === c) {
            Object.assign(c.globals, {
                currentInputWindowType: constants.WINDOW_TYPE_UNKNOWN,
                currentInputIndex: 0,
                currentInputAHRefName: c.actionHandler.refName,
            });
        }
    }

    loadSelectedRows(event) {
        if (event.key === "Enter" && this.props.urlParams[constants.URL_PARAM_SELECTED].length) {
            event.stopPropagation();
            event.preventDefault();
            this.showDetail(event, this.props.urlParams[constants.URL_PARAM_SELECTED][0]);
        }
    }

    arrowSelect(event) {
        if (
            ["ArrowUp", "ArrowDown"].includes(event.code)
            && !window.App.arrowsTaken
            && !this.props.parent.props.inDetail
        ) {
            event.stopPropagation();
            let i, sr, last_i, first_i, scroll_first, scroll_last,
                len = this.context.rows.length,
                srs = this.props.urlParams[constants.URL_PARAM_SELECTED],
                shiftIndex = this.data.shiftIndex;
            if (!this.props.urlParams[constants.URL_PARAM_SELECTED].length) {
                if (event.code === "ArrowUp") sr = this.context.pks.slice(-1)
                else sr = [this.context.pks[0]];
            } else {
                if (event.shiftKey && shiftIndex !== null) {
                    last_i = this.context.pks.indexOf(srs.slice(-1)[0]);
                    first_i = this.context.pks.indexOf(srs[0]);
                    if (first_i === shiftIndex) { // operate on last_i (last item index)
                        if (event.code === "ArrowDown") {
                            if (last_i < len - 1) sr = this.context.pks
                                .slice(shiftIndex, last_i+2);
                        } else {
                            if (last_i > shiftIndex) {
                                sr = this.context.pks.slice(shiftIndex, last_i);
                            } else if (last_i > 0) {
                                scroll_first = true
                                sr = this.context.pks.slice(last_i-1, shiftIndex+1);
                            }
                        }
                        if (!scroll_first) scroll_last = true;
                    } else { // operate on first_i (first item index)
                        scroll_first = true;
                        if (event.code === "ArrowDown") {
                            sr = this.context.pks.slice(first_i+1, shiftIndex+1)
                        } else if (first_i > 0) {
                            sr = this.context.pks.slice(first_i-1, shiftIndex+1)
                        }
                    }
                } else {
                    if (event.code === "ArrowUp") {
                        i = this.context.pks.indexOf(srs[0]);
                        if (i > 0) {
                            sr = [this.context.pks[i - 1]];
                        }
                    } else {
                        i = this.context.pks.indexOf(srs.slice(-1)[0]);
                        if (i < len - 1) {
                            sr = [this.context.pks[i + 1]];
                        }
                    }
                }
            }
            if (sr) {
                if (!event.shiftKey) {
                    if (event.code === "ArrowDown") {
                        this.data.shiftIndex = this.context.pks.indexOf(sr[0]);
                    } else {
                        this.data.shiftIndex = this.context.pks.indexOf(sr.slice(-1)[0]);
                    }
                }

                this.props.urlParams.controller.history.replace({[constants.URL_PARAM_SELECTED]: sr});
                this.props.parent.setState({loading: false});

                let el = Array.from(this.dataTable.getElement().querySelectorAll('tr.p-highlight'));
                let p_srabl_rect = this.dataTable.getElement().getBoundingClientRect();
                if (!el.length) return
                let last_el_out = el.slice(-1)[0].getBoundingClientRect()
                    .bottom - p_srabl_rect.bottom > 0;
                let first_el_out = el[0].getBoundingClientRect()
                    .top - p_srabl_rect.top < 0;
                let scroll = last_el_out || first_el_out;
                if (scroll) {
                    let block = "nearest";
                    if (scroll_last) el = el.slice(-1)[0];
                    if (scroll_first) el = el[0];
                    if (first_el_out && scroll_last) block = "end";
                    if (last_el_out && scroll_first) block = "start";
                    if (el.length) el = el[0];
                    el.scrollIntoView({block: block, behaviour: 'smooth'});
                }
            }
        }
    }

    keyPaginator(event) {
        // console.log("20240821", event);
        if (
            ["PageUp", "PageDown", "End", "Home"].includes(event.code)
            && !window.App.arrowsTaken
            && !this.props.parent.props.inDetail
        ) {
            event.preventDefault();
            let current_start = this.props.urlParams[constants.URL_PARAM_START] || 0,
                next_page_start = current_start + this.props.urlParams[constants.URL_PARAM_LIMIT],
                last_page_start = this.context.pageCount * this.props.urlParams[constants.URL_PARAM_LIMIT];
            if (event.code === "PageUp") {
                if (current_start) {
                    this.props.urlParams.controller.history.replace(
                        {[constants.URL_PARAM_START]: current_start - this.context.rows.length}
                    );
                }
            } else if (event.code === "PageDown") {
                if(next_page_start <= last_page_start) {
                    this.props.urlParams.controller.history.replace(
                        {[constants.URL_PARAM_START]: next_page_start}
                    );
                }
            } else if (event.code === "End") {
                this.props.urlParams.controller.history.replace(
                    {[constants.URL_PARAM_START]: last_page_start}
                );
            } else if (event.code === "Home") {
                this.props.urlParams.controller.history.replace(
                    {[constants.URL_PARAM_START]: 0}
                );
            }
        }
    }

    editorKeyDown(event) {
    //     // use event.code for the physical key pressed or
    //     // event.key for the character the key maps to.
    //     console.log(`20240820 ${event.ctrlKey ? "Ctrl+" : ""}${event.metaKey ? "Alt+" : ""}${event.code} (${event.key})`);

        // don't propagate key events like Delete, End and Home, which we want
        // to remain inside the cell editor:
        const editorKeys = ["Home", "End", "Delete", "Insert"];
        if (editorKeys.includes(event.code))
          event.stopPropagation();

        if (event.key === "Enter") {
            event.stopPropagation();

            let tr = event.target.closest("tr");
            tr = event.shiftKey ? tr.previousSibling : tr.nextSibling;

            if (tr) {
                tr.children[Array.prototype.indexOf.call(
                    event.target.closest("tr").childNodes,
                    event.target.closest("td")
                )].click();
            } else this.dataTable.closeEditingCell();
        }
        if (event.code === "Tab") {
            event.stopPropagation();
            event.preventDefault();
            // let td = event.target.closest("td");
            // td = event.shiftKey ? td.previousSibling : td.nextSibling;
            // if (td) td.click();
            let tbl = event.target.closest('table'),
                cols = Array.from(
                    // tbl.getElementsByClassName("p-cell-editor-key-helper")),
                    tbl.getElementsByClassName("lino-input-leaf")).filter(
                        el => !el.classList.contains("lino-disabled-leaf")),
                i = cols.findIndex(
                    n => n.closest("td").contains(event.target));
            i = event.shiftKey ? i - 1 : i + 1;
            cols[i].click()
        }
    }

    handleZoom() {
        this.setScrollHeight();
    }

    // To pass arbitrary objects to childrens on demand
    demandsFromChildren(obj) {
        this.data.roger = obj;
    }

    async onColReorder(e) {
        this.setState({columns: null});
        let showableColumns = new Map();
        e.columns.filter(col => !this.ex.u.isNaN(parseInt(col.props.field)))
        .forEach((col) => {
            showableColumns.set(parseInt(col.props.field), col.props.name);
        });
        await this.props.urlParams.controller.history.replace(
            {showableColumns: showableColumns});
        this.set_cols();
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    onBeforeEditorHide(col, event) {
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    onBeforeEditorShow(col) {
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    onEditorInit(col) {
    }

    onSubmit({rowIndex, originalEvent}) {
        if (originalEvent.type === "click" && originalEvent.ctrlKey) return;
        // this.controller.abort();
        // this.controller = new this.ex.AbortController.default();
        this.props.urlParams.controller.actionHandler.submit(
            {cellInfo: {rowIndex: rowIndex},
            // signal: this.controller.signal
        });
    }

    onCancel() {
        // console.log('Cancelled!');
    }

    columnEditor(col) {
        if (!this.props.urlParams.controller.static.actorData.editable || !col.editable) return undefined;
        // console.log("20240820 col is", col);
        const CellEditor = (column) => {
            const prop_bundle = {
                hide_label: true,
                [constants.URL_PARAM_WINDOW_TYPE]: constants.WINDOW_TYPE_TABLE,
                column: column,
                editing_mode: true,
                tabIndex: (Math.max(...Array.from(
                    this.props.urlParams.showableColumns.keys()
                )) * column.rowIndex) + col.fields_index,
            };
            return <div onKeyDown={this.editorKeyDown}>
                <this.ex.lc.LinoLayout {...prop_bundle} elem={col}/>
            </div>
            // return <this.ex.lc.LinoLayout {...prop_bundle} elem={col}/>
        }
        CellEditor.displayName = 'CellEditor';
        return CellEditor;
    }

    columnTemplate(col) {
        const CellTemplate = (rowData, column) => {
            let row_view_button,
                c = this.props.urlParams.controller,
                ad = c.static.actorData,
                overflow_control = {}, calview = ad.table_as_calendar;

            // if (!calview) overflow_control = {overflow: "hidden"};

            const prop_bundle = {
                editing_mode: false,
                hide_label: true,
                [constants.URL_PARAM_WINDOW_TYPE]: constants.WINDOW_TYPE_TABLE,
                column: column,
                tabIndex: (Math.max(...Array.from(
                    this.props.urlParams.showableColumns.keys()
                )) * column.rowIndex) + col.fields_index,
            };

            let elem = <this.ex.lc.LinoLayout {...prop_bundle} elem={col}/>
            if (calview) elem = <DragAndDrop {...prop_bundle}
                rowData={rowData} upc={this.props.urlParams.controller}>
                {elem}</DragAndDrop>

            return <React.Fragment>
                {row_view_button}
                <div style={overflow_control}>{elem}</div>
            </React.Fragment>
        }
        CellTemplate.displayName = 'CellTemplate';
        return CellTemplate;
    }

    onCellEditComplete(e) {
      // https://www.primefaces.org/primereact-v8/datatable/
      // start editing on next cell
      // use event.code for the physical key pressed or
      // event.key for the character the key maps to.
      this.onSubmit(e)

      let event = e.originalEvent;
      // console.log(`20240820 ${event.ctrlKey ? "Ctrl+" : ""}${event.metaKey ? "Alt+" : ""}${event.code} (${event.key})`);
      // if (["Home", "End", "Delete"].includes(event.code))
      //   event.stopPropagation();
      if (event.key === "Enter") {
          // Manually close (and submit) the entry if the keystoke comes from the numpad
          if (event.code === "NumpadEnter") this.dataTable.closeEditingCell();

          let tr = event.target.closest("tr");
          tr = event.shiftKey ? tr.previousSibling : tr.nextSibling;

          if (tr) {
              tr.children[Array.prototype.indexOf.call(
                  event.target.closest("tr").childNodes,
                  event.target.closest("td")
              )].click();
          }
      }
      if (event.code === "Tab") {
          // let td = event.target.closest("td");
          // td = event.shiftKey ? td.previousSibling : td.nextSibling;
          // if (td) td.click();
          let tbl = event.target.closest('table'),
              cols = Array.from(
                  // tbl.getElementsByClassName("p-cell-editor-key-helper")),
                  tbl.getElementsByClassName("lino-input-leaf")).filter(
                      el => !el.classList.contains("lino-disabled-leaf")),
              i = cols.findIndex(
                  n => n.closest("td").contains(event.target));
          i = event.shiftKey ? i - 1 : i + 1;
          cols[i].click()
      }
    }

    rowClassName(rowData) {
        if (!Array.isArray(rowData)) return {};
        let rowMeta = rowData.filter(cell => (![null, undefined].includes(cell)
            && typeof cell === 'object' && cell.meta))[0], styleClass = {};
        if (rowMeta && Object.prototype.hasOwnProperty.call(rowMeta, 'styleClass')) {
            styleClass[rowMeta.styleClass] = true;
            return styleClass
        }
    }

    set_cols() {
        if (this.props.urlParams.controller.static.actorData.col === undefined) { return; };
        const style = {verticalAlign: 'baseline', whiteSpace: 'wrap', overflow: "clip"},
            up = this.props.urlParams, c = up.controller, ad = c.static.actorData;
        // if (ad.table_as_calendar) style.padding = '0';

        let columns = []
        if (c.filled(ad.detail_action) && c.filled(ad.pk_index)) columns.push("DetailLink");
        const showRowReorderColumn = (
            up.rowReorder
            && !c.filled(up[constants.URL_PARAM_FILTER])
            && !c.filled(up[constants.URL_PARAM_SORT])
            && !c.actionHandler.getGridFilters().length
        );

        // 20241029 deactivated because i wonder whether it is useful:
        // if (ad.preview_limit > 0) columns.push("SelectCol");
        // console.log("20241029", up.showableColumns, ad.col);
        let dbColumns = Array.from(up.showableColumns.keys()).map(
            fields_index => ad.col.filter(col => col.fields_index === fields_index)[0]);

        if (!showRowReorderColumn && up.rowReorder)
            dbColumns = dbColumns.filter(col => col.name !== "dndreorder")

        columns = columns.concat(dbColumns).map((col, i) => {
            // console.log("20241029", col);
            let colWidth = col.width || col.preferred_width;
            if (colWidth) {
                if (colWidth < 2) colWidth = 2;
                colWidth = colWidth.toString() + "ch";
            }
            const passThrough = {headerCell: {
                title: (col.value && col.value.quicktip) || col.help_text
            }}
            return col.name === "dndreorder" ?
                <this.ex.prColumn.Column
                    field={String(col.fields_index)} key={i} pt={passThrough}
                    rowReorder={true} style={{width: "2rem"}}/>
                : col.name === "rowselect" ?
                <this.ex.prColumn.Column
                    align="center" key={i} selectionMode="multiple"
                    style={{width: '2em', padding: "unset", textAlign: "center"}}/>
                : col === "DetailLink"
                    ? <this.ex.prColumn.Column
                        align="center"
                        body={(rowData) => (<div className="l-span-clickable"
                            onClick={(e) => {
                                const pk = rowData[ad.pk_index];
                                if (pk === null) {
                                    c.actionHandler.runAction({action_full_name: ad.insert_action, actorId: ad.id});
                                } else this.showDetail(e, rowData[ad.pk_index], {clickCatch: e.ctrlKey});
                            }}
                            title={this.ex.i18n.t("Open detail view on root URL context")}>↗</div>)}
                        header={<div className="l-span-clickable"
                                style={{position: "relative"}}
                                onClick={(e) =>  up[constants.URL_PARAM_SELECTED].forEach(
                                    pk => this.showDetail(e, pk, {clickCatch: true}))}
                                title={this.ex.i18n.t("Open all selected rows in new tabs")}>
                                <div>⎘</div>
                                <div style={{position: "absolute", fontSize: "1ch", right: "0px"}}>M</div>
                            </div>}
                        key={i} style={{width: '2em', textAlign: "center"}}/>
                    : <this.ex.prColumn.Column
                        body={this.columnTemplate(col)}
                        cellIndex={i}
                        className={`l-grid-col l-grid-col-${col.name}`}
                        col={col}
                        editor={this.columnEditor(col)}
                        field={String(col.fields_index)}
                        name={col.name}
                        header={() => {
                            let label = this.context.overridden_column_headers[col.name] || col.label;
                            const { APP } = this.props.urlParams.controller;
                            const chInPx = APP.URLContext.root.chInPx.offsetWidth;

                            return <span>
                                <span
                                    className="col-header-label"
                                    ref={ref => {
                                        if (ref && label && (ref.offsetWidth / chInPx) < label.length
                                            && col.value.short_header) {
                                            ref.innerHTML = col.value.short_header;
                                        }
                                    }}
                                    value={col.fields_index}>
                                    {label}
                                </span>
                                {Object.prototype.hasOwnProperty.call(col, 'filter') && <>
                                    <span>&nbsp;&nbsp;</span>
                                    {col.filter.type === 'boolean'
                                        ? <GridFilter style={{display: 'inline'}} col={col} ge={this}/>
                                        : <React.Fragment><this.ex.prButton.Button
                                            icon="pi pi-filter"
                                            onClick={e => {
                                                this.filterPanels[col.fields_index].toggle(e);
                                                e.stopPropagation();
                                            }}/>
                                            <this.ex.prOverlayPanel.OverlayPanel ref={ref => this.filterPanels[col.fields_index] = ref}>
                                                <GridFilter col={col} ge={this}/>
                                            </this.ex.prOverlayPanel.OverlayPanel></React.Fragment>}
                                </>}
                            </span>}}
                        headerStyle={{maxWidth: colWidth}}
                        id={col.fields_index.toString() + col.name}
                        key={i}
                        onBeforeCellEditHide={this.onBeforeEditorHide}
                        onBeforeCellEditShow={this.onBeforeEditorShow}
                        onCellEditCancel={this.onCancel}
                        onCellEditComplete={this.onCellEditComplete}
                        onCellEditInit={this.onEditorInit}
                        pt={passThrough}
                        sortable={col.sortable}
                        style={Object.assign({maxWidth: colWidth}, style)}/>
            }
        );
        this.setState({columns: columns});
    }

    showDetail(event, pk, status={}) {
        this.props.urlParams.controller.actionHandler.singleRow(
            event, pk, this.props.urlParams.controller.APP.URLContext, status);
    }

    rowReorder(event) {
        const c = this.props.urlParams.controller;
        const ad = c.static.actorData;
        const action = c.actionHandler.findUniqueAction('move_by_n');
        if (!action) return;
        c.actionHandler.runAction({
            actorId: ad.id,
            action_full_name: action.full_name,
            [constants.URL_PARAM_SELECTED]: [event.value[event.dropIndex][ad.pk_index]],
            status: {
                data: {
                    seqno: event.dropIndex - event.dragIndex,
                },
            },
        });
    }

    render() {
        if (!this.state.ready || !this.state.columns || !this.context.success) return null;
        let selectionMode = 'checkbox';
        let reorderableRows = true;
        if (this.props.urlParams.controller.static.actorData.table_as_calendar) {
            selectionMode = null;
            reorderableRows = false;
        }
        return <React.Fragment>
            <this.ex.prDataTable.DataTable
                emptyMessage={this.context.no_data_text}
                lazy={true}
                size="small"
                loading={this.state.loading}
                onColReorder={this.onColReorder}
                onRowDoubleClick={this.showDetail}
                onRowReorder={this.rowReorder}
                onSelectionChange={(e) => {
                    let sr = e.value.map(r => r[this.props.urlParams.controller.static.actorData.pk_index]);
                    this.props.urlParams.controller.history.replace({[constants.URL_PARAM_SELECTED]: sr});
                    this.props.parent.setState({loading: false});
                }}
                onSort={async ({sortField, sortOrder}) => {
                    const up = this.props.urlParams;
                    const c = up.controller;
                    const noOldSort = !c.filled(up[constants.URL_PARAM_SORT])
                    await c.history.replace({
                        [constants.URL_PARAM_SORT]: up.showableColumns
                            .get(parseInt(sortField)),
                        [constants.URL_PARAM_SORTDIR]:
                            sortOrder === 1 ? "ASC" : "DESC",
                        sortField: sortField,
                        sortOrder: sortOrder,
                    });
                    /**
                     * Reset columns on the first set sort.
                     * If sort is already set or some gridFilter is set,
                     * then, set_cols is already done and the rowReorder
                     * column is not visible (so, no need for doing set_cols).
                     */
                    if (up.rowReorder
                        && !c.filled(up[constants.URL_PARAM_FILTER])
                        && !c.actionHandler.getGridFilters().length
                        && (noOldSort || !c.filled(sortField))
                    ) this.set_cols();
                }}
                editMode="cell"
                paginator={false}
                ref={this.onTableRef}
                removableSort={true}
                reorderableColumns={true}
                reorderableRows={reorderableRows}
                resizableColumns={true}
                rowClassName={this.rowClassName}
                scrollable={true}
                scrollHeight={this.state.scrollHeight}
                selection={this.context.rows.filter(
                    rd => this.props.urlParams[constants.URL_PARAM_SELECTED].includes(rd[this.props.urlParams.controller.static.actorData.pk_index]))}
                selectionAutoFocus={false}
                selectionMode={selectionMode}
                sortField={this.props.urlParams.sortField}
                sortOrder={this.props.urlParams.sortOrder}
                stripedRows={true}
                value={this.context.rows}>
                {this.state.columns}
            </this.ex.prDataTable.DataTable>
        </React.Fragment>
    }
}
