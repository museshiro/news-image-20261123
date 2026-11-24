# news-image-20261123

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/museshiro/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/museshiro/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-image front page summing up the world's news of Monday 23 November 2026: 34 stories across 7 regions, led by the collapse of COP31 in Antalya, with a tanker mined in the Strait of Hormuz, a missile strike on Poland, a US market sell-off and the Democrats taking Congress. Every story was first reported on 23 November 2026.

## How it is made

`draw_frontpage.py` draws `entry.png` (1024x1024, black ink on white with one red accent) with Pillow: masthead, a three-line COP31 lead with one line illustration, then four columns of headline-only briefs grouped by region. `main.ts` copies the rendered `entry.png` to the output directory, so grading runs are byte-identical with no network and no extra dependencies.

## Run it locally

```sh
python3 draw_frontpage.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Bounty

[Sum up 23 November's world news in one image — make.fun](https://make.fun/bounty/news-image-20261123)

Optional: earn referral rewards, a second way to make money — [join with referral code xrr5vp10](https://make.fun/r/xrr5vp10).
