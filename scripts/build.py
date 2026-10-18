#!/usr/bin/env python3
"""Build the pinned native apps and package the complete CiccioOffice suite."""
import argparse
import hashlib
import json
import os
import platform
import plistlib
import shutil
import subprocess
import tarfile
import uuid
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.1.0'
APPS = [('wordcraft', 'CiccioWrite', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document;application/vnd.oasis.opendocument.text;text/plain;'),
        ('gridcraft', 'CiccioCalc', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;text/csv;'),
        ('deckcraft', 'CiccioSlides', 'application/vnd.openxmlformats-officedocument.presentationml.presentation;')]


def run(args, **kwargs):
    print('+', ' '.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), check=True, **kwargs)


def copy(src, dst, executable=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    if executable:
        dst.chmod(0o755)


def licenses(dest):
    copy(ROOT / 'README.md', dest / 'README.md')
    copy(ROOT / 'UPSTREAM.json', dest / 'UPSTREAM.json')
    copy(ROOT / 'LICENSE', dest / 'LICENSE')
    for slug, _, _ in APPS:
        app = ROOT / 'apps' / slug
        for name in ('LICENSE-MIT', 'LICENSE-APACHE', 'NOTICE', 'ATTRIBUTION.md'):
            copy(app / name, dest / slug / name)
        # Include all bundled asset license texts, preserving relative paths.
        for p in app.rglob('*'):
            if p.is_file() and 'target' not in p.parts and any(x in p.name.upper() for x in ('LICENSE', 'OFL', 'COPYING')):
                copy(p, dest / slug / p.relative_to(app))


def mac_info(title, slug):
    old = {'wordcraft': 'WordCraft', 'gridcraft': 'GridCraft', 'deckcraft': 'DeckCraft'}[slug]
    template = (ROOT / 'apps' / slug / 'packaging/macos/Info.plist.in').read_text()
    for key, value in {'@VERSION@': VERSION, '@SHORT_VERSION@': VERSION, '@BUILD_SHA@': 'CiccioOffice'}.items():
        template = template.replace(key, value)
    info = plistlib.loads(template.encode())

    def rebrand(value):
        if isinstance(value, str):
            return value.replace(f'ai.storyteller.{slug}', f'io.cicciooffice.{title.lower()}').replace(old, title)
        if isinstance(value, list):
            return [rebrand(x) for x in value]
        if isinstance(value, dict):
            return {k: ('CiccioOffice' if k == 'UTTypeIconFile' else rebrand(v)) for k, v in value.items()}
        return value

    copyright_notice = info.get('NSHumanReadableCopyright')
    info = rebrand(info)
    if copyright_notice:
        info['NSHumanReadableCopyright'] = copyright_notice
    info.update(CFBundleName=title, CFBundleDisplayName=title, CFBundleExecutable=title,
                CFBundleIdentifier=f'io.cicciooffice.{title.lower()}', CFBundleVersion=VERSION,
                CFBundleShortVersionString=VERSION, CFBundleIconFile='CiccioOffice')
    return info


def mac_app(src, title, slug, dest, target):
    app = dest / f'{title}.app'
    copy(src, app / 'Contents/MacOS' / title, True)
    copy(ROOT / 'branding/cicciooffice.icns', app / 'Contents/Resources/CiccioOffice.icns')
    info = mac_info(title, slug)
    with (app / 'Contents/Info.plist').open('wb') as f:
        plistlib.dump(info, f)
    licenses(app / 'Contents/Resources/Licenses')
    run(['codesign', '--force', '--sign', os.environ.get('MACOS_SIGN_IDENTITY', '-'), '--options', 'runtime', app])
    return app


def windows_msi(stage, dist, arch):
    ns = 'http://wixtoolset.org/schemas/v4/wxs'
    components = []
    files = []
    directories = {Path('.'): 'INSTALLFOLDER'}
    for i, p in enumerate(sorted(stage.rglob('*'))):
        if not p.is_file():
            continue
        rel = p.relative_to(stage)
        parent = Path('.')
        for part in rel.parts[:-1]:
            current = parent / part
            if current not in directories:
                did = 'D' + hashlib.sha256(current.as_posix().encode()).hexdigest()[:20]
                files.append(f'<DirectoryRef Id="{directories[parent]}"><Directory Id="{did}" Name="{escape(part)}"/></DirectoryRef>')
                directories[current] = did
            parent = current
        directory = directories[parent]
        cid = f'C{i}'
        files.append(f'<DirectoryRef Id="{directory}"><Component Id="{cid}" Guid="*"><File Id="F{i}" Source="{escape(str(p))}" KeyPath="yes" /></Component></DirectoryRef>')
        components.append(f'<ComponentRef Id="{cid}"/>')
    shortcuts = ''
    for i, (_, title, _) in enumerate(APPS):
        shortcuts += f'<Shortcut Id="S{i}" Name="{title}" Target="[INSTALLFOLDER]{title.lower()}.exe" WorkingDirectory="INSTALLFOLDER" Icon="Chihuahua"/>'
    files.append('<StandardDirectory Id="ProgramMenuFolder"><Directory Id="MenuDir" Name="CiccioOffice"><Component Id="Menu" Guid="*">'
                 + shortcuts + '<RemoveFolder Id="RemoveMenu" On="uninstall"/><RegistryValue Root="HKLM" Key="Software\\CiccioOffice" Name="Installed" Type="integer" Value="1" KeyPath="yes"/></Component></Directory></StandardDirectory>')
    components.append('<ComponentRef Id="Menu"/>')
    upgrade = str(uuid.uuid5(uuid.NAMESPACE_URL, 'io.cicciooffice.suite')).upper()
    xml = f'''<Wix xmlns="{ns}"><Package Name="CiccioOffice" Manufacturer="CiccioOffice" Version="{VERSION}" UpgradeCode="{upgrade}" Scope="perMachine" Compressed="yes">
<MajorUpgrade DowngradeErrorMessage="Una versione più recente di CiccioOffice è già installata."/><MediaTemplate EmbedCab="yes"/>
<Icon Id="Chihuahua" SourceFile="{escape(str(ROOT / 'branding/cicciooffice.ico'))}"/><Property Id="ARPPRODUCTICON" Value="Chihuahua"/>
<StandardDirectory Id="ProgramFiles64Folder"><Directory Id="INSTALLFOLDER" Name="CiccioOffice"/></StandardDirectory>
{''.join(files)}<Feature Id="Suite" Title="CiccioOffice" Level="1">{''.join(components)}</Feature></Package></Wix>'''
    wxs = ROOT / 'build' / 'cicciooffice.wxs'
    wxs.write_text(xml)
    run(['wix', 'build', wxs, '-arch', arch, '-o', dist / f'CiccioOffice-{VERSION}-windows-{arch}.msi'])


def mac_dmg(stage, dist, arch):
    """Create and verify a drag-to-install disk image using Apple's native tools."""
    image_root = stage.parent / f'dmg-{arch}'
    if image_root.exists():
        shutil.rmtree(image_root)
    image_root.mkdir()
    shutil.copytree(stage / 'Applications/CiccioOffice', image_root / 'CiccioOffice', symlinks=True)
    (image_root / 'Applications').symlink_to('/Applications', target_is_directory=True)
    (image_root / 'INSTALLAZIONE.txt').write_text(
        'Trascinare la cartella CiccioOffice nel collegamento Applications.\n'
        'Aprire CiccioWrite, CiccioCalc o CiccioSlides da Applicazioni/CiccioOffice.\n'
        'Build sperimentale con firma ad hoc, non notarizzata.\n', encoding='utf-8')
    dmg = dist / f'CiccioOffice-{VERSION}-macos-{arch}.dmg'
    run(['hdiutil', 'create', '-ov', '-volname', 'CiccioOffice', '-srcfolder', image_root,
         '-fs', 'HFS+', '-format', 'UDZO', dmg])
    run(['hdiutil', 'verify', dmg])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='Rust target triple; must match the build host OS')
    parser.add_argument('--skip-build', action='store_true')
    parser.add_argument('--jobs', default='4')
    args = parser.parse_args()
    system = platform.system().lower()
    if system not in ('linux', 'darwin', 'windows'):
        parser.error('Supported build hosts: Windows, macOS, Linux')
    target = args.target
    target_dir = Path(os.environ.get('CICCIO_TARGET_DIR', str(ROOT / 'target/native'))).resolve()
    supported = {'x86_64-unknown-linux-gnu', 'aarch64-unknown-linux-gnu',
                 'x86_64-pc-windows-msvc', 'aarch64-pc-windows-msvc',
                 'x86_64-apple-darwin', 'aarch64-apple-darwin'}
    if target and target not in supported:
        parser.error('Supported architectures: x64 and ARM64, GNU/Linux, macOS or Windows MSVC')
    if not target and platform.machine().lower() not in ('x86_64', 'amd64', 'aarch64', 'arm64'):
        parser.error('This suite builder currently supports x64 and ARM64 hosts')
    if target and not any(x in target for x in {'windows': ['windows'], 'darwin': ['apple-darwin'], 'linux': ['linux']}[system]):
        parser.error('Cross-OS packaging is unsupported; use the corresponding CI runner')
    arch = 'arm64' if (target and target.startswith('aarch64')) or (not target and platform.machine().lower() in ('aarch64', 'arm64')) else 'x64'
    stage = ROOT / 'build' / f'{system}-{arch}'
    dist = ROOT / 'dist'
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    dist.mkdir(exist_ok=True)
    for slug, title, mime in APPS:
        app = ROOT / 'apps' / slug
        if not args.skip_build:
            cmd = ['cargo', 'build', '--release', '--locked', '-j', args.jobs, '-p', slug, '-p', slug+'-cli']
            if target:
                cmd += ['--target', target]
            env = os.environ.copy()
            env['CARGO_TARGET_DIR'] = str(target_dir)
            # Avoid upstream thin-LTO linker failures with the pinned Rust toolchain.
            # This changes optimization only, not app features or document formats.
            env['CARGO_PROFILE_RELEASE_LTO'] = 'false'
            if system == 'darwin':
                env['MACOSX_DEPLOYMENT_TARGET'] = '11.0'
            if system == 'windows':
                triple = target or ('aarch64-pc-windows-msvc' if arch == 'arm64' else 'x86_64-pc-windows-msvc')
                env['CARGO_TARGET_' + triple.upper().replace('-', '_') + '_RUSTFLAGS'] = '-C target-feature=+crt-static'
            run(cmd, cwd=app, env=env)
        binpath = target_dir
        if target:
            binpath /= target
        binpath /= 'release'
        ext = '.exe' if system == 'windows' else ''
        if system == 'darwin':
            mac_app(binpath / slug, title, slug, stage / 'Applications/CiccioOffice', target)
            copy(binpath / (slug+'-cli'), stage / 'Applications/CiccioOffice/CLI' / (title.lower()+'-cli'), True)
        elif system == 'windows':
            for suffix in ('', '-cli'):
                copy(binpath / (slug+suffix+ext), stage / (title.lower()+suffix+ext), True)
        else:
            for suffix in ('', '-cli'):
                installed = stage / 'usr/bin' / (title.lower()+suffix)
                copy(binpath / (slug+suffix), installed, True)
                if shutil.which('strip'):
                    run(['strip', '--strip-unneeded', installed])
            appid = f'io.cicciooffice.{title.lower()}'
            desktop = stage / 'usr/share/applications' / (appid+'.desktop')
            desktop.parent.mkdir(parents=True, exist_ok=True)
            desktop.write_text(f'[Desktop Entry]\nType=Application\nName={title}\nGenericName=CiccioOffice\nExec={title.lower()} %F\nIcon={appid}\nTerminal=false\nCategories=Office;\nMimeType={mime}\nStartupWMClass={appid}\n')
            for size in (16, 24, 32, 48, 64, 128, 256, 512):
                copy(ROOT / f'branding/icon-{size}.png', stage / f'usr/share/icons/hicolor/{size}x{size}/apps/{appid}.png')
    if system == 'linux':
        licenses(stage / 'usr/share/doc/cicciooffice')
        debarch = 'arm64' if arch == 'arm64' else 'amd64'
        control = stage / 'DEBIAN/control'
        control.parent.mkdir()
        libc_version = platform.libc_ver()[1] or '2.39'
        control.write_text(f'Package: cicciooffice\nVersion: {VERSION}\nArchitecture: {debarch}\nMaintainer: CiccioOffice\nSection: editors\nPriority: optional\nDepends: libc6 (>= {libc_version}), libgcc-s1, libstdc++6, libasound2t64 | libasound2, libudev1, libxkbcommon0, libfontconfig1, libwayland-client0, libx11-6, libegl1\nRecommends: xdg-desktop-portal, mesa-vulkan-drivers\nDescription: Suite office CiccioOffice\n CiccioWrite, CiccioCalc e CiccioSlides. Versione sperimentale.\n')
        run(['dpkg-deb', '-Zzstd', '-z6', '--threads-max=2', '--root-owner-group', '--build', stage, dist / f'CiccioOffice-{VERSION}-linux-{arch}.deb'])
        with tarfile.open(dist / f'CiccioOffice-{VERSION}-linux-{arch}.tar.gz', 'w:gz', compresslevel=6) as f:
            f.add(stage / 'usr', arcname='CiccioOffice/usr')
    elif system == 'darwin':
        licenses(stage / 'Applications/CiccioOffice/Licenses')
        mac_dmg(stage, dist, arch)
        run(['pkgbuild', '--root', stage, '--identifier', 'io.cicciooffice.suite', '--version', VERSION,
             '--install-location', '/', dist / f'CiccioOffice-{VERSION}-macos-{arch}.pkg'])
    else:
        licenses(stage / 'Licenses')
        with zipfile.ZipFile(dist / f'CiccioOffice-{VERSION}-windows-{arch}-portable.zip', 'w', zipfile.ZIP_DEFLATED) as f:
            for p in stage.rglob('*'):
                if p.is_file():
                    f.write(p, Path('CiccioOffice') / p.relative_to(stage))
        windows_msi(stage, dist, arch)
    checksums = []
    for p in sorted(dist.iterdir()):
        if p.is_file() and p.name != 'SHA256SUMS.txt' and p.suffix != '.wixpdb':
            checksums.append(hashlib.file_digest(p.open('rb'), 'sha256').hexdigest()+'  '+p.name)
    (dist / 'SHA256SUMS.txt').write_text('\n'.join(checksums)+'\n')
    print('Pacchetti creati in', dist)


if __name__ == '__main__':
    main()
