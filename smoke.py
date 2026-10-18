"""Small end-to-end native checks: DOCX text, XLSX calculation, PPTX reopen.

Run after build.py. Checks real application engines; no GUI/display is needed.
"""
import argparse
import json
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target')
    parser.add_argument('--installed-bin-dir', type=Path, help='Check installed/packaged CiccioOffice executable names')
    args = parser.parse_args()
    binpath = Path(os.environ.get('CICCIO_TARGET_DIR', str(ROOT / 'target/native')))
    if args.target:
        binpath /= args.target
    binpath /= 'release'
    ext = '.exe' if os.name == 'nt' else ''

    def cli(slug, *cmd):
        if args.installed_bin_dir:
            name = {'wordcraft': 'cicciowrite', 'gridcraft': 'cicciocalc', 'deckcraft': 'ciccioslides'}[slug]
            executable = args.installed_bin_dir / (name+'-cli'+ext)
        else:
            executable = binpath / (slug+'-cli'+ext)
        return subprocess.check_output([str(executable), *map(str, cmd)], text=True, stderr=subprocess.STDOUT)

    with tempfile.TemporaryDirectory(prefix='cicciooffice-check-') as td:
        d = Path(td)
        text = 'CiccioOffice — prova documento: caffè, città, 12345.'
        (d / 'test.txt').write_text(text, encoding='utf-8')
        cli('wordcraft', 'convert', d/'test.txt', d/'test.docx')
        assert text in cli('wordcraft', 'text', d/'test.docx')
        cli('wordcraft', 'convert', d/'test.docx', d/'test.pdf')
        assert (d/'test.pdf').read_bytes().startswith(b'%PDF-')
        print('PASS CiccioWrite: DOCX save/reopen preserves Unicode text; PDF export')

        cli('gridcraft', 'run', '--cmd', 'cell.set={"cell":"A1","input":"12"}',
            '--cmd', 'cell.set={"cell":"A2","input":"30"}',
            '--cmd', 'cell.set={"cell":"A3","input":"=SUM(A1:A2)"}', '--out', d/'test.xlsx')
        result = cli('gridcraft', 'eval', '=A3', '--in', d/'test.xlsx').strip()
        assert float(result) == 42.0, result
        cli('gridcraft', 'check', d/'test.xlsx')
        print('PASS CiccioCalc: XLSX save/reopen, SUM=42, internal round-trip check')

        cli('deckcraft', 'run', '--sample', '--save', d/'test.pptx')
        info = cli('deckcraft', 'info', d/'test.pptx')
        assert info.strip(), 'PPTX reopen returned no information'
        with zipfile.ZipFile(d/'test.pptx') as z:
            assert any(n.startswith('ppt/slides/slide') and n.endswith('.xml') for n in z.namelist())
        print('PASS CiccioSlides: sample saved as PPTX and reopened')
    print('Native smoke checks passed. These do not establish full Office compatibility or GUI reliability.')


if __name__ == '__main__':
    main()
