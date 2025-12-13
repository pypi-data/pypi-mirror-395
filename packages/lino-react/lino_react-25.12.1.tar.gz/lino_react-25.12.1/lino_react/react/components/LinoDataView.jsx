export const name = "LinoDataView";

import "./LinoDataView.css";

import React from "react";
import * as constants from './constants';
import { RegisterImportPool, Component, DataContextType } from "./Base";

let ex; const exModulePromises = ex = {
    prCard: import(/* webpackChunkName: "prCard_LinoDataView" */"primereact/card"),
    prDataView: import(/* webpackChunkName: "prDataView_LinoDataView" */"primereact/dataview"),
    prGalleria: import(/* webpackChunkName: "prGalleria_LinoDataView" */"primereact/galleria"),
    u: import(/* webpackChunkName: "LinoUtils_LinoDataView" */"./LinoUtils"),
    lc: import(/* webpackChunkName: "LinoComponents_LinoDataView" */"./LinoComponents"),
    i18n: import(/* webpackChunkName: "i18n_LinoDataView" */"./i18n"),
}
RegisterImportPool(ex);


export class LinoCards extends Component {
    static requiredModules = ["prCard", "prDataView", "lc", "u"]
    static iPool = ex;
    static contextType = DataContextType;
    constructor(props) {
        super(props);
        this.itemTemplate = this.itemTemplate.bind(this);
    }

    itemTemplate(rowData, layout) {
        const content = rowData.main_card_body ? <div dangerouslySetInnerHTML={{__html: rowData.main_card_body}}/> :
            <DataContextType.Provider value={rowData}><this.ex.lc.LinoLayout
                editing_mode={false}
                window_layout={this.props.urlParams.controller.static.actorData.card_layout}
                wt={constants.WINDOW_TYPE_CARDS}/>
            </DataContextType.Provider>

        let title = rowData.card_title;
        if (title.startsWith('<a')) {
            title = (<div dangerouslySetInnerHTML={{__html: title}}/>);
        } else {
            title = (<p>
                {rowData.card_title}<span
                    className="l-span-clickable"
                    onClick={(e) => {
                        this.props.urlParams.controller.actionHandler.singleRow(
                            null, rowData.id)}}>
                    <i className='pi pi-link'></i>
                </span>
            </p>);
        }
        return <this.ex.prCard.Card
            title={title}
            style={{
                margin: "20px",
                // width: "60ch",
                // overflow: "scroll",
                // maxWidth: "60ch"
            }}>
            {content}
        </this.ex.prCard.Card>
    }

    render() {
        if (!this.state.ready) return null;
        return <this.ex.prDataView.DataView
            emptyMessage={this.context.no_data_text}
            value={this.context.rows} layout="grid"
            itemTemplate={this.itemTemplate}/>
    }
}


export class LinoGalleria extends Component {
    static requiredModules = ["prGalleria", "i18n"];
    static iPool = ex;
    static contextType = DataContextType;

    async prepare() {
        await super.prepare();
        this.ex.i18n = this.ex.i18n.default;
    }
    constructor(props) {
        super(props);
        this.state = {activeIndex: 0};
    }

    imageTemplate(item) {
        return <img src={item.image_src} style={{maxWidth: "100%", maxHeight: "100%"}}/>
    }

    thumbnailTemplate(item) {
        return <img src={item.thumbnail_src} style={{width: "12ch", padding: "5px"}}/>
    }

    render() {
        if (!this.state.ready) return null;
        return <div className="card l-gallery">
            <this.ex.prGalleria.Galleria
                activeIndex={this.state.activeIndex}
                circular={true}
                fullScreen={true}
                item={this.imageTemplate}
                onItemChange={(e) => this.setState({activeIndex: e.index})}
                ref={ref => this.galleria = ref}
                showItemNavigators={true}
                showIndicators={true}
                showIndicatorsOnItem={true}
                showThumbnails={false}
                style={{maxWidth: "75%"}}
                value={this.context.rows}/>
            <div className="p-grid">
                {this.context.rows && this.context.rows.map((item, index) => {
                    return <div key={index}
                        style={{position: 'relative', width: 'fit-content',
                            display: 'inline-block'
                        }}>
                        {item.hasOwnProperty('memo_cmd') && <span
                            className="l-span-clickable"
                            title={this.ex.i18n.t("Copy memo command")}
                            style={{
                                position: 'absolute',
                                background: 'yellow',
                                right: '7px',
                                top: '7px',
                                width: '2.2ch',
                                textAlign: 'center',
                                borderRadius: '3px',
                                color: 'forestgreen',
                            }}
                            onClick={e => {
                                navigator.clipboard.writeText(item.memo_cmd);
                                this.props.urlParams.controller.APP.toast.show({
                                    severity: 'info',
                                    summary: this.ex.i18n.t('Info'),
                                    detail: this.ex.i18n.t(
                                        "Memo command ({{memo_cmd}}) has been copied to clipboard",
                                        {memo_cmd: item.memo_cmd}),
                                });
                            }}>
                            <i className="pi pi-copy"></i></span>}
                        <img
                            style={{maxWidth: "20ch", maxHeight: "35ch", padding: "5px"}}
                            onClick={() => {this.setState({activeIndex: index}, () => this.galleria.show())}}
                            src={item.image_src}/>
                    </div>
                })}
            </div>
        </div>
    }
}
