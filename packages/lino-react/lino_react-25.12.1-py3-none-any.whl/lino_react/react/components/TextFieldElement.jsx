import './TextFieldElement.css';

import React from "react";

import { RegisterImportPool } from "./Base";

import * as constants from "./constants";
import { LeafComponentInput } from "./LinoComponentUtils";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    prButton: import(/* webpackChunkName: "prButton_TextFieldElement" */"primereact/button"),
    qm: import(/* webpackChunkName: "quillmodules_TextFieldElement" */"./quillmodules"),
};RegisterImportPool(ex);


export class TextFieldElement extends LeafComponentInput {
    static requiredModules = ["prButton", "qm"].concat(LeafComponentInput.requiredModules);
    static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());
    constructor(props, context) {
        super(props, context);
        this.state = {...this.state,
                      plain: props.elem.field_options.format === "plain",
                      inGrid: props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE,
                }

        this.getLinoInput = this.getLinoInput.bind(this);
        this.innerHTML = this.innerHTML.bind(this);
    }

    async prepare() {
        await super.prepare();
        this.refStoreType = this.props.elem.field_options.virtualField ? "virtual" : "";
        this.setLeafRef({input: true, type: this.refStoreType});
    }

    onReady() {
        if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE) {
            if (
                !this.context.rows[this.props.column.rowIndex].slice(-1)[0].phantom &&
                !this.disabled()
            ) {
                this.setState({owb: <this.ex.prButton.Button
                    label="⏏"
                    onClick={() => {
                        const DO = () => {
                            const pk = this.context.rows[this.props.column.rowIndex][this.c.static.actorData.pk_index];
                            this.c.APP.URLContext.history.pushPath({
                                pathname: `${this.c.value.path}/${pk}/${this.props.elem.name}`,
                                params: this.c.actionHandler.defaultStaticParams()
                            });
                        }
                        if (this.c.isModified())
                            this.c.actionHandler.discardModDConfirm({agree: DO})
                        else DO();
                    }}
                    />});
            }
        }
    }

    componentWillUnmount() {
        delete this.c.dataContext.refStore[`${this.refStoreType}Leaves`][
            this.props.elem.name];
    }

    select() {
        // const range = this.quill.getSelection();
        // if (range) return;
        // this.quill.setSelection(0, this.quill.getLength());
    }

    getLinoInput() {
        const { APP, value } = this.c;
        const containerProps = {
            className: "l-editor",
            spellCheck: !APP.state.site_data.disable_spell_check,
            onKeyDown: (e) => {
                if (!((e.ctrlKey || e.metaKey) && e.code === "KeyS")) {
                    if (e.code !== "Tab" && e.code !== "Escape")
                        e.stopPropagation();
                } else {
                    if (this.state.inGrid) {
                        e.stopPropagation();
                        e.preventDefault();
                        document.body.click();
                    }
                }
            },
            lang: value[constants.URL_PARAM_USER_LANGUAGE],
        }

        const showHeader = !this.state.inGrid && !this.props.elem.field_options.noEditorHeader;
        return <div {...containerProps}>
            <this.ex.qm.QuillEditor
                autoFocus={this.leafIndexMatch()}
                c={this.c}
                headerExtend={null}
                htmlValue={this.state.plain ? null : this.getValue()}
                inGrid={this.state.inGrid}
                parent={this}
                plain={this.state.plain}
                showHeader={showHeader}
                value={this.state.plain ? this.getValue() : null}/>
        </div>
    }

    innerHTML() {
        if (this.props.elem.field_options.alwaysEditable) return this.getLinoInput();
        let innerHTML = super.innerHTML(constants.DANGEROUS_HTML);
        const gv = this.getValueByName;
        if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_DETAIL)
            innerHTML = <div dangerouslySetInnerHTML={{
                __html: gv(`${this.dataKey}_full_preview`) || gv(this.dataKey) || "\u00a0"}}/>;
        if (this.state.owb !== null) innerHTML = <div style={{position: "relative"}}>
            {innerHTML}
            <div style={{position: "absolute", bottom: "0px", right: "0px"}}>
                {this.state.owb}
            </div>
        </div>
        return innerHTML;
    }

    focus = () => {
        // if (this.quill) {
        //     this.quill.focus();
        // }
    }

    render() {
        if (!this.state.ready) return null;
        if (!this.props.editing_mode && !this.wrapperClasses.includes("ql-editor"))
            this.wrapperClasses.push("ql-editor");
        return super.render();
    }
}


export const PreviewTextFieldElement = TextFieldElement;
