# Claude Code Academic Skills

此技能从真实结合ai完成论文大修的实际经验中得出，希望能帮到从0开始科研的你。

## 安装

**项目级**（仅当前项目可用）：
```bash
cp -r paper-revision/ your-project/.claude/skills/
cp -r code-audit/ your-project/.claude/skills/
```

**全局**（所有项目可用）：
```bash
cp -r paper-revision/ ~/.claude/skills/
cp -r code-audit/ ~/.claude/skills/
```

## 技能概览

### `paper-revision` — 论文修改

revise-and-resubmit 的系统化工作流。

- LaTeX 论文编辑与编译验证
- 审稿意见→回复信的 7 种通用应对模式
- .docx 回复信格式修复（OMML 数学对象保护、字体一致性）
- latexdiff 高亮 PDF 生成（解决 soul/ulem 含 `\cite` 崩溃问题）
- 双语（中/英）论文同步修改
- 回复信中 AI 痕迹措辞检测与替换指南

### `code-audit` — 代码审计

机器学习训练代码库学术诚信审查。

- 10 种伪造数据统计指纹及检测命令
- 7 类论文-代码公式不一致模式编目
- 训练日志修复规程（从真实数据源修复，绝不凭空编造）
- 代码优先命名原则（去除审稿人框架标记）
- 14 项可交付性门禁检查清单

## 使用方式

技能由 Claude Code 根据任务上下文**自动加载**，无需手动调用。触发条件写在每个 `SKILL.md` 的 `description` 字段中。

也可以手动调用：
```
/paper-revision
/code-audit
```

## 设计原则

1. **代码为根本依据** — 代码与论文矛盾时改论文，不改代码
2. **先验证再断言** — 每条声称必须通过 grep/Read 核实
3. **伪造数据有统计指纹** — 真实训练的自然方差无法被简单复制
4. **最小化修改** — 只改审稿人要求的，不顺手"润色"无关段落

## 适用范围

计算机视觉及通用计算机科学领域的学术论文修改与代码审计。技能本身不绑定特定期刊、数据集或方法。


## 许可

MIT
