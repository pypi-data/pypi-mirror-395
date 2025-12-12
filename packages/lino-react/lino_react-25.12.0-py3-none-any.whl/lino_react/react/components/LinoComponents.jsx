export const name = "LinoComponents";

import "./LinoComponents.css";
import React from "react";
import PropTypes from "prop-types";
import * as constants from './constants';
import { RegisterImportPool, Component, getExReady, URLContextType,
    DataContextType } from "./Base";

import {Labeled, LeafComponentBase, LeafComponentInput,
    LeafComponentInputChoices, LeafComponentDelayedValue,
    maintainTableWidth, ABCComponent } from "./LinoComponentUtils";
import { ForeignKeyElement } from "./ForeignKeyElement";
import { TextFieldElement, PreviewTextFieldElement } from "./TextFieldElement";
import { DateFieldElement, TimeFieldElement } from "./datetime";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    classNames: import(/* webpackChunkName: "classnames_LinoComponents" */"classnames"),
    _: import(/* webpackChunkName: "lodash_LinoComponents" */"lodash"),
    weakKey: import(/* webpackChunkName: "weakKey_LinoComponents" */"weak-key"),
    prButton: import(/* webpackChunkName: "prButton_LinoComponents" */"primereact/button"),
    prCheckbox: import(/* webpackChunkName: "prCheckbox_LinoComponents" */"primereact/checkbox"),
    prFieldset: import(/* webpackChunkName: "prFieldset_LinoComponents" */"primereact/fieldset"),
    prFileUpload: import(/* webpackChunkName: "prFileUpload_LinoComponents" */"primereact/fileupload"),
    prInputNumber: import(/* webpackChunkName: "prInputNumber_LinoComponents" */"primereact/inputnumber"),
    prInputText: import(/* webpackChunkName: "prInputText_LinoComponents" */"primereact/inputtext"),
    prPanel: import(/* webpackChunkName: "prPanel_LinoComponents" */"primereact/panel"),
    prPassword: import(/* webpackChunkName: "prPassword_LinoComponents" */"primereact/password"),
    prProgressSpinner: import(/* webpackChunkName: "prProgressSpinner_LinoComponents" */"primereact/progressspinner"),
    prSplitter: import(/* webpackChunkName: "prSplitter_LinoComponents" */"primereact/splitter"),
    prTabView: import(/* webpackChunkName: "prTabView_LinoComponents" */"primereact/tabview"),
    lb: import(/* webpackChunkName: "LinoBody_LinoComponents" */"./LinoBody"),
    sc: import(/* webpackChunkName: "SiteContext_LinoComponents" */"./SiteContext"),
    ltb: import(/* webpackChunkName: "LinoToolbar_LinoComponents" */"./LinoToolbar"),
    tbc: import(/* webpackChunkName: "ToolbarComponents_LinoComponents" */"./ToolbarComponents"),
    lpp: import(/* webpackChunkName: "LinoParamsPanel_LinoComponents" */"./LinoParamsPanel"),
}
RegisterImportPool(ex);


function LinoProgressSpinner() {
    const localEx = getExReady(ex, ["prProgressSpinner"]);
    return !localEx.ready ? null : <localEx.prProgressSpinner.ProgressSpinner
        animationDuration="1.5s"
        strokeWidth="4"
        style={{height: "35px", width: "35px"}}/>
}

const LinoComponents = {
    TabPanel: class TabPanel extends Component {
        static requiredModules = ["prTabView", "classNames", "_"];
        static iPool = ex;
        static propTypes = {
            urlParams: PropTypes.object.isRequired,
            children: PropTypes.arrayOf(PropTypes.node).isRequired,
        };
        async prepare() {this.ex._ = this.ex._.default}
        constructor(props) {
            super(props);
            this.state = {
                ...this.state,
                activeIndex: props.urlParams.tab || 0,
            }
        }

        getSnapshotBeforeUpdate(prevProps) {
            if (!this.state.ready) return null;
            let snapshot = {},
                tIndex = this.props.urlParams.tab || 0;
            if (this.state.activeIndex != tIndex) {
                snapshot.tIndex = tIndex;
            }
            if (!this.ex._.isEqual(prevProps, this.props)) snapshot.render = true;
            if (Object.keys(snapshot).length) return snapshot;
            return null;
        }

        componentDidUpdate(_prevProps, _prevState, snapshot) {
            if (snapshot) {
                if ("tIndex" in snapshot)
                    this.setState({activeIndex: snapshot.tIndex})
                else if ('render' in snapshot) this.setState({loading: false});
            }
        }

        render() {
            if (!this.state.ready) return null;
            return <this.ex.prTabView.TabView
                activeIndex={this.state.activeIndex}
                className={this.ex.classNames.default("lino-panel")}
                onTabChange={(e) => this.props.urlParams.controller.history.replaceState({tab: e.index})}
                scrollable={true}>
                {React.Children.map(this.props.children, (panel, i) => {
                    return <this.ex.prTabView.TabPanel
                        key={i}
                        header={panel.props.elem.label}
                        contentClassName={"lino-panel"}>
                        {panel}
                    </this.ex.prTabView.TabPanel>
                })}
            </this.ex.prTabView.TabView>
        }
    },
    Panel: class Panel extends Component {
        static requiredModules = ["classNames", "_", "prSplitter"];
        static iPool = ex;
        static propTypes = {
            urlParams: PropTypes.object.isRequired,
            elem: PropTypes.object.isRequired,
            parent: PropTypes.object,
            children: PropTypes.arrayOf(PropTypes.node).isRequired,
        };
        static defaultProps = {header: true};
        async prepare() {
            this.ex.classNames = this.ex.classNames.default;
            this.ex._ = this.ex._.default;
        }
        constructor(props) {
            super(props);
            this.state = {
                ...this.state,
                children: null,
            }
            this.flexs = {}

            this.maintainTableWidth = maintainTableWidth.bind(this);
            this.messageInterceptor = this.messageInterceptor.bind(this);
            this.setChildren = this.setChildren.bind(this);

        }

        onReady() {
            this.panel_classes = this.ex.classNames(
                "l-panel",
                {
                    "l-panel-vertical": this.props.elem.vertical,
                    "l-panel-horizontal": !this.props.elem.vertical,
                    "l-panel-fieldset": this.props.elem.isFieldSet,
                    "l-whitewall-panel-header": window.App.data.themeName === 'whitewall',
                });
            this.setChildren(this.props);
            if (Object.keys(this.flexs).length > 1) {
                window.addEventListener('message', this.messageInterceptor);
            }
        }

        getSnapshotBeforeUpdate(prevProps) {
            if (!this.state.ready) return null;
            if (!this.ex._.isEqual(prevProps, this.props)) {
                return "requireRefresh"
            }
            return null
        }

        componentDidUpdate(_prevProps, _prevState, snapshot) {
            if (snapshot === null) return
            if (snapshot === "requireRefresh") {
                this.setChildren(this.props);
                this.setState({loading: false});
            }
        }

        componentWillUnmount() {
            if (Object.keys(this.flexs).length > 1) {
                window.removeEventListener('message', this.messageInterceptor);
            }
        }

        messageInterceptor(e) {
            if (e.data === "GridMount") {
                // this.maintainTableWidth();
            }
        }

        setChildren(props) {
            let {resizable_panel} = props.urlParams.controller.APP.state.site_data;
            resizable_panel = resizable_panel && !props.urlParams.controller.globals.isMobile &&
                Object.prototype.hasOwnProperty.call(props.elem, 'vertical') &&
                !props.elem.vertical && props.parent && ["main", 'TabPanel'].includes(props.parent.react_name);
            let children = React.Children.map(props.children, (child, i) => {
                let style = {};
                if (child.props.elem.value.flex) style.flex = `1 1 ${child.props.elem.value.flex}%`;
                let pss = {style: style, className: this.ex.classNames("l-component")}
                if (resizable_panel) return <this.ex.prSplitter.SplitterPanel {...pss} key={i}>
                    {child}
                </this.ex.prSplitter.SplitterPanel>
                return <div {...pss} key={i}>
                    {child}
                </div>
            });
            if (resizable_panel) children = <this.ex.prSplitter.Splitter style={{width: 'inherit'}}>
                {children}
            </this.ex.prSplitter.Splitter>
            this.setState({children: children});
        }

        render() {
            if (!this.state.ready) return null;
            return <div className={this.panel_classes}>
                {(!this.props.parent || this.props.parent.react_name !== "TabPanel") && this.props.elem.label &&
                <h1>{this.props.elem.label}</h1>}
                {this.state.children}
            </div>
        }
    },
    SlaveSummaryPanel: class SlaveSummaryPanel extends LeafComponentDelayedValue {
        static requiredModules = LeafComponentDelayedValue.requiredModules.concat([
            "prPanel", "prButton", "ltb", "tbc", "lpp"]);
        static iPool = Object.assign(ex, LeafComponentDelayedValue.iPool.copy());

        getChildren() {
            // if (!this.state.ready) return null;
            let style = {
                    height: "100%",
                    width: "100%",
                    display: "flex",
                    flexDirection: "column"
                };

            let summary = (this.state.value === null
                && this.delayed) ? <LinoProgressSpinner />
                : this.innerHTML(constants.DANGEROUS_HTML);
            if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE) {
                return summary
            } else {
                return <this.ex.prPanel.Panel
                    className="l-slave-summary-panel"
                    header={this.props.elem.label}
                    // headerTemplate={(...args) => {
                    //     console.log(args);
                    //     return this.props.elem.label
                    // }}
                    // icons={this.props.hasOwnContext ? <this.ex.ltb.LayoutButton/> :
                    //     <div dangerouslySetInnerHTML={{__html: this.state.buttons}} />
                    // icons={!this.state.buttons ? <this.ex.ltb.LayoutButton/> :
                    icons={this.state.buttons && <>
                        <div style={{float: "right"}} dangerouslySetInnerHTML={{__html: this.state.buttons}}/>
                        {/* <this.ex.tbc.ParamsPanelControl /> */}
                        {
                            // <this.ex.prButton.Button
                            //     className="p-transparent-button"
                            //     style={{border: "0px", background: 'transparent', color: 'black'}}
                            //     onClick={(e) => {
                            //         this.props.urlParams.controller.APP.URLContext
                            //         .history.pushPath({
                            //             pathname: `/api/${this.actorID.split('.').join('/')}`,
                            //             params: {mk: this.state.mk, mt: this.state.mt}});
                            //     }}
                            //     icon="pi pi-eject"  // pi-external-link until 20240930
                            //     label=""/>
                        }
                    </>}
                    style={style}>
                    {/* <this.ex.lpp.LinoParamsPanel /> */}
                    {summary}
                </this.ex.prPanel.Panel>
            }
        }
    },

    ChoiceListFieldElement: class ChoiceListFieldElement extends LeafComponentInputChoices {
        constructor(props, context) {
            super(props, context);
            this.options = props.urlParams.controller.APP.state.site_data
                .choicelists[props.elem.field_options.store];
        }
    },

    ChoicesFieldElement: class ChoicesFieldElement extends LeafComponentInputChoices {
        constructor(props, context) {
          // console.log("20240924", props);
            super(props, context);
            this.options = props.elem.field_options.store
                .map(x => ({'text': x[1], 'value': x[0]}));
        }
    },

    URLFieldElement: class URLFieldElement extends LeafComponentInput {
        constructor(props, context) {
            super(props, context);

            this.innerHTML = this.innerHTML.bind(this);
        }

        innerHTML() {
            let value = this.getValue();
            return <div
                className={(this.filled() && this.props[constants.URL_PARAM_WINDOW_TYPE] !== constants.WINDOW_TYPE_TABLE)
                    ? "l-ellipsis l-card" : "l-ellipsis"}
                style={{
                    "display": "block",
                    "textOverflow": "ellipsis",
                    "overflow": "hidden",
                    "whiteSpace": "nowrap",
                    "maxWidth": "290px"
                }}>
                <a href={value} title={value}>
                    {value || "\u00a0"}</a>
            </div>
        }
    },

    DisplayElement: class DisplayElement extends LeafComponentDelayedValue {
        static requiredModules = ["prFieldset"].concat(LeafComponentDelayedValue.requiredModules);
        static iPool = Object.assign(ex, LeafComponentDelayedValue.iPool.copy());

        constructor(props, context) {
            super(props, context, true);
        }

        getChildren() {
            // if (!this.state.ready) return null;
            let unit = (this.state.value === null && this.delayed)
                ? <LinoProgressSpinner />
                : this.innerHTML(constants.DANGEROUS_HTML);
            let elem = <Labeled
                {...this.props}
                elem={this.props.elem}
                isFilled={this.filled()}>
                {unit}
            </Labeled>
            if (this.props.elem.value.collapsible) {
                return <this.ex.prFieldset.Fieldset toggleable collapsed={this.props.urlParams.globals.isMobile}>
                    {elem}
                </this.ex.prFieldset.Fieldset>
            }
            return elem
        }
    },

    ConstantElement: Object.assign((props) => (<div
        dangerouslySetInnerHTML={{__html: props.elem.value.html || "\u00a0"}}/>),
        {propTypes: {elem: PropTypes.object.isRequired}}
    ),

    CharFieldElement: class CharFieldElement extends LeafComponentInput {
        async prepare() {
            await super.prepare();
            this.re = this.props.elem.field_options.maskRe && eval(this.props.elem.field_options.maskRe);
            this.inputState = {
                ...this.inputState,
                onChangeUpdateAssert: ((event) => {
                    if (this.re && !this.re.exec(event.target.value)) {
                        return false;
                    }
                    return true;
                }).bind(this),
            }
        }
    },

    DecimalFieldElement: class DecimalFieldElement extends LeafComponentInput {
        static requiredModules = ["prInputNumber"].concat(LeafComponentInput.requiredModules);
        static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());
        async prepare() {
            await super.prepare();
            this.inputState = {
                ...this.inputState,
                inputComponent: this.ex.prInputNumber.InputNumber,
                inputProps: {maxFractionDigits: 20, allowEmpty: true},
                getValueFromEvent: (e) => e.value,
            }

            // const { locale } = this.props.urlParams.controller.APP.state.user_settings;
            // const numerals = [
            //     ...new Intl.NumberFormat(
            //         locale, { useGrouping: false }
            //     ).format(9876543210)
            // ].reverse();
            // const numerals_exp = new RegExp(`[${numerals.join('')}]`, 'g');
            // this.decimal_sep = new Intl.NumberFormat(
            //     locale, { useGrouping: false }
            // ).format(1.1).trim().replace(numerals_exp, '');
        }

        getValue() {
            let v = super.getValue();
            if (!this.c.filled(v)) v = null;
            return v;
        }

        // onKeyDown(e) {
        //     super.onKeyDown(e)
        //     if (this.decimal_sep !== ".") {
        //         console.log("e", e);
        //         if (e.key === ".") {
        //             const element = this.findHTMLInputElement(this.inputEl);
        //             console.log("element", element);
        //             const event = new KeyboardEvent(
        //                 "keydown", {key: this.decimal_sep});
        //             console.log("event", event);
        //             element.dispatchEvent(event);
        //             element.dispatchEvent(new KeyboardEvent(
        //                 "keyup", {key: this.decimal_sep}))
        //         }
        //     }
        // }

        formatValue(v) {
            const { controller } = this.props.urlParams;
            if (!controller.filled(v)) return v;
            return new Intl.NumberFormat(
                controller.APP.state.user_settings.locale
            ).format(v);
        }
    },

    IntegerFieldElement: class IntegerFieldElement extends LeafComponentInput {
        async prepare() {
            await super.prepare();
            this.inputState = {
                ...this.inputState, inputProps: {keyfilter: "int"}}
        }
    },

    UppercaseTextFieldElement: class UppercaseTextFieldElement extends LeafComponentInput {
        async prepare() {
            await super.prepare();
            this.inputState = {
                ...this.inputState, inputProps: {onInput: (e) => {
                    e.target.value = ("" + e.target.value).toUpperCase();
                }}
            }
        }
    },

    IBANFieldElement: class IBANFieldElement extends LeafComponentInput {
        async prepare() {
            await super.prepare();
            this.inputState = {
                ...this.inputState, inputProps: {onInput: (e) => {
                    e.target.value = ("" + e.target.value).toUpperCase()
                    .replace(/[^ ]{4}(?! )(?!$)/g, a => a + " ");
                }}
            }
        }
    },

    PasswordFieldElement: class PasswordFieldElement extends LeafComponentInput {
        static requiredModules = ["prPassword"].concat(LeafComponentInput.requiredModules);
        static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());
        async prepare() {
            await super.prepare();
            this.inputState = {
                ...this.inputState,
                inputOnly: true,
                inputComponent: this.ex.prPassword.Password,
                inputProps: {feedback: false, promptLabel: "", toggleMask: true}
            }
        }
    },

    AutoFieldElement: class AutoFieldElement extends LeafComponentInput {
        async prepare() {
            await super.prepare();
            this.inputState = {
                ...this.inputState,
                inputProps: {type: "text", keyfilter: "pint"}
            }
        }
    },

    BooleanFieldElement: class BooleanFieldElement extends LeafComponentInput {
        static requiredModules = ["prCheckbox"].concat(LeafComponentInput.requiredModules);
        static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());
        constructor(props, context) {
            super(props, context);
            this.wrapperClasses.push('flex', 'align-items-center');
            this.onChangeUpdate = this.onChangeUpdate.bind(this);
            this.innerHTML = this.innerHTML.bind(this);
        }

        async prepare() {
            await super.prepare();
            this.inputState = {
                ...this.inputState,
                inputComponent: this.ex.prCheckbox.Checkbox,
                onChangeUpdateAssert: e => !(
                    this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE && e.originalEvent.key === "Enter"),
            }
        }

        onChangeUpdate(e) {
            this.update({[this.dataKey]: e.checked});
            if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE)
                this.submit()
            else this.setState({});
        }

        getCellStyleClasses = () => (super.getCellStyleClasses()
            .filter(cls => cls !== 'l-card'));

        render() {
            if (!this.state.ready) return null;
            const { wt } = this.props;
            const { label } = this.props.elem;
            const disabled = this.disabled()
            this.inputState.inputProps = {readOnly: disabled,
                checked: this.getValue() || false, style: {}, inputId: label}
            if (this.container) this.setCellStyle(this.container, disabled);
            return <div
                className={this.ex.classNames.default(this.wrapperClasses)}
                onKeyDown={this.onKeyDown} ref={this.onRef}
                title={Object.assign({}, this.props.elem.value || {}).quicktip
                    || this.props.elem.help_text
                }>
                    {this.getLinoInput()}
                    {wt !== constants.WINDOW_TYPE_TABLE &&
                        <label htmlFor={label}
                            className="ml-2 l-span-clickable"
                            style={{transform: "translate(0, 20%)"}}>{label}</label>}
            </div>
        }
    },

    PreviewTextFieldElement: PreviewTextFieldElement,
    TextFieldElement: TextFieldElement,
    DateFieldElement: DateFieldElement,
    TimeFieldElement: TimeFieldElement,
    ForeignKeyElement: ForeignKeyElement,

    FileFieldElement: class FileFieldElement extends LeafComponentInput {
        static requiredModules = ['prFileUpload', 'weakKey'].concat(LeafComponentInput.requiredModules);
        static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());
        constructor(props, context) {
            super(props, context);
            this.disabled = this.disabled.bind(this);
        }

        async prepare() {
            await super.prepare();
            this.ex.weakKey = this.ex.weakKey.default;
            this.UPLOAD_HANDLER_EVENT = {
                files: {},
                options: null,
            }
        }

        componentWillUnmount() {
            this.props.urlParams.controller.dataContext.saveUploadHandlerEvent(null);
        }

        disabled() {
            if (this.props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_DETAIL)
                return true;
            return super.disabled();
        }

        getLinoInput() {
            return <this.ex.prFileUpload.FileUpload
                auto={true}
                customUpload={true}
                // mode="basic"  // default "advanced"
                multiple={true}
                name={this.dataKey}
                onRemove={(removeEvent) => {
                    delete this.UPLOAD_HANDLER_EVENT.files[this.ex.weakKey(removeEvent.file)]
                    if (!Object.keys(this.UPLOAD_HANDLER_EVENT).length)
                        this.props.urlParams.controller.dataContext.saveUploadHandlerEvent(null);
                }}
                uploadHandler={handlerEvent => {
                    handlerEvent.files.forEach((file) => {
                        this.UPLOAD_HANDLER_EVENT.files[this.ex.weakKey(file)] = file
                    });
                    this.UPLOAD_HANDLER_EVENT.options = handlerEvent.options;
                    this.props.urlParams.controller.dataContext.saveUploadHandlerEvent(this.UPLOAD_HANDLER_EVENT);
                }}
                url={`api/${this.props.urlParams.packId}/${this.props.urlParams.actorId}`}
                />
        }

        innerHTML() {
            return <a href={"/media/" + this.getValue()}> {this.getValue() || "\u00a0"} </a>
        }
    },

    SlaveContainer: class SlaveContainer extends Component {
        static requiredModules = ["lb", "sc"];
        static iPool = ex;
        static propTypes = {
            urlParams: PropTypes.object.isRequired,
            elem: PropTypes.object.isRequired,
        };

        // async prepare() {
        //     await super.prepare();
        //     const {elem, urlParams} = this.props;
        //     this.actorID = elem.actor_id || elem.name;
        //     if (!name.includes("."))
        //         this.actorID = `${urlParams.packId}.${this.actorID}`
        // }

        render() {
            if (!this.state.ready) return null;
            const up = this.props.urlParams, c = up.controller;
            return <this.ex.sc.URLContext
                getChildren={(context) => {
                    let Child = this.ex.lb.LinoBody;
                    // let displayMode = context[constants.URL_PARAM_DISPLAY_MODE],
                    //     elem = [
                    //     constants.DISPLAY_MODE_SUMMARY,
                    //     constants.DISPLAY_MODE_HTML
                    // ].includes(displayMode) ? this.props.elem[displayMode] : null;
                    // if (context.controller.filled(elem)) {
                    //     Child = LinoComponents[elem.react_name];
                    //     return <Child elem={elem} hasOwnContext={true}
                    //         {...this.props} urlParams={context}/>
                    // };
                    return <Child actorData={context.controller.static.actorData} inDetail={true}/>
                }}
                params={c.actionHandler.masterRelateForSlave()}
                parentContext={c}
                // path={`/api/${this.actorID.split(".").join("/")}`}
                path={`/api/${this.props.elem.actor_id.split(".").join("/")}`}
                simple={false}/>
        }
    },

    SimpleRemoteComboFieldElement: (props) => {
        return <ForeignKeyElement {...props} simple={true} link={false}/>
    },

    UnknownElement: Object.assign((props) => {
        const context = React.useContext(DataContextType);
        let value = ABCComponent.getValueByName({
            name: props[constants.URL_PARAM_WINDOW_TYPE] === constants.WINDOW_TYPE_TABLE ? props.elem.fields_index : props.elem.name,
            props: props, context: context
        });
        return (
            <Labeled {...props} elem={props.elem} labeled={props.labeled} isFilled={props.urlParams.controller.filled(value)}>
                <span>{value || "\u00a0"}</span>
            </Labeled>
        )
    },
    {propTypes: {
        urlParams: PropTypes.object.isRequired,
        elem: PropTypes.object.isRequired,
        labeled: PropTypes.bool,
    }}),
};

LinoComponents.ActionParamsPanel = LinoComponents.Panel;
LinoComponents.ParamsPanel = LinoComponents.Panel;
LinoComponents.DetailMainPanel = LinoComponents.Panel;
LinoComponents.ComplexRemoteComboFieldElement = LinoComponents.ForeignKeyElement;
LinoComponents.QuantityFieldElement = LinoComponents.CharFieldElement; //Auto doesn't work as you need . or :
LinoComponents.HtmlBoxElement = LinoComponents.SlaveSummaryPanel;
LinoComponents.DateTimeFieldElement = LinoComponents.DisplayElement;
LinoComponents.GenericForeignKeyElement = LinoComponents.DisplayElement;
LinoComponents.IncompleteDateFieldElement = LinoComponents.CharFieldElement;
LinoComponents.ManyToManyElement = LinoComponents.DisplayElement;
LinoComponents.StoryElement = LinoComponents.SlaveSummaryPanel;
LinoComponents.ListElement = LinoComponents.SlaveSummaryPanel;
LinoComponents.HtmlElement = LinoComponents.SlaveSummaryPanel;
LinoComponents.TilesElement = LinoComponents.SlaveSummaryPanel;
// LinoComponents.TilesElement = LinoComponents.DisplayElement;
LinoComponents.GridElement = LinoComponents.SlaveContainer;


export class LinoLayout extends Component {
    static requiredModules = ["weakKey"];
    static iPool = ex;
    static contextType = URLContextType;

    static propTypes = {
        ...LeafComponentBase.propTypesFromLinoLayout,
        window_layout: PropTypes.string,
    };

    static defaultProps = {
        editing_mode: false,
        tabIndex: -1,
    }

    async prepare() {this.ex.weakKey = this.ex.weakKey.default}

    constructor(props, context) {
        super(props, context);
        this.inputCount = 0;
        this.renderComponent = this.renderComponent.bind(this);
    }

    render() {
        if (!this.state.ready) return null;
        this.inputCount = 0;
        let elem, choosers_dict;
        if (!this.props.elem) {
            let loData = this.context.controller.APP.state.site_data.form_panels[this.props.window_layout];
            elem = loData.main;
            choosers_dict = loData.choosers_dict;
        } else {
            elem = this.props.elem;
            choosers_dict = elem.choosers_dict;
        }
        return this.renderComponent(elem.react_name, {
            ...this.props,
            elem: elem,
            choosers_dict: choosers_dict
        })
    }

    /**
     *
     * Called whenever a layout object gets and renders a child
     * @param name
     * @returns Component or UnknownElement if the element is unknown
     * @private
     */
    renderComponent(name, props) {
        let Child = LinoComponents[name];
        if (Child === undefined) {
            Child = LinoComponents.UnknownElement;
            console.warn(`${name} does not exist`,);
        }

        this.inputCount += 1;
        // props.tabIndex = this.props.tabIndex > -1 ? this.props.tabIndex : this.inputCount; // Input Element tabindex
        props.leafIndex = this.inputCount;
        props.tabIndex = 0;
        const key = props.key;
        delete props.key

        return <Child {...props} key={key} urlParams={this.context} editing_mode={props.editing_mode || this.context.editing_mode}>
            {props.elem.items && props.elem.items.filter(e => !e.hidden)
                .map((e) => {
                    return this.renderComponent(
                        e.react_name,
                        {
                            ...props,
                            editing_mode: props.editing_mode || this.context.editing_mode,
                            key: this.ex.weakKey(e),
                            elem: e,
                            parent: props.elem,
                            urlParams: this.context,
                        }
                    )
                }
            )}
        </Child>
    }
}
