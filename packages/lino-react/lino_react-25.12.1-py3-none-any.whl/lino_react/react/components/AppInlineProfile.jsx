export const name = "AppInlineProfile";

import * as constants from "./constants";
import React from "react";
import PropTypes from "prop-types";
import { RegisterImportPool, Component } from "./Base";

let ex; const exModulePromises = ex = {
    prOverlayPanel: import(/* webpackChunkName: "prOverlayPanel_AppInlineProfile" */"primereact/overlaypanel"),
    prCard: import(/* webpackChunkName: "prCard_AppInlineProfile" */"primereact/card"),
    prButton: import(/* webpackChunkName: "prButton_AppInlineProfile" */"primereact/button"),
    prInputText: import(/* webpackChunkName: "prInputText_AppInlineProfile" */"primereact/inputtext"),
    i18n: import(/* webpackChunkName: "i18n_AppInlineProfile" */"./i18n"),
};RegisterImportPool(ex);


const THEME_NAMES = [
    'arya-blue',
    'arya-green',
    'arya-orange',
    'arya-purple',
    'bootstrap4-dark-blue',
    'bootstrap4-dark-purple',
    'bootstrap4-light-blue',
    'bootstrap4-light-purple',
    'fluent-light',
    'lara-dark-amber',
    'lara-dark-blue',
    'lara-dark-cyan',
    'lara-dark-green',
    'lara-dark-indigo',
    'lara-dark-pink',
    'lara-dark-purple',
    'lara-dark-teal',
    'lara-light-amber',
    'lara-light-blue',
    'lara-light-cyan',
    'lara-light-green',
    'lara-light-indigo',
    'lara-light-pink',
    'lara-light-purple',
    'lara-light-teal',
    'luna-amber',
    'luna-blue',
    'luna-green',
    'luna-pink',
    'md-dark-deeppurple',
    'md-dark-indigo',
    'md-light-deeppurple',
    'md-light-indigo',
    'mdc-dark-deeppurple',
    'mdc-dark-indigo',
    'mdc-light-deeppurple',
    'mdc-light-indigo',
    'mira',
    'nano',
    'nova',
    'nova-accent',
    'nova-alt',
    'rhea',
    'saga-blue',
    'saga-green',
    'saga-orange',
    'saga-purple',
    'soho-dark',
    'soho-light',
    'tailwind-light',
    'vela-blue',
    'vela-green',
    'vela-orange',
    'vela-purple',
    'viva-dark',
    'viva-light'
]


export class AppInlineProfile extends Component {
    static requiredModules = ["prOverlayPanel", "prCard", "prButton", "i18n",
        "prInputText"];
    static iPool = ex;

    static propTypes = {
        URLContext: PropTypes.object.isRequired,
    };

    async prepare() {
        await super.prepare();
        this.i18n = this.ex.i18n.default;
        this.InputText = this.ex.prInputText.InputText;
        this.Button = this.ex.prButton.Button;
        this.Card = this.ex.prCard.Card;
        this.OverlayPanel = this.ex.prOverlayPanel.OverlayPanel;
    }

    constructor(props) {
        super(props);
        this.upController = props.URLContext;
        this.c = props.URLContext;
        this.state = {...this.state, expanded: false, newPinNick: "",
            pinnedURLQuota: 10, pinnedURLs: {RSs: [], nicks: {}}};
        this.onClick = this.onClick.bind(this);
    }

    onClick(event) {
        if (this.pop) this.pop.toggle(event);
        this.setState({expanded: !this.state.expanded});
        event.preventDefault();
    }

    async switchSubstUser(su_id) {
        await this.c.history.replaceByType(
            {[constants.URL_PARAM_SUBST_USER]: su_id},
            constants.PARAM_TYPE_WINDOW, false, true);
        this.c.APP.reset();
        // We assume that it's equivalent to signIn, since we use a new user.
        // this.c.APP.reset(true);
    }

    renderActAsOverLay() {
        const { c } = this;
        const {act_as_title_text, act_as_subtext} = c.APP.state.user_settings;
        return <this.OverlayPanel ref={(el) => this.op = el} appendTo={c.APP.topDiv} className={"l-actas"}>
            <this.Card title={act_as_title_text} subTitle={act_as_subtext}>
                {c.APP.state.user_settings.authorities.map(auth =>
                    <React.Fragment key={auth[0]}>
                        <this.Button label={auth[1]} onClick={async (e) => {
                            this.op.hide();
                            await this.switchSubstUser(auth[0]);
                        }}/>
                        <br/>
                    </React.Fragment>
                )}
            </this.Card>
        </this.OverlayPanel>
    }

    /*
    renderURLPinsOverlay(c) {
        const removePin = (rs) => {
            const pURLs = {...this.state.pinnedURLs};
            delete pURLs.nicks[rs];
            pURLs.RSs = pURLs.RSs.filter(rs_ => rs !== rs_);
            c.history.putState(constants.PINNED_URL_STORE_KEY, pURLs);
            this.setState({pinnedURLs: pURLs});
        }
        const addPin = () => {
            const pURLs = {...this.state.pinnedURLs};
            pURLs.RSs.unshift(c.value.rs);
            pURLs.nicks[c.value.rs] = this.state.newPinNick;
            c.history.putState(constants.PINNED_URL_STORE_KEY, pURLs);
            this.setState({pinnedURLs: pURLs, newPinNick: ""});
            this.pURLop.hide();
        }
        return <this.OverlayPanel ref={ref => this.pURLop = ref}>
            {this.state.pinnedURLs.RSs.includes(c.value.rs) ? null :
                this.state.pinnedURLs.RSs.length < this.state.pinnedURLQuota ?
                    <div><div><label htmlFor="url-pin-input">{this.i18n.t(
                        "Pin current context (rs={{rs}})$t(colonSpaced)",
                        {rs: c.value.rs})}</label></div>
                    <this.InputText
                        id="url-pin-input" value={this.state.newPinNick}
                        onKeyDown={e => {if (e.key === "Enter") addPin()}}
                        placeholder={this.i18n.t("Nickname")}
                        onChange={e => this.setState({newPinNick: e.target.value})}/>
                    <this.Button icon="pi pi-star" style={{float: "right"}}
                        disabled={!c.filled(this.state.newPinNick)}
                        onClick={e => addPin()}/></div>
                    : <p style={{color: "red"}}>{
                        this.i18n.t("Pin quota limit ({{quota}}) reached",
                            {quota: this.state.pinnedURLQuota})}</p>
            }
            {this.state.pinnedURLs.RSs.map(rs => (<React.Fragment key={rs}>
                <hr/><div style={{display: "flex"}}>
                <this.Button
                    disabled={rs === c.value.rs}
                    icon="pi pi-external-link"
                    label={`${this.state.pinnedURLs.nicks[rs]} (rs=${rs})`}
                    onClick={(e) => {
                        if (c.history.has(rs)) {
                            this.pURLop.hide();
                            c.history.load({rs});
                        } else {
                            c.APP.toast.show({severity: "warn",
                                summary: this.i18n.t("Record lost, removing pin")});
                            removePin(rs);
                        }
                    }}
                    style={{background: "rgb(108, 137, 153)", flexGrow: "1"}}/>
                <this.Button icon="pi pi-trash" style={{float: "right"}}
                    onClick={e => removePin(rs)}/>
            </div></React.Fragment>))}
        </this.OverlayPanel>
    }
    */

    render() {
        if (!this.state.ready) return null;
        const { c } = this;
        const { APP, value } = c;
        const su_id = value[constants.URL_PARAM_SUBST_USER];
        let { username } = APP.state.user_settings;
        const {
            act_as_button_text, act_as_self_text, my_setting_text, su_name
        } = APP.state.user_settings;
        if (su_name)
            username = this.i18n.t(
                "{{username}} acting as {{su_name}}", {username, su_name});
        const _lang = value[constants.URL_PARAM_USER_LANGUAGE];
        return <div className="profile">
        <div id="pinned-url-container"></div>
        {/*
            {!c.globals.isMobile && <><this.Button
                label={this.i18n.t("Pinned URL(s)")}
                icon="pi pi-caret-down" iconPos="right"
                onClick={e => {
                    const pURLs = c.history.getState(constants.PINNED_URL_STORE_KEY);
                    if (c.filled(pURLs)) this.setState({pinnedURLs: pURLs});
                    this.pURLop.toggle(e);
                }}/>
                <span> | </span>
                {this.renderURLPinsOverlay(c)}
            </>}
          */}
            <span> | </span>
            <span
                className="l-span-clickable"
                onClick={e => APP.reload()}
                // style={{color: 'black'}}
                title={this.i18n.t("Clear site cache & URL parameters")}>
                &nbsp;⎚&nbsp;
            </span>
            {Object.keys(App.state.site_data.languages).length > 1 && <>
                <span> | </span>
                <this.Button
                    label={APP.state.site_data.languages[_lang]}
                    onClick={e => this.lsop.toggle(e)}/></>
            }
            <span> | </span>
            <this.OverlayPanel ref={ref => this.lsop = ref}>
                {Object.keys(APP.state.site_data.languages).filter(key => key != _lang).map(django_code =>
                    <React.Fragment key={django_code}>
                        <this.ex.prButton.Button
                            label={APP.state.site_data.languages[django_code]}
                            onClick={async (e) => {
                                APP.setLoadMask();
                                this.i18n.changeLanguage(django_code);
                                this.lsop.hide();
                                APP.reset();
                            }}/>
                        <br />
                    </React.Fragment>
                )}
            </this.OverlayPanel>
            {!APP.state.user_settings.logged_in ? <React.Fragment>
                <this.Button
                    icon="pi pi-power-off"
                    label={this.i18n.t("Sign in")}
                    onClick={APP.onSignOutIn}/>
                {APP.state.site_data.allow_online_registration && <this.Button
                    icon="pi pi-plus-circle"
                    label={this.i18n.t("Create account")}
                    onClick={APP.createAccount}/>}
            </React.Fragment> : <React.Fragment>
                <this.Button
                    // icon="pi pi-cog"
                    // iconPos="right"
                    // label={username}
                    label="👤"  // u+1F464
                    onClick={this.onClick}
                    tooltip={username}
                    tooltipOptions={{position: "left"}}/>
                {<this.OverlayPanel ref={ref => this.pop = ref}>
                    <this.Button
                        icon="pi pi-power-off"
                        label={this.i18n.t("Sign out")}
                        onClick={APP.onSignOutIn}/>
                    <br />
                    {su_id && <this.Button
                        icon="pi pi-user"
                        label={act_as_self_text}
                        onClick={async (e) => (await this.switchSubstUser(undefined))}/>}
                    <br />
                    {APP.state.user_settings.authorities.length > 0 && <this.Button
                        icon="pi pi-users"
                        label={act_as_button_text}
                        onClick={(e) => {
                            e.target = this.actAsEl;
                            this.op.toggle(e)
                        }}
                        ref={(el) => this.actAsEl = el}/>}
                    <br />
                    <this.Button
                        icon="pi pi-sliders-v"
                        label={my_setting_text}
                        onClick={APP.onMysettings}/>
                </this.OverlayPanel>}
                {this.renderActAsOverLay()}
            </React.Fragment>}
        </div>
    }
}
