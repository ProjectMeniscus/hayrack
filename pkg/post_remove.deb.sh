#!/bin/sh
# postrm script for hayrack
#
# see: dh_installdeb(1)

set -e

# summary of how this script can be called:
#        * <postrm> `remove'
#        * <postrm> `purge'
#        * <old-postrm> `upgrade' <new-version>
#        * <new-postrm> `failed-upgrade' <old-version>
#        * <new-postrm> `abort-install'
#        * <new-postrm> `abort-install' <old-version>
#        * <new-postrm> `abort-upgrade' <old-version>
#        * <disappearer's-postrm> `disappear' <overwriter>
#          <overwriter-version>
# for details, see http://www.debian.org/doc/debian-policy/ or
# the debian-policy package


case "$1" in
        purge)
        echo "Purging hayrack..." >&2
        if (getent passwd hayrack) > /dev/null 2>&1; then
            userdel hayrack || true
        fi

        if (getent group hayrack) > /dev/null 2>&1; then
            groupdel hayrack || true
        fi

        [ -e /var/log/hayrack ] && rm -rf /var/log/hayrack
        [ -e /usr/share/hayrack ] && rm -rf /usr/share/hayrack
        [ -e /etc/hayrack ] && rm -rf /etc/hayrack
        ;;

    upgrade|failed-upgrade|abort-upgrade)
        echo "upgrade ignored"
    ;;

    remove|abort-install|disappear)
        [ -e /usr/share/hayrack ] && rm -rf /usr/share/hayrack
    ;;

    *)
        echo "postrm called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac

exit 0