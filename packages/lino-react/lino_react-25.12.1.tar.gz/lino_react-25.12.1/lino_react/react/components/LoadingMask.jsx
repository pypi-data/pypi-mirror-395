export const name = "LoadingMask";

import React from "react";
import PropTypes from "prop-types";
import { RegisterImportPool, getExReady, Component } from "./Base";

let ex; const exModulePromises = ex = {
    prProgressSpinner: import(/* webpackChunkName: "prProgressSpinner_LoadingMask" */"primereact/progressspinner"),
    prProgressBar: import(/* webpackChunkName: "prProgressBar_LoadingMask" */"primereact/progressbar"),
}
RegisterImportPool(exModulePromises);


export function LinoLoadMask(props) {
    const localEx = getExReady(ex, ["prProgressSpinner"]);
    return !localEx.ready ? null : <div
        style={{height: '100vh', width: '100vw', background: '#1b2c3159',
            textAlign: 'center', position: 'fixed', top: '0', left: '0',
            bottom: '0', right: '0', zIndex: '99999'
        }}>
        <localEx.prProgressSpinner.ProgressSpinner
            animationDuration="1s"
            className="vertical-center"
            strokeWidth='50'
            style={{
                borderRadius: '50%',
                overflow: 'hidden',
                width: '150px',
                height: '150px',
            }}/>
    </div>
}


export class LoadingMask extends Component {
    static requiredModules = ["prProgressSpinner"];
    static iPool = ex;

    static propTypes = {
        masking: PropTypes.element,
        mask: PropTypes.bool,
        fillHeight: PropTypes.bool,
        backgroundColor: PropTypes.string
    };
    static defaultProps = {
        fillHeight: false,
         backgroundColor: "#007ad9",
    };

    render() {
        if (!this.state.ready) return null;
        const {masking, children, mask, fillHeight, backgroundColor} = this.props;
        // const Comp = "Table";
        // return loaded ? this.props.render(data, Comp) : <p>{placeholder}</p>;
        let wrapingStyle = {position: "relative"};
        if (fillHeight) {
            wrapingStyle.height = "100%";
        } else {
            wrapingStyle.overflow = "hidden" // if no fill, hide overflow. (used to hide loading mask when children is height 0
        }

        return <div style={wrapingStyle}>
            <div className={"lino-loading-mask"}
                 style={{
                     display: mask ? "block" : "none",
                     backgroundColor: backgroundColor,

                 }}>
                <div style={{
                    position: "absolute",
                    top: "50%",
                    right: "50%",
                    transform: "translate(50%,-50%)"
                }}>
                    <this.ex.prProgressSpinner.ProgressSpinner/>
                </div>
            </div>
            {children}
        </div>
    }
};


export function LinoProgressBar(props) {
    const localEx = getExReady(ex, ["prProgressBar"]);
    return !localEx.ready ? null : <localEx.prProgressBar.ProgressBar
        mode="indeterminate"
        className={props.loading ? "" : "lino-transparent"}
        style={{height: '5px'}}/>
}
