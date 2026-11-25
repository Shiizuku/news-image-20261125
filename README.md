# The World in One Day — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Shiizuku/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Shiizuku/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A newspaper-broadsheet image summing up the world's news of Wednesday
25 November 2026 in one page. Entry for the
[make.fun](https://make.fun/bounty/news-image-20261125) competition
`news-image-20261125`.

## The six stories

1. **First Pakistani in orbit** — China's Shenzhou-24 blasts off for
   Tiangong with Muhammad Zeeshan Ali aboard, the first Pakistani in orbit
   and the first foreign astronaut to visit the Chinese space station.
   (Reuters, Xinhua)
2. **Houthi drone hits Riyadh's tallest tower** — eleven wounded as a drone
   strikes the 385-metre PIF tower in the King Abdullah Financial District,
   the second hit on the landmark in under a week. (Reuters)
3. **Kyiv confirms strike on Russian ship** — Zelenskiy says Ukraine hit a
   Russian cargo vessel in the Gulf of Finland; Moscow calls the drone
   attacks "terrorism". (Reuters)
4. **Huawei convicted in U.S. trial** — a federal jury convicts the Chinese
   telecoms giant over its Iran business in a sprawling criminal case.
   (Reuters)
5. **Medal of Freedom for Giuliani** — President Trump awards Rudy Giuliani
   the nation's highest civilian honour at the White House. (Reuters)
6. **Malaysia to return 6,500 Rohingya** — PM Anwar says refugees will be
   sent back to Myanmar in December, days after the ICJ genocide ruling.
   (Reuters)

## How it works

`draw_image.py` (Python stdlib + PIL only) draws the broadsheet from
scratch — masthead, hero rocket panel, tower panel and four story cards —
into `entry.png` (1024×823, PNG, under 1 MiB). It is fully deterministic:
running it twice produces byte-identical output.

`main.py` (stdlib only) copies `entry.png` into the directory named by
`MAKEFUN_OUTPUT_DIR` and verifies the copy's sha256.

```sh
python3 draw_image.py        # renders entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
