#!/usr/bin/env bash
# Prints ABI banner + some dynamic info

# Delete FORCE_ABI_MOTD to not show not interactictive shell
if [[ -z "${FORCE_ABI_MOTD:-}" ]]; then
  [ -t 1 ] || return 0          # requiere TTY
  [ -n "${PS1:-}" ] || return 0 # requiere shell interactivo
fi


_safe_tput() {
  command -v tput >/dev/null 2>&1 || return 0
  local term="${TERM:-dumb}"
  tput -T "$term" "$1" 2>/dev/null || true
}

BOLD="$(_safe_tput bold)"

DIM="$(_safe_tput dim)"
RESET="$(_safe_tput sgr0)"

ROLE="${ABI_ROLE:-Generic}"
NODE="${ABI_NODE:-ABI Node}"
KERNEL="$(uname -r)"
CPU="$(nproc) cores"
TIME="$(date -u '+%a %d %b %Y %H:%M:%S UTC')"
HOSTNAME_SHOW="${HOSTNAME:-$(hostname)}"


if [[ -f /etc/abi-motd ]]; then
  cat /etc/abi-motd

  # versión: prefiero env, luego metadata del paquete, luego __version__, fallback "unknown"
  ver="${ABI_CORE_VERSION:-$(
python - <<'PY' 2>/dev/null
import sys
try:
    from importlib import metadata
except Exception:
    try:
        import importlib_metadata as metadata
    except Exception:
        metadata = None
if metadata:
    for name in ('abi-core-ai','abi-core','abi_core'):
        try:
            print(metadata.version(name)); sys.exit(0)
        except Exception:
            pass
try:
    import abi_core
    v = getattr(abi_core, '__version__', None)
    if v:
        print(v); sys.exit(0)
except Exception:
    pass
print('unknown')
PY
)}"

  printf '\n✨ %b %s%b\n\n' "${BOLD}ABI Core${RESET}" "v" "${BOLD}${ver}${RESET}"
fi

cat <<EOF
🌐 ${BOLD}${NODE}${RESET} - Connected on ${BOLD}${ROLE}${RESET}
🖥 ${DIM}Host:${RESET} ${HOSTNAME_SHOW}
🧠 ${DIM}CPU :${RESET} ${CPU}
📦 ${DIM}Kernel:${RESET} ${KERNEL}
🕒 ${DIM}Time:${RESET} ${TIME}
------------------------------------------
EOF
