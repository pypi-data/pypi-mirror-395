export const name = "LinoDialog";

import React from "react";
import PropTypes from "prop-types";
import * as constants from './constants';
import { RegisterImportPool, getExReady, Component, URLContextType } from "./Base";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
let ex; const exModulePromises = ex = {
    queryString: import(/* webpackChunkName: "queryString_LinoDialog" */"query-string"),
    prButton: import(/* webpackChunkName: "prButton_LinoDialog" */"primereact/button"),
    prDialog: import(/* webpackChunkName: "prDialog_LinoDialog" */"primereact/dialog"),
    u: import(/* webpackChunkName: "LinoUtils_LinoDialog" */"./LinoUtils"),
    lc: import(/* webpackChunkName: "LinoComponents_LinoDialog" */"./LinoComponents"),
    lwc: import(/* webpackChunkName: "LinoWebCam_LinoDialog" */"./LinoWebCam"),
    lbb: import(/* webpackChunkName: "LinoBbar_LinoDialog" */"./LinoBbar"),
    sc: import(/* webpackChunkName: "SiteContext_LinoDialog" */"./SiteContext"),
    i18n: import(/* webpackChunkName: "i18n_LinoDialog" */"./i18n"),
};RegisterImportPool(ex);


export class DialogFactory extends Component {
    static requiredModules = ["queryString", "u"];
    static iPool = ex;
    static propTypes = {
        APP: PropTypes.object.isRequired,
    }

    constructor(props) {
        super(props);
        this.state = {
            ...this.state,
            children: new Map(),
            callbacks: new Map(),
        }
        this.dialogRefs = {};

        this.create = this.create.bind(this);
        this.createCallback = this.createCallback.bind(this);
        this.remove = this.remove.bind(this);
        this.removeCallback = this.removeCallback.bind(this);
    }

    async create(actionHandler, execute_args) {
        const { context } = actionHandler;
        let unknownActor = !(context.value.hasActor
                && context.static.actorData.id === execute_args.actorId),
            dialogContextProps = {
                factory: this,
                id: context.newSlug().toString(),
                unknownActor: unknownActor,
            }, urlContextProps = {},
            path = `api/${execute_args.actorId.split(".").join("/")}`,
            ad = !unknownActor ? context.static.actorData : await context.getActorData(execute_args.actorId);
        urlContextProps.params = {
            action_dialog: !!(execute_args.action[constants.URL_PARAM_ACTION_NAME] !== "insert" || execute_args.action.has_parameters),
            action_full_name: execute_args.action.full_name,
            [constants.URL_PARAM_DISPLAY_MODE]: constants.DISPLAY_MODE_DETAIL,
            [constants.URL_PARAM_WINDOW_TYPE]: constants.WINDOW_TYPE_DETAIL,
        }
        if (execute_args.action.full_name === ad.insert_action)
            urlContextProps.params[constants.URL_PARAM_WINDOW_TYPE] = constants.WINDOW_TYPE_INSERT;
        urlContextProps.status = execute_args.status || {};
        urlContextProps.parentContext = context;
        if (!unknownActor) {
            urlContextProps.inherit = true;
            dialogContextProps.contextController = context;
        }
        else {
            urlContextProps.path = `/${path}`;
        }
        dialogContextProps.urlContextProps = urlContextProps;
        let dialogProps = {executeArgs: execute_args};

        // DataContext values
        let data = {data: {disabled_fields: {}}}, status = execute_args.status;
        if (status) {
            // if (execute_args.action[constants.URL_PARAM_ACTION_NAME] === "verify") {
            //     Object.assign(data.data, {
            //         email: this.APP.state.user_settings.email,
            //         verification_code: ""})
            // } else
            if (status.data_record) data = status.data_record
            else if (status.field_values) Object.assign(
                data.data, status.field_values);
        }
        if (!execute_args.action.has_parameters &&
            execute_args.action.full_name === ad.insert_action
        ) {
            let sr;
            if (!status || !status.data_record) {
                let p = !unknownActor ? actionHandler.defaultStaticParams() : {...execute_args.preprocessedStack};
                Object.assign(p, {
                    fmt: "json", [constants.URL_PARAM_ACTION_NAME]: execute_args.action[constants.URL_PARAM_ACTION_NAME],
                    [constants.URL_PARAM_SELECTED]: context.value[constants.URL_PARAM_SELECTED],
                });
                sr = [...p[constants.URL_PARAM_SELECTED]];
                sr.push("-99999");
                this.props.APP.setLoadMask();
                data = await actionHandler.silentFetch(
                    {path:`${actionHandler.URLAppendPKFromSR(path, sr)}?${this.ex.queryString.default.stringify(p)}`});
                this.props.APP.unsetLoadMask();
            } else sr = [-99999];
            urlContextProps.params[constants.URL_PARAM_SELECTED] = sr;
        }

        if (!data.title) data.title = data.data.title || execute_args.action.label;
        dialogProps.data = data;

        this.state.children.set(dialogContextProps.id,
            <DialogContext key={dialogContextProps.id} {...dialogContextProps}
                ref={ref => this.dialogRefs[dialogContextProps.id] = ref}>
                <LinoDialog {...dialogProps}/>
            </DialogContext>
        );
        this.setState({});
        if (execute_args.preprocessedStack.callback && execute_args.preprocessedStack.callback.callbackType === "postWindowInit") {
            execute_args.preprocessedStack.callback.callback(dialogContextProps.id);
        }
    }

    createWebcamDialog(context, preprocessedStack, holderId) {
        const id = context.newSlug().toString();
        this.state.children.set(id,
            <LinoWebCamDialog factory={this} holderId={holderId} id={id}
                key={id} preprocessedStack={preprocessedStack}/>);
        this.setState({});
    }

    createCallback(callbackArgs = {}) {
        callbackArgs.factory = this;
        this.state.callbacks.set(
            callbackArgs.id,
            <LinoCallbackDialog key={callbackArgs.id} {...callbackArgs}/>);

        this.setState({});
    }

    createParamDialog(context, paramNames, title, ok, agreeLabel) {
        const id = context.newSlug().toString();
        this.state.children.set(id,
            <DialogContext key={id} id={id} factory={this}
                urlContextProps={{
                    parentContext: context,
                    inherit: true,
                }}>
                <LinoInputDialog ok={ok} paramNames={paramNames} title={title}
                    agreeLabel={agreeLabel}/>
            </DialogContext>)
        this.setState({});
    }

    remove(id) {
        this.state.children.delete(id);
        delete this.dialogRefs[id];
        this.setState({});
    }

    removeCallback(id) {
        this.state.callbacks.delete(id);
        this.setState({});
    }

    removeParamDialog() {

    }

    render() {
        return <React.Fragment>
            {Array.from(this.state.children.values())}
            {Array.from(this.state.callbacks.values())}
        </React.Fragment>
    }
}


function onKeyDown(dialog, callbackD=false) {
    return (event) => {
        event.stopPropagation();
        if ((event.ctrlKey || event.metaKey) && event.code === "KeyS") {
            if (!callbackD && !dialog.context.action_dialog) {
                event.preventDefault();
                dialog.context.controller.actionHandler.submit({});
            }
        } else
        if (event.key === "Enter") {
            if (callbackD) dialog.dialogRef.current.getFooter()
                .getElementsByClassName('l-confirm-yes')[0].click()
            else if (dialog.context.action_dialog) dialog.ok()
            else {
                event.preventDefault();
                dialog.context.controller.actionHandler.submit({});
            }
        } else if (event.code === "Escape") {
            if (callbackD) dialog.dialogRef.current.getFooter()
                .getElementsByClassName('l-confirm-no')[0].click()
            else dialog.close();
        }
    }
}


function ConfirmButtons({
    agreeLabel, disagreeLabel, agree, disagree
}) {
    const [_agreeLabel, setAgreeLabel] = React.useState(agreeLabel);
    const [_disagreeLabel, setDisagreeLabel] = React.useState(disagreeLabel);
    const localEx = getExReady(ex, ["prButton", "i18n"], (mods) => {
        mods.i18n = mods.i18n.default;
        if (!_agreeLabel) setAgreeLabel(mods.i18n.t("OK"));
        if (!_disagreeLabel) setDisagreeLabel(mods.i18n.t("Cancel"));
    });
    return !localEx.ready ? null : <React.Fragment>
        <localEx.prButton.Button
            className="l-confirm-no"
            label={_disagreeLabel}
            onClick={disagree}/>
        <localEx.prButton.Button
            className="l-confirm-yes"
            label={_agreeLabel}
            onClick={agree}/>
    </React.Fragment>
}

ConfirmButtons.propTypes = {
    agree: PropTypes.func.isRequired,
    agreeLabel: PropTypes.string,
    disagree: PropTypes.func.isRequired,
    disagreeLabel: PropTypes.string,
}


class DialogContext extends Component {
    static requiredModules = ["sc"];
    static iPool = ex;
    static propTypes = {
        children: PropTypes.element.isRequired,
        factory: PropTypes.instanceOf(DialogFactory).isRequired,
        id: PropTypes.string.isRequired,
        unknownActor: PropTypes.bool,
        urlContextProps: PropTypes.object.isRequired,
    }
    static defaultProps = {
        unknownActor: false,
    }

    attachContextRoot(ref) {
        if (ref) {
            this.dialog = ref;
            ref.root = this;
        }
    }

    render() {
        if (!this.state.ready) return null;
        let dialog = React.cloneElement(this.props.children, {
            ref: (ref) => this.attachContextRoot(ref),
        });
        return <this.ex.sc.URLContext
            {...this.props.urlContextProps}
            simple={true}>
            {dialog}
        </this.ex.sc.URLContext>
    }
}


function LinoWebCamDialog(props) {
    const [parentMountDone, setParentMountDone] = React.useState(false);
    const localEx = getExReady(ex, ["prDialog", "lwc", "i18n"], (mods) => {
        mods.i18n = mods.i18n.default;
        const assertHolderMount = () => {
            let match = props.holderId in props.factory.dialogRefs &&
                props.factory.dialogRefs[props.holderId].dialog &&
                props.factory.dialogRefs[props.holderId].dialog.dialogRef.current;
            if (match) setParentMountDone(true)
            else setTimeout(assertHolderMount, 100);
        }
        assertHolderMount();
    });
    const [dim, setDim] = React.useState({height: null, width: null});
    const captureDone = React.useCallback((data) => {
        props.preprocessedStack.image = data;
        const dialog = props.factory.dialogRefs[props.holderId].dialog;
        const maxWidth = dialog.dialogRef.current.getContent().offsetWidth;
        let img = `<img src="${data}" style="max-width: ${
            Math.round(maxWidth * 0.9)
        }px; display: block; margin: auto; max-height: 50vh;"/>`
        dialog.setState({beforeContent: img});
        props.factory.remove(props.id);
    });
    return !parentMountDone ? null : <localEx.prDialog.Dialog
        closable={true}
        closeOnEscape={true}
        draggable={false}
        header={localEx.i18n.t("Capture Image")}
        maximizable={false}
        maximized={true}
        modal={true}
        onHide={e => props.factory.remove(props.id)}
        resizable={false}
        visible={true}>
        {dim.height === null ? <div ref={ref => {if (ref) {setDim({
                height: ref.parentElement.offsetHeight,
                width: ref.parentElement.offsetWidth})}}}/>
            : <div className="vertical-center" style={{textAlign: "center"}}>
            <localEx.lwc.LinoWebCam
                captureDone={captureDone}
                height={Math.round(dim.height * 0.9)}
                width={Math.round(dim.width * 0.9)}/>
        </div>}
    </localEx.prDialog.Dialog>
}

LinoWebCamDialog.propTypes = {
    factory: PropTypes.instanceOf(DialogFactory).isRequired,
    holderId: PropTypes.string.isRequired,
    id: PropTypes.string.isRequired,
    preprocessedStack: PropTypes.object.isRequired,
}


function LinoCallbackDialog({
    simple = false, agree, disagree, factory, id, message, title, xcallback
}) {
    const dialogRef = React.createRef();
    const localEx = getExReady(ex, ["prButton", "prDialog"]);
    return !localEx.ready ? null : <div onKeyDown={onKeyDown({dialogRef: dialogRef}, true)}><localEx.prDialog.Dialog
        closable={false}
        closeOnEscape={false}
        footer={simple
            ? <ConfirmButtons agree={agree} disagree={disagree}/>
            : <React.Fragment>
                {xcallback.buttons.map(button => (<localEx.prButton.Button
                    className={`p-button-secondary l-confirm-${button[0]}`}
                    key={button[0]}
                    label={button[1]}
                    onClick={() => {
                        factory.removeCallback(id);
                        eval(xcallback[button[0] + "_resendEvalJs"]);
                    }}/>
                ))}
            </React.Fragment>}
        header={title}
        maximizable={true}
        modal={true}
        onHide={e => factory.removeCallback(id)}
        ref={dialogRef}
        visible={true}>
        <div
            dangerouslySetInnerHTML={{__html: message}}
            ref={ref => {if (ref) ref.focus()}}
            tabIndex={0}/>
    </localEx.prDialog.Dialog></div>
}


/**
* simple and xcallback are mutually exclusive.
* when simple is set to true, props must include:
*   [agree, disagree]
**/
LinoCallbackDialog.propTypes = {
    agree: (props, ...args) => {
        if (props.simple) return PropTypes.func.isRequired(props, ...args);
    },
    disagree: (props, ...args) => {
        if (props.simple) return PropTypes.func.isRequired(props, ...args);
    },
    factory: PropTypes.instanceOf(DialogFactory).isRequired,
    id: PropTypes.string.isRequired,
    message: PropTypes.string.isRequired,
    simple: PropTypes.bool,
    title: PropTypes.string.isRequired,
    xcallback: (props, ...args) => {
        if (!props.simple) return PropTypes.object.isRequired(props, ...args);
    },
}


/**
* Can have one of the context type below:
*   - Inherited context: (Writable LinoBody.context // Context is available through a Delegate)
*   - Delegated context: (Readonly LinoBody.context)
*   - Own Context: (new instance of URLContext)
**/
class LinoDialog extends Component {
    static requiredModules = ["prDialog", "lc", "sc", "lbb"];
    static iPool = ex;

    static contextType = URLContextType;

    static propsTypes = {
        afterContent: PropTypes.string,
        beforeContent: PropTypes.string,
        closable: PropTypes.bool,
        closeOnEscape: PropTypes.bool,
        data: PropTypes.object.isRequired,
        executeArgs: PropTypes.object.isRequired,
    }

    static defaultProps = {
        afterContent: null,
        beforeContent: null,
        closeOnEscape: false,
        closable: true,
    }
    constructor(props) {
        super(props);
        this.state = {
            ...this.state,
            actionMeta: null,
            afterContent: props.afterContent,
            beforeContent: props.beforeContent,
            context: null,
        }

        this.dialogRef = React.createRef();

        this.close = this.close.bind(this);
        this.forceClose = this.forceClose.bind(this);
        this.ok = this.ok.bind(this);
        this.renderDialogStyle = this.renderDialogStyle.bind(this);
        this.renderDialogContentStyle = this.renderDialogContentStyle.bind(this);
    }

    async prepare() {
        this.DataContext = new this.ex.sc.DataContext({root: this, context: this.props.data,
            next: (dc) => {
                this.state.context = dc.mutableContext;
                let c = this.context.controller;
                c.setContextType(constants.CONTEXT_TYPE_ACTION);
                c.attachDataContext(this.DataContext);
                let actionMeta = {...this.context.controller.static.actorData.actions_list.find(
                    ba => ba[constants.URL_PARAM_ACTION_NAME] === this.props.executeArgs.action.full_name)};
                actionMeta.windowSize = this.context.controller.APP.state.site_data
                    .form_panels[actionMeta.window_layout].window_size;
                this.setState({actionMeta: actionMeta})}
        });
    }

    forceClose() {
        this.root.props.factory.remove(this.root.props.id);
    }

    close(event) {
        if (!this.context.controller.isModified()) {
            this.root.props.factory.remove(this.root.props.id);
        } else {
            this.context.controller.actionHandler.discardModDConfirm({
                agree: e => this.root.props.factory.remove(this.root.props.id),
            });
        }
    }

    async ok() {
        await this.context.controller.actionHandler.executeAction(this.props.executeArgs);
    }

    renderDialogContentStyle(windowSize) {
        if (windowSize && windowSize[1] && windowSize[1] !== "auto")
            return {height: (windowSize[1] * 3) + "ch"};
        return {};
    }

    renderDialogStyle(windowSize) {
        if (windowSize && windowSize[0])
            return {width: Math.floor(windowSize[0] * 1.5) + "ch"};
        return {};
    }

    render() {
        if (!this.state.ready) return null;
        return <this.ex.sc.DataContext.Context.Provider value={this.state.context}>
            {this.state.actionMeta !== null &&
                <div onKeyDown={onKeyDown(this)}><this.ex.prDialog.Dialog
                    closable={this.props.closable}
                    closeOnEscape={this.props.closeOnEscape}
                    contentStyle={this.renderDialogContentStyle(this.state.actionMeta.windowSize)}
                    footer={this.context.action_dialog
                        ? <ConfirmButtons agree={this.ok} disagree={this.close}/>
                        : <div className="l-bbar">
                            <this.ex.lbb.LinoBbar
                                action_full_name={this.props.executeArgs.action.full_name}
                                resetable={false}/>
                        </div>
                    }
                    header={this.state.context.title}
                    maximizable={true}
                    modal={false}
                    onHide={this.close}
                    ref={this.dialogRef}
                    style={this.renderDialogStyle(this.state.actionMeta.windowSize)}
                    visible={true}>
                    {this.state.beforeContent && <div dangerouslySetInnerHTML={{__html: this.state.beforeContent}}/>}
                    <this.ex.lc.LinoLayout
                        editing_mode={true}
                        window_layout={this.state.actionMeta.window_layout}
                        wt={this.context[constants.URL_PARAM_WINDOW_TYPE]}/>
                    {this.state.afterContent && <div dangerouslySetInnerHTML={{__html: this.state.afterContent}}/>}
                </this.ex.prDialog.Dialog></div>
            }
        </this.ex.sc.DataContext.Context.Provider>
    }
}


const LinoInputDialog = React.forwardRef(
    function LinoInputDialog({paramNames, title, ok, agreeLabel}, reference) {
        const ref = React.useRef({});
        const context = React.useContext(URLContextType)
        const [elem, setElem] = React.useState(null);

        const localEx = getExReady(ex, ["lc", "prDialog", "sc"], (mods) => {
            reference(ref.current);

            const data = { disabled_fields: {} };
            const elem = {
                items: Object.keys(paramNames).map(name => {
                    const def = paramNames[name];
                    data[name] = "default" in def ? def.default : null;
                    return {
                        editable: true,
                        label: name,
                        name: name,
                        react_name: def.react_name,
                        value: {},
                        field_options: {},
                    }
                }),
                name: "main",
                react_name: "Panel",
                value: {},
                vertical: true,
            };

            ref.DataContext = new mods.sc.DataContext({
                root: ref, context: {
                    data, title: title,
                }, next: (dc) => {
                    ref.context = dc.mutableContext;
                    let c = context.controller;
                    c.setContextType(constants.CONTEXT_TYPE_ACTION);
                    c.attachDataContext(ref.DataContext);
                    setElem(elem);
                }
            });
        });

        const close = React.useCallback(() => {
            const { factory, id } = ref.current.root.props;
            factory.remove(id);
        }, [])

        const agree = React.useCallback(() => {
            const done = ok(ref.context.data);
            if (done) close();
        })

        return localEx.ready && elem &&
            <localEx.sc.DataContext.Context.Provider value={ref.context}>
                <localEx.prDialog.Dialog
                    footer={<ConfirmButtons
                        agree={agree} agreeLabel={agreeLabel} disagree={close}/>}
                    header={title}
                    onHide={close}
                    onKeyDown={(event) => {if(event.key == "Enter") agree()} }
                    visible={true}>
                    <localEx.lc.LinoLayout
                        editing_mode={true}
                        elem={elem}/>
                </localEx.prDialog.Dialog>
            </localEx.sc.DataContext.Context.Provider>
    }
);

LinoInputDialog.propTypes = {
    agreeLabel: PropTypes.string,
    ok: PropTypes.func.isRequired,
    paramNames: PropTypes.object.isRequired,
    title: PropTypes.string.isRequired,
}
