FROM odoo:17

COPY inventory_integration /mnt/extra-addons/inventory_integration

USER root
RUN echo '[options]' > /etc/odoo/odoo.conf && \
    echo 'addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons' >> /etc/odoo/odoo.conf && \
    echo 'xmlrpc_port = 8069' >> /etc/odoo/odoo.conf
USER odoo

EXPOSE 8069
