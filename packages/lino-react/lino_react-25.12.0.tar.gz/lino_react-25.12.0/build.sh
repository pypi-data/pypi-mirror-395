#!/bin/bash
npm run build
ln -s ../../../translations/extracts/i18n lino_react/react/static/react/locales
git add lino_react/react/static/react/
git add -u lino_react/react/config/react/main.html
