#!/usr/bin/env python3
import sys
import os


def mkdir(path, owner=101, group=101):
    path = path.strip().rstrip('/')
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            return False

    os.chown(path, owner, group)
    return True

"""@Deprecated"""
if __name__ == '__main__':
    # Create directories
    pkg = '/usr/lib/python3/dist-packages/odoo'
    conf = '/etc/odoo'
    var = '/var/lib/odoo'
    extra = '/mnt/extra-addons'
    ok = mkdir(pkg) and mkdir(conf) and mkdir(var) and mkdir(extra)

    if not ok:
        print("Create directorys failure.", file=sys.stderr)
        sys.exit(1)

    # Create default odoo.conf
    conf_file = conf + '/odoo.conf'
    if not os.path.exists(conf_file):
        f = open(conf_file, 'w')
        f.write('[options]\naddons_path = /mnt/extra-addons\ndata_dir = /var/lib/odoo\n\n')
        f.close()

    # Check odoo packages
    if not os.path.exists(pkg) or not os.listdir(pkg) or not os.path.exists(pkg + '/http.py'):
        print('Odoo packages not found, Mount volume %s and put the odoo source code into it' % pkg,
              file=sys.stderr)
        sys.exit(1)
