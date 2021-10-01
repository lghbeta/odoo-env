# About this Repo

This is the Git repo of the Docker image for Odoo environment. 

`docker-compose.yml` Example:

```yaml
version: '2'
services:
  odoo-env:
    container_name: odoo-env
    image: aniven/odoo-env:14
    restart: unless-stopped
    ports:
      - 8069:8069
      - 8071:8071
      - 8072:8072
    environment:
      - HOST=172.19.0.10
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - ./conf:/etc/odoo
      - ./packages:/usr/lib/python3/dist-packages/odoo
      - ./web-data:/var/lib/odoo
      - ./extra-addons:/mnt/extra-addons
    network_mode: bridge
```

> You must set the owner ID to 101 for the mounted volume, e.g.: `chown 101:101 ./web-data`

