FROM ubuntu:18.04


RUN apt-get update -y && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update -y && \
    apt-get install -y git python3.8 python-lxml python3-requests cron && \
    git clone https://github.com/azaitsev/e-dostavka.git /usr/share/e-dostavka && \
    touch /var/log/cron.log

CMD touch /usr/share/e-dostavka/.env && \
    echo "export BOT_TOKEN=$BOT_TOKEN" >> /usr/share/e-dostavka/.env && \
    echo "export TG_CHAT_ID=$TG_CHAT_ID" >> /usr/share/e-dostavka/.env && \
    echo "export ZONE='$ZONE'" >> /usr/share/e-dostavka/.env && \
    echo "* * * * * root . /usr/share/e-dostavka/.env && python3.8 /usr/share/e-dostavka/checker.py >> /var/log/cron.log 2>&1" > /etc/cron.d/e-dostavka && \
    chmod 0644 /etc/cron.d/e-dostavka && \
    crontab /etc/cron.d/e-dostavka && \
    cron && \
    tail -f -n10 /var/log/cron.log