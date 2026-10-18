# Asset attribution

Every non-code asset in this repository (images, icons, fonts, example files, presets) is listed here with its author, source and licence. `cargo xtask assets` (part of `cargo xtask ci`) fails if an asset file is missing from this table.

**Policy (mandatory):** GridCraft contains **no Microsoft, Adobe, Avid or Autodesk iconography, images, artwork, fonts, templates, themes, table styles or sample files**. Every asset is original work by GridCraft contributors or third-party material under an open licence (OSI open source, public domain / CC0, or Creative Commons that allows redistribution). Screenshots of Microsoft software are never committed. Font files are not added here: shared fonts live in [storytold/craft-fonts](https://github.com/storytold/craft-fonts), an optional build input (`CRAFT_FONTS_DIR`). The one exception is the ArtCraft brand files in `docs/brand/`: ArtCraft trademarks, not open source, used under `docs/brand/LICENSE-brand.txt`.

Generated-in-code art is original and has no file to list: the UI icon set (`crates/ui-egui/src/icons.rs`), themes (`crates/engine/src/cmd/view.rs`), cell styles (`crates/engine/src/cmd/format.rs`), table styles (`crates/engine/src/tables.rs`), chart palettes and the sample workbooks (`crates/engine/src/sample.rs`).

| Asset | Author | Source | Licence | Notes |
|---|---|---|---|---|
| `assets/app-icon/README.md` | GridCraft contributors | original | MIT OR Apache-2.0 | Icon documentation |
| `assets/app-icon/LICENSE.txt` | (licence text) | original | — | Licence of the app icon files |
| `docs/images/hero-sales.png` | GridCraft contributors | screenshot of GridCraft rendered offscreen (`crates/ui-egui/examples/snapshot.rs`) showing an original sample workbook | MIT OR Apache-2.0 | README screenshot; no third-party content |
| `docs/images/budget.png` | GridCraft contributors | screenshot of GridCraft rendered offscreen (`crates/ui-egui/examples/snapshot.rs`) showing an original sample workbook | MIT OR Apache-2.0 | README screenshot; no third-party content |
| `docs/images/grades-formulas.png` | GridCraft contributors | screenshot of GridCraft rendered offscreen (`crates/ui-egui/examples/snapshot.rs`) showing an original sample workbook | MIT OR Apache-2.0 | README screenshot; no third-party content |
| `docs/images/dark-insert.png` | GridCraft contributors | screenshot of GridCraft rendered offscreen (`crates/ui-egui/examples/snapshot.rs`) showing an original sample workbook | MIT OR Apache-2.0 | README screenshot; no third-party content |
| `docs/images/pivot.png` | GridCraft contributors | screenshot of GridCraft rendered offscreen (`crates/ui-egui/examples/snapshot.rs`) showing an original sample workbook | MIT OR Apache-2.0 | README screenshot; no third-party content |
| `docs/images/format-chart.png` | GridCraft contributors | screenshot of GridCraft rendered offscreen (`crates/ui-egui/examples/snapshot.rs`) showing an original sample workbook | MIT OR Apache-2.0 | README screenshot; no third-party content |
| `docs/images/page-break.png` | GridCraft contributors | screenshot of GridCraft rendered offscreen (`crates/ui-egui/examples/snapshot.rs`) showing an original sample workbook | MIT OR Apache-2.0 | README screenshot; no third-party content |


## CiccioOffice replacement icons (2026-10-18)

Original generated Chihuahua icon; source and prompt in `../../branding/ATTRIBUTION.md`. Upstream ArtCraft trademark image files have been removed.

| File | Origin | License | Use |
|---|---|---|---|
| `assets/app-icon/gridcraft-1024.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/gridcraft-macos-512.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/gridcraft.icns` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/gridcraft.ico` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/gridcraft.svg` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/hicolor/128x128/apps/io.cicciooffice.cicciocalc.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/hicolor/16x16/apps/io.cicciooffice.cicciocalc.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/hicolor/24x24/apps/io.cicciooffice.cicciocalc.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/hicolor/256x256/apps/io.cicciooffice.cicciocalc.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/hicolor/32x32/apps/io.cicciooffice.cicciocalc.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/hicolor/48x48/apps/io.cicciooffice.cicciocalc.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/hicolor/512x512/apps/io.cicciooffice.cicciocalc.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/hicolor/64x64/apps/io.cicciooffice.cicciocalc.png` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `assets/app-icon/hicolor/scalable/apps/io.cicciooffice.cicciocalc.svg` | CiccioOffice; OpenAI-generated original `../../branding/chihuahua.png`, mechanically resized/packaged | MIT, to the extent protectable rights exist; see root LICENSE | Chihuahua application icon |
| `docs/brand/LICENSE-brand.txt` | ArtCraft Team; original upstream legal notice | Original trademark terms, retained as legal text only | Provenance; the trademark image assets are not distributed |
