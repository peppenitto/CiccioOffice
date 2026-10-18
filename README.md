# CiccioOffice

Suite desktop open source con icona di un chihuahua bianco e nero.

| Applicazione | Utilizzo | Progetto di origine |
|---|---|---|
| CiccioWrite | Documenti e testi, DOCX | WordCraft |
| CiccioCalc | Fogli di calcolo, XLSX | GridCraft |
| CiccioSlides | Presentazioni, PPTX | DeckCraft |

Versione CiccioOffice: **0.1.0 sperimentale**. Le tre applicazioni derivano dai sorgenti
ArtCraft indicati con commit esatto in `UPSTREAM.json`. CiccioOffice è un progetto
indipendente, non supportato né approvato da ArtCraft o Microsoft. I motori delle tre
applicazioni sono quelli originali: il cambio di nome non elimina le limitazioni
di compatibilità e stabilità descritte nei rispettivi `docs/gaps.md` e `ROADMAP.md`.
I motori conservano la versione upstream 0.8.0, distinta dalla versione della suite.

## Installazione dei pacchetti compilati

- **Windows 10/11, x64 / ARM64:** aprire il file `.msi`. Sono installate le tre app,
  disponibili nel menu Start, con disinstallazione dalle Impostazioni.
  In alternativa estrarre lo ZIP portable e avviare gli `.exe`.
- **macOS Intel / Apple Silicon:** aprire il `.dmg` e trascinare la cartella
  `CiccioOffice` nel collegamento `Applications`. In alternativa aprire il `.pkg`.
  Le tre app vengono installate
  in `/Applications/CiccioOffice`. Le build di sviluppo sono firmate ad hoc e non
  notarizzate; la distribuzione pubblica richiede una firma Developer ID e notarizzazione.
- **Linux Ubuntu 24.04 / Debian compatibile, x64 / ARM64:**
  `sudo apt install ./CiccioOffice-0.1.0-linux-x64.deb` (scegliere ARM64 se necessario).
  Disinstallare con `sudo apt remove cicciooffice`.
  Il `.tar.gz` contiene l'albero `usr` per altre distribuzioni con glibc 2.39 o
  successiva e librerie equivalenti. Non è un eseguibile statico universale;
  per distribuzioni più vecchie compilare dai sorgenti sul sistema di destinazione.

Questa cartella contiene i sorgenti e le ricette di compilazione. Gli installer
esistono solo dopo una compilazione riuscita: consultare `VALIDAZIONE.md` per lo
stato realmente verificato. Non sono presenti installer Windows/macOS precompilati.

## Compilazione automatica su GitHub

1. Creare un repository GitHub e caricare **il contenuto** di questa cartella
   alla sua radice, inclusa `.github/workflows/build.yml`.
2. Aprire **Actions → Build CiccioOffice → Run workflow**.
3. Al completamento scaricare gli artifact di ogni piattaforma: `.msi` e ZIP
   su Windows; `.dmg` e `.pkg` su macOS; `.deb` e `.tar.gz` su Linux.

La matrice compila nativamente Windows x64/ARM64, macOS Intel/Apple Silicon e
Linux x64/ARM64. Il workflow non pubblica release, non invia modifiche ai progetti
originali e non usa certificati o credenziali dei loro autori. Disponibilità dei
runner, costi e quote dipendono dall'account GitHub. Le build e gli installer su
sistemi non disponibili in questa sessione devono ancora essere verificati.

## Compilazione locale

Requisiti comuni: Python 3.11+, Rust **1.99.1** con Cargo, accesso a crates.io
e GitHub per scaricare le dipendenze fissate nei `Cargo.lock`.

Ubuntu 24.04:

```sh
sudo apt update
sudo apt install build-essential pkg-config libasound2-dev libudev-dev \
  libxkbcommon-dev libfontconfig1-dev libssl-dev libx11-dev libwayland-dev \
  libegl1-mesa-dev dpkg-dev
python3 scripts/build.py
```

Windows: installare Visual Studio Build Tools (C++ desktop + Windows SDK), Rust
MSVC, Python e .NET SDK. Installare WiX con
`dotnet tool install --global wix --version 5.0.2`, poi `python scripts/build.py`.
Per ARM64 serve la toolchain ARM64 e `--target aarch64-pc-windows-msvc`.

macOS: installare Xcode Command Line Tools, Rust e Python. Eseguire
`python3 scripts/build.py`; per un'architettura specifica usare
`--target aarch64-apple-darwin` oppure `--target x86_64-apple-darwin`,
con il target Rust corrispondente installato. `pkgbuild` e `codesign` sono inclusi
negli strumenti Apple. Non è prevista compilazione macOS da Linux.

Le build richiedono tempo e diversi GB. Output in `dist/`, checksum SHA-256 inclusi.
La compilazione della suite disattiva thin LTO: nel primo tentativo con la
toolchain fissata il linker ha segnalato simboli mancanti. Le funzionalità sono
invariate; cambia soltanto questa ottimizzazione di compilazione.
`python3 scripts/smoke.py` verifica salvataggio/riapertura DOCX, esportazione PDF,
calcolo e riapertura XLSX, creazione e riapertura PPTX. Non è una certificazione
di compatibilità con tutti i documenti Microsoft Office.
Per usare una cartella temporanea esterna per gli oggetti di compilazione,
impostare `CICCIO_TARGET_DIR` a un percorso assoluto; usare lo stesso valore
anche per `scripts/smoke.py` e per `--skip-build`.
Il programma di compilazione si interrompe al primo errore senza presentare
pacchetti incompleti come riusciti. `--skip-build` richiede binari già compilati
in `target/native/<target-opzionale>/release/`.

## Identità e licenze

Titoli visibili e icone sono CiccioOffice. I nomi interni dei crate Rust, i
protocolli e i formati nativi originali restano invariati per ridurre il rischio
di incompatibilità. Ogni app mantiene i crediti dei contributori originali.
Loghi ArtCraft rimossi; icone applicazione sostituite dal chihuahua.

Codice originale: MIT OR Apache-2.0, con testi, copyright, `NOTICE` e attribuzioni
originali conservati sotto `apps/`. Codice di integrazione CiccioOffice: MIT,
si veda `LICENSE`. L'icona è generata appositamente per questo progetto;
provenienza e prompt in `branding/ATTRIBUTION.md`.
