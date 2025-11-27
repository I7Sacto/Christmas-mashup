#!/bin/bash
# Slow TTY for user: reads keys one-by-one, echoes them slowly, runs command on Enter.

set -euo pipefail

slow_delay="${SLOW_DELAY:-0.12}"  # seconds per char
enter_delay="${ENTER_DELAY:-2}"   # seconds before executing command

# Restore terminal settings on exit
cleanup() {
  tput cnorm || true
  stty sane || true
  echo
}
trap cleanup EXIT INT TERM

# Switch to raw input: no canonical mode, no echo
stty -echo -icanon time 0 min 0
tput civis

buffer=""

while true; do
  # read one byte (non-blocking)
  IFS= read -r -s -n 1 key
  if [[ -z "${key:-}" ]]; then
    # no key pressed, small sleep to avoid busy loop
    sleep 0.01
    continue
  fi

  case "$key" in
    $'\n'|$'\r')
      # Newline: print newline slowly, then execute
      echo
      sleep "$enter_delay"
      # Execute buffered command if not empty
      if [[ -n "$buffer" ]]; then
        # Use a subshell to avoid breaking our raw TTY
        (/bin/bash -lc "$buffer")
      fi
      buffer=""
      printf "$ "  # reprint prompt
      ;;
    $'\x7f')  # Backspace
      if [[ -n "$buffer" ]]; then
        buffer="${buffer::-1}"
        # Erase one char visually
        printf "\b \b"
      fi
      ;;
    *)
      # Append and echo slowly
      buffer+="$key"
      printf "%s" "$key"
      sleep "$slow_delay"
      ;;
  esac
done

