export const name = "LinoComponentUtils";

import React from 'react';
import PropTypes from 'prop-types';
import { RegisterImportPool, getExReady, Component, DataContextType } from "./Base";

import * as constants from "./constants";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    classNames: import(/* webpackChunkName: "classNames_LinoComponentUtils" */"classnames"),
    prDropdown: import(/* webpackChunkName: "prDropdown_LinoComponentUtils" */"primereact/dropdown"),
    prInputText: import(/* webpackChunkName: "prInputText_LinoComponentUtils" */"primereact/inputtext"),
    queryString: import(/* webpackChunkName: "queryString_LinoComponentUtils" */"query-string"),
    sc: import(/* webpackChunkName: "SiteContext_LinoComponentUtils" */"./SiteContext"),
    u: import(/* webpackChunkName: "LinoUtils_LinoComponentUtils" */"./LinoUtils"),
};RegisterImportPool(ex);


export function maintainTableWidth(count) {
    let keys = Object.keys(this.flexs),
        fo_conditional = count !== undefined ? keys.length === count : keys.length > 1;
    if (fo_conditional) {
        keys.forEach(key => {
            var tbl = document.getElementById(key)
                .getElementsByClassName('p-datatable');
            if (tbl.length === 1) {
                tbl = tbl[0]
                let width = tbl.getBoundingClientRect().width / document
                    .getElementsByClassName('layout-topbar')[0]
                    .getBoundingClientRect().width;
                if (width > this.flexs[key]) {
                    Array.from(tbl.querySelectorAll(
                        '.p-datatable table')).forEach(el => {
                            if (Array.from(el.classList).join(' ')
                                .includes('p-datatable')) el.style
                                    .setProperty('table-layout', 'auto');
                        });
                }
            }
        });
    }
}


export const Labeled = ({
    actions = [], label, elem, children,
    hide_label = false, isFilled = false,
}) => {
    const localEx = getExReady(ex, ['classNames']);
    label = label || elem.label;
    return !localEx.ready ? null : <React.Fragment>
        {!hide_label && label && <React.Fragment>
            <label
                className={localEx.classNames.default(
                    "l-label", "l-span-clickable",
                    {"l-label--unfilled": !isFilled},
                )}
                title={Object.assign({}, elem.value || {}).quicktip
                    || elem.help_text}>
                    {label}
                    {actions.map((action, i) => <React.Fragment key={i}>
                        &nbsp;|&nbsp;
                        {
                            // <span
                            //     className="l-span-clickable"
                            //     onClick={e => action.run(e)}>
                            //     {action.label}</span>
                        }
                        <span dangerouslySetInnerHTML={{__html: action}} />
                    </React.Fragment>)}:</label>
            <br/>
        </React.Fragment>}
        {children}
    </React.Fragment>
}


Labeled.propTypes = {
    actions: PropTypes.array,
    label: PropTypes.string,
    elem: PropTypes.object.isRequired,
    hide_label: PropTypes.bool,
    isFilled: PropTypes.bool,
    children: PropTypes.element.isRequired,
}


export class ABCComponent {
    static getValueByName({name, props, context}) {
        if (props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_PARAMS)
            return context.param_values[name];
        return props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE
            ? context.rows[props.column.rowIndex][name]
            : props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_CARDS
                ? context[name] : context.data[name];
    }
}


export class LeafComponentBase extends Component {
    static requiredModules = ["classNames"];
    static iPool = ex;
    static contextType = DataContextType;
    static propTypesFromLinoLayout = {
        column: PropTypes.object,
        editing_mode: PropTypes.bool,
        hide_label: PropTypes.bool,
        [constants.URL_PARAM_WINDOW_TYPE]: PropTypes.oneOf([
            constants.WINDOW_TYPE_TABLE,
            constants.WINDOW_TYPE_DETAIL,
            constants.WINDOW_TYPE_CARDS,
            constants.WINDOW_TYPE_GALLERIA,
            constants.WINDOW_TYPE_INSERT,
            constants.WINDOW_TYPE_PARAMS,
            constants.WINDOW_TYPE_UNKNOWN,
        ]),
        tabIndex: PropTypes.number.isRequired,
    }

    static propTypes = {
        ...LeafComponentBase.propTypesFromLinoLayout,
        elem: PropTypes.object.isRequired,
        urlParams: PropTypes.object.isRequired,
        // leafIndex used in onLeafMount handler
        leafIndex: PropTypes.number.isRequired,
    }

    static defaultProps = {
        editing_mode: false,
        hide_label: false,
        [constants.URL_PARAM_WINDOW_TYPE]: constants.WINDOW_TYPE_UNKNOWN,
    }

    constructor(props, context) {
        super(props, context);
        this.wrapperClasses = []
        this.dataKey = props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE
            ? props.elem.fields_index : props.elem.name;
        this.upController = props.urlParams.controller;
        this.c = props.urlParams.controller;

        this.filled = this.filled.bind(this);
        this.getValue = this.getValue.bind(this);
        this.getValueByName = this.getValueByName.bind(this);
        this.innerHTML = this.innerHTML.bind(this);
        this.setLeafRef = this.setLeafRef.bind(this);
    }

    filled = () => (!["", null, undefined].includes(this.getValue()));

    getValueByName(name) {
        return ABCComponent.getValueByName({
            name: name, props: this.props, context: this.context});
    }

    getValue() {
        return this.getValueByName(this.dataKey);
    }

    formatValue(v) {
        return v;
    }

    innerHTML(dangerous, style={}) {
        let v = this.formatValue(this.getValue());
        if (!this.c.filled(v)) v = "\u00a0";
        if (v instanceof Object) v = JSON.stringify(v);
        if (dangerous) {
            return <div style={style} dangerouslySetInnerHTML={{__html: v}}/>
        } else {
            return <div style={style}>{v}</div>
        }
    }

    setLeafRef({input=false, type=""} = {}) {
        if (
            this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_DETAIL ||
            this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_INSERT
        ) {
            this.upController.dataContext.setLeafRef({
                name: type === 'slave' ? this.actorID
                    : this.props.elem.name, ref: this, input: input, type: type});
            const {controller} = this.props.urlParams;
            controller.onLeafMount();
        }
    }
}


export class LeafComponentDelayedValue extends LeafComponentBase {
    static requiredModules = ["queryString", "sc"].concat(LeafComponentBase.requiredModules);
    static propTypes = {
        ...LeafComponentBase.propTypes,
        hasOwnContext: PropTypes.bool.isRequired
    }
    static defaultProps = {
        ...LeafComponentBase.defaultProps,
        hasOwnContext: false
    }

    constructor(props, context, notSlave=false) {
        super(props, context);
        this.delayed = !!props.elem.delayed_value;
        const masterRelate = {}
        if (!props.hasOwnContext) Object.assign(masterRelate,
            this.upController.actionHandler.masterRelateForSlave());
        this.state = {
            ...this.state, value: null, data_url: null, ...masterRelate,
            key: this.upController.newSlug(),
            haveCTX: this.delayed && !notSlave,
        }
        this.state.UCMount = !this.state.haveCTX || !this.delayed;
        this.actorID = props.elem.actor_id || (props.elem.name.includes('.')
            ? props.elem.name : `${props.urlParams.packId}.${props.elem.name}`);

        this.shouldComponentUpdate = this.shouldComponentUpdate.bind(this);
        this.getData = this.getData.bind(this);
        this.getValue = this.getValue.bind(this);
        this.update = this.update.bind(this);
    }

    onReady() {
        let val = super.getValue();
        if (!this.delayed) {
            this.setState({value: val});
            return;
        }
        if (!this.props.hasOwnContext) this.setLeafRef({type: 'slave'});
        this.upController.globals.panels[this.actorID] = this;
        if (val !== null) this.getData(val.delayed_value_url)
        else this.setState({value: "\u00a0", data_url: undefined});
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    shouldComponentUpdate(nextProps, nextState, context) {
        const val = super.getValue();
        let update = (
            this.state.value !== nextState.value ||
            this.state.UCMount !== nextState.UCMount ||
            this.state.ready !== nextState.ready
        );
        if (this.delayed) update = update || (this.state.value !== null &&
            (val || {}).delayed_value_url !== this.state.data_url);
        return update;
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    componentDidUpdate(prevProps, prevState) {
        const val = super.getValue();
        if (this.delayed) {
            if (this.state.data_url !== (val || {}).delayed_value_url) {
                this.setState({value: null});
                if (val !== null) this.update()
                else this.setState({value: "\u00a0", data_url: undefined});
            }
        } else this.setState({value: val});
    }

    componentWillUnmount() {
        delete this.upController.globals.panels[this.actorID];
    }

    getValue() {
        return this.state.value;
    }

    getData(data_url) {
        if (!this.state.UCMount) return;
        // const myParams = this.upController.actionHandler.getParams();
        const params = this.props.urlParams.controller.actionHandler.getParams();
        // params.childParams = JSON.stringify(myParams);
        // this.props.urlParams.controller.actionHandler.defaultStaticParams(params);
        params[constants.URL_PARAM_REQUESTING_PANEL
        ] = this.upController.actionHandler.refName;

        this.upController.actionHandler.silentFetch({
            // path: `${data_url}?${this.ex.queryString.default.stringify(this.upController.actionHandler.commonParams())}`
            path: `${data_url}?${this.ex.queryString.default.stringify(params)}`
        }).then((data) => {
            this.setState({value: data.data, buttons: data.buttons,
                           data_url: data_url});
            this.upController.root.setState({});
        });
    }

    liveUpdate = (params) => {
        if (params.mk == null ||
            (params.mk === this.state.mk && params.mt === this.state.mt)
        ) this.update();
    }

    update() {
        this.getData(super.getValue().delayed_value_url);
    }

    getChildren() {
        throw "NotImplemented";
    }

    render() {
        if (!this.state.ready) return null;
        const up = this.props.urlParams, c = up.controller;
        return this.state.haveCTX ? <this.ex.sc.URLContext
            getChildren={(context) => {
                context.controller.setContextType(constants.CONTEXT_TYPE_SLAVE_GRID);
                const elem = this.getChildren();
                return elem;
            }}
            params={c.actionHandler.masterRelateForSlave()}
            parentContext={c}
            path={`/api/${this.actorID.split(".").join("/")}`}
            onContextReady={(context) => {
                this.upController = context.controller;
                // const c = context.controller;
                // const param_values = {}
                // if (c.static.actorData.params_layout) {
                //     c.static.actorData.params_fields.reduce((v, name) => {
                //         v[name] = null;
                //         return v;
                //     }, param_values);
                // }
                // this.DataContext = new this.ex.sc.DataContext({
                //     root: this, context: {param_values}, next: (dc) => {
                //         c.attachDataContext(dc);
                //     }
                // });
                this.setState({UCMount: true});
            }}
            simple={false}
            summary={this}/>
            : this.getChildren();
    }
}


export class LeafComponentInput extends LeafComponentBase {
    static requiredModules = ["prInputText", "u"].concat(LeafComponentBase.requiredModules);
    constructor(props, context) {
        super(props, context);

        this.wrapperClasses.push("lino-input-leaf");

        this.state = {
            ...this.state,
            textSelected: false
        }

        this.styleClasses = [
            "disabled-input",
            "l-card",
            "unsaved-modification",
        ]

        this.clockTimer = null;

        this.disabled = this.disabled.bind(this);
        this.filled = this.filled.bind(this);
        this.focus = this.focus.bind(this);
        this.getCellStyleClasses = this.getCellStyleClasses.bind(this);
        this.getLinoInput = this.getLinoInput.bind(this);
        this.onChangeUpdate = this.onChangeUpdate.bind(this);
        this.onInputRef = this.onInputRef.bind(this);
        this.onKeyDown = this.onKeyDown.bind(this);
        this.onRef = this.onRef.bind(this);
        this.setCellStyle = this.setCellStyle.bind(this);
        this.submit = this.submit.bind(this);
        this.leafIndexMatch = this.leafIndexMatch.bind(this);
        this.update = this.update.bind(this);
    }

    async prepare() {
        this.inputState = {
            inputComponent: this.ex.prInputText.InputText,
            inputOnly: false,
            inputProps: {},
            onChangeUpdateAssert: () => true,
            postOnChange: () => null,
            getValueFromEvent: (event) => event.target.value,
        }
        this.setLeafRef({input: true});
    }

    disabled() {
        if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_CARDS)
            return true;
        if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_PARAMS)
            return false;
        if (!this.props.elem.editable) return true;
        if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE) {
            let row = this.context.rows[this.props.column.rowIndex],
                last_item = row[row.length - 1];

            // No meta, assume not disabled;
            if (!last_item || !last_item.meta || last_item.phantom) return false;
            // disable_editing set to true;
            if (row[row.length - 2]) return true;
            // check name in the disabled_fields meta;
            return row[row.length - 3][this.props.elem.name] || false;
        } else {
            if (this.context.data.disable_editing) return true;
            return this.context.data.disabled_fields[this.props.elem.name] || false;
        }
    }

    /**
     * Find HTML input element
     */
    findHTMLInputElement(ref) {
        if (!ref) return ref;
        if (ref.focusInput) ref = ref.focusInput
        else if (ref.inputRef) ref = ref.inputRef.current
        else if (Object.prototype.hasOwnProperty.call(ref, 'getInput')) ref = ref.getInput();
        return ref;
    }

    select(input) {
        const _select = (_input) => {
            this.state.textSelected = true;
            _input.select();
        }
        if (input.select) {_select(input); return}
        if (this.container) input = this.container.getElementsByTagName('input')[0];
        if (input && input.select) _select(input);
    }

    focus() {
        let ref = this.findHTMLInputElement(this.inputEl);
        // if (ref && !this.focusSet) {
        if (ref) {
            if (ref.focus) {
                ref.focus()
            } else if (ref.click) {
                ref.click();
            }
            // this.focusSet = true
            this.select(ref);
        }
    }

    getCellStyleClasses(disabled) {
        let styleClasses = [];
        if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE) {
            if (this.context.modifiedRows[this.props.column.rowIndex].includes(
                this.props.elem.fields_index
            )) {
                styleClasses.push("unsaved-modification");
            }
        } else {
            styleClasses.push('l-card');
            if (this.props[constants.URL_PARAM_WINDOW_TYPE] !== constants.WINDOW_TYPE_CARDS) {
                if (disabled) styleClasses.push("disabled-input")
                else if (this.context.modified.includes(this.props.elem.name))
                    styleClasses.push("unsaved-modification");
            }
        }
        return styleClasses;
    }

    getValue() {
        let v = super.getValue();
        if (!this.c.filled(v)) v = "";
        return v;
    }

    getLinoInput() {
        return <this.inputState.inputComponent
            // autoFocus={this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE ? true : undefined}
            onChange={(e) => {
                if (!this.inputState.onChangeUpdateAssert(e)) return;
                this.onChangeUpdate(e);
                this.inputState.postOnChange(e);
            }}
            ref={this.onInputRef}
            style={{width: "100%"}}
            tabIndex={this.props.tabIndex}
            value={this.getValue()}
            {...this.inputState.inputProps}/>;
    }

    onChangeUpdate(e) {
        this.update({[this.dataKey]: this.inputState.getValueFromEvent(e)});
        this.setState({});
    }

    onInputRef(ref) {
        this.inputEl = ref;
        if (ref) {
            // if (ref != this.inputEl) this.focusDone = false;
            // if (!this.focusDone) {
            //     let htmlInput = this.findHTMLInputElement(ref);
            //     if (document.activeElement === htmlInput) return;
            //     if (this.leafIndexMatch()) this.focus();
            //     this.focusDone = true
            // }
            if (this.leafIndexMatch()) this.focus();
        }
    }

    onKeyDown(event) {
        if (event.code === "Escape" &&
        this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_DETAIL &&
        this.props.editing_mode) {
            this.ex.u.toggleEditingMode(this.props.urlParams);
        }
    }

    onRef(ref) {
        this.container = ref;
        const disabled = this.disabled();
        
        const handleClick = () => {
            if (disabled) return;
            
            // Check if text is selected
            const selection = window.getSelection();
            const hasSelection = selection && selection.toString().length > 0;
            if (hasSelection) return;
            
            Object.assign(this.upController.globals, {
                currentInputRowIndex: Object.assign({rowIndex: 0}, this.props.column).rowIndex,
                currentInputIndex: this.props.leafIndex,
                currentInputWindowType: this.props[constants.URL_PARAM_WINDOW_TYPE],
                currentInputAHRefName: this.upController.actionHandler.refName,
            });
            
            if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_DETAIL) {
                if (!this.props.editing_mode) {
                    this.upController.history.replaceState({editing_mode: true});
                } else {
                    if (this.state.textSelected) {
                        this.setState({textSelected: false});
                    } else {
                        this.select(this.findHTMLInputElement(this.inputEl));
                    }
                }
            }
        };
        
        const setupClickHandlers = () => {
            this.container.onclick = () => {
                // if (this.clickTimer !== null) {
                //     clearTimeout(this.clickTimer);
                //     this.clickTimer = null;
                // } else {
                //     this.clickTimer = setTimeout(() => {
                //         this.clickTimer = null;
                //         handleClick();
                //     }, 250);
                // }
                handleClick();
            };
            
            // this.container.ondblclick = () => {
            //     if (this.clickTimer !== null) {
            //         clearTimeout(this.clickTimer);
            //         this.clickTimer = null;
            //     }
            // };
        };

        if (ref) {
            if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE) {
                this.container = ref.closest("td");
                setupClickHandlers();
            }
            else if (
                this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_DETAIL ||
                this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_INSERT
            ) {
                setupClickHandlers();
            }
        }
        this.setCellStyle(this.container, disabled);
    }

    setCellStyle(ref, disabled) {
        if (ref) {
            let classes = this.getCellStyleClasses(disabled);
            this.styleClasses.forEach(item => {ref.classList.remove(item)});
            classes.forEach(item => {ref.classList.add(item)});
        }
    }

    submit() {
        this.upController.actionHandler.submit({
            cellInfo: {rowIndex: this.props.column.rowIndex}});
    }

    leafIndexMatch() {
        if (
            this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE &&
            this.props.column.rowIndex !== this.upController.globals.currentInputRowIndex
        ) return false;
        if (
            this.props[constants.URL_PARAM_WINDOW_TYPE] === this.upController.globals.currentInputWindowType &&
            this.upController.actionHandler.refName === this.upController.globals.currentInputAHRefName &&
            this.props.leafIndex === this.upController.globals.currentInputIndex
        ) return true;
        return false;
    }

    update(values) {
        this.upController.actionHandler.update({
            values: values, elem: this.props.elem, col: this.props.column,
            windowType: this.props[constants.URL_PARAM_WINDOW_TYPE]});
    }

    render(hide_label=this.props.hide_label) {
        if (!this.state.ready) return null;
        const disabled = this.disabled();
        if (this.container) this.setCellStyle(this.container, disabled);
        return <Labeled {...this.props}
            actions={(this.context.field_actions || {})[this.props.elem.name] || []}
            hide_label={hide_label}
            elem={this.props.elem} isFilled={this.filled()}>
            <div
                className={this.ex.classNames.default(
                    this.wrapperClasses,
                    {"lino-disabled-leaf": disabled},
                )}
                onKeyDown={this.onKeyDown}
                ref={this.onRef}>
                    {this.inputState.inputOnly ? this.getLinoInput() :
                        this.props.editing_mode && !disabled ?
                            this.getLinoInput() : this.innerHTML()}
            </div>
        </Labeled>
    }
}


export class LeafComponentInputChoices extends LeafComponentInput {
    static requiredModules = ["prDropdown"].concat(LeafComponentInput.requiredModules);
    constructor(props, context) {
        super(props, context);
        this.wrapperClasses.push("l-ChoiceListFieldElement");
        this.state = {
            ...this.state,
            hidden_value: null
        }

        this.dataKeyHidden = props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE
            ? props.elem.fields_index_hidden
            : props.elem.name + "Hidden";

        this.getLinoInput = this.getLinoInput.bind(this);
        this.getValue = this.getValue.bind(this);
        this.innerHTML = this.innerHTML.bind(this);
    }

    onKeyDown = (e) => {
        super.onKeyDown(e);
        if (e.key === "Enter" && this.inputEl.getOverlay()) e.stopPropagation();
    }

    getValue() {
        return {
            text: super.getValue(),
            value: this.getValueByName(this.dataKeyHidden)};
    }

    getLinoInput() {
        return <this.ex.prDropdown.Dropdown
            // appendTo={this.inputEl ? this.findHTMLInputElement(this.inputEl) : window.App.topDiv}
            autoFocus={this.leafIndexMatch()}
            itemTemplate={(item) => {
                return <div dangerouslySetInnerHTML={{__html: item.text}}/>
            }}
            onChange={(e) => {
                if (e.originalEvent.ctrlKey || e.originalEvent.altKey) return;
                this.update({[this.dataKey]: e.value || null,  // have null instead of undefined
                    [this.dataKeyHidden]: e.value || null});
                this.setState({});
            }}
            optionLabel="text"
            options={this.options}
            // panelStyle={{zIndex: "99999"}}
            // ref={this.onInputRef}
            ref={ref => this.inputEl = ref}
            showClear={this.props.elem.field_options.allowBlank}
            style={{width: "100%"}}
            tabIndex={this.props.tabIndex}
            value={this.getValue().value}
            valueTemplate={(item) => {
                if (item) return <div dangerouslySetInnerHTML={{__html: item.text}}/>
                return <div>&nbsp;</div>;
            }}/>
    }

    innerHTML() {
        let v = super.getValue();
        if (!this.c.filled(v)) v = "\u00a0";
        // return <div style={{whiteSpace: "nowrap"}}>{v}</div>
        return <div /* style={{whiteSpace: "nowrap"}} */ dangerouslySetInnerHTML={{__html: v}}/>
    }
}
