export const name = "DashboardItems";

import React from "react";
import PropTypes from "prop-types";
import { RegisterImportPool, Component } from "./Base";

let ex; const exModulePromises = ex = {
    lm: import(/* webpackChunkName: "LoadingMask_DashboardItems" */"./LoadingMask"),
    prButton: import(/* webpackChunkName: "prButton_DashboardItems" */"primereact/button"),
    queryString: import(/* webpackChunkName: "queryString_DashboardItems" */"query-string"),
};RegisterImportPool(ex);


class DashboardItem extends Component {
    static requiredModules = ['lm', 'queryString', 'prButton'];
    static iPool = ex;

    static propTypes = {
        itemIndex: (props, ...args) => {
            if (!props.dashboardMain) return PropTypes.number.isRequired(props, ...args);
        },
        dashboardMain: PropTypes.bool.isRequired,
        APP: PropTypes.object.isRequired
    }
    static defaultProps = {
        dashboardMain: false
    }
    async prepare() {
        super.prepare();
        this.ex.queryString = this.ex.queryString.default;
    }
    constructor(props) {
        super(props);
        this.state = {...this.state, data: null, mask: true, actorID: null}
        this.reload = this.reloadData;
    }

    onReady() {
        this.reloadData();
    }

    liveUpdate = (params) => this.reload();

    /**
    * @param {bool} selfInit self-initiated reload through the refresh button
    */
    reloadData = (selfInit) => {
        this.setState({mask: true});
        const query = {fmt: 'json'}, { APP } = this.props,
            { actionHandler } = APP.URLContext;
        actionHandler.commonParams(query);
        const path = this.props.dashboardMain ? 'api/main_html' : `dashboard/${this.props.itemIndex}`;
        actionHandler.silentFetch({
            path: `${path}?${this.ex.queryString.stringify(query)}`,
            signal: actionHandler.abortController.signal
        }).then((data) => {
            if (data.version_mismatch && (this.props.itemIndex === 0 || selfInit)) {
                APP.reload();
                return;
            }
            this.setState({data: data.html, mask: false, actorID: data.actorID});
        })
    }

    render() {
        if (!this.state.ready) return null;
        const {data} = this.state;
        if (!this.props.APP.URLContext.filled(data)) return null;
        return <this.ex.lm.LoadingMask mask={this.state.mask}>
            {!this.props.dashboardMain && <this.ex.prButton.Button
                icon="pi pi-refresh" style={{float: 'right'}}
                onClick={(e) => {
                    this.reloadData(true);
                }}/>}
            <div dangerouslySetInnerHTML={{__html: data}}/>
        </this.ex.lm.LoadingMask>
    }
}


export class DashboardItems extends Component {
    static propTypes = {
        APP: PropTypes.object.isRequired
    };
    constructor(props) {
        super(props);
        this.state = {
            ...this.state,
            items: Array((props.APP.state.user_settings.dashboard_items || 0) + 1)
        };
        this.reloadData = this.reload;
    }

    reload() {
        this.props.APP.URLContext.actionHandler.clearRequestPool();
        this.state.items.forEach((item, i) => {
            item.reload()
        });
    }

    render() {
        if (!this.state.ready) return null;
        return <div>
            {[...this.state.items.keys()].map(i =>
                <DashboardItem
                    dashboardMain={i === 0} itemIndex={i - 1} APP={this.props.APP}
                    key={i} ref={ref => this.state.items[i] = ref}/>
            )}
        </div>
    }
}
