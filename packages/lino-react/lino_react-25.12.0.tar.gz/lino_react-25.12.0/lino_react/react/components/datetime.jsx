export const name = "datetime";

import React from 'react';
import PropTypes from 'prop-types';
import * as constants from './constants';
import { LeafComponentInput } from "./LinoComponentUtils";
import { RegisterImportPool } from "./Base";

let ex; const exModulePromises = ex = {
    prCalendar: import(/* webpackChunkName: "prCalendar_datetime" */"primereact/calendar"),
};RegisterImportPool(ex);


class DTFieldElement extends LeafComponentInput {
    static requiredModules = ["prCalendar"].concat(LeafComponentInput.requiredModules);
    static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());
    constructor(props) {
        super(props);

        this.getLinoInput = this.getLinoInput.bind(this);
        this.getValue = this.getValue.bind(this);
        this.innerHTML = this.innerHTML.bind(this);
        this.isValid = this.isValid.bind(this);
        this.updateValue = this.updateValue.bind(this);
    }

    getLinoInput(fieldProps={}) {
        return <this.ex.prCalendar.Calendar
            {...fieldProps}
            className={"l-DateFieldElement"}
            inputMode={this.props.urlParams.controller.globals.isMobile ? 'numeric' : 'none'}
            inputStyle={{width: "100%"}}
            keepInvalid={true}
            onChange={(e) => this.updateValue(e)}
            onClearButtonClick={(e) => {e.value = null; this.updateValue(e)}}
            // TODO: check if https://github.com/primefaces/primereact/commit/16eafe5a171154da63bbfa9d83f84827e9d8363f#
            // is available on a packaged version
            // onSelect={(e) => this.updateValue(e)}
            ref={this.onInputRef}
            showButtonBar={true}
            showIcon={this.props[constants.URL_PARAM_WINDOW_TYPE] !== constants.WINDOW_TYPE_TABLE}
            showOnFocus={false}
            style={{width: "100%"}}
            tabIndex={this.props.tabIndex}
            value={this.getValue()}/>
    }

    getValue() {
        let v = super.getValue();
        if (!this.props.urlParams.controller.filled(v)) return null;
        return this.str2date(v);
    }

    innerHTML = () => (<div>{super.getValue() || "\u00a0"}</div>);

    isValid = (v) => (
        v === null || v instanceof Date || this.str2date(v) instanceof Date);

    updateValue(e) {
        let value = e.value;
        if (!this.props.urlParams.controller.filled(value)) value = null
        else if (value instanceof Date) value = this.date2str(value);

        this.container.classList.remove('dangling-modification');
        this.container.classList.remove('unsaved-modification');

        if (this.isValid(value)) {
            this.update({[this.dataKey]: value});
            this.setCellStyle(this.container, false);
        } else this.container.classList.add('dangling-modification');
    }
}


export class DateFieldElement extends DTFieldElement {
    constructor(props) {
        super(props);
        this.date2str = this.date2str.bind(this);
        this.getLinoInput = this.getLinoInput.bind(this);
        this.str2date = this.str2date.bind(this);
    }

    date2str(date) {
        return ("0" + date.getDate()).slice(-2) + "." +
            ("0" + (date.getMonth() + 1)).slice(-2) + "." +
            date.getFullYear();
    }

    getLinoInput = () => super.getLinoInput({
        dateFormat: "dd.mm.yy", yearNavigator: true, yearRange: "1900:2900"});

    str2date(value) {
        let parts = value.split(".");
        if (parts.length === 3 && !parts.includes("") && parts[2].length === 4)
            return new Date(parts[2], parts[1] - 1, parts[0]);
        return false;
    }
}


export class TimeFieldElement extends DTFieldElement {
    constructor(props) {
        super(props);
        this.date2str = this.date2str.bind(this);
        this.getLinoInput = this.getLinoInput.bind(this);
        this.str2date = this.str2date.bind(this);
    }

    date2str(date) {
        return ("0" + date.getHours()).slice(-2) + ":" +
            ("0" + date.getMinutes()).slice(-2);
    }

    getLinoInput = () => super.getLinoInput(
        {hourFormat: '24', showTime: true, timeOnly: true});

    str2date(timeStr) {
        let regex = /^(\d(?:\d(?=[.,:; ]?\d\d|[.,:; ]\d|$))?)?[.,:; ]?(\d{0,2})$/g;
        if (timeStr.match(regex)) {
            let m = regex.exec(timeStr),
                viewDate = new Date(),
                hours = m[1],
                min = m[2];
            viewDate.setHours(hours || 0);
            viewDate.setMinutes(min || 0);
            return viewDate;
        }
        return false;
    }
}


export class DateFilter extends DateFieldElement {
    static propTypes = {
        parent: PropTypes.object.isRequired,
    }

    static defaultProps = {
        editing_mode: true,
        hide_label: true,
    }

    constructor(props) {
        super(props);

        this.disabled = this.disabled.bind(this);
        this.filled = this.filled.bind(this);
        this.getValue = this.getValue.bind(this);
        this.update = this.update.bind(this);
    }

    filled = () => this.props.parent.context.controller.filled(this.props.value);
    disabled = () => false;
    getValue() {
        if (!this.filled()) return null;
        return this.str2date(this.props.parent.state.value);
    }
    update = (values) => this.props.parent.pushFilter({value: values[this.dataKey]});
}
