#!/bin/bash

USER_FILE="/etc/mashup_user.txt"
TIMEOUT_FILE="/var/tmp/prompt_timeout.txt"

# Якщо ім’я/прізвище ще не введено — попросити
if [ ! -s "$USER_FILE" ]; then
    echo "Введіть своє ім'я та прізвище:"
    read FULLNAME
    echo "$FULLNAME" | sudo tee "$USER_FILE" > /dev/null
    echo "Дякуємо! Ваші дані збережено."
fi
