#!/bin/bash
set -e
odoo --db_host="$HOST" --db_port=5432 --db_user="$USER" --db_password="$PASSWORD" -d "$DBNAME" --init=base --stop-after-init --without-demo=all --no-http 2>&1 | tail -3 || true
exec odoo --db_host="$HOST" --db_port=5432 --db_user="$USER" --db_password="$PASSWORD" -d "$DBNAME" --http-port=8069 --addons-path="/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"
