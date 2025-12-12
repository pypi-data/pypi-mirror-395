export const name = "LinoUtils";

import * as constants from "./constants";

let exModules;

export function pushExternalModules(modules) {
    exModules = modules;
}


// Checks if a number is NaN && NaN is the only JavaScript entity that is not equal to itself.
export const isNaN = (variable => variable !== variable);

// simple test to check if running on a mobile or not.
export function isMobile() {
    return window.matchMedia("only screen and (max-width: 760px)").matches;
}


export function getNextToolbarState(current_state) {
    let next_item_index = constants.TOOLBAR_STATES_ORDER.indexOf(current_state) + 1;
    if (next_item_index == constants.TOOLBAR_STATES_ORDER.length)
        return constants.TOOLBAR_STATES_ORDER[0];
    return constants.TOOLBAR_STATES_ORDER[next_item_index];
}


export function fillParamDefaults(params, actorData) {
    if (!(constants.URL_PARAM_LIMIT in params)) {
        Object.assign(params, {
            [constants.URL_PARAM_LIMIT]: (actorData.preview_limit === 0)
                ? 99999 : actorData.preview_limit
        })
    }
    // if (!(constants.URL_PARAM_START in params))
    //     Object.assign(params, {[constants.URL_PARAM_START]: 0});
    return params;
}


export function getDisplayMode(actorData, availableWidth) {
    let dm = undefined, displayRules = actorData.default_display_modes;
    if (displayRules) {
      for (var i = 0; i < displayRules.length; i++) {
        let item = displayRules[i];
        let w = item[0];
        if (w != null) {
            if (w > availableWidth) {
                dm = item[1];
                break;
            }
        } else {
            dm = item[1];
        }
      }
    }
    return dm;
}


// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds.
export function debounce(func, timeout=300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => {func.apply(this, args)}, timeout);
    }
};


export function toggleEditingMode(context) {
    const c = context.controller, toggle = () => c.history.replaceState({
        editing_mode: !context.editing_mode});
    if (!context.editing_mode) toggle()
    else if (!c.isModified()) toggle()
    else c.actionHandler.discardModDConfirm({agree: toggle});
}


export function setRpRefFactory(rpStore) {
    return function (el, manual_rp) {
        let rp;
        if (el) {
            rp = manual_rp === undefined ? exModules.weakKey.default(el) : manual_rp;
            rpStore[rp] = el;
            el.rp = rp;
        }
        Object.keys(rpStore).forEach(rp => {
            if (rpStore[rp] === null) {
                delete rpStore[rp]
            }
        });
    }
}


/**
 *
 * @param obj: obj of pvkey:val pairs
 * @param params_fields: actor's list of pv fields in the correct order, found in sitedata.actors.[actorID].params_fields
 * @returns Array of PVs for url inputing.
 */
export function pvObj2array(obj, params_fields) {
    // this.state.params_values is used in this method
    let fields = Object.keys(obj);
    return params_fields.map((f_name) => {
        // Only give hidden value if the key is in params_values.
        // Previously used || assignement, which caused FK filter values being sent as PVs
        let value;
        if (fields.includes(f_name + "Hidden")) value = obj[f_name + "Hidden"];
        else value = obj[f_name];

        if (value === undefined) value = null;
        return value
    })
}

export function getSiteDataKey(URLContext, userSettings) {
    let {user_type, site_lang, site_name, su_user_type} = userSettings;
    return `ActorData_${su_user_type || user_type}_${URLContext.value[constants.URL_PARAM_USER_LANGUAGE] || site_lang}_${site_name}`;
}
