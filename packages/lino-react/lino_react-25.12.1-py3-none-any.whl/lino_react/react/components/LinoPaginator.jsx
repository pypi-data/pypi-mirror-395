export const name = "LinoPaginator";

import React from "react";
import * as constants from './constants';
import { RegisterImportPool, Component, URLContextType } from "./Base";

let ex; const exModulePromises = ex = {
    prButton: import(/* webpackChunkName: "prButton_LinoPaginator" */"primereact/button"),
    prDropDown: import(/* webpackChunkName: "prDropDown_LinoPaginator" */"primereact/dropdown"),
    prPaginator: import(/* webpackChunkName: "prPaginator_LinoPaginator" */"primereact/paginator"),
    prInputNumber: import(/* webpackChunkName: "prInputNumber_LinoPaginator" */"primereact/inputnumber"),
    u: import(/* webpackChunkName: "LinoUtils_LinoPaginator" */"./LinoUtils"),
    i18n: import(/* webpackChunkName: "i18n_LinoPaginator" */"./i18n"),
}
RegisterImportPool(ex);


export class LinoPaginator extends Component {
    static requiredModules = ["prButton", "prDropDown", "prPaginator", "u", "i18n", "prInputNumber"];
    static iPool = ex;
    static contextType = URLContextType;

    async prepare() {
        await super.prepare();
        this.ex.i18n = this.ex.i18n.default;
    }

    constructor(props, context) {
        super(props);
        this.state = { ...this.state };

    }

    render() {
        if (!this.state.ready) return null;
        let c = this.context.controller,
            ad = c.static.actorData,
            ttl = c.dataContext.mutableContext.count;
        if (ad.preview_limit === 0 || ttl === 0 ||
            ttl === undefined || ad.simple_paginator
        ) return null;
        const { mutableContext } = c.dataContext;
        const count = mutableContext.rows.length;
        const lmt = this.context[constants.URL_PARAM_LIMIT];
        // const lmt = ad.preview_limit;
        // console.log("20240919 LinoPaginator", ad, ttl, lmt, this.context);
        return <div ref={el => this.container = el}><this.ex.prPaginator.Paginator
            alwaysShow={false}
            first={mutableContext.offset || this.context[constants.URL_PARAM_START] || 0}
            rows={lmt}
            totalRecords={ttl}
            template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown CurrentPageReport JumpToPageInput"
            onPageChange={(e) => {
              {/* console.log("20240919 Hello", e); */}
              this.context.controller.history.replace({
                [constants.URL_PARAM_START]: e.page * lmt,
                [constants.URL_PARAM_LIMIT]: e.rows});
            }}
            ref={el => this.pg = el}
            rowsPerPageOptions={[5, 10, 15, 20, 30, 50, 100]}
            rightContent={
                ttl && <span
                    className={"l-grid-count"}
                    onKeyDown={e => {
                        if (['Home', 'End', 'Delete'].includes(e.code))
                            e.stopPropagation()}}>
                    {ttl}{this.ex.i18n.t(" rows")}
                </span>
            }
        /></div>
    }
}
