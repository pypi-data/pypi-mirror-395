export const name = "LinoEditor";

import React from "react";
import { RegisterImportPool, URLContextType } from "./Base";
import { quillToolbar, overrideImageButtonHandler, getQuillModules,
    invokeRefInsert, quillLoad, QuillNextEditor, changeDelta, refInsert,
    onRightClick, tableContextMenuProps, Delta } from "./quillmodules";
import { LeafComponentInput } from "./LinoComponentUtils";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    AbortController: import(/* webpackChunkName: "AbortController_LinoEditor" */"abort-controller"),
    i18n: import(/* webpackChunkName: "i18n_LinoEditor" */"./i18n"),
    // prButton: import(/* webpackChunkName: "prButton_LinoEditor" */"primereact/button"),
    // prEditor: import(/* webpackChunkName: "prEditor_LinoEditor" */"primereact/editor"),
    // prDialog: import(/* webpackChunkName: "prDialog_LinoEditor" */"primereact/dialog"),
    prContextMenu: import(/* webpackChunkName: "prContextMenu_LinoEditor" */"primereact/contextmenu"),
    prUtils: import(/* webpackChunkName: "prUtils_LinoEditor" */"primereact/utils"),
    u: import(/* webpackChunkName: "LinoUtils_LinoEditor" */"./LinoUtils"),
};RegisterImportPool(ex);


export class LinoEditor extends LeafComponentInput {
    static requiredModules = ["i18n", "AbortController", "prContextMenu",
        "prUtils", "u"].concat(LeafComponentInput.requiredModules);
    static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());

    static defaultProps = {
        ...LeafComponentInput.defaultProps,
        leafIndex: 0,
    }

    async prepare() {
        await super.prepare();
        this.controller = new this.ex.AbortController.default();
        this.ex.i18n = this.ex.i18n.default;
    }

    constructor(props) {
        super(props);
        this.state = {...this.state,
                      plain: props.elem.field_options.format === "plain"}

        this.closeEditor = this.closeEditor.bind(this);
        this.onGlobalKeyDown = this.onGlobalKeyDown.bind(this);
    }

    onReady() {
        window.addEventListener('keydown', this.onGlobalKeyDown);
    }

    componentWillUnmount() {
        window.removeEventListener('keydown', this.onGlobalKeyDown);
        this.controller.abort();
    }

    onGlobalKeyDown(e) {
        if (e.code == 'Escape') this.closeEditor(e);
    }

    closeEditor() {
        const { c } = this;
        const DO = () => {
            c.history.pushPath({
                pathname: `/api/${c.value.packId}/${c.value.actorId}/${c.value.pk}`,
                params: c.actionHandler.defaultStaticParams()
            })
        }
        if (!c.isModified()) {DO()} else
            c.actionHandler.discardModDConfirm({agree: DO});
    }

    headerExtend() {
        return <>
            {this.state.plain
                ? refInsert(this)
                : quillToolbar.commonHeader(this)
            }
            <span className="ql-formats">
                <button type='button'
                    onClick={async (e) => {
                        const data = await this.c.actionHandler.submit({});
                        if (data.success) this.closeEditor(e);
                    }}
                    aria-label='Submit changes'>
                    <i className="pi pi-save"></i></button>
                <button type='button'
                    onClick={this.closeEditor}
                    aria-label='Close window'>
                    <i className="pi pi-times"></i></button>
            </span>
        </>
    }

    render () {
        if (!this.state.ready) return null;
        return <URLContextType.Consumer>
            {value => {
                const { APP } = value.controller;
                const { modules, meta } = getQuillModules(
                    APP,
                    value.controller.actionHandler.silentFetch,
                    this.controller.signal,
                    value.controller.mentionValues,
                    this.ex.i18n,
                    this,
                );
                return <div className="l-editor"
                    spellCheck={!APP.state.site_data.disable_spell_check}
                    onContextMenu={onRightClick(this)}
                    onKeyDown={async (e) => {
                        if ((e.ctrlKey || e.metaKey) && e.code === "KeyS") {
                            e.stopPropagation();
                            e.preventDefault();
                            const data = await this.c.actionHandler.submit({});
                            if (data.success) this.closeEditor(e);
                        } else if (e.ctrlKey && e.shiftKey && e.code == "KeyL") {
                            e.stopPropagation();
                            e.preventDefault();
                            invokeRefInsert(this);
                        } else if (e.code !== 'Escape') e.stopPropagation();
                    }}>
                    <div id={meta.toolbarID}>
                        {this.headerExtend()}
                    </div>
                    {
                    <QuillNextEditor
                        config={{
                            modules: modules,
                            theme: "snow",
                        }}
                        defaultValue={this.state.plain ? new Delta().insert(this.getValue()) : null}
                        dangerouslySetInnerHTML={this.state.plain ? null : {__html: this.getValue()}}
                        onTextChange={changeDelta(this)}
                        onReady={(quill) => {
                            window.elem = this;
                            this.quill = quill;
                            quillLoad(this, quill);
                            overrideImageButtonHandler(quill);
                            quill.focus();
                        }}/>
                    }
                    {
                    // <this.ex.prEditor.Editor
                    //     headerTemplate={this.headerExtend()}
                    //     modules={modules}
                    //     onLoad={e => {
                    //         this.quill = this.inputEl.getQuill();
                    //         quillLoad(this, this.quill);
                    //         overrideImageButtonHandler(this.quill);
                    //     }}
                    //     onTextChange={(e) => onTextChange(this, e)}
                    //     ref={ref => this.inputEl = ref}
                    //     style={{background: "#ffffff"}}
                    //     value={this.context.data[value.fieldName]}/>
                    }
                    <this.ex.prContextMenu.ContextMenu
                        {...tableContextMenuProps(this)}
                        ref={ref => this.tableContextMenu = ref}/>
                    <div id="raw-editor-container"
                        onKeyDown={e => e.stopPropagation()}></div>
                </div>
            }}
        </URLContextType.Consumer>
    }
}
