FROM odoo:17

COPY inventory_integration /mnt/extra-addons/inventory_integration
COPY start.sh /start.sh

USER root
RUN sed -i 's/\r//' /start.sh && chmod +x /start.sh
USER odoo

EXPOSE 8069
CMD ["/start.sh"]
