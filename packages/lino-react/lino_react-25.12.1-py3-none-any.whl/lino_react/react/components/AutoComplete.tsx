export const name: string = "AutoComplete";
import * as t from './types';

import React from "react";
import PropTypes from "prop-types";
import { RegisterImportPool, ImportPool } from "./Base";
import { LeafComponentInput } from "./LinoComponentUtils";
import * as constants from "./constants";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex: ImportPool; const exModulePromises = ex = {
    queryString: import(/* webpackChunkName: "queryString_AutoComplete" */"query-string"),
    prAutoComplete: import(/* webpackChunkName: "prAutoComplete_AutoComplete" */"primereact/autocomplete"),
    AbortController: import(/* webpackChunkName: "AbortController_AutoComplete" */"abort-controller"),
    i18n: import(/* webpackChunkName: "i18n_AutoComplete" */"./i18n"),
    u: import(/* webpackChunkName: "LinoUtils_AutoComplete" */"./LinoUtils"),
};RegisterImportPool(ex);


export class AutoComplete extends LeafComponentInput {
    static requiredModules = ['prAutoComplete', "AbortController"].concat(LeafComponentInput.requiredModules);
    static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());

    hasClearButton: boolean;
    clear?: () => void;
    props: t.LeafInputProps;
    choicesURL?(query: string, start: number, limit: number): string;
    clearButton?: HTMLElement | null;
    onSelect?(e: { value: { text: string; value: string | number | null } }): void;
    scroller: { getElementRef: () => React.RefObject<HTMLElement> } | null;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    controller: any;
    state: t.ObjectAny & {textSelected: boolean;};

    constructor(props: t.LeafInputProps) {
        super(props);
        this.state = {
            ...this.state,
            count: 999,
            [constants.URL_PARAM_FILTER]: "",
            [constants.URL_PARAM_LIMIT]: 15,
            [constants.URL_PARAM_START]: 0,
            lazyLoading: false,
            rows: [],
            value: null,
        }

        this.hasClearButton = false;

        this.getChoices = this.getChoices.bind(this);
        this.getLinoInput = this.getLinoInput.bind(this);
        this.itemTemplate = this.itemTemplate.bind(this);
        this.onKeyDown = this.onKeyDown.bind(this);
    }

    onReady() {
        if (this.hasClearButton && !this.clear) throw Error("clear NotImplemented");
        const v = this.getValue();
        this.setState({
            [constants.URL_PARAM_FILTER]: v.text,
            [constants.URL_PARAM_LIMIT]: this.props.urlParams[
                constants.URL_PARAM_LIMIT],
            value: v,
        });
        this.controller = new this.ex.AbortController.default();
    }

    onKeyDown = (event) => {
        super.onKeyDown(event);
        if (["Enter", "NumpadEnter"].includes(event.code) && this.inputEl.getOverlay())
            event.stopPropagation();
        if (['ArrowDown', 'ArrowUp'].includes(event.code)) {
            if (this.inputEl && !this.inputEl.getOverlay()) {
                if (!this.state.rows.length) this.getChoices(this.state[constants.URL_PARAM_FILTER]);
                this.inputEl.show();
            } else if (!this.state.lazyLoading) {
                const sItem = this.scroller.getElementRef().current.querySelector('li.p-highlight');
                if (sItem) {
                    const {top, bottom} = this.scroller.getElementRef().current.getBoundingClientRect();
                    const sItemRect = sItem.getBoundingClientRect();

                    if (sItemRect.top < top) sItem.scrollIntoView(true)
                    else if (sItemRect.bottom > bottom) sItem.scrollIntoView(false);
                }
            }
            event.stopPropagation();
        }
    }

    itemTemplate = (item) => {
        const i = typeof item === "object" ? item.text : item;
        return <div>{i || "\u00a0"}</div>
    }

    getChoices = (query: string, limit?: number) => {
        this.controller.abort();
        this.controller = new this.ex.AbortController.default();
        limit = limit || this.state[constants.URL_PARAM_LIMIT];
        const start = limit === this.state[constants.URL_PARAM_LIMIT]
            ? this.state[constants.URL_PARAM_START]
            : this.state[constants.URL_PARAM_LIMIT];
        this.upController.actionHandler.silentFetch({
            path: this.choicesURL(query, start, limit),
            signal: this.controller.signal
        }).then((data) => {
            let rows = data.rows;
            if (this.state.rows.length) {
                rows = rows.filter(row => row.text !== "" && row.value !== null);
            }
            rows = this.state.rows.concat(rows);

            /**
             * In case of a learing combo set the non-existent query
             * as the value (which creates a new database record on
             *               the server against the value)
             */
            if ((this.props.elem.field_options || {}).allowCreate) {
                if (rows.filter(row => row.text == query).length === 0)
                    rows.unshift({text: query, value: query});
            }

            this.setState({
                [constants.URL_PARAM_FILTER]: query,
                [constants.URL_PARAM_LIMIT]: limit,
                count: data.count, lazyLoading: false,
                rows: rows,
            });
        });
    }

    getLinoInput(customProps = {}) {
        if (this.state.value === null) return null;
        return <React.Fragment><this.ex.prAutoComplete.AutoComplete
            completeMethod={(e) => {
                if (e.originalEvent.type === 'click' && this.state.rows.length) {
                    this.inputEl.show();
                    return;
                }
                this.state.rows = [];
                this.getChoices(e.query, this.state[constants.URL_PARAM_LIMIT]);
            }}
            dropdown={true}
            field="text"
            itemTemplate={this.itemTemplate}
            onChange={e => this.setState({
                value: Object.assign(this.state.value, {
                    text: e.value, value: null}),
                rows: [],
                [constants.URL_PARAM_LIMIT]: this.props.urlParams[
                    constants.URL_PARAM_LIMIT],
            })}
            onSelect={this.onSelect}
            onShow={() => {
                if (this.clearButton) {
                    this.clearButton.style.visibility = 'hidden'
                }
            }}
            ref={this.onInputRef}
            scrollHeight="200px"
            suggestions={this.state.rows}
            tabIndex={this.props.tabIndex}
            value={this.state.value.text}
            virtualScrollerOptions={{
                itemSize: 35,
                lazy: true,
                loading: this.state.lazyLoading,
                onScrollIndexChange: (event) => {
                    const l = this.state[constants.URL_PARAM_LIMIT];
                    if (l - event.first < 15 && !this.state.lazyLoading
                        && this.state.count > l
                    ) {
                        this.setState({lazyLoading: true});
                        this.getChoices(
                            this.state[constants.URL_PARAM_FILTER], l + 15);
                    }
                },
                ref: el => this.scroller = el,
                scrollHeight: "195px",
                style: {minWidth: '30ch'},
            }}
            {...customProps}/>
            {this.hasClearButton && this.props.elem.field_options.allowBlank
                && this.state.value.text
                && <i key={this.state.touch} ref={el => this.clearButton = el}
                className={"pi pi-times l-fk-clear"}
                onClick={this.clear}
                style={{visibility: 'visible', cursor: "pointer"}}/>}
        </React.Fragment>
    }
}

type QuickFilterProps = t.LeafInputProps & {
    wide: boolean;
}

export class QuickFilter extends AutoComplete {
    static requiredModules = ['queryString', "i18n", "u"].concat(AutoComplete.requiredModules);

    static propTypes = {
        ...AutoComplete.propTypes,
        wide: PropTypes.bool,
    }

    static defaultProps = {
        ...AutoComplete.defaultProps,
        editing_mode: true,
        elem: {},
        tabIndex: 0,
        wide: false,
        [constants.URL_PARAM_WINDOW_TYPE]: constants.WINDOW_TYPE_UNKNOWN,
        leafIndex: 0,
    }

    props: QuickFilterProps;
    focusSet: boolean = false;

    async prepare() {
        await super.prepare();
        this.ex.i18n = this.ex.i18n.default;
        this.focus = this.ex.u.debounce(this.focus.bind(this), 200);
    }

    constructor(props: QuickFilterProps) {
        super(props);
        this.wrapperClasses = ["l-grid-quickfilter"];
        this.styleClasses = [];

        this.choicesURL = this.choicesURL.bind(this);
        this.getLinoInput = this.getLinoInput.bind(this);
        this.getValue = this.getValue.bind(this);
        this.onSelect = this.onSelect.bind(this);
    }

    getLinoInput() {
        return super.getLinoInput({
            placeholder: this.ex.i18n.t("Quick search"),
            style: {
                width: this.props.wide ? "100%" : undefined,
                marginRight: this.props.wide ? "1ch" : undefined,
                marginLeft: this.props.wide ? "1ch" : undefined,
            }
        })
    }

    getValue() {
        return {text: this.props.urlParams[constants.URL_PARAM_FILTER],
            value: null}
    }

    choicesURL(query, start, limit) {
        return `choices/${this.props.urlParams.packId}/${this.props.urlParams.actorId}?${
            this.ex.queryString.default.stringify(Object.assign(this.upController
                .actionHandler.defaultStaticParams(), {
                    [constants.URL_PARAM_FILTER]: query,
                    [constants.URL_PARAM_START]: start,
                    [constants.URL_PARAM_LIMIT]: limit
                }))}`;
    }

    focus() {
        if (!this.focusSet) {
            this.focusSet = true;
            super.focus();
        }
    }

    onSelect(event) {
        const pk = event.value.value,
            c = this.upController;
        c.history.pushPath({
            pathname: `/api/${this.props.urlParams.packId}/${this.props.urlParams.actorId}/${pk}`,
            params: c.actionHandler.defaultStaticParams(),
        });
    }

    render() {
        if (!this.state.ready) return null;
        return this.getLinoInput();
    }
}
