==================================
Jest puppeteer testing environment
==================================

Run before testing::

    $ a  # activate virtual environment
    $ echo 0 | sudo tee /proc/sys/kernel/apparmor_restrict_unprivileged_userns

Run after testing::

    $ echo 1 | sudo tee /proc/sys/kernel/apparmor_restrict_unprivileged_userns

See: `AppArmor User Namespace Restrictions <https://chromium.googlesource.com/chromium/src/+/main/docs/security/apparmor-userns-restrictions.md>`_.

Run test on top of server hosting a lino site::

    $ BASE_SITE=avanti npm test
    $ BASE_SITE=noi npm test
