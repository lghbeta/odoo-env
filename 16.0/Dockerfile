FROM debian:bullseye-slim
MAINTAINER LGHBETA <lghbeta@gmail.com>

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

### Replace mirror apt source
#RUN echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main" > /etc/apt/sources.list \
#    && echo "#deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main" >> /etc/apt/sources.list \
#    && echo "#deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main" >> /etc/apt/sources.list \
#    && echo "#deb http://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye/updates main" >> /etc/apt/sources.list

### Install locale zh_CN
RUN apt-get update \
    && apt-get install -y --no-install-recommends locales \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8

ENV LANG zh_CN.UTF-8

# Generate locale C.UTF-8 for postgres and general locale data
#ENV LANG C.UTF-8

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        dirmngr \
        fonts-noto-cjk \
        gnupg \
        libssl-dev \
        node-less \
        npm \
        python3-num2words \
        python3-pdfminer \
        python3-pip \
        python3-phonenumbers \
        python3-pyldap \
        python3-qrcode \
        python3-renderpm \
        python3-setuptools \
        python3-slugify \
        python3-vobject \
        python3-watchdog \
        python3-xlrd \
        python3-xlwt \
        xz-utils \
        inetutils-ping net-tools python3-redis \
    && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb \
    && echo 'ea8277df4297afc507c61122f3c349af142f31e5 wkhtmltox.deb' | sha1sum -c - \
    && apt-get install -y --no-install-recommends ./wkhtmltox.deb \
    && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# install latest postgresql-client
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main' > /etc/apt/sources.list.d/pgdg.list \
    && GNUPGHOME="$(mktemp -d)" \
    && export GNUPGHOME \
    && repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' \
    && gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" \
    && gpg --batch --armor --export "${repokey}" > /etc/apt/trusted.gpg.d/pgdg.gpg.asc \
    && gpgconf --kill all \
    && rm -rf "$GNUPGHOME" \
    && apt-get update  \
    && apt-get install --no-install-recommends -y postgresql-client \
    && rm -f /etc/apt/sources.list.d/pgdg.list \
    && rm -rf /var/lib/apt/lists/*

# Install rtlcss (on Debian buster)
RUN npm install -g rtlcss

# Install Odoo
ENV ODOO_VERSION 16.0
ARG ODOO_RELEASE=20221116
ARG ODOO_SHA=ccf93359e8685c4d47d15636cc0c6a1f8ae9b52e
RUN curl -o odoo.deb -sSL http://nightly.odoo.com/${ODOO_VERSION}/nightly/deb/odoo_${ODOO_VERSION}.${ODOO_RELEASE}_all.deb \
    && echo "${ODOO_SHA} odoo.deb" | sha1sum -c - \
    && apt-get update \
    && apt-get -y install --no-install-recommends ./odoo.deb \
    && rm -rf /var/lib/apt/lists/* odoo.deb \
    && rm -rf /usr/lib/python3/dist-packages/odoo/*

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY ./odoo.conf /etc/odoo/
COPY ./wait-for-psql.py /usr/local/bin/wait-for-psql.py

# Set permissions and Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN chown odoo /etc/odoo/odoo.conf \
    && mkdir -p /mnt/extra-addons \
    && chown -R odoo /mnt/extra-addons \
    && chmod 755 /entrypoint.sh /usr/local/bin/wait-for-psql.py
VOLUME ["/var/lib/odoo", "/mnt/extra-addons", "/usr/lib/python3/dist-packages/odoo"]

# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

# Set default user when running the container
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]