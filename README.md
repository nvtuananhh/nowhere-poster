# VELMORA — The Poster for a Place That Isn't There

A travel poster for an invented place: **VELMORA — the isles that rise
with the tide**. Floating green isles with waterfalls drift under a
great ringed sun, above layered violet ridges and a teal sea that
catches the sun's glitter. Big cream title, gold tagline, vintage
limited palette.

## Run

```sh
python3 main.py
```

Writes `/output/entry.png` (1024x1024 RGB PNG).

## How it works

Pure Python 3 standard library only — `zlib`, `struct`, `math`,
`random` (fixed seeds). No network, no fonts, no image libraries.
The PNG encoder is written by hand (signature, IHDR, IDAT with
filter-0 rows, IEND). All lettering uses a 5x7 bitmap font authored
in `main.py` for A–Z, 0–9 and basic punctuation.

Deterministic: running it twice produces byte-identical output.

## License

MIT — see `LICENSE`.
