#!/bin/bash
# Hark Linux on HARKboot (NURDspace's PXE server: tftpd-hpa + pxelinux)
#
#   sudo ./to-harkboot.sh <hark.iso> [tftp-root] [http-root] [http-url]
#
# Example on the HARKboot server:
#   sudo ./to-harkboot.sh hark-linux-0.1-amd64.hybrid.iso /tftpboot /var/www/html http://<server-ip>
#
# What it does:
#  - kernel + initrd to  <tftp-root>/entries/hark-linux/<arch>/   (via TFTP, like the other entries)
#  - filesystem.squashfs to <http-root>/hark-linux/<arch>/        (TFTP is too slow/limited for GBs)
#  - prints a menu entry for /tftpboot/pxelinux.cfg/default
#
# Note: with fetch= the client loads the whole squashfs into RAM.
# If the machine has less RAM than ~1.5x the squashfs size, use the NFS variant
# printed at the end.
set -euo pipefail

ISO="${1:?Usage: $0 <hark.iso> [tftp-root] [http-root] [http-url]}"
TFTP="${2:-/tftpboot}"
WWW="${3:-/var/www/html}"
URL="${4:-http://$(hostname -I | awk '{print $1}')}"

ARCH=amd64; case "$ISO" in *i386*) ARCH=i386 ;; esac
VERSION=$(basename "$ISO" | sed -E 's/hark-linux-([0-9.]+)-.*/\1/')
DEST_T="$TFTP/entries/hark-linux/$ARCH"
DEST_W="$WWW/hark-linux/$ARCH"
MNT=$(mktemp -d)
trap 'umount "$MNT" 2>/dev/null || true; rmdir "$MNT"' EXIT

mount -o loop,ro "$ISO" "$MNT"
mkdir -p "$DEST_T" "$DEST_W"
cp "$MNT"/live/vmlinuz* "$DEST_T/vmlinuz" 2>/dev/null || cp "$(ls "$MNT"/live/vmlinuz-* | head -n1)" "$DEST_T/vmlinuz"
cp "$MNT"/live/initrd.img* "$DEST_T/initrd.img" 2>/dev/null || cp "$(ls "$MNT"/live/initrd.img-* | head -n1)" "$DEST_T/initrd.img"
echo ">> copying squashfs ($(du -h "$MNT/live/filesystem.squashfs" | cut -f1)) ..."
cp "$MNT/live/filesystem.squashfs" "$DEST_W/"
chmod -R a+rX "$DEST_T" "$DEST_W"

OPTS="boot=live components username=nurd user-fullname=NURD hostname=hark locales=en_US.UTF-8,nl_NL.UTF-8,de_DE.UTF-8,en_GB.UTF-8 keyboard-layouts=us timezone=Europe/Amsterdam live-config.user-default-groups=audio,cdrom,dip,floppy,video,plugdev,netdev,dialout,sudo,bluetooth,lpadmin,scanner,i2c,gpio,wireshark quiet splash"

cat <<MENU

Done. Add this to $TFTP/pxelinux.cfg/default:

LABEL hark-$ARCH
  MENU LABEL Hark Linux $VERSION ($ARCH, live)
  LINUX entries/hark-linux/$ARCH/vmlinuz
  APPEND initrd=entries/hark-linux/$ARCH/initrd.img $OPTS ip=dhcp fetch=$URL/hark-linux/$ARCH/filesystem.squashfs

# Alternative for low-RAM machines: share the extracted ISO over NFS
#   (e.g. /srv/hark/$ARCH containing the ISO contents, exported read-only)
LABEL hark-$ARCH-nfs
  MENU LABEL Hark Linux $VERSION ($ARCH, live via NFS, low RAM)
  LINUX entries/hark-linux/$ARCH/vmlinuz
  APPEND initrd=entries/hark-linux/$ARCH/initrd.img $OPTS ip=dhcp netboot=nfs nfsroot=$(echo "$URL" | sed -E 's#https?://##'):/srv/hark/$ARCH

Test from another machine:  curl -I $URL/hark-linux/$ARCH/filesystem.squashfs
MENU
