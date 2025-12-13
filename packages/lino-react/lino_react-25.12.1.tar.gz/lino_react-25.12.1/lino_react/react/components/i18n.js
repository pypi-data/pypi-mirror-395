import { URL_PARAM_USER_LANGUAGE, PARAM_TYPE_WINDOW } from './constants';
import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import HttpApi from "i18next-http-backend";
import { initReactI18next } from "react-i18next";


export const TransInit = (context, next) => {
    const detector = new LanguageDetector();
    detector.addDetector({
        name: "LinoLanguageDetector",
        lookup: (options) => {
            return context.value[URL_PARAM_USER_LANGUAGE];
        },
        cacheUserLanguage(lng, options) {
            context.fillPlaceHolder(PARAM_TYPE_WINDOW, URL_PARAM_USER_LANGUAGE, lng);
            context.history.replaceByType({[URL_PARAM_USER_LANGUAGE]: lng},
                PARAM_TYPE_WINDOW, false, true);
        }
    });

    i18n
    .use(HttpApi)
    .use(detector)
    .use(initReactI18next)
    .init({
        debug: false,
        load: "languageOnly",
        fallbackLng: window.Lino.i18nFallbackLng,
        keySeparator: false,
        interpolation: {
          escapeValue: false // react already safes from xss
        },
        react: {
            useSuspense: true
        },
        backend: {
            loadPath: "/static/react/locales/{{lng}}/{{ns}}.json",
            // addPath: "/static/react/locales/{{lng}}/{{ns}}.json"
        },
        detection: {
            order: ["queryString", "cookie", "LinoLanguageDetector", "localStorage"],
            lookupQuerystring: URL_PARAM_USER_LANGUAGE,
            lookupCookie: URL_PARAM_USER_LANGUAGE,
            lookupLocalStorage: URL_PARAM_USER_LANGUAGE,
            // lookupSessionStorage: URL_PARAM_USER_LANGUAGE
            caches: ["LinoLanguageDetector", "localStorage", "cookie"],
        }
    });

    next(i18n);
}


export default i18n;
