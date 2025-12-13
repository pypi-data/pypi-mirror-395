export const name = "LinoBbar";

import "./LinoBbar.css";

import * as constants from './constants';
import React from "react";
import PropTypes from "prop-types";
import { RegisterImportPool, Component, URLContextType } from "./Base";

let ex; const exModulePromises = ex = {
    _: import(/* webpackChunkName: "lodash_LinoBbar" */"lodash"),
    prButton: import(/* webpackChunkName: "prButton_LinoBbar" */"primereact/button"),
    prSplitButton: import(/* webpackChunkName: "prSplitButton_LinoBbar" */"primereact/splitbutton"),
    i18n: import(/* webpackChunkName: "i18n_LinoBbar" */"./i18n"),
};RegisterImportPool(ex);


export class LinoBbar extends Component {
    static requiredModules = ["prButton", "prSplitButton", "_", "i18n"];
    static iPool = ex;

    static contextType = URLContextType;

    static propTypes = {
        action_full_name: PropTypes.string.isRequired,
        nonCollapsibles: PropTypes.bool,
        onSide: PropTypes.bool,
        resetable: PropTypes.bool,
    }
    static defaultProps = {
        nonCollapsibles: false,
        onSide: false,
        resetable: true,
    }

    async prepare() {
        await super.prepare();
        this.ex.i18n = this.ex.i18n.default;
    }

    constructor(props) {
        super(props);
        this.state = {...this.state, overflowShow: false};
        this.action2buttonProps = this.action2buttonProps.bind(this);
        this.render_buttons = this.render_buttons.bind(this);
        this.render_overflow = this.render_overflow.bind(this);
        this.render_actionbutton = this.render_actionbutton.bind(this);
        this.render_splitActionButton = this.render_splitActionButton.bind(this);
        this.runAction = this.runAction.bind(this);
    }

    runAction(action, tba, event) {
        if (tba.js_handler) {
            eval(tba.js_handler);
            return
        }

        let runnable = {
            action_full_name: tba[constants.URL_PARAM_ACTION_NAME],
            actorId: this.context.controller.static.actorData.id,
            pollContext: true,
        }

        if (action.hasOwnProperty('actor')) {
            if (action.actor !== runnable.actorId) runnable.pollContext = false;
            runnable.actorId = action.actor;
        }
        if (action.select_rows) runnable[constants.URL_PARAM_SELECTED] = this.context[constants.URL_PARAM_SELECTED];
        if (event.ctrlKey) runnable.clickCatch = true;
        this.context.controller.actionHandler.checkAndRunAction(runnable);
    }

    render_overflow() {
        return <div>
            <this.ex.prButton.Button icon={"pi pi-ellipsis-v"} onClick={this.setState({overflowShow: !this.state.overflowShow})}/>
            <div>

            </div>
        </div>
    }

    action2buttonProps(tba, action, bbar) {
        let icon_and_label = {label: action.label, className: `l-button-${action[constants.URL_PARAM_ACTION_NAME]}`};
        if (action.icon) {
            icon_and_label.icon = action.icon;
            icon_and_label.label = bbar ? undefined : icon_and_label.label;
        }
        else if (action.button_text) {
            icon_and_label.label = action.button_text;
            if (action.button_text.length === 1) {
                icon_and_label.style = {fontSize: "1.2rem"}
            }
        }
        // console.log((action.select_rows && this.context[constants.URL_PARAM_SELECTED]
        //         && this.context[constants.URL_PARAM_SELECTED].length === 0),
        //     this.context.controller.disabled(action[constants.URL_PARAM_ACTION_NAME]),
        //     (action[constants.URL_PARAM_ACTION_NAME] === 'submit_detail' && !this.context.editing_mode),
        //     (this.props.onSide && !action.show_in_side_toolbar && action[constants.URL_PARAM_ACTION_NAME] !== 'submit_detail'),
        //     (this.props.nonCollapsibles && !action.never_collapse)
        // );
        icon_and_label.disabled = (
            (action.select_rows && this.context[constants.URL_PARAM_SELECTED]
                && this.context[constants.URL_PARAM_SELECTED].length === 0
            )
            || this.context.controller.disabled(action[constants.URL_PARAM_ACTION_NAME])
            || (action[constants.URL_PARAM_ACTION_NAME] === 'submit_detail' && !this.context.editing_mode)
            || (this.props.onSide && !action.show_in_side_toolbar && action[constants.URL_PARAM_ACTION_NAME] !== 'submit_detail')
            || (this.props.nonCollapsibles && !action.never_collapse)
        );
        icon_and_label.tooltip = tba.help_text || action.label;
        icon_and_label.tooltipOptions = {position: this.props.onSide ? 'left' : 'bottom'};

        return icon_and_label;
    }

    render_actionbutton(tba) {
        let {action} = this.context.controller.actionHandler.getAction(tba[constants.URL_PARAM_ACTION_NAME], false);
        if (action) {
            let icon_and_label = this.action2buttonProps(tba, action, true);
            if (icon_and_label.disabled) return
            return <this.ex.prButton.Button {...icon_and_label}
                key={Math.random()}
                onClick={(e) => this.runAction(action, tba, e)}/>
        } else {
        }
    }

    render_splitActionButton(combo) {
        let actionArray = combo.menu.map(
            n => this.context.controller.actionHandler.getAction(n[constants.URL_PARAM_ACTION_NAME], false).action);
        if (actionArray[0]) {
            let model = actionArray.map((action, i) => {
                let props = this.action2buttonProps(combo.menu[i], action, i === 0);
                props.command = (e) => this.runAction(action, combo.menu[i], e);
                return props;
            });
            let icon_and_label = this.ex._.default.cloneDeep(model[0]);
            if (icon_and_label.disabled) return
            let command = icon_and_label.command;
            delete icon_and_label.command;
            // if (model.length === 1) return <this.ex.prButton.Button
            //     {...icon_and_label}
            //     key={Math.random()}
            //     onClick={command}/>
            return <this.ex.prSplitButton.SplitButton
                {...icon_and_label}
                key={Math.random()}
                model={model}
                onClick={command}/>
        }
    }

    render_buttons() {
        let ba = this.context.controller.static.actorData.actions_list.find(ba => ba[constants.URL_PARAM_ACTION_NAME] === this.props.action_full_name);
        if (!ba) return;
        let tbas = ba.toolbarActions;
        return tbas && tbas.map((tba, i) => {
            if (tba.combo && tba.menu.length > 1) {
                return this.render_splitActionButton(tba);
            } else if (tba.combo) {
                return this.render_actionbutton(tba.menu[0]);
            } else {
                return this.render_actionbutton(tba);
            }
        })
    }

    render() {
        if (!this.state.ready) return null;
        return <React.Fragment>
            {this.props.resetable && <this.ex.prButton.Button
                icon="pi pi-refresh"
                onClick={e => {
                    const { actionHandler } = this.context.controller;
                    actionHandler.refresh();
                    actionHandler.refreshDelayedValue(true);
                }}
                tooltip={this.ex.i18n.t("Reload this view from the underlying database")}
                tooltipOptions={{position: "bottom"}}/>}
            {this.render_buttons()}
        </React.Fragment>
    }
};
