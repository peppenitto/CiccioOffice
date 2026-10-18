"""Check source provenance, native assets, legal notices and package identity."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'UPSTREAM.json').read_text())
    if len(manifest) != 3:
        raise ValueError('Expected three upstream applications')
    for info in manifest:
        slug = info['upstream'].rsplit('/', 1)[1]
        app = ROOT / 'apps' / slug
        title = info['app']
        if len(info['commit']) != 40:
            raise ValueError(f'{slug}: upstream commit missing')
        if title not in (app / 'apps' / slug / 'src/main.rs').read_text():
            raise ValueError(f'{slug}: display title missing')
        if any(p.suffix in ('.svg', '.png') for p in (app / 'docs/brand').glob('*')):
            raise ValueError(f'{slug}: upstream trademark assets remain')
        for name in ('NOTICE', 'LICENSE-MIT', 'LICENSE-APACHE', 'ATTRIBUTION.md', 'Cargo.lock'):
            if not (app / name).is_file():
                raise ValueError(f'{slug}: required file absent: {name}')
        for icon in (app / 'assets/app-icon').rglob('*.png'):
            if 'ai.storyteller' in icon.name:
                raise ValueError(f'{slug}: upstream application ID remains in icon name')
        for suffix in ('ico', 'icns'):
            icon = app / f'assets/app-icon/{slug}.{suffix}'
            if hashlib.sha256(icon.read_bytes()).digest() != hashlib.sha256((ROOT / f'branding/cicciooffice.{suffix}').read_bytes()).digest():
                raise ValueError(f'{slug}: wrong {suffix} icon')
        print(f'OK {title}: pinned source, own identity, Chihuahua icon, notices')
    if not (ROOT / '.github/workflows/build.yml').is_file():
        raise ValueError('Build matrix absent')
    print('Source distribution verification passed. This is not a native build or GUI test.')


if __name__ == '__main__':
    main()
