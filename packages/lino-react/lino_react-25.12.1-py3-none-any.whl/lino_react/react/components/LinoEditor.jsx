export const name = "LinoEditor";

import React from "react";
import { RegisterImportPool } from "./Base";
import { LeafComponentInput } from "./LinoComponentUtils";
import * as constants from "./constants";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    qm: import(/* webpackChunkName: "quillmodules_LinoEditor" */"./quillmodules"),
};RegisterImportPool(ex);


export class LinoEditor extends LeafComponentInput {
    static requiredModules = ["qm"].concat(LeafComponentInput.requiredModules);
    static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());

    static defaultProps = {
        ...LeafComponentInput.defaultProps,
        leafIndex: 0,
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
        return <span className="ql-formats">
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
    }

    render () {
        if (!this.state.ready) return null;
        const { APP } = this.c;
        return <div className="l-editor"
            lang={this.c.value[constants.URL_PARAM_USER_LANGUAGE]}
            onKeyDown={async (e) => {
                if ((e.ctrlKey || e.metaKey) && e.code === "KeyS") {
                    e.stopPropagation();
                    e.preventDefault();
                    const data = await this.c.actionHandler.submit({});
                    if (data.success) this.closeEditor(e);
                } else if (e.code !== 'Escape') e.stopPropagation();
            }}
            spellCheck={!APP.state.site_data.disable_spell_check}>
                <this.ex.qm.QuillEditor
                    autoFocus={true}
                    c={this.c}
                    headerExtend={this.headerExtend()}
                    htmlValue={this.state.plain ? null : this.getValue()}
                    inGrid={false}
                    parent={this}
                    plain={this.state.plain}
                    showHeader={true}
                    value={this.state.plain ? this.getValue() : null} />
        </div>
    }
}
