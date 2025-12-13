// See: https://gitlab.com/lino-framework/lino/-/blob/master/lino/core/constants.py

export const URL_PARAM_LINO_VERSION = "lv";
export const URL_PARAM_MAIN_JS_TIMESTAMP = "mjsts";

export const URL_PARAM_WINDOW_TYPE = 'wt';

export const WINDOW_TYPE_TABLE = 't';
export const WINDOW_TYPE_DETAIL = 'd';
export const WINDOW_TYPE_CARDS = 'c';
export const WINDOW_TYPE_GALLERIA = 'g';
export const WINDOW_TYPE_INSERT = "i";
export const WINDOW_TYPE_PARAMS = "p";
export const WINDOW_TYPE_TEXT = "text";
export const WINDOW_TYPE_UNKNOWN = null;

export const URL_PARAM_DISPLAY_MODE = "dm";

export const DISPLAY_MODE_TABLE = "grid";
export const DISPLAY_MODE_DETAIL = "detail";
export const DISPLAY_MODE_CARDS = "cards";
export const DISPLAY_MODE_LIST = "list";
export const DISPLAY_MODE_GALLERY = "gallery";
export const DISPLAY_MODE_STORY = 'story';
export const DISPLAY_MODE_SUMMARY = "summary";
export const DISPLAY_MODE_HTML = "html";
export const DISPLAY_MODE_TILES = "tiles";

export const DM_WT_MAP = {
	[DISPLAY_MODE_TABLE]: WINDOW_TYPE_TABLE,
	[DISPLAY_MODE_DETAIL]: WINDOW_TYPE_DETAIL,
	[DISPLAY_MODE_CARDS]: WINDOW_TYPE_CARDS,
	[DISPLAY_MODE_LIST]: null,
	[DISPLAY_MODE_GALLERY]: WINDOW_TYPE_GALLERIA,
	[DISPLAY_MODE_STORY]: null,
	[DISPLAY_MODE_SUMMARY]: null,
	[DISPLAY_MODE_HTML]: null,
	[DISPLAY_MODE_TILES]: null,
}

export const URL_PARAM_SUBST_USER = 'su';
export const URL_PARAM_GRIDFILTER = 'filter';
export const URL_PARAM_FILTER = 'query';
export const URL_PARAM_TAB = 'tab';
export const URL_PARAM_SORT = 'sort';
export const URL_PARAM_SORTDIR = 'dir';
export const URL_PARAM_START = 'start';
export const URL_PARAM_LIMIT = 'limit';
export const URL_PARAM_SELECTED = 'sr';
export const URL_PARAM_FORMAT = 'fmt';
export const URL_PARAM_REQUESTING_PANEL = 'rp';
export const URL_PARAM_MASTER_TYPE = 'mt';
export const URL_PARAM_MASTER_PK = 'mk';
export const URL_PARAM_ACTION_NAME = 'an';
export const URL_PARAM_PARAM_VALUES = 'pv';

export const URL_FORMAT_JSON = 'json';
export const URL_FORMAT_HTML = 'html';

export const URL_PARAM_USER_LANGUAGE = 'ul';

export const URL_PARAM_WIDTHS = 'cw';
export const URL_PARAM_HIDDENS = 'ch';
export const URL_PARAM_COLUMNS = 'ci';

export const CHOICES_TEXT_FIELD = 'text';
export const CHOICES_VALUE_FIELD = 'value';
export const CHOICES_HIDDEN_SUFFIX = "Hidden";

export const CHOICES_BLANK_FILTER_VALUE = "<BLANK>";
export const CHOICES_NOT_BLANK_FILTER_VALUE ="<!BLANK>";

export const ACTION_DISCARD_EDIT = [
	'submit_detail',
	'delete_selected'
]

export const GUI_PARAMS = [
	'tab'
]

export const TOOLBAR_STATE_HIDDEN = "hidden";
export const TOOLBAR_STATE_VISIBLE = "visible";
export const TOOLBAR_STATE_PARTIALLY_VISIBLE = "partially-visible";
export const TOOLBAR_STATES_ORDER = [
	TOOLBAR_STATE_VISIBLE,
	TOOLBAR_STATE_PARTIALLY_VISIBLE,
	TOOLBAR_STATE_HIDDEN
]

export const DANGEROUS_HTML = true;

export const CONTEXT_TYPE_SINGLE_ROW = "SingleRow";
export const CONTEXT_TYPE_MULTI_ROW = "MultiRow";
export const CONTEXT_TYPE_TEXT_FIELD = "TextField";
export const CONTEXT_TYPE_ACTION = "Action";
export const CONTEXT_TYPE_SLAVE_GRID = "SlaveGrid";

export const FLAG_CLONE_URL = 1;
export const FLAG_CLONE_UI = 1 << 1;
export const FLAG_CLONE_DATA = 1 << 2;

export const UNINITIALIZED = {};

// WEB_SOCKET_MESSAGE_TYPE
export const WSM_TYPE = {
	NOTIFICATION: 'NOTIFICATION',
	CHAT: 'CHAT',
	LIVE_PANEL_UPDATE: 'PANEL_UPDATE'
}

export const PRIMARY_KEY_MYSELF = 'myself';
export const PRIMARY_KEY_ROW = 'row';

export const ABSTRACT_PRIMARY_KEYS = [
	PRIMARY_KEY_MYSELF, PRIMARY_KEY_ROW
]

export const PARAM_TYPE_GLOBAL = "site-globals";
export const PARAM_TYPE_WINDOW = "window-globals";
export const PARAM_TYPE_VIEW = "view-params";
export const PARAM_TYPE_IMPLICIT = "implicit";

export const SITE_GLOBALS_KEYS = [
	"latestWID"
];

export const WINDOW_GLOBALS_KEYS = [
	URL_PARAM_SUBST_USER, URL_PARAM_USER_LANGUAGE
];

// export const PINNED_URL_STORE_KEY = "pinned-urls";

export const DATE_EXP = /^\d{2}.\d{2}.(\d{2}|\d{4})$/;
export const TIME_EXP = /^\d*:(\d{2})$/;

export const STR_JSON_ITENT = "JSON:::";

export const LOGLEVEL_INFO = 1;
export const LOGLEVEL_DEBUG = 2;


export function debugMessage(...args) {
	// eslint-disable-next-line no-undef
	if (LINO_LOGLEVEL >= LOGLEVEL_DEBUG) {
		console.log(...args);
	}
}
