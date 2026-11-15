# 大明国家机器

https://huzhe01.github.io/ming-state-machine/

从唐到近代的中国政治制度演变图解，重点拆解明朝：中枢（内阁票拟、司礼监批红）、奏章流转、军事（统兵与调兵分离）、地方（三司与督抚）、司法（三法司与厂卫）、赋役（一条鞭法）和制度时间线。明代数字和引文对照《明史》原文，出处列在页面末尾。

纯静态 HTML，所有图都是内联 SVG。

- `template.html`：正文、样式和交互脚本
- `build.py`：计算 8 张图的坐标，生成 `index.html`（Artifact 版）和 `docs/index.html`（GitHub Pages 版）

```bash
python3 build.py
```
