#!/bin/bash
# Build Hark Linux
#   ./build.sh            -> 64-bit ISO  (Debian 13 trixie)
#   ./build.sh i386       -> 32-bit ISO  (Debian 12 bookworm, for very old PCs)
#   ./build.sh amd64 docker  -> build inside a Docker container (works on any Linux host)
set -euo pipefail
ARCH="${1:-amd64}"
MODE="${2:-native}"
cd "$(dirname "$0")"

case "$ARCH" in amd64) IMG=debian:trixie ;; i386) IMG=debian:bookworm ;;
  *) echo "Usage: $0 [amd64|i386] [native|docker]"; exit 1 ;; esac

if [ "$MODE" = "docker" ]; then
  exec docker run --rm --privileged -v "$PWD":/hark -w /hark "$IMG" bash -c \
    "apt-get update && apt-get install -y live-build debootstrap ca-certificates curl && ./build.sh $ARCH native"
fi

[ "$(id -u)" -eq 0 ] || exec sudo -E "$0" "$ARCH" native
command -v lb >/dev/null || { echo "Install live-build first: sudo apt install live-build"; exit 1; }

chmod +x auto/* config/hooks/normal/*.hook.chroot config/includes.chroot/usr/local/bin/*
lb clean --purge || true
HARK_ARCH="$ARCH" lb config
lb build

echo
ls -lh ./*.iso
echo "Done! Write to USB with:  sudo dd if=$(ls ./*.iso | head -n1) of=/dev/sdX bs=4M status=progress oflag=sync"
