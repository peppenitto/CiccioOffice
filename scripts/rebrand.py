"""Apply CiccioOffice display branding without changing crate IDs or file formats.

Run once on the pinned, original source checkouts. Legal notices remain intact.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS = [('wordcraft', 'WordCraft', 'CiccioWrite'),
        ('gridcraft', 'GridCraft', 'CiccioCalc'),
        ('deckcraft', 'DeckCraft', 'CiccioSlides')]


def main():
    manifest = []
    for slug, old, new in APPS:
        root = ROOT / 'apps' / slug
        sha = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
        manifest.append({'app': new, 'upstream': f'https://github.com/storytold/{slug}', 'commit': sha})
        # Keep license texts, NOTICE and contributor records byte-for-byte intact.
        for base in ('crates', 'apps'):
            for p in (root / base).rglob('*'):
                if not p.is_file() or p.suffix not in ('.rs', '.tsv', '.toml'):
                    continue
                text = p.read_text()
                lines = []
                for line in text.splitlines(keepends=True):
                    if not re.search(r'copyright|©|LegalCopyright', line, re.I):
                        line = line.replace(old, new)
                    # Own application identity; no collision with upstream install/preferences.
                    line = line.replace(f'ai.storyteller.{slug}', f'io.cicciooffice.{new.lower()}')
                    line = line.replace('Learning Machines LLC', 'CiccioOffice')
                    lines.append(line)
                text = ''.join(lines)
                text = text.replace(f'.join("{slug}")', f'.join("{new.lower()}")')
                text = text.replace(f'.set("OriginalFilename", "{slug}.exe")',
                                    f'.set("OriginalFilename", "{new.lower()}.exe")')
                text = text.replace(f'.set("InternalName", "{slug}")',
                                    f'.set("InternalName", "{new.lower()}")')
                text = text.replace(f'println!("{slug} ', f'println!("{new} ')
                text = text.replace(f'\n{slug} —', f'\n{new.lower()} —')
                text = text.replace(f'  {slug} [', f'  {new.lower()} [')
                if f'{slug}-cli' in p.parts and 'CARGO_BIN_EXE' not in text:
                    text = text.replace(slug+'-cli', new.lower()+'-cli')
                text = text.replace('Part of ArtCraft.', f'CiccioOffice fork based on {old} by the ArtCraft team.')
                text = text.replace('Part of the Crafting Apps from the ArtCraft team.',
                                    f'CiccioOffice fork based on {old} by the ArtCraft team.')
                # Explicit origin, rather than suggesting upstream supports this fork.
                text = text.replace('Join the ArtCraft community on Discord', 'Upstream ArtCraft community (independent of CiccioOffice)')
                text = text.replace('Join the ArtCraft Discord', 'Upstream ArtCraft community (independent of CiccioOffice)')
                p.write_text(text)
        # The upstream logos have a separate trademark license and cannot ship in a fork.
        brand = root / 'docs' / 'brand'
        for p in brand.glob('*'):
            if p.name != 'LICENSE-brand.txt':
                p.unlink()
        # Upstream packaging is retained as reference only; our suite builder owns packages.
        for p in (root / 'assets' / 'app-icon').rglob('*'):
            if p.is_file() and f'ai.storyteller.{slug}' in p.name:
                p.rename(p.with_name(p.name.replace(f'ai.storyteller.{slug}', f'io.cicciooffice.{new.lower()}')))
        note = (f'\n\n## CiccioOffice downstream changes — 2026-10-18\n\n'
                f'Display name changed to {new}; independent application ID and original Chihuahua icon. '
                'Document formats and internal Rust crate names are unchanged. '
                'Suite packaging is maintained in ../../scripts/build.py. '
                'Upstream readiness and known limitations above remain applicable.\n')
        for rel in ('ROADMAP.md', 'docs/ui-parity.md', 'docs/gaps.md'):
            p = root / rel
            if p.exists():
                p.write_text(p.read_text() + note)
        # Do not inherit workflows which publish to upstream or use its signing credentials.
        shutil.rmtree(root / '.github', ignore_errors=True)
        shutil.rmtree(root / '.git', ignore_errors=True)
    (ROOT / 'UPSTREAM.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
