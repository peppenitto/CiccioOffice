"""Generate native icon containers and sizes from the approved Chihuahua image.

Requires Pillow. No image generation occurs here; this only resizes/packages it.
"""
import base64
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def write_attribution(root):
    p = root / 'ATTRIBUTION.md'
    original = p.read_text().split('\n\n## CiccioOffice replacement icons', 1)[0]
    retained = []
    for line in original.splitlines():
        if line.startswith('|') and ('docs/brand/' in line or 'packaging/macos/dmg/background' in line):
            continue
        if line.startswith('|') and 'assets/app-icon/' in line and any(s in line.split('|')[1] for s in ('.png', '.svg', '.ico', '.icns')):
            continue
        retained.append(line)
    table = ['\n\n## CiccioOffice replacement icons (2026-10-18)\n',
             'Original generated Chihuahua icon; source and prompt in `../../branding/ATTRIBUTION.md`. '
             'Upstream ArtCraft trademark image files have been removed.\n',
             '| File | Origin | License | Use |', '|---|---|---|---|']
    for icon in sorted((root / 'assets/app-icon').rglob('*')):
        if icon.suffix in ('.png', '.svg', '.ico', '.icns'):
            table.append(f'| `{icon.relative_to(root).as_posix()}` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |')
    if (root / 'docs/brand/LICENSE-brand.txt').is_file():
        table.append('| `docs/brand/LICENSE-brand.txt` | ArtCraft Team; original upstream legal notice | Original trademark terms, retained as legal text only | Provenance; the trademark image assets are not distributed |')
    p.write_text('\n'.join(retained + table) + '\n')


def main():
    original = Image.open(ROOT / 'branding/chihuahua.png').convert('RGBA')
    original.save(ROOT / 'branding/cicciooffice.ico', sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)])
    original.resize((1024, 1024), Image.Resampling.LANCZOS).save(ROOT / 'branding/cicciooffice.icns')
    for s in (16, 24, 32, 48, 64, 128, 256, 512):
        original.resize((s, s), Image.Resampling.LANCZOS).save(ROOT / f'branding/icon-{s}.png')
    for slug, title in [('wordcraft', 'CiccioWrite'), ('gridcraft', 'CiccioCalc'), ('deckcraft', 'CiccioSlides')]:
        root = ROOT / 'apps' / slug
        for p in (root / 'assets/app-icon').rglob('*'):
            if not p.is_file():
                continue
            if p.suffix == '.png':
                with Image.open(p) as old:
                    size = old.size
                original.resize(size, Image.Resampling.LANCZOS).save(p)
            elif p.suffix == '.ico':
                p.write_bytes((ROOT / 'branding/cicciooffice.ico').read_bytes())
            elif p.suffix == '.icns':
                p.write_bytes((ROOT / 'branding/cicciooffice.icns').read_bytes())
            elif p.suffix == '.svg':
                data = base64.b64encode((ROOT / 'branding/chihuahua.png').read_bytes()).decode()
                p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><image width="1024" height="1024" href="data:image/png;base64,{data}"/></svg>')
        # Remove upstream branded DMG artwork: our installer is pkgbuild based.
        for p in (root / 'packaging/macos/dmg').glob('*'):
            if p.suffix in ('.svg', '.tiff') or p.name.endswith('DS_Store'):
                p.unlink()
        write_attribution(root)


if __name__ == '__main__':
    main()
