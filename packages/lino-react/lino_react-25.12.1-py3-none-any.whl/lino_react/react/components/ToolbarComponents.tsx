import * as t from "./types";
import * as constants from "./constants";
import React from "react";
import { URLContextType, RegisterImportPool, getExReady } from "./Base";
import type { ImportPool } from "./Base";

let ex: ImportPool;
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const exModulePromises = ex = {
    prButton: import(/* webpackChunkName: "prButton_ToolbarComponents" */"primereact/button"),
    i18n: import(/* webpackChunkName: "i18n_ToolbarComponents" */"./i18n"),
};RegisterImportPool(ex);


export function ParamsPanelControl() {
    const context: t.NavigationContextValue = React.useContext(URLContextType);
    const c: t.NavigationContext = context.controller;
    const localEx = getExReady(ex, ["prButton", "i18n"], (mods) => {
        mods.i18n = mods.i18n.default;
    });
    return !localEx.ready ? null : c.static.actorData.params_layout
        && (c.contextType == constants.CONTEXT_TYPE_MULTI_ROW
            // || (c.static.actorData.enable_slave_params
            //     && c.contextType === constants.CONTEXT_TYPE_SLAVE_GRID
            // )
        )
        && c.APP.state.site_data.data_exporter
        && <React.Fragment>
        <localEx.prButton.Button
            className="l-button-pv_control"
            icon="pi pi-sliders-h"
            onClick={() => {
                c.history.replace(
                    {pvPVisible: !context.pvPVisible});
            }}
            tooltip={context.pvPVisible ?
                localEx.i18n.t("Hide parameters panel") :
                localEx.i18n.t("Show parameters panel")}
            tooltipOptions={{position : "bottom"}}/>
        {Object.keys(context[constants.URL_PARAM_PARAM_VALUES] || {}).length !== 0 && <localEx.prButton.Button
            icon={"pi pi-times-circle"}
            onClick={() => {
                c.dataContext.updateState({param_values: {
                    ...c.dataContext.contextBackup.param_values}});
                c.history.replace({pv: []});
            }}
            tooltip={localEx.i18n.t("Clear and set the parameter values to default")}
            tooltipOptions={{position: "bottom"}}/>
        }
    </React.Fragment>
}
