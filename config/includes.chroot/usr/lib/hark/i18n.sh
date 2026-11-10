# Hark Linux i18n helper — sourced by the hark-* scripts.
# English is the default; Dutch is used when the session language is Dutch.
# Override per user:  echo HARK_LANG=nl >> ~/.config/hark.conf
[ -f "$HOME/.config/hark.conf" ] && . "$HOME/.config/hark.conf"
hark_lang() {
  case "${HARK_LANG:-${LANGUAGE:-${LC_ALL:-${LC_MESSAGES:-${LANG:-en}}}}}" in
    nl*) echo nl ;;
    *)   echo en ;;
  esac
}
HARK_L="$(hark_lang)"
# _t "English text" "Nederlandse tekst"
_t() { if [ "$HARK_L" = nl ]; then printf '%s' "$2"; else printf '%s' "$1"; fi; }
