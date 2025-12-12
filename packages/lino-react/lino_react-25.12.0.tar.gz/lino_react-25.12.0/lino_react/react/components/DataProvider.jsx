export const name = "DataProvider";

import React from "react";
import PropTypes from "prop-types";
import * as constants from './constants';
import { RegisterImportPool, Component } from "./Base";

let ex; const exModulePromises = ex = {
    queryString: import(/* webpackChunkName: "queryString_DataProvider" */"query-string"),
    AbortController: import(/* webpackChunkName: "AbortController_DataProvider" */"abort-controller"),
    whatwgFetch: import(/* webpackChunkName: "whatwgFetch_DataProvider" */"whatwg-fetch"),
    prProgressSpinner: import(/* webpackChunkName: "prProgressSpinner_DataProvider" */"primereact/progressspinner"),
    lm: import(/* webpackChunkName: "LoadingMask_DataProvider" */"./LoadingMask"),
    i18n: import(/* webpackChunkName: "i18n_DataProvider" */"./i18n"),
}
RegisterImportPool(ex);


export class DataProvider extends Component {
    static requiredModules = [
        'queryString', "AbortController", "whatwgFetch", "prProgressSpinner",
        "lm", "i18n"]

    static iPool = ex;

    static propTypes = {
        endpoint: PropTypes.string.isRequired,
        render: PropTypes.func.isRequired,
        post_data: PropTypes.func,
        hideLoading: PropTypes.bool,
        useEverLoaded: PropTypes.bool,

    };
    static defaultProps = {
        post_data: (data) => (data),
        hideLoading: false,
        useEverLoaded: false,
    };

    async prepare() {
        await super.prepare();
        this.ex.i18n = this.ex.i18n.default;
    }

    constructor() {
        super();
        this.state = {
            ...this.state,
            data: [],
            loaded: false,
            placeholder: "Loading...",
            actorID: null,
        };
        this.reloadData = this.reloadData.bind(this);
        this.reload = this.reloadData;
        this.update = this.reloadData;
    }

    onReady() {
        this.controller = new this.ex.AbortController.default();
        this.reloadData();
    }

    componentWillUnmount() {
        this.controller.abort();
        delete window.App.URLContext.globals.panels[this.state.actorID];
    }

    liveUpdate = (params) => this.update();

    reloadData() {
        this.setState({loaded: false});
        let query = {fmt: "json"}
        window.App.URLContext.actionHandler.commonParams(query);
        this.ex.whatwgFetch.fetch(this.props.endpoint + `?${this.ex.queryString.default.stringify(query)}`, {
            signal: this.controller.signal})
            .then(response => {
                if (response.status !== 200) {
                    this.setState({placeholder: this.ex.i18n.t("Something went wrong")});
                    return {status:response.status$} //
                }
                return response.json();
            })
            .then(data => {
                this.props.post_data(data);
                this.setState({data: data, loaded: true,
                    everloaded: true, actorID: data.actorID});
                window.App.URLContext.globals.panels[data.actorID] = this;
            }).catch(function(ex) {
              if (ex.name === 'AbortError') {
                console.log('request aborted', ex)
              }
            })
    };

    render() {
        if (!this.state.ready) return null;
        const {data, loaded, placeholder, everloaded} = this.state;
        const {render} = this.props;
        // const Comp = "Table";
        // return loaded ? this.props.render(data, Comp) : <p>{placeholder}</p>;
        if (everloaded && !loaded) {
            // is loading with data, use loading mask
            return <this.ex.lm.LoadingMask mask={true}>
                {render(data)}
            </this.ex.lm.LoadingMask>
        }
        else {
            return <this.ex.lm.LoadingMask mask={false}>
                {loaded || everloaded && this.props.useEverLoaded
                    ? render(data) : this.props.hideLoading ? <div/> : <this.ex.prProgressSpinner.ProgressSpinner/>}
            </this.ex.lm.LoadingMask>
        }
    }
}
