---
name: paper-revision
description: Use when responding to reviewer comments (rebuttal, revise-and-resubmit), editing LaTeX manuscript text or tables, generating highlighted diff PDFs with latexdiff, fixing .docx response letter formatting issues (font inconsistency, missing math objects), verifying cross-references between response and manuscript, synchronizing bilingual (Chinese/English) papers, or preparing final resubmission packages. 当需要回复审稿意见、修改LaTeX论文、生成高亮diff、修复.docx回复信格式、核实交叉引用、同步中英文论文、或准备重修提交包时使用。触发词：reviewer response rebuttal revise-and-resubmit camera-ready proof 审稿意见 回复信 latexdiff 高亮手稿 论文修改
---

# 论文修改

## 概述

学术论文 revise-and-resubmit 系统化工作流。核心原则：**每条声称必须与论文原文核实；代码与论文矛盾时以代码为准。**

## 何时使用

- 收到审稿意见，需回复并修改论文正文
- 回复信 (.docx) 出现格式异常（字体大小不一、数学公式/下标显示为乱码）
- 需生成修改高亮 PDF 但常规 latexdiff 编译崩溃
- 回复信中引用"Table 2""Section 4.1"等需逐一核实
- 维持中英文两版论文同步
- 准备 camera-ready 或最终提交包

## 何时不用

- 从零写论文 → `research-writing-skill`
- 处理 Word/PPT 格式的正文 → `office-academic-skill`
- 调试或整理实验代码 → `code-debug`

## 快速参考

| 任务 | 关键操作 | 注意 |
|------|----------|------|
| 编辑 LaTeX | 精确匹配 `old_string`，多文件改动用 `replace_all` | 先 `grep` 确认范围 |
| 表格加行 | `\textbf{值}`=最优，`\underline{值}`=次优 | 新增最优行时旧行降级 |
| 回复信引用核实 | 对每个 `\ref{}` 和章节名 `grep` 论文源码 | 新增章节会使编号整体漂移 |
| .docx 数学对象 | XML 层操作 `lxml.etree`，检查 `w:sz` 为 `"22"` | 绝不用 `paragraph.text =` |
| latexdiff | `\textcolor{blue}` 替代 `\hl{}`防 `\cite` 崩溃 | 加 `--append-safecmd` 保护自定义命令 |
| 两版 TeX diff | 按节 `diff` 源码，不用 PDF 文本提取 | PDF 断字和双栏布局产生巨量噪音 |
| 提交前检查 | 清理 `.aux` `.log` `.out`，更新 `.gitignore` | `grep "undefined" paper.log` |

## 回复信 (.docx) — 三种静默破坏模式

1. **`paragraph.text = "..."`** — python-docx 高层 API 静默删除所有 OMML 数学对象，带下标的指标名变成残文
2. **字号翻倍** — 未读取现有 `w:sz` 就硬编码，11pt = 半磅值 `"22"`，写成 `"44"` 则字号翻倍
3. **数学下标丢失** — 清空段落重写时 OMML `m:sSub` 元素被丢弃

**修复流程：发现（提取 XML 看 w:sz/w:rFonts）→ 编辑（修改 w:r 元素，用 OMML m:sSub 处理下标）→ 验证（全文档 w:sz 应唯一值 `"22"`）。** 委托给 `docx` skill 或使用 `lxml.etree` 直接操作 XML。

## 高亮 PDF (latexdiff) — soul/ulem 与学术论文不兼容

`soul` 的 `\hl{}` 和 `ulem` 的 `\sout{}` 遇到 `\cite{}` 会触发 `\SOUL@eval` 无限递归。新增段落引用密集时编译必然崩溃。

**唯一稳定方案：**
```latex
\providecommand{\DIFadd}[1]{\textcolor{blue}{#1}}
\providecommand{\DIFdel}[1]{\textcolor{red}{#1}}
```
外加：`latexdiff --append-safecmd="\Figure" --append-safecmd="\Table" old.tex new.tex > diff.tex`

## 双语论文同步

同步流程：英文版修改完成并编译通过 → `git diff` 或 `latexdiff` 提取修改集 → 逐条映射到中文版对应位置 → 中文版 `xelatex` 编译 → 双版本交叉引用一致性检查。中文用 XeLaTeX + UTF-8 + `\usepackage{xeCJK}`。

## 回复措辞 — 避免 AI 痕迹

| 去除 | 替换为 |
|------|--------|
| We fully recognize / We sincerely appreciate | 直接陈述操作 |
| comprehensive investigation | we examined / we compared |
| 明确承认 / 我们承认 | 直接陈述实验数据 |
| insightful comment from the reviewer | 删除，直接回应 |

**正确回复结构：** (1) 可选：一句客观的合理性陈述，(2) 具体做了什么改动，(3) 关键结果，(4) 论文位置交叉引用。

## 常见错误

| 错误 | 修正 |
|------|------|
| 回复信引用的章节名/表号在论文中不存在 | 写之前 `grep` 核实；新增内容后重新统计编号 |
| `paragraph.text =` 后数学公式变成乱码 | 用 `lxml.etree` 在 XML 级别编辑 |
| latexdiff 含 `\cite` 编译 `TeX capacity exceeded` | 改用 `\textcolor` 方案 |
| 对比两版 PDF 产生数百条假差异 | 按节 diff TeX 源码 |
| 修改了审稿人没要求的段落 | 始终问：这条修改对应哪条审稿意见？ |
| 回复信中承认"我们的不足"过度道歉 | 直接陈述实验事实和原因，不做姿态性检讨 |

## 配套文件

- `references/reviewer-response-patterns.md` — 审稿意见→回复的通用应对模式与措辞范例
- `references/latex-table-patterns.md` — 学术表格格式化参考与常见模板
