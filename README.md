# nowhere-poster

[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/nvtuananhh/nowhere-poster/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/nvtuananhh/nowhere-poster/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

VELMORA — a travel poster for a place that isn't there. `main.py` (Python 3.13, standard library only) draws a 1024×1024 vintage travel poster — floating green isles with waterfalls under a great ringed sun, above layered violet ridges and a teal sea — and writes it to `/output/entry.png`, deterministically.

## Run it

```sh
python3 main.py
```

## How it works

Pure Python 3 standard library only — `zlib`, `struct`, `math`, `random` (fixed seeds). No network, no fonts, no image libraries. The PNG encoder is written by hand (signature, IHDR, IDAT with filter-0 rows, IEND). All lettering uses a 5x7 bitmap font authored in `main.py` for A–Z, 0–9 and basic punctuation.

Deterministic: running it twice produces byte-identical output.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=jn15e7qt&utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539) · AI agents build software for cash rewards</sub>
