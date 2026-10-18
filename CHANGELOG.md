# CiccioOffice 0.1.0 — 18 ottobre 2026

- Raccolti i tre progetti desktop originali ai commit riportati in `UPSTREAM.json`.
- Nomi visibili CiccioWrite, CiccioCalc e CiccioSlides.
- Icona originale: chihuahua bianco e nero, con formati PNG, ICO e ICNS.
- Rimossi i loghi ArtCraft soggetti a licenza di marchio separata.
- ID delle applicazioni `io.cicciooffice.*`; cartelle preferenze distinte.
- Crediti, copyright e licenze originali conservati.
- Compilatore Rust fissato e dipendenze originali fissate nei Cargo.lock.
- Script unico per compilazione nativa e pacchetto suite.
- Ricette MSI + portable per Windows, PKG per macOS, DEB + tar per Linux.
- Matrice GitHub Actions per x64 e ARM64 su ciascun sistema.
- Controlli automatici di marchio, provenienza, DOCX/PDF, XLSX e PPTX.
- Thin LTO disattivato nel builder dopo un errore di collegamento della prima build.

Nessuna nuova funzione di elaborazione documenti è stata aggiunta ai motori
originali. La compatibilità con Office resta quella delle rispettive versioni
upstream, ancora sperimentali. Le verifiche effettivamente eseguite e gli
eventuali limiti di questa consegna sono elencati in `VALIDAZIONE.md`.
