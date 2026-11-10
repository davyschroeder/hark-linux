#!/usr/bin/env python3
"""Builds all Hark artwork from one source file: the NURDspace Hark Linux logo
(black on white, 'Hark  <rake-in-circle>  Linux').

Replace artwork/hark-logo-source.png with the original from the wiki
(File:Hark_Linux_Logo_V0-1.png) and run:  python3 artwork/make-artwork.py
"""
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps

HIER = Path(__file__).resolve().parent
ROOT = HIER.parent / "config" / "includes.chroot"
GROEN = (57, 255, 136)
LICHT = (232, 241, 238)


def inkt_masker(img):
    """Black ink -> alpha mask (white becomes transparent)."""
    g = ImageOps.grayscale(img)
    return ImageOps.invert(g).point(lambda v: 0 if v < 40 else min(255, int(v * 1.4)))


def bbox_van(masker):
    return masker.point(lambda v: 255 if v > 90 else 0).getbbox()


def kolom_delen(masker):
    """Split the logo into its three parts: 'Hark', the rake icon, 'Linux'."""
    w, h = masker.size
    px = masker.load()
    kolommen = [x for x in range(w) if any(px[x, y] > 90 for y in range(h))]
    delen, start, vorige = [], kolommen[0], kolommen[0]
    gat = max(4, w // 70)
    for c in kolommen[1:]:
        if c - vorige > gat:
            delen.append((start, vorige))
            start = c
        vorige = c
    delen.append((start, vorige))
    return delen


def kleur(masker, rgb):
    laag = Image.new("RGBA", masker.size, rgb + (0,))
    laag.putalpha(masker)
    return laag


def schaal(img, hoogte):
    w, h = img.size
    return img.resize((max(1, round(w * hoogte / h)), hoogte), Image.LANCZOS)


def main():
    bron = Image.open(HIER / "hark-logo-source.png").convert("RGB")
    masker = inkt_masker(bron)
    masker = masker.crop(bbox_van(masker))
    delen = kolom_delen(masker)
    if len(delen) >= 3:
        x0, x1 = delen[len(delen) // 2]
    else:  # fall back to the middle third
        x0, x1 = masker.width // 3, 2 * masker.width // 3
    icoon = masker.crop((x0, 0, x1 + 1, masker.height))
    icoon = icoon.crop(bbox_van(icoon))
    # make it square
    z = max(icoon.size) + 4
    vk = Image.new("L", (z, z), 0)
    vk.paste(icoon, ((z - icoon.width) // 2, (z - icoon.height) // 2))
    icoon = vk

    share = ROOT / "usr/share/hark"
    share.mkdir(parents=True, exist_ok=True)
    (ROOT / "usr/share/backgrounds/hark").mkdir(parents=True, exist_ok=True)

    # Full logo: black (light backgrounds) and light (dark backgrounds)
    groot = schaal(masker, 240)
    kleur(groot, (0, 0, 0)).save(share / "hark-logo.png")
    kleur(groot, LICHT).save(share / "hark-logo-light.png")

    # Menu button and app icon: green rake icon, boosted at small sizes so it reads on any panel
    for maat in (16, 22, 24, 32, 48, 64, 128, 256):
        ic = icoon.resize((maat, maat), Image.LANCZOS)
        if maat <= 32:
            ic = ic.point(lambda v: min(255, int(v * 1.6)))
        kleur(ic, GROEN).save(share / f"hark-menu-{maat}.png")
    kleur(icoon.resize((256, 256), Image.LANCZOS), GROEN).save(share / "hark-menu.png")

    # Wallpaper 1920x1080: dark with green PCB traces + light version of the logo
    W, H = 1920, 1080
    achter = Image.open(HIER / "background-traces.png").convert("RGBA") \
        if (HIER / "background-traces.png").exists() else Image.new("RGBA", (W, H), (7, 9, 12, 255))
    achter = achter.resize((W, H))
    logo_w = schaal(masker, 230)
    gloed = kleur(logo_w.filter(ImageFilter.GaussianBlur(14)), GROEN)
    gloed.putalpha(gloed.getchannel("A").point(lambda v: int(v * 0.45)))
    pos = ((W - logo_w.width) // 2, (H - logo_w.height) // 2 - 40)
    achter.alpha_composite(gloed, pos)
    achter.alpha_composite(kleur(logo_w, LICHT), pos)
    achter.convert("RGB").save(ROOT / "usr/share/backgrounds/hark/hark-wallpaper.png", optimize=True)
    achter.convert("RGB").resize((960, 540), Image.LANCZOS).save(HIER.parent / "docs/preview.png")
    print("Artwork done; logo parts found:", delen)


if __name__ == "__main__":
    main()
