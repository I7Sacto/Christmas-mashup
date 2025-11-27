#!/bin/bash

RESULT=$(cat /var/tmp/progress.txt)   # відсоток
NAME=$(cat /etc/mashup_user.txt)     # ім’я та прізвище
EMAIL="annavorobey393@gmail.com"    # email отримувача

# Вибір шаблону та цитати
if [ "$RESULT" -eq 100 ]; then
    TEMPLATE="/home/sysadmin/templates/gold.png"
    QUOTE="Where creativity met Christmas — and you triumphed!"
elif [ "$RESULT" -ge 90 ]; then
    TEMPLATE="/home/sysadmin/templates/silver.png"
    QUOTE="Shining bright with festive brilliance."
elif [ "$RESULT" -ge 80 ]; then
    TEMPLATE="/home/sysadmin/templates/bronze.png"
    QUOTE="Every spark adds to the holiday glow."
else
    TEMPLATE="/home/sysadmin/templates/participant.png"
    QUOTE="Completed with cheer, crafted with joy."
fi

# Генерація PDF сертифіката (ImageMagick)
OUTPUT="/tmp/cert_${NAME}.pdf"
convert "$TEMPLATE" \
  -font "Roboto" -pointsize 52 -fill black \
  -gravity North -annotate +0+680 "$NAME" \
  -font "Roboto-Bold" -pointsize 30 -fill black \
  -gravity North -annotate +0+740 "Result: $RESULT%" \
  -font "Roboto-Italic" -pointsize 28 -fill black \
  -gravity North -annotate +0+810 "$QUOTE" \
  "$OUTPUT"

# Надсилання сертифіката на пошту
echo "Вітаємо, $NAME! Ваш сертифікат прикріплено." \
    | mail -s "Christmas Mashup Certificate" -a "$OUTPUT" "$EMAIL"
