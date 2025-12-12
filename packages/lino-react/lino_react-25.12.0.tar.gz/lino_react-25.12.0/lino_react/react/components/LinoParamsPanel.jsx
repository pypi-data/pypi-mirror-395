export const name = "LinoParamsPanel";


import React from "react";
import * as constants from './constants';
import { RegisterImportPool, getExReady, URLContextType } from "./Base";

let ex; const exModulePromises = ex = {
    u: import(/* webpackChunkName: "LinoUtils_LinoParamsPanel" */"./LinoUtils"),
    lc: import(/* webpackChunkName: "LinoComponents_LinoParamsPanel" */"./LinoComponents"),
};RegisterImportPool(ex);


export function LinoParamsPanel(props) {
    const context = React.useContext(URLContextType);
    if (!context.controller.static.actorData.params_layout) return null;

    const localEx = getExReady(ex, ['u', 'lc']);
    return !localEx.ready ? null : <div
        hidden={!context.pvPVisible}
        className="l-params-panel l-header">
        <localEx.lc.LinoLayout
            editing_mode={true}
            window_layout={context.controller.static.actorData.params_layout}
            wt={constants.WINDOW_TYPE_PARAMS}/>
    </div>
}
