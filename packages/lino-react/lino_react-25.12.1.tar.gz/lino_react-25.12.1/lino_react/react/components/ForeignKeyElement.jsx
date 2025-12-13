export const name = "ForeignKeyElement";

import React from 'react';
import PropTypes from 'prop-types';

import { RegisterImportPool } from "./Base";
import { AutoComplete } from "./AutoComplete";
import * as constants from "./constants";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    _: import(/* webpackChunkName: "lodash_ForeignKeyElement" */"lodash"),
};RegisterImportPool(ex);


export class ForeignKeyElement extends AutoComplete {
    static requiredModules = ["_"].concat(AutoComplete.requiredModules);
    static iPool = Object.assign(ex, AutoComplete.iPool.copy());

    static propTypes = {
        ...AutoComplete.propTypes,
        simple: PropTypes.bool,
        link: PropTypes.bool,
    };
    static defaultProps = {
        ...AutoComplete.defaultProps,
        simple: false,
        link: true,
    };

    async prepare() {
        await super.prepare();
        this.ex._ = this.ex._.default;
    }

    constructor(props) {
        super(props);
        this.wrapperClasses.push("l-ForeignKeyElement");

        this.state = {
            ...this.state,
            currentValue: null,
        }

        this.dataKeyHidden = props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE
            ? props.elem.fields_index_hidden
            : props.elem.name + "Hidden";

        this.hasClearButton = false;

        this.getSnapshotBeforeUpdate = this.getSnapshotBeforeUpdate.bind(this);
        this.componentDidUpdate = this.componentDidUpdate.bind(this);

        this.choicesURL = this.choicesURL.bind(this);
        this.getLinoInput = this.getLinoInput.bind(this);
        this.getValue = this.getValue.bind(this);
        this.innerHTML = this.innerHTML.bind(this);
        this.OnExternalLinkClick = this.OnExternalLinkClick.bind(this);
        this.onSelect = this.onSelect.bind(this);
        this.clear = this.clear.bind(this);
    }

    onReady() {
        this.setState({currentValue: this.getValue()});
        super.onReady();
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    getSnapshotBeforeUpdate(_prevProps, _prevState) {
        if (!this.state.ready) return {};
        let contextValue = this.getValue()
        if (!this.ex._.isEqual(contextValue, this.state.currentValue))
            return {contextUpdate: contextValue};
        return {};
    }

    componentDidUpdate(_prevProps, _prevState, snapshot) {
        if (snapshot.contextUpdate)
            this.setState({value: {...snapshot.contextUpdate},
                currentValue: snapshot.contextUpdate});
    }

    choicesURL(query, start, limit) {
        let uc = this.props.urlParams;
        let actorData = uc.controller.static.actorData,
            // context_fields = actorData.choosers_dict && actorData.choosers_dict[this.props.elem.name],
            context_fields = this.props.choosers_dict && this.props.choosers_dict[this.props.elem.name],
            dataParams = {query: query};
        if (context_fields) {
            context_fields.forEach((cf) => {
                if (this.props[constants.URL_PARAM_WINDOW_TYPE] !== constants.WINDOW_TYPE_TABLE) {
                    let cf_value = this.getValueByName(cf + "Hidden");
                    if (cf_value === undefined) cf_value = this.getValueByName(cf);
                    dataParams[cf] = cf_value;
                } else {
                    const pk = this.context.rows[this.props.column.rowIndex][actorData.pk_index];
                    if (pk !== null) { // Avoid putting context field value when the row is phantom row.
                        let col = actorData.col.find(c => c.name === cf);
                        // TODO: what happens when a col is not found.
                        if (col) dataParams[cf] = this.getValueByName(
                            col.fields_index_hidden || col.fields_index);
                    }
                }
            });
        }
        let aH = uc.controller.actionHandler;
        let finalSlug = "";
        if (uc.action_full_name) {
            const { action } = aH.getAction(uc.action_full_name, false)
            if (action.has_parameters) finalSlug = `/${action[constants.URL_PARAM_ACTION_NAME]}`;
        }
        return `choices/${uc.packId}/${uc.actorId}/${this.props.elem.name}${finalSlug}?${
            aH.parser.stringify(
                Object.assign(aH.commonParams(), {
                    ...dataParams,
                    [constants.URL_PARAM_START]: start,
                    [constants.URL_PARAM_LIMIT]: limit}))}`;
    }

    getLinoInput() {
        return super.getLinoInput({onClear: this.clear});
    }

    getValue() {
        return {text: super.getValue(),
            value: this.getValueByName(this.dataKeyHidden)}
    }

    OnExternalLinkClick(e) {
        let related_actor_id = this.props.elem.field_options.related_actor_id;
        e.stopPropagation();
        let c = this.props.urlParams.controller;
        c.APP.URLContext.history.pushPath({
            pathname: `/api/${related_actor_id.split(".").join("/")}/${
                this.getValueByName(this.dataKeyHidden)}`,
            params: c.actionHandler.defaultStaticParams(),
        });
    };

    onSelect(e) {
        this.setState({value: e.value});
        this.update({[this.dataKey]: e.value.text,
            [this.dataKeyHidden]: e.value.value});
    }

    clear() {
        this.update({[this.dataKey]: "", [this.dataKeyHidden]: null});
        this.setState({value: {text: "", value: null},
            [constants.URL_PARAM_FILTER]: ""});
    }

    innerHTML() {
        if (this.state.value === null) return null;
        return <React.Fragment>
            {this.state.value.text && this.props.link && this.props.elem.field_options.view_permission &&
                <div
                    className="l-span-clickable"
                    ref={el => {
                        if (el) el.onclick = this.OnExternalLinkClick;
                    }}
                >↗&nbsp;</div>}
            <div style={{whiteSpace: "nowrap", width: "100%"}}>{this.state.value.text || "\u00a0"}</div>
        </React.Fragment>
    }
}
