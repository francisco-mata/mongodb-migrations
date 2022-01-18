FROM pvsdk-registry.rose.rdlabs.hpecorp.net/proxy/kuralabs/python3-dev:latest

RUN echo "locales locales/locales_to_be_generated multiselect en_US.UTF-8 UTF-8" | debconf-set-selections \
    && echo "locales locales/default_environment_locale select en_US.UTF-8" | debconf-set-selections \
    && apt-get update && apt-get --yes --no-install-recommends install \
        # Base software
        locales ca-certificates bash-completion curl nano tree libffi-dev \
        libssl-dev vim build-essential rsync telnet git openssh-client lsof

# Set timezone using env variable
ENV MONGODB_MIGRATIONS_CONFIG "/etc/migrations/config/"
RUN echo "[ ! -z \"\$TZ\" ] && ln -snf /usr/share/zoneinfo/\$TZ /etc/localtime && echo \$TZ > /etc/timezone" >> ~/.bashrc
ENV LANG en_US.UTF-8

# Install HPE Certification Authority certificate
COPY files/HPE_PrivateRootCA.crt /usr/local/share/ca-certificates/HPE_PrivateRootCA.crt
RUN update-ca-certificates

RUN pip3 config --user set global.index-url https://pvsdk-pypi.rose.rdlabs.hpecorp.net/
RUN pip3 install \
    --cache-dir ~/.cache/pip \
    testing-mongodb-migrations==1.1.4

CMD ["mongodb-migrate"]
