export const name = "AppTopbar";

import "./AppTopBar.css";

import React from "react";
import PropTypes from "prop-types";
import { RegisterImportPool, Component } from "./Base";
import { AppInlineProfile } from "./AppInlineProfile";

let ex; const exModulePromises = ex = {
    classNames: import(/* webpackChunkName: "classNames_AppTopbar" */"classnames"),
};RegisterImportPool(ex);


export class AppTopbar extends Component {
    static requiredModules = ["classNames"];
    static iPool = ex;

    static defaultProps = {
        onToggleMenu: null,
        unseenCount: 0,
    };

    static propTypes = {
        onToggleMenu: PropTypes.func.isRequired,
        URLContext: PropTypes.object.isRequired,
        useChat: PropTypes.bool,
        WS: PropTypes.bool,
        unseenCount: PropTypes.number,
    };

    constructor(props){
        super(props);
        const { URLContext } = props;
        this.state = {profile: URLContext.APP.state.site_data.no_user_model
            ? null : <AppInlineProfile URLContext={URLContext}/>,
            links: "\u00a0"}
        URLContext.actionHandler.reloadables["AppTopBar"] = this;
        this.upController = URLContext;
        this.onReady = this.onReady.bind(this);
    }

    onReady() {
        setTimeout(this.upController.APP.handleZoom, 1000);
        this.getTopLinks();
    }

    componentWillUnmount() {
        delete this.props.URLContext.actionHandler.reloadables["AppTopBar"];
    }

    reload() {
        this.getTopLinks();
    }

    getTopLinks() {
        const { URLContext } = this.props;
        URLContext.actionHandler.handledFetch({path: "api/top_links",
            silent: true, response_callback: (data) => {
                console.log("top_links", data);
                this.setState(data);
            }});
    }

    render() {
        if (!this.state.ready) return null;
        // let titleClassName = "l-site-title ";
        const { APP } = this.upController;
        // if (APP.data.themeName === 'whitewall') titleClassName += "l-whitewall-site-title "
        return (
            <div ref={el => APP.tbContainer = el} className="layout-topbar clearfix">
                <a className="layout-menu-button" onClick={this.props.onToggleMenu}>
                    <span className="pi pi-bars"/>
                </a>
                <a className="layout-home-button" onClick={event => {
                    // onHomeButton [oldname]
                    if (event.ctrlKey) window.open('/')
                    else if (APP.location.pathname !== "/")
                        this.upController.history.pushPath({pathname: "/"})
                    else {
                        if (APP.dashboard) APP.dashboard.reloadData()
                        else this.upController.actionHandler.reload();
                    }
                }}>
                    <span className="pi pi-home"/>
                </a>
                {APP.state.site_data.editing_frontend &&
                    <a className="layout-home-button"
                    onClick={(e) => {
                        let target = "_self";
                        if (e.ctrlKey) {
                            target = "_blank";
                        }
                        window.open(location.origin, target);
                    }}>
                    <span className="pi pi-globe"/>
                </a>}
                <div className="layout-topbar-icons" style={{display: "inline"}}>
                    {this.state.profile}
                </div>
                <div id="l-top-links" style={{
                        display: "inline", float: "right", marginRight: "10px"}}
                    dangerouslySetInnerHTML={{__html: this.state.links}}/>
            </div>
        );
    }
}
