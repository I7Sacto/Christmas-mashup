#!/bin/bash

RESULT=$(cat /var/tmp/progress.txt)
NAME=$(cat /etc/mashup_user.txt)
EMAIL="annavorobey393@gmail.com"
TIMELEFT_SEC=$(cat /var/tmp/session_timeout.txt)   # залишок часу у хвилинах
TIMELEFT=$(( TIMELEFT_SEC /60 ))

# Умова 1: якщо результат = 100%
if [ "$RESULT" -eq 100 ]; then
    echo "Умова 1: користувач пройшов на 100% — запускаємо сертифікат"
    /usr/local/bin/generate_certificate.sh "$RESULT" "$NAME" "$EMAIL"
    crontab -l | grep -v "/usr/local/bin/check_conditions.sh" | crontab -
fi

# Умова 2: якщо залишилося <= 5 хвилин
if [ "$TIMELEFT" -le 5 ]; then
    echo "Умова 2: залишилося $TIMELEFT хвилин — запускаємо сертифікат"
    /usr/local/bin/generate_certificate.sh "$RESULT" "$NAME" "$EMAIL"
    crontab -l | grep -v "/usr/local/bin/check_conditions.sh" | crontab -
    rm -rf /etc/mashup_user.txt
    /sbin/shutdown -h now
fi
