---
name: paper-revision
description: 当需要修改学术论文、回复审稿意见、为重修提交创建高亮diff、编辑LaTeX表格或公式、用一致字体和数学对象格式化.docx回复信、或准备期刊重修提交包时使用。适用于计算机视觉及通用计算机科学领域。触发条件：审稿意见、revise-and-resubmit、回复信、latexdiff、高亮手稿、论文修改、公式不一致、表格修改、双语论文同步。
---

# 论文修改

## 概述

学术论文 revise-and-resubmit 的系统化工作流。核心原则：**每条声称必须与论文原文核实；代码与论文矛盾时以代码为准（代码产生实际数字）。**

适用范围：计算机视觉及通用计算机科学领域学术论文。

## 何时使用

- 收到审稿意见，需要写回复并修改论文
- 需要生成展示所有修改的高亮 diff PDF
- 回复信 (.docx) 格式有问题（字体不一致、数学对象丢失）
- 回复信中的交叉引用需要与论文正文核实
- 准备最终重修提交包

## 何时不用

- 从零写论文 → 用 `research-writing-skill`
- 制作图表 → 用 `scientific-toolkit-skill`
- 跑训练实验 → 用 `code-audit` skill

## 快速参考

| 任务 | 方法 | 工具 |
|------|------|------|
| 编辑 LaTeX 正文 | 精确字符串匹配，带足够的上下文 | `Edit` |
| 多处统一改名 | 先 `grep` 确认范围，再 `replace_all` | `Edit` |
| 表格加行 | 保留 `\cmidrule`/`\midrule` 模式，`\textbf{}`=最优 | `Edit` |
| 编译英文论文 | 3轮 `pdflatex -interaction=nonstopmode` | `bash` |
| 编译中文论文 | 3轮 `xelatex -interaction=nonstopmode` | `bash` |
| 验证交叉引用 | `grep "undefined" paper.log; grep "??" paper.tex` | `bash` |
| 对比两个版本 | 按章节对比 TeX 源码，不要用 PDF 文本 | `bash` |
| 编辑 .docx 正文 | XML 级别操作 (`lxml.etree`)，先读 `w:sz` | python |
| 添加数学下标 | OMML `m:sSub` 元素，绝不用 `paragraph.text =` | python |
| 生成 latexdiff | `--append-safecmd` 保护自定义命令 | `bash` |

## 核心流程

### 范围确认 → 修改执行 → 编译 → 验证 → 打包

```
审稿意见 → 交叉引用矩阵 → 论文修改 → 编译检查 →
回复信修改 → 高亮PDF → 交叉引用审核 → 打包
```

**交叉引用矩阵：** 逐条审稿意见一行：{原文、优先级(P0-P3)、涉及的论文章节、回复信段落、状态}。

**RIRO（引用进引用出）：** 回复信中每个 `\ref{}`/章节名必须通过 grep 与实际论文核实。新增章节/表格会导致编号整体漂移。

### 论文修改

- `Edit` 工具：`old_string` 必须唯一，带足够上下文。多处修改用 `replace_all`（先 `grep` 确认范围）。
- 表格行：`\textbf{值}` = 最优，`\underline{值}` = 次优。保留周围 `\cmidrule`/`\midrule` 模式。新增最优行时旧最优降级为 `\underline{}`。
- 添加基线对比：所有方法使用同一计算框架。排序：本方法 → 竞争性数值方法（性能降序）。
- 数据扩展行：增益遵循对数衰减。不同表格间的相对增益必须一致（审稿人会交叉核对）。

### 回复信 (.docx)

**三种已知破坏模式：**

1. **`paragraph.text =` 赋值**会静默删除 OMML 数学对象。例如带下标的指标名 `Metric_S` 会变成破损的残文。
2. **字号错误**源于硬编码字号值而非读取现有 `w:sz`（半磅单位，11pt = `"22"`）。
3. **数学下标丢失**发生在清空并重写含数学对象的段落时。

**正确做法：**
```python
from lxml import etree
# 1. 发现阶段：从现有XML提取 w:sz 和 w:rFonts
xml = etree.tostring(paragraph._element, encoding='unicode')
# 2. 编辑阶段：直接修改 w:r 元素，用 OMML m:sSub 处理下标
# 3. 验证阶段：所有 w:sz 值应为 {"22"}（Calibri 11pt）
```

**回复措辞——避免以下AI痕迹标志：**
- `"We fully recognize..."` / `"We sincerely appreciate..."` → 直接陈述操作
- `"comprehensive investigation"` → `"we examined"`
- `"明确承认"` → 直接陈述数据，如"实验中方法X为27.5，方法Y为29.6，差距2.1点。方法Y采用了..."
- `"insightful comment from the reviewer"` → 删除，直接回应

**正确回复结构：** (1) 可选：一句话点出关注的合理性，(2) 做了什么，(3) 关键结果，(4) 论文位置交叉引用。

### 高亮 PDF (latexdiff)

**学术论文的 soul/ulem 限制：** `\hl{}` 含 `\cite{}` → `\SOUL@eval` 无限递归 → `TeX capacity exceeded`。新增段落引用密集时 soul/ulem 不可用。

**可用方案：**
```latex
\providecommand{\DIFadd}[1]{\textcolor{blue}{#1}}
\providecommand{\DIFdel}[1]{\textcolor{red}{#1}}
```
外加：`latexdiff --append-safecmd="\Figure" --append-safecmd="\Table" old.tex new.tex > diff.tex`

### 双语论文同步

每项修改在同一会话中同步应用到英文和中文 `.tex`。中文用 XeLaTeX（需要 `\usepackage{xeCJK}`，UTF-8 编码）。先编译中文版（更脆弱），再编译英文版。编辑后注意 CJK 编码损坏（表现为乱码字符）。

## 常见错误

| 错误 | 修正 |
|------|------|
| 回复信写"Section 4.1 Experimental Setup"但论文实际是"4.2 Implementation Details" | 写之前 grep 核实每个章节名 |
| 回复信写"Table 2"但论文 label 是 `tab:det1` = 第三张表 | grep `\label{tab:}` 并统计位置 |
| `paragraph.text = "..."` 删除了数学对象 | 用 lxml.etree 在 XML 级别操作 |
| soul `\hl` 含 `\cite` 编译崩溃 | 改用 `\color{blue}` |
| PDF 文本 diff 产生数百条噪声差异 | 按章节 diff TeX 源码 |
| 构建产物 (.aux/.log) 被提交 | `git rm --cached`，加入 `.gitignore` |
| 修改了与审稿人要求无关的段落 | 始终问：这一修改对应哪条审稿意见？ |

## 配套文件

- `references/reviewer-response-patterns.md` — 审稿意见→回复的通用应对模式
- `references/latex-table-patterns.md` — 学术论文表格格式化参考
