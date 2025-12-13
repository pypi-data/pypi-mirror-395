
// TODO: needs more work.
export type LeafInputProps = {
    urlParams: any;
    tabIndex: number;
    elem: any;
}

export type ParamsDynDep = StringKeyedObject & {
    next: (t: DynDep) => void;
}

export interface DynDep {
    exModules: StringKeyedObject;
    ex: StringKeyedObject;
    onReady: (params?: ParamsDynDep) => void;
}

export interface DynDepBase extends Omit<DynDep, 'onReady'> {
    ready: boolean;
    onReady: (params: ParamsDynDep) => void;
}

export type CellInfo = {
    rowIndex: number;
}

export type ContextType = "SingleRow" | "MultiRow" | "Action";

export type StringKeyedObject = {
    [propertyName: string]: any;
}

export type IntegerKeyedObject = {
    [propertyName: number]: any;
}

export type ObjectAny = StringKeyedObject & IntegerKeyedObject;

export type Data = ObjectAny;

export type ResponseCallback = (data: Data) => void;

export type ContextPath = {
    pathname: string;
    params?: ViewParams;
}

export type DisplayMode = (
    "grid"  // DISPLAY_MODE_TABLE = "grid"
    | "detail"  // DISPLAY_MODE_DETAIL = "detail"
    | "cards"  // DISPLAY_MODE_CARDS = "cards"
    | "list"  // DISPLAY_MODE_LIST = "list"
    | "gallery"  // DISPLAY_MODE_GALLERY = "gallery"
    | "story"  // DISPLAY_MODE_STORY = 'story'
    | "summary"  // DISPLAY_MODE_SUMMARY = "summary"
    | "tiles"  // DISPLAY_MODE_TILES = "tiles"
    | "html");  // DISPLAY_MODE_HTML = "html"
export type SortDirection = "ASC" | "DESC";
export type WindowType = (
    "d"  // WINDOW_TYPE_DETAIL = 'd'
    | "i"  // WINDOW_TYPE_INSERT = "i"
    | "p");  // WINDOW_TYPE_PARAMS = "p"
export type URLFormat = (
    "json"  // URL_FORMAT_JSON = 'json'
    | "html");  // URL_FORMAT_HTML = 'html'
export type GridFilter = {
    field: string;
    type: 'list' | 'string' | 'numeric' | 'boolean' | 'date';
    value: any;
    comparison?: 'exact' | 'lt' | 'gt';
}
export type QPWindowGlobals = {
    su?: number;  // URL_PARAM_SUBST_USER = 'su'
    ul?: string;  // URL_PARAM_USER_LANGUAGE = 'ul'
}
export type QPView = {
    query?: string;  // URL_PARAM_FILTER
    lv?: number;  // URL_PARAM_LINO_VERSION = "lv"
    wt?: WindowType;  // URL_PARAM_WINDOW_TYPE = 'wt'
    dm?: DisplayMode;  // URL_PARAM_DISPLAY_MODE = "dm";
    filter?: GridFilter[];  // URL_PARAM_GRIDFILTER = 'filter';
    sort?: string;  // URL_PARAM_SORT = 'sort';
    dir?: SortDirection;  // URL_PARAM_SORTDIR = 'dir' (direction?)
    start?: number;  // URL_PARAM_START = 'start'
    limit?: number;  // URL_PARAM_LIMIT = 'limit'
    sr?: number[] | [string];  // URL_PARAM_SELECTED = 'sr';
    fmt?: URLFormat;  // URL_PARAM_FORMAT = 'fmt'
    rp?: string;  // URL_PARAM_REQUESTING_PANEL = 'rp'
    mt?: number;  // URL_PARAM_MASTER_TYPE = 'mt'
    mk?: number | string;  // URL_PARAM_MASTER_PK = 'mk'
    an?: string;  // URL_PARAM_ACTION_NAME = 'an'
    pv?: any[];  // URL_PARAM_PARAM_VALUES = 'pv'
    cw?: number[];  // URL_PARAM_WIDTHS = 'cw'
    ch?: boolean[];  // URL_PARAM_HIDDENS = 'ch'
    ci?: string[];  // URL_PARAM_COLUMNS = 'ci'
}

export type QueryParams = QPWindowGlobals & QPView;

//TOOLBAR_STATE_HIDDEN | TOOLBAR_STATE_VISIBLE | TOOLBAR_STATE_PARTIALLY_VISIBLE
export type ToolbarState = "hidden" | "visible" | "partially-visible";

export type UIConfigParams = {
    editing_mode?: boolean;
    pvPVisible?: boolean;
    showableColumns?: Map<number, string>;
    sortField?: number;
    sortOrder?: number;
    tab?: number;
    toolbarState?: ToolbarState;
}

export type ContextBasics = {
    hasActor?: boolean;
    path?: string;
};

export type ViewParams = ContextBasics & UIConfigParams & QPView;

export type ContextParams = ViewParams & QPWindowGlobals;

export type StateClone = {
    clone: true;
    windowGlobals?: QPWindowGlobals;
    // params?: QueryParams & UIConfigParams & ContextBasics;
    params?: ViewParams;
    mutableData?: Data;
    immutableData?: Data;
    runnable?: ArgsRunAction;
    children?: {[propertyName: string]: StateClone}[];
};

export type ContextGlobals = {
    isMobile: boolean;
    currentInputIndex: number;
    currentInputRowIndex: null | number;
    currentInputWindowType: null | string;
    currentInputAHRefName: string;
}

export type DataParams = PreprocessedStack & Data;

export type ArgsFetchXHR = {
    body?: DataParams;
    path: string;
    response_callback?: ResponseCallback;
    signal?: any;
    silent?: boolean;
}

export type ArgsNavigationContext = {
    APP: APP;
    iPool: iPool;
    value?: StringKeyedObject;
    root?: any;
}
export type NavigationContext = any;
export type NavigationContextValue = ObjectAny & {
    controller?: NavigationContext;
}

export type ArgsActionResponse = {
    response: any;
    response_callback?: ResponseCallback;
}

export type BaseParams = {
    mk?: number | string;
    mt?: number;
}

export type Status = {
    rqdata?: any;
    xcallback?: any;
    data?: any;
    record_id?: number;
    base_params?: BaseParams;
    param_values?: StringKeyedObject;
    fv?: any[];
    data_record?: any;
    field_values?: any;
    clickCatch?: boolean;
}

export type Action = {
    an: string;
    full_name: string;
    preprocessor?: string;
    select_rows?: boolean;
    window_action?: boolean;
    auto_save?: boolean;
}

export type ArgsRunAction = {
    action_full_name: string;
    actorId: string;
    default_record_id?: string | number;
    response_callback?: ResponseCallback;
    rowIndex?: number | 'detail';
    status?: Status;
    sr?: number[] | [string];
    clickCatch?: boolean;
    pollContext?: boolean;
}

export type ArgsExecute = {
    action?: any;
    actorId?: string;
    response_callback?: ResponseCallback;
    rowIndex?: number | 'detail';
    status?: Status;
    preprocessedStack?: PreprocessedStack;
    pollContext?: boolean;
}

export interface URLParser extends DynDepBase {
    parseShallow: (s: string, options?: {sanitizeValue?: boolean}) => ObjectAny;
    parse: (s: string, options?: {sanitizeValue?: boolean}) => ObjectAny;
    sanitize: (v: any) => any;
    sanitizeArrayUnparse: (array: any[]) => any[];
    stringify: (object: ObjectAny, usePrefix?: boolean) => string;
}

export type reload = () => null;

export type Reloadable = {reload: reload;}

export type Reloadables = {
    [propertyName: string]: Reloadable;
}

export interface ActionHandler extends DynDepBase {
    context: NavigationContext;
    executeAction: (obj: ArgsExecute) => void;
    fetch: (args: ArgsFetchXHR) => Promise<Data>;
    parser: URLParser;
    refName: string;
    runAction: (obj: ArgsRunAction) => void;
    abortController: any;
    reloadables: Reloadables;
}

export type ArgsDialogCreate = {
    action?: any;
    actorID: string;
    actionHandler: ActionHandler;
    execute_args?: ArgsExecute;
}

/** Works only with action_dialog(s) */
export type PreprocessorCallback = {
    callback: (windowId: string) => void;
    callbackType: "postWindowInit";
}

export type PreprocessedStack = QueryParams & {
    image?: string;
    callback?: PreprocessorCallback;
};

export type preprocessor = (
    context: NavigationContext, preprocessedStack: PreprocessedStack) => PreprocessedStack;

export type Lino = {
    captureImage?: preprocessor;
    get_current_grid_config?: preprocessor;
    lv?: number;
    site_name?: string;
    testRuntime?: boolean;
}

declare global {
    interface Window {
        Lino: Lino;
        App: any;
    }
}

export type APP = any;

export type iPool = any;

export type LeafComponentRef = {
    name: string | number;  // elem.name | elem.fields_index
    ref: any;
    type: 'virtual' | 'slave' | '';  // '' string means regular
    input?: boolean;  // specifies whether the component has editing features.
}

export type WebcamSettings = {
    width: number;
    height: number;
    pixelRatio: number;
    mirrored: boolean;
}

export type Settings = {
    webcam?: WebcamSettings;
}

export type ElemLMin = {
    label: string;
    value?: {quicktip?: string};
    help_text?: string;
}

export type PropValidateRestArgs = [
    propName: string,
    componentName: string,
    location: string,
    propFullName: string
];

export interface LeafComponentInput {
    dataKey: string | number;
    getValue: () => any;
    leafIndexMatch: () => boolean;
    update: (values: ObjectAny) => void;
};
