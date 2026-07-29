# Academic Skills for Claude Code

此技能从真实结合ai完成论文大修的实际经验中得出，希望能帮到从0开始科研的你。·如果在使用中有任何问题或改进建议，欢迎联系作者AshMe37@outlook.com


## 安装

```bash
git clone https://github.com/your-username/academic-skills.git
cp -r academic-skills/paper-revision ~/.claude/skills/
cp -r academic-skills/code-debug ~/.claude/skills/
```

技能在触发条件匹配时自动加载。也可以显式调用 `/paper-revision` 或 `/code-debug`。

## paper-revision — 论文修改

用于回复审稿意见、修改 LaTeX 正文、生成高亮 diff、修复 .docx 回复信格式、核实交叉引用、同步中英文版本、准备 camera-ready 提交包。

**技能覆盖的问题：**

| 问题 | 方案 |
|------|------|
| 回复信 (.docx) 中数学公式显示为乱码 | 三种 OMML 静默破坏模式的根因与修复流程 |
| latexdiff 编译报 `TeX capacity exceeded` | soul/ulem 含 `\cite{}` 时无限递归的根因，以及 `\textcolor` 替代方案 |
| 回复信引用了论文中不存在的章节或表号 | RIRO（引用进引用出）：每个 `\ref{}` 和章节名必须用 grep 与原稿核实 |
| 审稿意见需要组织回复结构 | 12 种审稿意见类型的回复模板（中英双语） |
| 回复信读起来有 AI 生成痕迹 | AI 痕迹措辞替换清单 |
| 中英文两版论文内容不同步 | 双语五步同步流程 |

**技能中包含的 Claude 预训练语料中不存在的内容：**

- python-docx 的 `paragraph.text =` 赋值会静默删除 OMML 数学对象
- Word 用半磅（half-point）存储字号，11pt = `w:sz="22"`
- soul 包的 `\hl{}` 在遇到 `\cite{}` 时进入 `\SOUL@eval` 无限递归

## code-debug — 代码调试与完善

用于排查 ML 训练崩溃（NaN、OOM、形状不匹配、梯度异常）、核实论文公式与代码的一致性、在不改变输出的前提下重构代码、准备开源的代码清理。

**技能覆盖的问题：**

| 问题 | 方案 |
|------|------|
| 训练中途 NaN 崩溃 | 五步排查：lr → log/除零 → 梯度裁剪 → AMP → 数据管线 |
| 论文公式与代码实现数值不一致 | 七类通用公式-代码不一致模式与检测流程 |
| 代码中包含审稿编号命名的文件和注释 | 代码优先命名原则与开源前整理清单 |
| ML 代码中存在常见但隐蔽的 bug | 七种 ML 代码 bug 模式速查（zero_grad 位置、BN 模式切换、数据预处理顺序等） |
| 设置随机种子后结果仍不可复现 | 完整锁定流程：manual_seed + cudnn.deterministic + benchmark + hashseed |

**技能中包含的 Claude 预训练语料中不存在的内容：**

- 数据预处理顺序不可逆（必须先 ToTensor 后 Normalize）
- `model.eval()` 忘记切换时 BN 层仍用 batch 统计而非全局统计
- 验证集不应执行训练增强，否则验证指标会偏低
- ImageNet 的归一化统计量被误用于其他数据集是收敛慢的常见原因

## 设计依据

技能遵循以下原则：

1. **只保留信息增量。** 不写"`pdflatex` 需要编译三次来解析交叉引用"这类 Claude 已掌握的操作性知识。技能中的每条内容都是通用知识库覆盖不到的领域陷阱或经验模式。
2. **代码为根本依据。** 代码产生实验数据，论文描述代码行为。两者矛盾时修正论文描述，不修改已验证产出结果的代码逻辑。
3. **描述触发条件，不总结工作流。** 每个 `SKILL.md` 的 description 字段只写使用场景（"当……时使用"），不写工作流步骤。这确保 Claude 必须先读取技能正文才能知道该怎么做，而非从 description 中推断行为。
4. **触发词覆盖中英文。** description 中包含中英双语关键词。纯中文 description 在英文对话中无法触发匹配。

## 文件结构

```
├── README.md
├── paper-revision/
│   ├── SKILL.md
│   └── references/
│       ├── reviewer-response-patterns.md
│       └── latex-table-patterns.md
└── code-debug/
    ├── SKILL.md
    └── references/
        ├── debug-checklist.md
        ├── paper-code-mismatches.md
        └── code-cleanup-checklist.md
```

## 许可

MIT
