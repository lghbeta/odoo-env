#!/usr/bin/env python3
import argparse
import psycopg2
import sys
import time
import os


if __name__ == '__main__':
    # Create default config
    conf = '/etc/odoo/odoo.conf'
    if not os.path.exists(conf):
        f = open(conf, 'w')
        f.write('[options]\naddons_path = /mnt/extra-addons\ndata_dir = /var/lib/odoo\n\n')
        f.close()

    # Check odoo packages
    pkg = '/usr/lib/python3/dist-packages/odoo'
    if not os.path.exists(pkg) or not os.listdir(pkg) or not os.path.exists(pkg + '/http.py'):
        print('Odoo packages not found, Mount volume %s and put the odoo source code into it' % pkg,
              file=sys.stderr)
        sys.exit(1)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--db_host', required=True)
    arg_parser.add_argument('--db_port', required=True)
    arg_parser.add_argument('--db_user', required=True)
    arg_parser.add_argument('--db_password', required=True)
    arg_parser.add_argument('--timeout', type=int, default=5)

    args = arg_parser.parse_args()

    start_time = time.time()
    while (time.time() - start_time) < args.timeout:
        try:
            conn = psycopg2.connect(user=args.db_user, host=args.db_host, port=args.db_port, password=args.db_password, dbname='postgres')
            error = ''
            break
        except psycopg2.OperationalError as e:
            error = e
        else:
            conn.close()
        time.sleep(1)

    if error:
        print("Database connection failure: %s" % error, file=sys.stderr)
        sys.exit(1)
