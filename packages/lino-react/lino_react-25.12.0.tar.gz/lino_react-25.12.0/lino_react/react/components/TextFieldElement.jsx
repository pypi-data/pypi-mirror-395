import './TextFieldElement.css';

import React from "react";

import { RegisterImportPool } from "./Base";

import { overrideImageButtonHandler, invokeRefInsert, changeDelta,
    quillToolbar, refInsert, getQuillModules, quillLoad, QuillNextEditor,
    onRightClick, tableContextMenuProps, Delta} from "./quillmodules";
import * as constants from "./constants";
import { LeafComponentInput } from "./LinoComponentUtils";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    // _: import(/* webpackChunkName: "lodash_TextFieldElement" */"lodash"),
    AbortController: import(/* webpackChunkName: "AbortController_TextFieldElement" */"abort-controller"),
    i18n: import(/* webpackChunkName: "i18n_TextFieldElement" */"./i18n"),
    prButton: import(/* webpackChunkName: "prButton_TextFieldElement" */"primereact/button"),
    // prEditor: import(/* webpackChunkName: "prEditor_TextFieldElement" */"primereact/editor"),
    // prInputTextArea: import(/* webpackChunkName: "prInputTextArea_TextFieldElement" */"primereact/inputtextarea"),
    // prPanel: import(/* webpackChunkName: "prPanel_TextFieldElement" */"primereact/panel"),
    prContextMenu: import(/* webpackChunkName: "prContextMenu_TextFieldElement" */"primereact/contextmenu"),
    prUtils: import(/* webpackChunkName: "prUtils_TextFieldElement" */"primereact/utils"),
    u: import(/* webpackChunkName: "LinoUtils_TextFieldElement" */"./LinoUtils"),
};RegisterImportPool(ex);


export class TextFieldElement extends LeafComponentInput {
    static requiredModules = ["prButton", "i18n", "prUtils", "AbortController",
        "prContextMenu", "u"].concat(LeafComponentInput.requiredModules);
    static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());
    constructor(props, context) {
        super(props, context);
        this.state = {...this.state, new_window: false,
                      plain: props.elem.field_options.format === "plain",
                      inGrid: props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE,
                      key: this.c.newSlug().toString(), owb: null,
                }

        this.data_context = context;

        this.getLinoInput = this.getLinoInput.bind(this);
        this.innerHTML = this.innerHTML.bind(this);
        // this.onQuillLoad = this.onQuillLoad.bind(this);
    }

    async prepare() {
        await super.prepare();
        this.ex.i18n = this.ex.i18n.default;
        // this.ex._ = this.ex._.default;
        this.controller = new this.ex.AbortController.default();
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

    // shouldComponentUpdate(nextProps, nextState, context) {
    //     if (context !== this.state.context) {
    //         this.data_context = context;
    //         return true;
    //     }
    //     if (!this.ex._.isEqual(nextProps, this.props)) return true;
    //     const v = ABCComponent.getValueByName({
    //         name: this.dataKey, props: nextProps, context});
    //     if (v !== this.getValue()) return true;
    //     // if (!this.ex._.isEqual(nextState, this.state)) return true;
    //     if (nextState.ready !== this.state.ready) return true;
    //     return false;
    // }

    componentWillUnmount() {
        this.controller.abort();
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
            // onClick: (e) => {
            //     e.stopPropagation();
            // },
            onContextMenu: onRightClick(this),
            onKeyDown: (e) => {
                if (!((e.ctrlKey || e.metaKey) && e.code === "KeyS")) {
                    if (e.code !== "Tab" && e.code !== "Escape")
                        e.stopPropagation();
                    if (e.ctrlKey && e.shiftKey && e.code == "KeyL") {
                        e.stopPropagation();
                        e.preventDefault();
                        invokeRefInsert(this);
                    }
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
        const { modules, meta } = getQuillModules(
            APP,
            this.c.actionHandler.silentFetch,
            this.controller.signal,
            this.c.mentionValues,
            this.ex.i18n,
            this,
            showHeader,
        )
        // if (this.state.plain) {
        //     quillStyle.fontFamily = '"Courier New", Courier, monospace';
        // }
        return <div {...containerProps}>
            {showHeader &&
                <div id={meta.toolbarID}>
                    {this.state.plain
                        ? refInsert(this)
                        : quillToolbar.commonHeader(this)}
                </div>
            }
            {
            <QuillNextEditor
                config={{
                    modules: modules,
                    theme: "snow",
                }}
                dangerouslySetInnerHTML={this.state.plain ? null : {__html: this.getValue()}}
                defaultValue={this.state.plain ? new Delta().insert(this.getValue()) : null}
                onTextChange={changeDelta(this)}
                onReady={(quill) =>{
                    this.quill = quill;

                    quillLoad(this, quill);

                    if (this.leafIndexMatch()) this.focus();

                    if (this.state.plain) return;

                    if (this.props.elem.field_options.noEditorHeader || this.state.inGrid) return;
                    if (this.c.APP.state.site_data.installed_plugins.includes('uploads'))
                        overrideImageButtonHandler(quill);
                }}/>
            }
            <this.ex.prContextMenu.ContextMenu
                {...tableContextMenuProps(this)}
                ref={ref => this.tableContextMenu = ref}/>
            <div id="raw-editor-container"
                onKeyDown={e => e.stopPropagation()}></div>
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
        if (this.quill) {
            this.quill.focus();
            // setTimeout(
            //     // this.quill.root.click,
            //     this.quill.focus,
            //     50
            // )
        }
    }

    // onQuillLoad() {
    //     this.quill = this.inputEl.getQuill();
    //     // console.log("20240922 onQuillLoad", this.dataKey, this.state.plain, this.getValue());
    //     if (this.leafIndexMatch()) this.focus();
    //     // this.focusDone = false;
    //     // this.quill.on("selection-change", (range) => {
    //     //     if (!this.focusDone) {
    //     //         if (this.leafIndexMatch()) this.quill.focus();
    //     //         // if (this.leafIndexMatch()) this.quill.root.click();
    //     //         this.focusDone = true;
    //     //     }
    //     // });
    //
    //     quillLoad(this, this.quill);
    //
    //     if (this.state.plain) { this.quill.setText(this.getValue() || ""); return;}
    //     if (this.props.elem.field_options.noEditorHeader || this.state.inGrid) return;
    //     if (this.c.APP.state.site_data.installed_plugins.includes('uploads'))
    //         overrideImageButtonHandler(this.quill);
    //
    //     // try {
    //     //     const root = this.quill && this.quill.root;
    //     //     if (root && !this._imgMutationObserver) {
    //     //         this._imgMutationObserver = new MutationObserver((mutations) => {
    //     //             let changed = false;
    //     //             for (const m of mutations) {
    //     //                 if (m.type === 'attributes' && m.target && m.target.tagName === 'SPAN') { changed = true; break; }
    //     //             }
    //     //             if (changed) {
    //     //                 try {
    //     //                     const html = root.innerHTML;
    //     //                     // persist editor content (this.updateValue writes to the model)
    //     //                     // this.update({[this.dataKey]: html});
    //     //                     console.log("mutations", html);
    //     //                 } catch (e) { console.error('persist image size failed', e); }
    //     //             }
    //     //         });
    //     //         this._imgMutationObserver.observe(root, { attributes: true, subtree: true, attributeFilter: ['style'] });
    //     //     }
    //     // } catch (e) { console.error(e); }
    // }

    render() {
        if (!this.state.ready) return null;
        if (!this.props.editing_mode && !this.wrapperClasses.includes("ql-editor"))
            this.wrapperClasses.push("ql-editor");
        // console.log("TextFieldElement.render");
        return super.render()  /*, [{label: "⏏", run: (e) => {
            const DO = () => {
                this.c.history.pushPath({
                    pathname: `${this.c.value.path}/${this.props.elem.name}`,
                    params: this.c.actionHandler.defaultStaticParams()
                });
            }
            if (this.c.isModified())
                this.c.actionHandler.discardModDConfirm({agree: DO});
            else DO();
        }}]); */
    }
}


export const PreviewTextFieldElement = TextFieldElement;
