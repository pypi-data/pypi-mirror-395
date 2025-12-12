export const name = "quillmodules";

import "./quillmodules.css";

import Quill from 'quill';
import Delta from "@quill-next/delta-es";
export { Delta };
import QuillNextEditor from "quill-next-react";
import { tableId } from "quill/dist/formats/table";
import Container from "quill/dist/blots/container";
import QuillImageDropAndPaste from 'quill-image-drop-and-paste';
import BlotFormatter from '@enzedonline/quill-blot-formatter2';
import htmlEditButton from "quill-html-edit-button";
import { Mention, MentionBlot } from 'quill-mention';
import React from 'react';
import { RegisterImportPool } from "./Base";

import "@enzedonline/quill-blot-formatter2/dist/css/quill-blot-formatter2.css"; // align styles

const NextTableModule = Quill.import("modules/table");
const NextTableCell = Quill.import("formats/table");
const NextTableRow = Quill.import("formats/table-row");
const NextTableContainer = Quill.import("formats/table-container");
const TableBody = Quill.import("formats/table-body");


class TableCell extends NextTableCell {
    static create(value) {
        let node;
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

    static formats(domNode, scroll) {
        const formats = {};
        formats.row = super.formats(domNode, scroll);
        if (domNode.hasAttribute("class")) {
            const klass = domNode.getAttribute("class");
            if (klass && klass.length) formats.class = klass;
        }
        return formats;
    }


    formats() {
        return { [TableCell.blotName]: TableCell.formats(this.domNode) };
    }

    format(name, value) {
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
    static create(value) {
        const node = super.create();
        if (value && value.length) {
            node.setAttribute("class", value);
        }
        return node;
    }

    static formats(domNode) {
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
    format(name, value) {
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

    optimize(...args) {
        Container.prototype.optimize.call(this, ...args);
        this.children.forEach((child) => {
            if (child.next == null) return;
            const childFormats = child.formats();
            const nextFormats = child.next.formats();
            // if (childFormats.table !== nextFormats.table) {
            if (childFormats.table.row !== nextFormats.table.row) {
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

    static create(value) {
        const node = super.create(value);
        if (value && value.length) {
            node.setAttribute("class", value);
        }
        return node;
    }

    static formats(domNode) {
        if (domNode.hasAttribute("class")) {
            return domNode.getAttribute("class");
        }
        return undefined;
    }

    formats() {
        return { [TableContainer.blotName]: TableContainer.formats(this.domNode) };
    }

    format(name, value) {
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
                    value = TableCell.formats(row.children.head.domNode);
                }
                // Pass an object so the new cell keeps both data-row and class
                const blot = this.scroll.create(TableCell.blotName, value);
                row.appendChild(blot);
                blot.optimize(); // Add break blot
            });
        });
    }

    insertColumn(index) {
        const [body] = this.descendant(TableBody);
        if (body == null || body.children.head == null) return;
        body.children.forEach((row) => {
            const ref = row.children.at(index);
            const value = TableCell.formats(ref.domNode);
            const cell = this.scroll.create(TableCell.blotName, value);
            row.insertBefore(cell, ref);
        });
    }

    insertRow(index) {
        const [body] = this.descendant(TableBody);
        if (body == null || body.children.head == null) return;
        const id = tableId();
        // copy row classes from first body row if present
        const templateRow = body.children.head;
        const templateRowClass = templateRow && templateRow.domNode ? templateRow.domNode.getAttribute('class') : undefined;
        let rowClass;
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
    insertTable(rows, columns) {
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

const QuillImageData = QuillImageDropAndPaste.ImageData;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    queryString:  import(/* webpackChunkName: "queryString_quillmodules" */"query-string"),
};RegisterImportPool(ex);


export const tableContextMenuProps = (elem) => {
    const { i18n } = elem.ex;

    const module = () => {
        elem.quill.focus();
        return elem.quill.getModule("table");
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
                const { quill } = elem;
                const [table, row, cell] = module().getTable();
                const ctx = elem.c;
                let tableClasses = i18n.t("TABLE class"),
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
                    let _cell, ccs = data[cellClasses].split(",")
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


export const onRightClick = (elem) => {
    if (elem.state.plain) return null;
    return (e) => {
        const { quill } = elem;
        const tableModule = quill.getModule("table");
        const [table] = tableModule.getTable();
        if (table !== null) {
            e.preventDefault();
            elem.tableContextMenu.show(e);
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


export const onTextChange = (elem, e) => {
    // console.log("onTextChange", e);
    // cleans up the trailing new line (\n)
    const plainValue = e.textValue.slice(0, -1);
    let value = (elem.state.plain ? plainValue : e.htmlValue ) || "";
    elem.update({[elem.dataKey]: value});
    // elem.setState({})
}


export const getQuillModules = (
    APP, silentFetch, signal, mentionValues, i18n, elem, hasToolbar = true
) => {
    const toolbarID = `l-ql-toolbar-${elem.props.elem.name}`;
    const modules = {
        toolbar: `#${toolbarID}`,
        mention: quillMention({
            silentFetch: silentFetch,
            signal: signal,
            mentionValues: mentionValues,
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
    if (hasToolbar) {
        modules.htmlEditButton = {
            msg: i18n.t('Edit HTML here, when you click "OK" the quill editor\'s contents will be replaced'),
            prependSelector: "div#raw-editor-container",
            okText: i18n.t("Ok"),
            cancelText: i18n.t("Cancel"),
            buttonTitle: i18n.t("Show HTML source"),
        }
    }
    if (APP.state.site_data.installed_plugins.includes('uploads'))
        modules.imageDropAndPaste = {handler: imageHandler(elem)};
    modules.keyboard = {
        bindings: {
            home: {
                key: "Home",
                shiftKey: null,
                handler: function (range, context) {
                    const { quill } = elem;
                    let [line] = quill.getLine(range.index);
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
    if (elem.state.plain) modules.keyboard.bindings["list autofill"] = false;

    if (!hasToolbar) delete modules.toolbar;

    const meta = {toolbarID};

    return {modules, meta};
}


export const changeDelta = (elem) => {
    return (delta, oldContents, source) => {
        // copied from primereact/components/lib/editor/Editor.js
        const quill = elem.quill;
        let firstChild = quill.container.children[0];
        let html = firstChild ? firstChild.innerHTML : null;
        let text = quill.getText();

        if (html === '<p><br></p>') {
            html = null;
        }

        // GitHub primereact #2271 prevent infinite loop on clipboard paste of HTML
        if (source === 'api') {
            const htmlValue = quill.container.children[0];
            const editorValue = document.createElement('div');

            editorValue.innerHTML = elem.getValue() || '';

            // this is necessary because Quill rearranged style elements
            if (elem.ex.prUtils.DomHandler.isEqualElement(htmlValue, editorValue)) {
                return;
            }
        }

        onTextChange(elem, {
            htmlValue: html,
            textValue: text,
            delta: delta,
            source: source
        });
    }
}


export const overrideImageButtonHandler = (quill) => {
    quill.getModule('toolbar').addHandler('image', (clicked) => {
        if (clicked) {
            let fileInput;
            // fileInput = quill.container.querySelector('input.ql-image[type=file]');
            // if (fileInput == null) {
                fileInput = document.createElement('input');
                fileInput.setAttribute('type', 'file');
                fileInput.setAttribute('accept', 'image/png, image/gif, image/jpeg, image/bmp, image/x-icon');
                fileInput.classList.add('ql-image');
                fileInput.addEventListener('change', (e) => {
                    const files = e.target.files;
                    let file;
                    if (files.length > 0) {
                        file = files[0];
                        const type = file.type;
                        const reader = new FileReader();
                        reader.onload = (e) => {
                            const dataURL = e.target.result;
                            imageHandler({quill})(
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

export const imageHandler = (elem) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    return (imageDataURL, type, imageData) => {
        const { quill } = elem;
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
            let values = mentionValues[mentionChar];
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
            <option defaultValue={true}></option>
            <option value='serif'></option>
            <option value='monospace'></option>
        </select>
    </span>
    <span className="ql-formats">
        <select className="ql-size">
            <option value="small"></option>
            <option defaultValue={true}></option>
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
            <option defaultValue={true}></option>
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

export const invokeRefInsert = (elem) => {
    const { APP } = elem.props.urlParams.controller;
    const { URLContext } = APP;
    let index = (elem.quill.getSelection() || {}).index;
    if (index === undefined || index < 0)
        index = elem.quill.getLength();
    URLContext.actionHandler.runAction({
        action_full_name: URLContext.actionHandler.findUniqueAction("insert_reference").full_name,
        actorId: "about.About",
        response_callback: (data) => {
            if (data.success)
                elem.quill.insertText(index, data.message);
        }
    });
}

export const refInsert = (elem) => {
    if (!elem.c.APP.state.site_data.installed_plugins.includes('memo'))
        return null;
    return <span className="ql-formats">
        <button type='button'
            onClick={() => invokeRefInsert(elem)}
            aria-label='Open link dialog'>
            <i className="pi pi-link"></i></button>
    </span>
}

const commonHeader = (elem) => {
    return <>
        {quillToolbarHeaderTemplate}
        {refInsert(elem)}
        {
        <span className="ql-formats">
            <button type="button"
                onClick={() => {
                    const ctx = elem.props.urlParams.controller;
                    const title = elem.ex.i18n.t("rows x columns");
                    const rows_text = elem.ex.i18n.t("Rows");
                    const columns_text = elem.ex.i18n.t("Columns");
                    const ok = (data) => {
                        const rows = parseInt(data[rows_text]);
                        const cols = parseInt(data[columns_text]);
                        const rowsNaN = elem.ex.u.isNaN(rows);
                        if (rowsNaN || elem.ex.u.isNaN(cols)) {
                            ctx.APP.toast.show({
                                severity: "warn",
                                summary: elem.ex.i18n.t("Not a number '{{dir}}'",
                                    {dir: rowsNaN
                                        ? elem.ex.i18n.t("rows")
                                        : elem.ex.i18n.t("columns")}),
                            });
                            return false;
                        }
                        const t = elem.quill.getModule("table");
                        elem.quill.focus();
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

export const quillToolbar = {
    header: quillToolbarHeaderTemplate,
    commonHeader: commonHeader,
}


export { QuillNextEditor };
