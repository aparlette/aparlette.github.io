---
title: "Photo Gallery"
description: "Photos."
---

Placeholder. Blowfish's `gallery` shortcode builds a lightbox grid from plain
image tags — drop files into this page's bundle and reference them:

```
{{</* gallery */>}}
  <img src="game-01.jpg" class="grid-w33" />
  <img src="game-02.jpg" class="grid-w33" />
  <img src="game-03.jpg" class="grid-w33" />
{{</* /gallery */>}}
```

Shown escaped until real images exist. Hugo generates the thumbnails at build
time, so you commit full-size originals once and never think about it again.
