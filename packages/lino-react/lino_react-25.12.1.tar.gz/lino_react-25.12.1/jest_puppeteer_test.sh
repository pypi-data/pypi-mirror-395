#!/usr/bin/env bash

echo 0 | sudo tee /proc/sys/kernel/apparmor_restrict_unprivileged_userns;

if [ "$1" != "skipprep" ] ; then
	python puppeteers/avanti/manage.py prep --noinput
	python puppeteers/noi/manage.py prep --noinput
fi

BASE_SITE=avanti npm run itest
BASE_SITE=noi npm run itest

echo 1 | sudo tee /proc/sys/kernel/apparmor_restrict_unprivileged_userns;
