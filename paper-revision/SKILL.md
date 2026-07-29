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
| 回复信引用核实 | 对每个 `\ref{}` 和章节名 `grep` 论文源码；提交前跑 `scripts/verify_cross_refs.py &lt;目录&gt;` 做全量扫描 | 新增章节会使编号整体漂移 |
| .docx 数学对象 | XML 层操作 `lxml.etree`；`scripts/validate_docx_fonts.py` 检查字号一致性；`scripts/fix_docx_fonts.py` 自动修复 | 绝不用 `paragraph.text =` |
| latexdiff | `\textcolor{blue}` 替代 `\hl{}`防 `\cite` 崩溃 | 加 `--append-safecmd` 保护自定义命令 |
| 两版 TeX diff | 按节 `diff` 源码，不用 PDF 文本提取。`scripts/semantic_diff.py old.tex new.tex` 自动按节对比 | PDF 断字和双栏布局产生巨量噪音 |
| 提交前检查 | 清理 `.aux` `.log` `.out`，更新 `.gitignore` | `grep "undefined" paper.log` |
| **防止死循环** | **同一命令最多重试 3 次；3 次失败后报告具体错误给用户，不继续重试** | **编译失败先读 .log，不无修改地反复编译** |

## 回复信 (.docx) — 三种静默破坏模式

1. **`paragraph.text = "..."`** — python-docx 高层 API 静默删除所有 OMML 数学对象，带下标的指标名变成残文
2. **字号翻倍** — 未读取现有 `w:sz` 就硬编码，11pt = 半磅值 `"22"`，写成 `"44"` 则字号翻倍
3. **数学下标丢失** — 清空段落重写时 OMML `m:sSub` 元素被丢弃

**修复流程：发现（提取 XML 看 w:sz/w:rFonts）→ 编辑（修改 w:r 元素，用 OMML m:sSub 处理下标）→ 验证（运行 `scripts/validate_docx_fonts.py file.docx` 检查全文字号字体一致性）。** 委托给 `docx` skill 或使用 `lxml.etree` 直接操作 XML。

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
| 同一命令反复执行无进展（死循环） | 编译失败先读 .log 定位根因再改源文件；连续 3 次失败报告用户 |
| .aux/.log/.out 被提交到 git | .gitignore 中加入 `*.aux` `*.log` `*.out` `*.synctex.gz` |
| LaTeX 编译报 `can't write on file` | `rm paper.pdf` 后重新编译（PDF 被阅读器锁定） |
| CJK 中文版编译出现乱码字符 | 不从 PDF 复制中文回源文件；确保 .tex 保存为 UTF-8 |

## 论文版本管理 — 防止混乱与丢失

以下问题来自实际论文修改过程中反复出现的情况。

### 版本命名约定

每次重大修改前，先复制当前版本到带编号的新文件（如 `paper_v2.tex`、`paper_v3.tex`），保留所有中间版本。不要直接在唯一副本上修改。

会话开始时，先 `git status` 和 `ls *.tex` 确认当前工作版本是哪一份。不要假设"上次改的是 v3"——读取文件头部注释或 git log 确认。

### 提交与备份

每完成一轮修改（如"处理完审稿人 1 的三条意见"）后立即 git commit。单次 commit 的变更范围应控制在 50-200 行。如果修改涉及多个独立关注事项，拆分为多个 commit。不要等到所有审稿意见都处理完再提交——进程崩溃或会话超时会丢失全部未提交的修改。

每日工作结束后将修改 push 到远程仓库。本地 git 历史在进程异常退出时可能损坏。

### 恢复丢失的修改

当会话异常退出导致修改丢失时，先检查 git reflog 和 `git stash list`。如果修改确实只在丢失的会话中存在过，重新执行修改时必须以**完全相同的旧文件为基准**——如果在此期间文件已被其他操作改动，先 git diff 确认当前基准与上次是否一致，再重新应用修改。不要在已经部分修改的文件上盲目重新执行——先 `git checkout` 回到干净状态。

### 修改前的确认机制

当用户在会话中途说"取消对论文的修改"时，确认用户指的是撤销**哪些**修改——是本次会话的全部修改，还是某个特定操作，还是所有修改（包括之前会话的）。确认后再执行，并告知用户哪些已被撤销、哪些保留。

## 避免循环与上下文过载

以下问题来自实际论文修改会话中两次出现无意义循环的情况（用户两次中断并要求停止）。

### 循环的症状与触发条件

**症状：** Claude 在多个 `Bash`/`Grep`/`Read` 调用之间循环，每轮输出基本相同，而不推进实际任务。

**常见触发条件：**
- 一次处理过多关注事项（如 6 条审稿意见同时放在一个 prompt 中）
- 编译失败后用相同命令反复重试而不修改源文件
- 上下文窗口接近上限时，前期信息被截断导致重复读取同一段代码
- 用户 prompt 过于宽泛（"完成所有修改"）而没有明确的单步目标

### 防止措施

- 每次聚焦一条审稿意见，完成并验证后再处理下一条
- 编译失败超过两次时：先读 `.log` 文件定位具体错误，修改 `.tex` 源文件，再重新编译。不要无修改地反复编译
- 如果发现自己在重复之前做过的操作，立即停止，问用户"当前优先级是什么，是否继续当前方向"
- 使用 TaskCreate 将大任务拆分为明确的子任务，每完成一个标记 completed

### 用户中断后的恢复

当用户说"不要再循环了"或"停止"时：立即停止所有操作，用一句话说明当前状态（完成了什么、卡在什么地方），然后等待用户给出下一个具体指令。不要主动重新开始被中断的任务。

## 模型切换与多会话管理

以下问题来自实际论文修改过程中中途切换 Claude 模型、以及多会话并行导致状态丢失的情况。

### 模型切换的影响

- 切换到不同模型（如 sonnet → haiku → opus → fable）可能导致模型对前面上下文的"理解"不同。切换后应先用一句话确认当前论文的版本状态和修改进度
- 部分模型可能不支持特定路由（`claude-fable-5` 返回 "模型路由未配置"），切换前确认目标模型可用
- 如果切换模型后发现输出质量明显下降，考虑回到之前的模型完成关键步骤，或缩小任务范围

### 后台进程与会话退出

- `run_in_background: true` 启动的后台子代理在主会话退出时会**丢失状态**
- 重新打开会话时，不要假设后台任务已完成——检查其输出目录是否有部分结果
- 关键操作（如编译、完整性检查）不要放在后台——在前台执行以便即时看到结果

### 跨会话状态

- `.claude/skills/` 和 `CLAUDE.md` 跨会话持久化，但对话中的中间理解不持久化
- 每新开会话时，先确认：当前论文版本、已完成的修改列表、待处理的审稿意见、上次卡在哪里
- 如果使用 memory 功能，保存关键决策而非工作进度（memory 适用于长期偏好，不适用于短期任务状态）

## 配套文件

- `references/reviewer-response-patterns.md` — 审稿意见→回复的通用应对模式与措辞范例
- `references/latex-table-patterns.md` — 学术表格格式化参考与常见模板
