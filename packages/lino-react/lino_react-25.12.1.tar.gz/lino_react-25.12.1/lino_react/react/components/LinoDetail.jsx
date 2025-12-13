export const name = "LinoDetail";

import React from "react";
import PropTypes from "prop-types";
import * as constants from './constants';
import { RegisterImportPool, Component, DataContextType } from "./Base";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    lc: import(/* webpackChunkName: "LinoComponents_LinoDetail" */"./LinoComponents"),
    u: import(/* webpackChunkName: "LinoUtils_LinoDetail" */"./LinoUtils"),
}
RegisterImportPool(ex);


export class LinoDetail extends Component {
    static requiredModules = ['lc', 'u'];
    static iPool = ex;

    static contextType = DataContextType;

    static propTypes = {
        editing_mode: PropTypes.bool,
        window_layout: PropTypes.string,
        urlParams: PropTypes.object.isRequired,
    };
    static defaultProps = {
        editing_mode: false,
    };

    constructor(props) {
        super(props);

        this.navigate = this.navigate.bind(this);
        this.onKeyDown = this.onKeyDown.bind(this);
    }

    onReady() {
        window.addEventListener('keydown', this.onKeyDown);
    }

    componentWillUnmount() {
        if (this.state.ready) window.removeEventListener('keydown', this.onKeyDown);
        const c = this.props.urlParams.controller;
        if (c.APP.URLContext === c) {
            Object.assign(c.globals, {
                currentInputWindowType: constants.WINDOW_TYPE_UNKNOWN,
                currentInputIndex: 0,
                currentInputAHRefName: c.actionHandler.refName,
            });
        }
    }

    navigate = (which) => {
        let navinfo = this.context.navinfo;
        if (navinfo) {
            let uc = this.props.urlParams, c = uc.controller,
                path = `/api/${uc.packId}/${uc.actorId}`, pk = navinfo[which],
                rs = uc.detailNav.get(pk);

            if (rs && c.history.has(rs))
                c.history.push({params: c.history.getState(rs), actorData: c.static.actorData})
            else {
                rs = c.newSlug();
                uc.detailNav.set(pk, rs);
                c.history.pushPath({
                    pathname: `${path}/${pk}`,
                    params: Object.assign(c.actionHandler.getParams(), {
                        rs: rs, tab: uc.tab})
                });
            }
        }
    }

    onKeyDown(event) {
        const stopPrevent = () => {
            event.preventDefault();event.stopPropagation()}
        if ((event.ctrlKey || event.metaKey) && event.code === "KeyS") {
            stopPrevent();
            let uc = this.props.urlParams
            if (uc.editing_mode) {
                if (uc.controller.dataContext.isModified()) {
                    // document.activeElement.blur();
                    uc.controller.actionHandler.submit({});
                } else uc.controller.history.replaceState({editing_mode: false});
            } else uc.controller.history.replaceState({editing_mode: true});
        } else
        if (["PageUp", "PageDown", "End", "Home"].includes(event.code)
            && (document.activeElement.value === ""
                || document.activeElement.value === undefined)) {
            stopPrevent();
            let navinfo = this.context.navinfo, navigate = this.navigate;
            if (!navinfo) return;
            if (event.code === "PageUp" && navinfo.prev) navigate('prev')
            else if (event.code === "PageDown" && navinfo.next) navigate('next')
            else if (event.code === "End" && navinfo.next) navigate('last')
            else if (event.code === "Home" && navinfo.prev) navigate('first');
        }
    }

    render() {
        if (!this.state.ready) return null;
        return <this.ex.lc.LinoLayout
            window_layout={this.props.window_layout}
            wt={constants.WINDOW_TYPE_DETAIL}/>
    }
}
