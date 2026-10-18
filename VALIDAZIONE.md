# Stato della consegna — CiccioOffice 0.1.0

Aggiornamento: 18 ottobre 2026. Versione sperimentale.

## Verifiche completate sui sorgenti

- Tre repository originali scaricati; commit registrati in `UPSTREAM.json`.
- Testi LICENSE-MIT, LICENSE-APACHE e NOTICE originali conservati byte per byte;
  checksum in `LEGAL-CHECK.json`.
- Nomi applicazione, identificatori e icone sostituiti; controllo `scripts/verify.py` passato.
- Script Python controllati con `py_compile`.
- Manifest MSI generato su dati di prova: XML valido, ID directory univoci,
  inventario completo dei file e tre collegamenti al menu Start.
- Icona chihuahua bianco e nero generata, controllata e convertita in PNG/ICO/ICNS.

## Compilazioni e pacchetti realmente completati

**Linux x64 (Ubuntu 24.04 / glibc 2.39): tutte e tre le app grafiche e le tre CLI
sono state compilate in modalità release.** Generati il pacchetto DEB e il tar.gz.
Il DEB è stato estratto in una cartella di prova; i test funzionali seguenti sono
passati anche sugli eseguibili estratti dal pacchetto, dopo la rimozione dei simboli.
I sei eseguibili rispondono a `--version`; `ldd` non segnala librerie mancanti.
Il tar.gz è stato letto interamente e contiene tutte e sei le applicazioni/CLI.

| Prova funzionale | Esito |
|---|---|
| CiccioWrite: TXT con accenti e simboli → DOCX → riapertura, testo preservato | Passata |
| CiccioWrite: DOCX → PDF, una pagina leggibile con testo selezionabile e accenti | Passata |
| CiccioCalc: 12 + 30 con SUM, salvataggio XLSX e riapertura, risultato 42 | Passata |
| CiccioCalc: controllo interno delle formule e fedeltà di riapertura XLSX | Passata, nessuna differenza |
| CiccioSlides: creazione da esempio, salvataggio PPTX, riapertura e controllo struttura ZIP | Passata |
| Attribuzioni degli asset, gate originali dei tre progetti | Passate: 45 / 24 / 37 file |
| 29 icone PNG confrontate con il chihuahua approvato, ridimensionato | Identiche |
| ICO/ICNS dei tre programmi confrontati con quelli della suite | Identici |

I primi tentativi di compilazione hanno incontrato errori del linker e un oggetto
vuoto. La build riuscita ha usato una cartella temporanea separata per gli oggetti
e thin LTO disattivato. Per CiccioSlides è stata resa disponibile la libreria ALSA
richiesta dal progetto originale. Il builder e il workflow dichiarano le dipendenze.

## Piattaforme predisposte, ancora da compilare

- Windows x64/ARM64: ricetta MSI/ZIP pronta; manifest XML controllato, installer nativo non prodotto qui.
- macOS Intel/Apple Silicon: ricette DMG e PKG pronte; plist controllati, installer nativo non prodotto qui.
- Linux ARM64: ricetta DEB/tar pronta; compilazione ARM64 non eseguita qui.

Il workflow GitHub è predisposto ma non è stato avviato. L'account collegato è
peppenitto; il connettore non restituisce repository accessibili e non espone
la creazione di repository o l'avvio diretto di workflow. Nessun repository è
stato creato o pubblicato. Il DMG deve ancora essere prodotto su macOS:
la ricetta usa hdiutil create e hdiutil verify e include il collegamento Applications.

## Limiti delle verifiche

La verifica visiva di CiccioCalc è riuscita con rendering fuori schermo a
1200×800, usando il documento di esempio e il renderer software Vulkan.
Non sono stati effettuati un collaudo manuale completo delle GUI, la suite
integrale `cargo xtask ci`, una certificazione di compatibilità Office, né
firma pubblica/notarizzazione degli installer. I limiti dei motori alpha originali
restano applicabili. I pacchetti presenti in `dist/` sono solo quelli Linux x64;
l'archivio sorgente non sostituisce un installer Windows o macOS.
