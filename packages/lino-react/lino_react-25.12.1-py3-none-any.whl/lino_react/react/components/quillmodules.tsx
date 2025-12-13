export const name = "quillmodules";

import "./quillmodules.css";

import * as t from './types';
import React from 'react';
import PropTypes from "prop-types";
import Quill, { Delta } from 'quill';
export { Delta };
import QuillNextEditor from "quill-next-react";
import { tableId } from "quill/dist/formats/table";
import Container from "quill/dist/blots/container";
import QuillImageDropAndPaste from 'quill-image-drop-and-paste';
import BlotFormatter from '@enzedonline/quill-blot-formatter2';
import htmlEditButton from "quill-html-edit-button";
import { Mention, MentionBlot } from 'quill-mention';
import { RegisterImportPool, type ImportPool, getExReady } from "./Base";

import "@enzedonline/quill-blot-formatter2/dist/css/quill-blot-formatter2.css"; // align styles

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const NextTableModule = Quill.import("modules/table") as any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const NextTableCell = Quill.import("formats/table") as any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const NextTableRow = Quill.import("formats/table-row") as any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const NextTableContainer = Quill.import("formats/table-container") as any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const TableBody = Quill.import("formats/table-body") as any;


class TableCell extends NextTableCell {
    static create(value: string | null | { row: string; class?: string }): HTMLElement {
        let node: HTMLElement;
        if (typeof value === "string" || value == null) {
            node = super.create(value);
        } else {
            node = super.create(value.row);

            if (value.class) {
                node.setAttribute("class", value.class);
            }
        }
        return node;
    }

    static formats(domNode: HTMLElement, scroll: unknown): { row?: string; class?: string } {
        const formats: { row?: string; class?: string } = {};
        formats.row = super.formats(domNode, scroll);
        if (domNode.hasAttribute("class")) {
            const klass = domNode.getAttribute("class");
            if (klass && klass.length) formats.class = klass;
        }
        return formats;
    }


    formats(): { [TableCell.blotName]: { row?: string; class?: string } } {
        return { [TableCell.blotName]: TableCell.formats(this.domNode, this.scroll) };
    }

    format(name: string, value: string | { row?: string; class?: string } | null): void {
        if (name === TableCell.blotName) {
            if (typeof value === "string") {
                throw new Error("TableCell.format: string value is not supported, use an object { row?: string, class?: string }");
            } else
            if (typeof value === "object" && value != null) {
                if (value.row) super.format(name, value.row);
                if (value.class && value.class.length) {
                    this.domNode.setAttribute("class", value.class);
                } else {
                    if (this.domNode.hasAttribute("class"))
                        this.domNode.removeAttribute("class");
                }
            }
        } else {
            super.format(name, value);
        }
    }
}


class TableRow extends NextTableRow {
    static create(value?: string | null): HTMLElement {
        const node = super.create() as HTMLElement;
        if (value && value.length) {
            node.setAttribute("class", value);
        }
        return node;
    }

    static formats(domNode: HTMLElement): string | undefined {
        if (domNode.hasAttribute("class")) {
            return domNode.getAttribute("class");
        }
        return undefined;
    }

    formats() {
        return { [TableRow.blotName]: TableRow.formats(this.domNode) };
    }


    /**
     * Allow:
     * - row.format('table-row', 'my-class')  // convenience (treat 'table-row' as class setter)
     */
    format(name: string, value: string | null | undefined): void {
        if (name === TableRow.blotName) {
            if (value && value.length)
                this.domNode.setAttribute("class", value)
            else this.domNode.removeAttribute("class");
        } else {
            super.format(name, value);
        }
    }

    checkMerge() {
        if (Container.prototype.checkMerge.call(this) && this.next.children.head != null) {
            const thisHead = this.children.head.formats();
            const thisTail = this.children.tail.formats();
            const nextHead = this.next.children.head.formats();
            const nextTail = this.next.children.tail.formats();
            return (
                thisHead.table.row === thisTail.table.row &&
                thisHead.table.row === nextHead.table.row &&
                thisHead.table.row === nextTail.table.row
            );
        }
        return false;
    }

    optimize(...args: unknown[]): void {
        Container.prototype.optimize.call(this, ...args);
        this.children.forEach((child: TableCell) => {
            if (child.next == null) return;
            const childFormats = child.formats();
            const nextFormats = child.next.formats();
            // if (childFormats.table !== nextFormats.table) {
            if (childFormats[TableCell.blotName]?.row !== nextFormats[TableCell.blotName]?.row) {
                const next = this.splitAfter(child);
                if (next) {
                    next.optimize();
                }
                // We might be able to merge with prev now
                if (this.prev) {
                    this.prev.optimize();
                }
            }
        });
    }
}


class TableContainer extends NextTableContainer {

    static create(value?: string | null): HTMLElement {
        const node = super.create(value) as HTMLElement;
        if (value && value.length) {
            node.setAttribute("class", value);
        }
        return node;
    }

    static formats(domNode: HTMLElement): string | undefined {
        if (domNode.hasAttribute("class")) {
            return domNode.getAttribute("class");
        }
        return undefined;
    }

    formats() {
        return { [TableContainer.blotName]: TableContainer.formats(this.domNode) };
    }

    format(name: string, value: string | null | undefined): void {
        if (name === TableContainer.blotName) {
            if (value && value.length) {
                this.domNode.setAttribute("class", value);
            } else {
                this.domNode.removeAttribute("class");
            }
        } else {
            super.format(name, value);
        }
    }

    balanceCells() {
        const rows = this.descendants(TableRow);
        const maxColumns = rows.reduce((max, row) => {
            return Math.max(row.children.length, max);
        }, 0);
        rows.forEach((row) => {
            new Array(maxColumns - row.children.length).fill(0).forEach(() => {
                let value = null;
                if (row.children.head != null) {
                    value = TableCell.formats(row.children.head.domNode, this.scroll);
                }
                // Pass an object so the new cell keeps both data-row and class
                const blot = this.scroll.create(TableCell.blotName, value);
                row.appendChild(blot);
                blot.optimize(); // Add break blot
            });
        });
    }

    insertColumn(index: number) {
        const [body] = this.descendant(TableBody);
        if (body == null || body.children.head == null) return;
        body.children.forEach((row: TableRow) => {
            const ref = row.children.at(index);
            const value = TableCell.formats(ref.domNode, ref.scroll);
            const cell = this.scroll.create(TableCell.blotName, value);
            row.insertBefore(cell, ref);
        });
    }

    insertRow(index: number) {
        const [body] = this.descendant(TableBody);
        if (body == null || body.children.head == null) return;
        const id = tableId();
        // copy row classes from first body row if present
        const templateRow = body.children.head;
        const templateRowClass = templateRow && templateRow.domNode ? templateRow.domNode.getAttribute('class') : undefined;
        let rowClass: string;
        if (templateRowClass && templateRowClass.length)
            rowClass = templateRowClass;
        const row = this.scroll.create(TableRow.blotName, rowClass);
        body.children.head.children.forEach(() => {
            // preserve classes on created cells from the template cell
            const headCell = templateRow.children.head;
            const cellClass = headCell && headCell.domNode ? headCell.domNode.getAttribute('class') : undefined;
            const cell = this.scroll.create(TableCell.blotName, { row: id, class: cellClass || undefined });
            row.appendChild(cell);
        });
        const ref = body.children.at(index);
        body.insertBefore(row, ref);
    }
}


class TableModule extends NextTableModule {
    insertTable(rows: number, columns: number) {
        const range = this.quill.getSelection();
        if (range == null) return;
        const delta = new Array(rows).fill(0).reduce((memo) => {
          const text = new Array(columns).fill('\n').join('');
          return memo.insert(text, {table: {row: tableId()}});
        }, new Delta().retain(range.index));
        this.quill.updateContents(delta, Quill.sources.USER);
        this.quill.setSelection(range.index, Quill.sources.SILENT);
        this.balanceTables();
    }
}


Quill.register('modules/imageDropAndPaste', QuillImageDropAndPaste);
Quill.register('modules/blotFormatter2', BlotFormatter);
Quill.register({"blots/mention": MentionBlot, "modules/mention": Mention});
Quill.register('modules/htmlEditButton', htmlEditButton);

Quill.register('modules/table', TableModule);
Quill.register('formats/table-row', TableRow);
Quill.register('formats/table', TableCell);
Quill.register('formats/table-container', TableContainer);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const QuillImageData: any = QuillImageDropAndPaste.ImageData;

let ex: ImportPool; const exModulePromises = ex = {
    AbortController: import(/* webpackChunkName: "AbortController_quillmodules" */"abort-controller"),
    prContextMenu: import(/* webpackChunkName: "prContextMenu_quillmodules" */"primereact/contextmenu"),
    prUtils: import(/* webpackChunkName: "prUtils_quillmodules" */"primereact/utils"),
    queryString:  import(/* webpackChunkName: "queryString_quillmodules" */"query-string"),
    i18n: import(/* webpackChunkName: "i18n_quillmodules" */"./i18n"),
    u: import(/* webpackChunkName: "LinoUtils_quillmodules" */"./LinoUtils"),
};RegisterImportPool(ex);


export const tableContextMenuProps = ({i18n, quillRef, c}) => {
    const module = () => {
        quillRef.current.focus();
        return quillRef.current.getModule("table");
    }

    const model = [
        {
            command: () => {
                module().insertColumnLeft();
            },
            icon: <span>&nbsp;⭰&nbsp;</span>,
            label: i18n.t("Insert column left"),
        },
        {
            command: () => {
                module().insertColumnRight();
            },
            icon: <span>&nbsp;⭲&nbsp;</span>,
            label: i18n.t("Insert column right"),
        },
        {
            command: () => {
                module().insertRowAbove();
            },
            icon:  <span>&nbsp;⭱&nbsp;</span>,
            label: i18n.t("Insert row above"),
        },
        {
            command: () => {
                module().insertRowBelow();
            },
            icon: <span>&nbsp;⭳&nbsp;</span>,
            label: i18n.t("Insert row below"),
        },
        {
            command: () => {
                module().deleteColumn();
            },
            icon: "pi pi-delete-left",
            label: i18n.t("Delete column"),
        },
        {
            command: () => {
                module().deleteRow();
            },
            icon: "pi pi-eraser",
            label: i18n.t("Delete row"),
        },
        {
            command: () => {
                module().deleteTable();
            },
            icon: "pi pi-trash",
            label: i18n.t("Delete table"),
        },
        {
            command: () => {
                const quill = quillRef.current;
                const [table, row, cell] = module().getTable();
                const ctx = c;
                const tableClasses = i18n.t("TABLE class"),
                    rowClasses = i18n.t("TR class"),
                    cellClasses = i18n.t("TD class"),
                    applyToAllRow = i18n.t("Apply to all rows"),
                    applyToAllCell = i18n.t("Apply to all cells"),
                    applyToAllCellOfThisRow = i18n.t("Apply to all cells of this row"),
                    title = i18n.t("Manage classes"),
                    agreeLabel = i18n.t("Apply");

                const ok = (data) => {
                    const tcs = data[tableClasses].split(",")
                        .filter(item => !!item).join(" ").trim();

                    quill.formatLine(quill.getIndex(table), 1, TableContainer.blotName, tcs);

                    const formatRow = (classes, row) => {
                        quill.formatLine(quill.getIndex(row), 1, TableRow.blotName, classes);
                    }

                    const rcs = data[rowClasses].split(",")
                    .filter(item => !!item).join(" ").trim();

                    formatRow(rcs, row);
                    let _row;
                    if (data[applyToAllRow]) {
                        _row = row.prev;
                        while (_row !== null) {
                            formatRow(rcs, _row);
                            _row = _row.prev;
                        }
                        _row = row.next;
                        while (_row !== null) {
                            formatRow(rcs, _row);
                            _row = _row.next;
                        }
                    }

                    const allCell = data[applyToAllCell];
                    let _cell;
                    const ccs = data[cellClasses].split(",")
                        .filter(item => !!item).join(" ").trim();
                    quill.formatLine(quill.getIndex(cell), 1, TableCell.blotName, { class: ccs });

                    if (allCell || data[applyToAllCellOfThisRow]) {
                        _cell = cell.prev;
                        while (_cell !== null) {
                            quill.formatLine(quill.getIndex(_cell), 1, TableCell.blotName, { class: ccs });
                            _cell = _cell.prev;
                        }
                        _cell = cell.next;
                        while (_cell !== null) {
                            quill.formatLine(quill.getIndex(_cell), 1, TableCell.blotName, { class: ccs });
                            _cell = _cell.next;
                        }
                    }

                    if (allCell) {
                        _row = row.prev;
                        while (_row !== null) {
                            _cell = _row.children.head;
                            if (_cell.prev !== null) {
                                throw new Error("Programming error, row.children.head returned cell with prev item")
                            }
                            while (_cell !== null) {
                                quill.formatLine(quill.getIndex(_cell), 1, TableCell.blotName, { class: ccs });
                                _cell = _cell.next;
                            }
                            _row = _row.prev;
                        }

                        _row = row.next;
                        while (_row !== null) {
                            _cell = _row.children.head;
                            if (_cell.prev !== null) {
                                throw new Error("Programming error, row.children.head returned cell with prev item")
                            }
                            while (_cell !== null) {
                                quill.formatLine(quill.getIndex(_cell), 1, TableCell.blotName, { class: ccs });
                                _cell = _cell.next;
                            }
                            _row = _row.next;
                        }
                    }
                    quill.emitter.emit('text-change');
                    return true;
                }

                ctx.APP.dialogFactory.createParamDialog(ctx, {
                    [tableClasses]: {
                        default: table.domNode.getAttribute("class") || "",
                        react_name: "CharFieldElement",
                    },
                    [rowClasses]: {
                        default: row.domNode.getAttribute("class") || "",
                        react_name: "CharFieldElement",
                    },
                    [applyToAllRow]: {
                        default: false,
                        react_name: "BooleanFieldElement",
                    },
                    [cellClasses]: {
                        default: cell.domNode.getAttribute("class") || "",
                        react_name: "CharFieldElement",
                    },
                    [applyToAllCellOfThisRow]: {
                        default: false,
                        react_name: "BooleanFieldElement",
                    },
                    [applyToAllCell]: {
                        default: false,
                        react_name: "BooleanFieldElement",
                    },
                }, title, ok, agreeLabel);
            },
            icon: <span>&nbsp;🄿&nbsp;</span>,  // \u1F13F
            label: i18n.t("Properties"),
        },
    ]
    return {model}
}


const onRightClick = ({plain, quillRef, elementRef}) => {
    if (plain) return null;
    return (e) => {
        const tableModule = quillRef.current.getModule("table");
        const [table] = tableModule.getTable();
        if (table !== null) {
            e.preventDefault();
            elementRef.current.show(e);
        }
    }
}


// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const quillLoad = (elem, quill) => {
    // const value = elem.getValue();
    // if (elem.state.plain) {
    //     quill.setText(value || "");
    // } else {
    //     quill.clipboard.dangerouslyPasteHTML(value);
    // }
}


const onTextChange = (parent, plain, e) => {
    // console.log("onTextChange", e);
    // cleans up the trailing new line (\n)
    const plainValue = e.textValue.slice(0, -1);
    const value = (plain ? plainValue : e.htmlValue ) || "";
    parent.update({[parent.dataKey]: value});
    // elem.setState({})
}


const getQuillModules = (
    {signal, i18n, props, quillRef}
) => {
    const { c } = props;
    const toolbarID = `l-ql-toolbar-${props.parent.props.elem.name}`;
    const modules: t.StringKeyedObject = {
        toolbar: `#${toolbarID}`,
        mention: quillMention({
            silentFetch: c.actionHandler.silentFetch,
            signal,
            mentionValues: c.mentionValues,
        }),
        blotFormatter2: {
            debug: true,
            resize: {
                useRelativeSize: true,
            },
            video: {
                registerBackspaceFix: false
            }
        },
        table: true,
    }
    if (props.showHeader) {
        modules.htmlEditButton = {
            msg: i18n.t('Edit HTML here, when you click "OK" the quill editor\'s contents will be replaced'),
            prependSelector: "div#raw-editor-container",
            okText: i18n.t("Ok"),
            cancelText: i18n.t("Cancel"),
            buttonTitle: i18n.t("Show HTML source"),
        }
    }
    if (props.c.APP.state.site_data.installed_plugins.includes('uploads'))
        modules.imageDropAndPaste = {handler: imageHandler(quillRef)};
    modules.keyboard = {
        bindings: {
            home: {
                key: "Home",
                shiftKey: null,
                handler: function (range, context) {
                    const quill = quillRef.current;
                    const [line] = quill.getLine(range.index);
                    if (line && line.domNode.tagName === "LI") {
                      // Move to the start of text inside the list item
                      if (context.event.shiftKey) {
                          const index = line.offset(quill.scroll);
                          quill.setSelection(index, range.index - index, "user");
                      } else {
                          quill.setSelection(line.offset(quill.scroll), 0, "user");
                      }
                      return false; // stop default browser behavior
                    }
                    return true;
                },
            },
        }
    }

    // Disable "- " from creating a bullet list or any other autofill.
    // https://github.com/slab/quill/blob/539cbffd0a13b18e9c65eb84dd35e6596e403158/packages/quill/src/modules/keyboard.ts#L550
    if (props.plain) modules.keyboard.bindings["list autofill"] = false;

    if (!props.showHeader) delete modules.toolbar;

    const meta = {toolbarID};

    return {modules, meta};
}


export const changeDelta = ({quillRef, parent, prUtils, plain}) => {
    return (delta, _oldContents, source) => {
        // copied from primereact/components/lib/editor/Editor.js
        const quill = quillRef.current;
        const firstChild = quill.container.children[0];
        let html = firstChild ? firstChild.innerHTML : null;
        const text = quill.getText();

        if (html === '<p><br></p>') {
            html = null;
        }

        // GitHub primereact #2271 prevent infinite loop on clipboard paste of HTML
        if (source === Quill.sources.API) {
            const htmlValue = quill.container.children[0];
            const editorValue = document.createElement('div');

            // editorValue.innerHTML = elem.props.urlParams.controller.dataContext.contextBackup || '';
            editorValue.innerHTML = parent.getValue() || '';

            // this is necessary because Quill rearranged style elements
            if (prUtils.DomHandler.isEqualElement(htmlValue, editorValue)) {
                return;
            }
        }

        // reorder attributes of the content to have a stable String representation
        if (html) {
            const div = document.createElement('div');
            div.innerHTML = html;
            function reorderAttributes(node) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    const attrs = Array.from(node.attributes) as Attr[];
                    attrs.sort((a, b) => a.name.localeCompare(b.name));
                    for (let i = 0; i < attrs.length; i++) {
                        node.removeAttribute(attrs[i].name);
                    }
                    for (let i = 0; i < attrs.length; i++) {
                        node.setAttribute(attrs[i].name, attrs[i].value);
                    }
                }
                for (let i = 0; i < node.childNodes.length; i++) {
                    reorderAttributes(node.childNodes[i]);
                }
            }
            reorderAttributes(div);
            html = div.innerHTML;

            // fix for quill inserting <br> instead of <br/>
            // html = html.replaceAll(/<br>/g, '<br/>');
        }

        onTextChange(parent, plain, {
            htmlValue: html,
            textValue: text,
            delta: delta,
            source: source
        });
    }
}


export const overrideImageButtonHandler = (quillRef) => {
    quillRef.current.getModule('toolbar').addHandler('image', (clicked) => {
        if (clicked) {
            // let fileInput;
            // fileInput = quill.container.querySelector('input.ql-image[type=file]');
            // if (fileInput == null) {
                const fileInput = document.createElement('input');
                fileInput.setAttribute('type', 'file');
                fileInput.setAttribute('accept', 'image/png, image/gif, image/jpeg, image/bmp, image/x-icon');
                fileInput.classList.add('ql-image');
                fileInput.addEventListener('change', (e) => {
                    const files = (e.target as HTMLInputElement).files;
                    let file;
                    if (files.length > 0) {
                        file = files[0];
                        const type = file.type;
                        const reader = new FileReader();
                        reader.onload = (e) => {
                            const dataURL = e.target.result;
                            imageHandler(quillRef)(
                                dataURL,
                                type,
                                new QuillImageData(dataURL, type, file.name)
                            );
                            fileInput.value = '';
                        }
                        reader.readAsDataURL(file);
                    }
                })
            // }
            fileInput.click();
        }
    })
}

export const imageHandler = (quillRef) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    return (imageDataURL, type, imageData) => {
        const quill = quillRef.current;
        let index = (quill.getSelection() || {}).index;
        if (index === undefined || index < 0) index = quill.getLength();
        quill.insertEmbed(index, 'image', imageDataURL);
        const imageBlot = quill.getLeaf(index)[0];
        imageBlot.domNode.setAttribute('width', '100%');
        imageBlot.domNode.setAttribute('height', 'auto');
    }
}

export const quillMention = ({silentFetch, signal, mentionValues}) => {
    function mentionSource(searchTerm, renderList, mentionChar) {
        if (searchTerm.length === 0) {
            const values = mentionValues[mentionChar];
            renderList(values, searchTerm);
        } else {
            ex.resolve(['queryString']).then(({queryString}) => {
                silentFetch({path: `suggestions?${queryString.default.stringify({
                    query: searchTerm, trigger: mentionChar})}`, signal: signal})
                .then(data => renderList(data.suggestions, searchTerm));
            });
        }
    }

    return {
        allowedChars: /^[A-Za-z0-9\s]*$/,
        mentionDenotationChars: window.App.state.site_data.suggestors,
        source: mentionSource,
        listItemClass: "ql-mention-list-item",
        mentionContainerClass: "ql-mention-list-container",
        mentionListClass: "ql-mention-list",
        dataAttributes: ["value", "link", "title", "denotationChar"],
    }
}

const quillToolbarHeaderTemplate = <React.Fragment>
    <span className="ql-formats">
        <select className='ql-header' defaultValue='0'>
            <option value='1'>Header 1</option>
            <option value='2'>Header 2</option>
            <option value='3'>Header 3</option>
            <option value='4'>Header 4</option>
            <option value='0'>Normal</option>
        </select>
        <select className='ql-font'>
            <option defaultValue="true"></option>
            <option value='serif'></option>
            <option value='monospace'></option>
        </select>
    </span>
    <span className="ql-formats">
        <select className="ql-size">
            <option value="small"></option>
            <option defaultValue="true"></option>
            <option value="large"></option>
            <option value="huge"></option>
        </select>
    </span>
    <span className="ql-formats">
        <button className="ql-script" value="sub"></button>
        <button className="ql-script" value="super"></button>
    </span>
    <span className="ql-formats">
        <button type='button' className='ql-bold' aria-label='Bold'></button>
        <button type='button' className='ql-italic' aria-label='Italic'></button>
        <button type='button' className='ql-underline' aria-label='Underline'></button>
    </span>
    <span className="ql-formats">
        <select className='ql-color'></select>
        <select className='ql-background'></select>
    </span>
    <span className="ql-formats">
        <button type='button' className='ql-list' value='ordered' aria-label='Ordered List'></button>
        <button type='button' className='ql-list' value='bullet' aria-label='Unordered List'></button>
        <select className='ql-align'>
            <option defaultValue="true"></option>
            <option value='center'></option>
            <option value='right'></option>
            <option value='justify'></option>
        </select>
    </span>
    <span className="ql-formats">
        <button type='button' className='ql-link' aria-label='Insert Link'></button>
        <button type='button' className='ql-image' aria-label='Insert Image'></button>
        <button type='button' className='ql-code-block' aria-label='Insert Code Block'></button>
    </span>
    <span className="ql-formats">
        <button type='button' className='ql-clean' aria-label='Remove Styles'></button>
    </span>
</React.Fragment>

const invokeRefInsert = ({quill, c}) => {
    const { APP } = c;
    const { URLContext } = APP;
    let index = (quill.getSelection() || {}).index;
    if (index === undefined || index < 0)
        index = quill.getLength();
    URLContext.actionHandler.runAction({
        action_full_name: URLContext.actionHandler.findUniqueAction("insert_reference").full_name,
        actorId: "about.About",
        response_callback: (data) => {
            if (data.success)
                quill.insertText(index, data.message);
        }
    });
}

const refInsert = ({quillRef, c}) => {
    if (!c.APP.state.site_data.installed_plugins.includes('memo'))
        return null;
    return <span className="ql-formats">
        <button type='button'
            onClick={() => invokeRefInsert({quill: quillRef.current, c})}
            aria-label='Open link dialog'>
            <i className="pi pi-link"></i></button>
    </span>
}

const commonHeader = ({quillRef, c, i18n, u}) => {
    return <>
        {quillToolbarHeaderTemplate}
        {refInsert({quillRef, c})}
        {
        <span className="ql-formats">
            <button type="button"
                onClick={() => {
                    const ctx = c;
                    const title = i18n.t("rows x columns");
                    const rows_text = i18n.t("Rows");
                    const columns_text = i18n.t("Columns");
                    const ok = (data) => {
                        const rows = parseInt(data[rows_text]);
                        const cols = parseInt(data[columns_text]);
                        const rowsNaN = u.isNaN(rows);
                        if (rowsNaN || u.isNaN(cols)) {
                            ctx.APP.toast.show({
                                severity: "warn",
                                summary: i18n.t("Not a number '{{dir}}'",
                                    {dir: rowsNaN
                                        ? i18n.t("rows")
                                        : i18n.t("columns")}),
                            });
                            return false;
                        }
                        const t = quillRef.current.getModule("table");
                        quillRef.current.focus();
                        t.insertTable(rows, cols);
                        return true;
                    }
                    ctx.APP.dialogFactory.createParamDialog(ctx, {
                        [rows_text]: {
                            react_name: "IntegerFieldElement",
                            default: 3,
                        },
                        [columns_text]: {
                            react_name: "IntegerFieldElement",
                            default: 3,
                        }
                    }, title, ok);
                }}>
                <i className="pi pi-table"></i></button>
        </span>
        }
    </>
}

export type QuillEditorProps = {
    autoFocus?: boolean;
    c: t.NavigationContext;
    headerExtend?: React.ReactNode;
    htmlValue?: string;
    inGrid: boolean;
    parent: t.LeafComponentInput;
    plain: boolean;
    showHeader: boolean;
    value?: string;
};


export function QuillEditor(props: QuillEditorProps) {
    const quillRef = React.useRef<Quill | null>(null);
    const ctxMenuRef = React.useRef(null);
    const aControllerRef = React.useRef<AbortController | null>(null);
    const localEx = getExReady(
        exModulePromises,
        ["i18n", "prContextMenu", "u", "AbortController", "prUtils"],
        (mods) => {
            mods.i18n = mods.i18n.default;
            mods.AbortController = mods.AbortController.default;
            aControllerRef.current = new mods.AbortController();
            const { modules, meta } = getQuillModules({
                props,
                signal: aControllerRef.current.signal,
                i18n: mods.i18n,
                quillRef,
            });
            mods.modules = modules;
            mods.meta = meta;
        }
    );
    React.useEffect(() => {
        return () => {
            if (aControllerRef.current) {
                aControllerRef.current.abort();
            }
        }
    }, []);
    return !localEx.ready ? null : <div
        onContextMenu={onRightClick({
            plain: props.plain,
            quillRef,
            elementRef: ctxMenuRef
        })}
        onKeyDown={(e) => {
            if (e.ctrlKey && e.shiftKey && e.code == "KeyL") {
                e.stopPropagation();
                e.preventDefault();
                invokeRefInsert({quill: quillRef.current, c: props.c});
            }
        }}>
        {props.showHeader &&
            <div id={localEx.meta.toolbarID}>
                {props.plain ? refInsert({quillRef, c: props.c})
                    : commonHeader({quillRef, c: props.c, i18n: localEx.i18n, u: localEx.u})}
                {props.headerExtend}
            </div>
        }
        <QuillNextEditor 
            config={{modules: localEx.modules, theme: 'snow'}}
            defaultValue={props.plain ? new Delta().insert(props.value) : null}
            dangerouslySetInnerHTML={props.plain ? null : {__html: props.htmlValue}}
            onReady={(quill) => {
                quillRef.current = quill;
                if (props.autoFocus || props.parent.leafIndexMatch()) quill.focus();
                quillLoad(props.parent, quill);
                if (!props.showHeader || props.inGrid || props.plain) return;
                if (props.c.APP.state.site_data.installed_plugins.includes('uploads')) {
                    overrideImageButtonHandler(quillRef);
                }
            }}
            onTextChange={changeDelta({
                parent: props.parent,
                plain: props.plain,
                prUtils: localEx.prUtils,
                quillRef,
            })}/>
        <localEx.prContextMenu.ContextMenu
            {...tableContextMenuProps({i18n: localEx.i18n, quillRef, c: props.c})}
            ref={ctxMenuRef}/>
        <div id="raw-editor-container"
            onKeyDown={e => e.stopPropagation()}></div>
    </div>
}
QuillEditor.propTypes = {
    value: (props, ...args: t.PropValidateRestArgs) => {
        if (props.plain) return PropTypes.string.isRequired(props, ...args);
        return null;
    },
    htmlValue: (props, ...args: t.PropValidateRestArgs) => {
        if (!props.plain) return PropTypes.string.isRequired(props, ...args);
        return null;
    },
    plain: PropTypes.bool.isRequired,
    showHeader: PropTypes.bool.isRequired,
    c: PropTypes.object.isRequired,
    parent: PropTypes.object.isRequired,
    inGrid: PropTypes.bool.isRequired,
    headerExtend: PropTypes.node,
    autoFocus: PropTypes.bool,
};
