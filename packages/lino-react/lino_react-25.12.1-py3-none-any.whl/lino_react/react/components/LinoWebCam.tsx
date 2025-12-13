// LinoWebCam.tsx
/** @module LinoWebCam */

export const name: string = "LinoWebCam";

// @ts-ignore
import * as React from 'react';
// @ts-ignore
import PropTypes from 'prop-types';
import * as t from './types';
import { RegisterImportPool, getExReady, URLContextType } from "./Base";

// @ts-ignore
import Webcam from "react-webcam";

let ex; const exModulePromises = ex = {
    // @ts-ignore
    prButton: import(/* webpackChunkName: "prButton_LinoWebCam" */"primereact/button"),
    // @ts-ignore
    prOverlayPanel: import(/* webpackChunkName: "prOverlayPanel_LinoWebCam" */"primereact/overlaypanel"),
    // @ts-ignore
    prInputNumber: import(/* webpackChunkName: "prInputNumber_LinoWebCam" */"primereact/inputnumber"),
    // @ts-ignore
    prInputSwitch: import(/* webpackChunkName: "prInputSwitch_LinoWebCam" */"primereact/inputswitch"),
    // @ts-ignore
    lcu: import(/* webpackChunkName: "LinoComponentUtils_LinoWebCam" */"./LinoComponentUtils"),
    // @ts-ignore
    i18n: import(/* webpackChunkName: "i18n_LinoWebCam" */"./i18n"),
};RegisterImportPool(ex);

type WebcamState = {
    err_msg?: null | string;
    deviceId?: null | string;
    devices?: string[];
}

type WCReferences = {
    capture?: React.MouseEventHandler<HTMLElement>;
    props?: LinoWebCamProps;
    self?: CamController;
    setState?: Function;
    state?: WebcamState;
    switchCamera?: React.MouseEventHandler<HTMLElement>;
    webcamRef?: React.RefObject<Webcam>;
}

interface CamController {
    buildMediaConstraints(): MediaTrackConstraints;
    mediaTrackConstraints: MediaTrackConstraints;
    store: WCReferences;
    settings: t.WebcamSettings;
    settingsMod: t.WebcamSettings;
}

class CamController implements CamController {
    static buildReferences = (store: WCReferences): WCReferences => {
        store.webcamRef = React.useRef(null);
        store.capture = React.useCallback(
            (event) => {
                store.props.captureDone(store.webcamRef.current.getScreenshot());
            },
        [store.webcamRef]);

        const [state, setState] = React.useState<WebcamState>({
            err_msg: null, deviceId: null, devices: []});

        store.state = state;
        store.setState = React.useCallback((st: WebcamState) =>
            setState((old: WebcamState) => Object.assign({}, old, st)), []);

        store.switchCamera = React.useCallback(
            event => {
                let i = (state.devices.indexOf(state.deviceId) + 1) % state.devices.length;
                store.setState({deviceId: state.devices[i]});
            },
        []);
        return store;
    }

    constructor(store: WCReferences) {
        this.store = store;
        this.buildMediaConstraints();
    }

    buildMediaConstraints(): MediaTrackConstraints {
        const constraints: MediaTrackConstraints = {};
        this.settings = window.App.getSettings().webcam;
        if (this.settings !== undefined) {
            constraints.height = this.settings.height;
            constraints.width = this.settings.width;
        } else {
            constraints.height = this.store.props.height * devicePixelRatio;
            constraints.width = this.store.props.width * devicePixelRatio;
            this.settings = Object.assign({}, constraints as t.WebcamSettings, {pixelRatio: devicePixelRatio, mirrored: true});
            window.App.setSettings({webcam: this.settings});
        }
        this.settingsMod = {...this.settings};
        if (this.store.state.deviceId) constraints.deviceId = this.store.state.deviceId
        else constraints.facingMode = "environment";
        this.mediaTrackConstraints = constraints;
        return constraints;
    }
}

type LinoWebCamProps = {
    captureDone: (data: string) => void;
    height: number;
    width: number;
}

type CamSettingsProps = {CC: CamController};

const CamSettings: React.FC<CamSettingsProps> = (props) => {
    const {settings, settingsMod} = props.CC;
    const [mirrored, setMirrored] = React.useState<boolean>(settings.mirrored);
    const localEx = getExReady(ex, ["prInputNumber", "prInputSwitch", "lcu", "i18n"]);
    const getInput = React.useCallback(
        ({label, max = null, min, onValueChange, suffix, value}) => (<div>
            <localEx.lcu.Labeled elem={{label: label}}>
                <localEx.prInputNumber.InputNumber buttonLayout="horizontal"
                    max={max} min={min} onValueChange={onValueChange}
                    showButtons={true} suffix={suffix} value={value}/>
            </localEx.lcu.Labeled></div>), [localEx]);
    return !localEx.ready ? null : <>
        {// TODO: interpolation translate
            getInput({label: 'Height (# > 512)', max: props.CC.store.props.height,
            min: 512, onValueChange: (e) => Object.assign(settingsMod,
                {height: e.value * settingsMod.pixelRatio}),
            suffix: 'px', value: settings.height / settings.pixelRatio})}
        <br/>
        {getInput({label: 'Width (# > 512)', max: props.CC.store.props.width,
            min: 512, onValueChange: (e) => Object.assign(settingsMod,
                {width: e.value * settingsMod.pixelRatio}),
            suffix: 'px', value: settings.width / settings.pixelRatio})}
        <br/>
        {getInput({label: 'Pixel ratio (# > 1)', min: 1, onValueChange: (e) => {
                Object.assign(settingsMod, {
                    height: (settingsMod.height / settingsMod.pixelRatio) * e.value,
                    width: (settingsMod.width / settingsMod.pixelRatio) * e.value,
                    pixelRatio: e.value});
            }, suffix: 'dpr', value: settings.pixelRatio})}
        <br/>
        <div>
            <localEx.lcu.Labeled elem={{label: localEx.i18n.t("Mirrored")}}>
                <localEx.prInputSwitch.InputSwitch
                    checked={mirrored}
                    onChange={e => {
                        setMirrored(e.value);
                        Object.assign(settingsMod, {mirrored: e.value});
                    }}/>
            </localEx.lcu.Labeled>
        </div>
    </>
};CamSettings.propTypes = {CC: PropTypes.instanceOf(CamController).isRequired};

type CamActionsProps = {CC: CamController};

const CamActions: React.FC<CamActionsProps> = (props) => {
    const opRef = React.useRef(null);
    const buttonStyle = {background: "white", color: "black",
        borderRadius: "50%", width: "5ch", height: "5ch", margin: "5px"};
    const localEx = getExReady(ex, ["prButton", "prOverlayPanel"]);
    return !localEx.ready ? null : <><localEx.prButton.Button
        icon="pi pi-camera"
        onClick={props.CC.store.capture}
        style={buttonStyle}/>
    {props.CC.store.state.devices.length > 1 &&
        <localEx.prButton.Button
            icon="pi pi-undo"
            onClick={props.CC.store.switchCamera}
            style={buttonStyle}/>}
    <localEx.prButton.Button
        icon="pi pi-cog"
        onClick={e => opRef.current.toggle(e)}
        style={buttonStyle}/>
    <div onKeyDown={e => e.stopPropagation()}>
        <localEx.prOverlayPanel.OverlayPanel
            onHide={e => {
                // @ts-ignore
                document.activeElement.blur();
                window.App.setSettings({webcam: props.CC.settingsMod});
                props.CC.buildMediaConstraints();
                props.CC.store.setState({});
            }}
            onShow={e => opRef.current.align()}
            ref={opRef}
            showCloseIcon={true}>
            <CamSettings CC={props.CC}/>
        </localEx.prOverlayPanel.OverlayPanel>
    </div></>
};CamActions.propTypes = {CC: PropTypes.instanceOf(CamController).isRequired};

export const LinoWebCam: React.FC = (props: LinoWebCamProps) => {
    const store: React.RefObject<WCReferences> = React.useRef({props: props});
    CamController.buildReferences(store.current);

    const { state, setState } = store.current;

    React.useEffect(() => {
        // @ts-ignore
        document.activeElement.blur();
        store.current.self = new CamController(store.current);
        navigator.mediaDevices.enumerateDevices().then(devs => setState(
            {devices: devs.filter(
                ({kind}) => kind === "videoinput").map(d => d.deviceId)}));
    }, []);

    const { self } = store.current;

    return !state.devices.length ? null : <>
        <div style={{position: 'absolute'}}>{state.err_msg}</div>
        <Webcam
            audio={false}
            forceScreenshotSourceSize={true}
            height={self.settings.height / self.settings.pixelRatio}
            mirrored={self.settings.mirrored}
            onUserMedia={uM => {
                if (state.deviceId === null)
                    setState({deviceId: uM.getVideoTracks()[0].getSettings().deviceId})}}
            onUserMediaError={exempt => {
                if (state.err_msg === null) setState({err_msg:
                    "Please allow camera access to take a photo."})}}
            ref={store.current.webcamRef}
            screenshotFormat="image/jpeg"
            videoConstraints={self.mediaTrackConstraints}
            width={self.settings.width / self.settings.pixelRatio}
            />
        <div
            style={{position: "absolute", bottom: "40px", left: "50%",
                transform: "translate(-50%, 0)"}}>
            <CamActions CC={self}/>
        </div>
    </>
}


LinoWebCam.propTypes = {
    height: PropTypes.number.isRequired,
    width: PropTypes.number.isRequired,
    captureDone: PropTypes.func.isRequired,
}
