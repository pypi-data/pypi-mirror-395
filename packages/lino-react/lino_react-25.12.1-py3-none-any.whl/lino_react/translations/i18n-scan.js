const path = require('path');
const vfs = require('vinyl-fs');
const scanner = require('i18next-scanner');

const setDefaultValue = (lang, ns, key, options) => (options.defaultValue || key);
// const setDefaultValue = (lang, ns, key, options) => {
//     if (key === 'Sort By{{colonSpaced}}{{value}}')
//         console.log(lang, ns, key, options);
//     return options.defaultValue || key;
// }

// vfs.src([path.join(__dirname, '../react/components/*.(js|jsx|ts|tsx)')])
vfs.src([path.join(__dirname, '../react/static/react/main*.js')])
    .pipe(scanner({
        // See: options -> https://github.com/i18next/i18next-scanner#options
        defaultValue: setDefaultValue,
        removeUnusedKeys: true,
        lngs: ['en', 'bn', 'de', 'fr', 'et'],
        resource: {
            loadPath: path.join(__dirname, 'extracts/i18n/{{lng}}/{{ns}}.json'),
            savePath: 'extracts/i18n/{{lng}}/{{ns}}.json',
        }
    }))
    .pipe(vfs.dest(__dirname));
