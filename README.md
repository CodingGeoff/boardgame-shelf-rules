# 桌游店货架识别与规则文档

根据 5 轮共 16 张桌游店货架照片，逐层识别出的桌游清单，以及每款游戏的中文规则文档。

- 识别结果：约 167 种游戏和扩展，约 282 盒
- 规则文档：155 份，放在 [`boardgames/`](boardgames/) 文件夹
- 货架原图：[`photos/`](photos/)（16 张已全部上传）
- **规则合集**：[`boardgames/ALL_合集.md`](boardgames/ALL_合集.md)（全部 155 篇合成一个文件；如果 GitHub 因为文件太大不渲染，可以看 [上册 01–78](boardgames/ALL_合集_上册_01-78.md) / [下册 79–155](boardgames/ALL_合集_下册_79-155.md)）
- **智能选桌游网站**：<https://codinggeoff.github.io/boardgame-shelf-rules/>（[`index.html`](index.html)），支持中文和英文提问，可切换中英文界面
- **English rules / 英文规则**：[`boardgames/en/`](boardgames/en/README.md)，155 篇完整英文版（另有 [Part 1](boardgames/en/ALL_EN_part1_01-78.md) / [Part 2](boardgames/en/ALL_EN_part2_79-155.md) 合集）
- **高清照片（手机可打开）**：[`photos/web/`](photos/web/)（每张约 0.5–0.9 MB）；没有货架编号区域的特写在 [`photos/crops/`](photos/crops/)
- 总索引：[`boardgames/README.md`](boardgames/README.md)，按货架位置列出每款游戏的数量和文档链接，文末附待确认清单和资料说明

文中标 ⚠️ 的地方表示资料不足或版本待核对，请以盒内说明书为准。

## 智能选桌游（index.html）

打开 `index.html`（下载后双击即可离线使用；开启 GitHub Pages 后可以在线访问）：

- **✨ 智能推荐**：直接用中文或英文写想法（例如 “Something like Catan for 3-4 players, not too long”），也可以中英混写，例如“我们 5 个人，一小时以内，想玩吹牛或推理，别太烧脑，有一个 10 岁小朋友”，同时可以叠加人数、时长、年龄、复杂度、类型（想要或排除）等条件。
- **匹配算法**：
  - 中文意图解析：识别人数和人数区间、时长、年龄、复杂度、30 多类同义词，支持“不要…/别太…”这样的否定。
  - 英文意图解析：数字和英文数词、players/people、minutes/hours/half an hour、N-year-old、light/heavy、40 类英文同义词映射到中文标签；否定（no / not / without / avoid / non-）按从句判断范围；常见拼写错误自动纠正。
  - 提到具体游戏：问“where is Brass Birmingham”会把这款排第一；“像卡坦岛 / like Avalon but shorter”按游戏相似度（标签 IDF + 文档相似度 + 人数/时长/复杂度）推荐，并支持 shorter / lighter / heavier 这类相对条件。
  - 边缘情况：空输入、人数矛盾（会提示）、超大人数（100 人 → 找 20 人以上的游戏）、0 人、全部是否定条件、乱码输入；严格过滤下没有结果时自动放宽并提示。
  - 多维加权评分：人数、最佳人数、时长、年龄、复杂度、类型（按 IDF 加权）、文字相似度（字符二元组 TF-IDF 余弦）。
  - 严格过滤：不满足人数、年龄、排除项的游戏直接隐藏。
  - MMR 多样化重排：避免结果全是同一类游戏。
  - 每条结果都附推荐理由和评分明细，权重可以手动调整。
- **📍 位置**：每个结果都显示货架编号（黑色标签）；39 款看不到编号的游戏显示推断区域（黄色虚线，标“推断”），并附特写图。点照片在页面内打开高清版，可以放大。
- **📷 高清照片**视图：16 张货架照片 + 8 张无编号区域特写 + 39 款无编号游戏清单。
- **📖 文档**：在页面内阅读完整规则文档，可以在“中文原文（含深入玩法）”和“English rules”之间切换；还会列出“喜欢这款，也可以试试”的相似游戏。
- 另有“全部游戏”表格（可搜索、排序）、“货架地图”、“规则合集”三个视图。

## 文档结构

每篇 `boardgames/NN_*.md` = 原规则 + 新增的 **「深入玩法：教学、策略与易错点」** 章节，内容包括：一句话介绍、人数/时长/年龄/复杂度/标签、5 分钟教学顺序、进阶策略、常见错误、适合/不适合。

## 重新生成

`tools/` 中是生成脚本：元数据在 `tools/meta/m1–m5.py`，`deepen.py` 写入深入章节，`merge2.py` 生成合集，`build_en.py` 由 `tools/meta/en1–en4.py` 生成英文文档，`build.py` 加 `template.html` 生成 `index.html`。脚本里的路径是整理时的工作目录，使用时请按需修改。
