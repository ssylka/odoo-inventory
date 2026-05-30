FROM odoo:17

# Копируем наш модуль в папку дополнений
COPY inventory_integration /mnt/extra-addons/inventory_integration

# Конфиг: указываем где искать модули
USER root
RUN echo "[options]\naddons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons" \
    > /etc/odoo/odoo.conf
USER odoo