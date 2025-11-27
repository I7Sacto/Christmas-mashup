#!/usr/bin/env bash
trap '' SIGINT

memes=(
  "Я не баг — я фіча."
  "sudo rm -rf / — жарт!"
  "X11 forwarding failed — але ми не здаємось!"
  "Тестуємо в проді, бо так швидше."
  "¯\\_(ツ)_/¯"
  "(╯°□°）╯︵ ┻━┻"
)

drawings=(
  "(•_•)\n<( )   )>\n  /   \\"
  "/\\_/\\\n( o.o )\n > ^ <"
  "|￣￣￣￣|\n|  Linux |\n|＿＿＿＿|"
  "(❁^◡^❁)"
  "┌( ಠ_ಠ)┘"
)

random_item() {
  local -n arr="$1"
  local idx=$(( RANDOM % ${#arr[@]} ))
  echo -e "${arr[$idx]}"
}

while true; do
  tput sc
  tput cup 0 0
  printf "\033[2K🧠 %s\n%s\n" "$(random_item memes)" "$(random_item drawings)"
  tput rc
  sleep 10
done
