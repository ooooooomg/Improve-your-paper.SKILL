# Academic Skills for Claude Code

此技能从真实结合 AI 完成论文大修的实际经验中得出，希望能帮到从 0 开始科研的你。

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
| 回复信 (.docx) 中数学公式显示为乱码 | 三种 OMML 静默破坏模式的根因与修复流程；`scripts/fix_docx_fonts.py` 自动修复字号不一致 |
| latexdiff 编译报 `TeX capacity exceeded` | soul/ulem 含 `\cite{}` 时无限递归的根因，以及 `\textcolor` 替代方案 |
| 回复信引用了论文中不存在的章节或表号 | RIRO：每个 `\ref{}` 和章节名必须用 grep 与原稿核实；提交前跑 `scripts/verify_cross_refs.py` 全量扫描 |
| 审稿意见需要组织回复结构 | 12 种审稿意见类型的回复模板（中英双语） |
| 回复信读起来有 AI 生成痕迹 | AI 痕迹措辞替换清单 |
| 中英文两版论文内容不同步 | 双语五步同步流程；`scripts/semantic_diff.py` 按节对比两个版本 |
| .docx 字号或字体不统一 | `scripts/validate_docx_fonts.py` 检测；`scripts/fix_docx_fonts.py` 自动修复 |
| 论文版本混乱、修改丢失 | 版本命名约定、提交纪律、恢复丢失修改的流程 |
| 同一命令反复执行陷入死循环 | 同一命令最多重试 3 次；编译失败先读 .log 定位根因 |

**技能中包含的 Claude 预训练语料中不存在的内容：**

- python-docx 的 `paragraph.text =` 赋值会静默删除 OMML 数学对象
- Word 用半磅存储字号，11pt = `w:sz="22"`
- soul 包的 `\hl{}` 在遇到 `\cite{}` 时进入 `\SOUL@eval` 无限递归

## code-debug — 代码调试与完善

用于排查 ML 训练崩溃（NaN、OOM、形状不匹配、梯度异常）、核实论文公式与代码的一致性、在不改变输出的前提下重构代码、准备开源的代码清理。

**技能覆盖的问题：**

| 问题 | 方案 |
|------|------|
| 训练中途 NaN 崩溃 | 五步排查：lr → log/除零 → 梯度裁剪 → AMP → 数据管线 |
| 论文公式与代码实现数值不一致 | 七类通用公式-代码不一致模式与检测流程 |
| 代码中包含审稿编号命名的文件和注释 | 代码优先命名原则与开源前整理清单 |
| ML 代码中存在常见但隐蔽的 bug | 七种 ML 代码 bug 模式速查 |
| 设置随机种子后结果仍不可复现 | 完整锁定流程：manual_seed + cudnn.deterministic + benchmark + hashseed |
| CUDA OOM 或驱动版本不一致 | `scripts/check_env.py` 输出完整环境信息 |
| Checkpoint 加载后参数全为零或随机值 | `scripts/verify_checkpoints.py` 区分真实 checkpoint 与残桩/空文件 |
| 多个实验结果文件中数值完全相同 | `scripts/check_data_integrity.py` 检测冻结值、时间戳碰撞、不可能零值 |
| 结果与预期不符但代码逻辑没问题 | `scripts/check_env.py` 排查环境差异导致的数值偏差 |

**技能中包含的 Claude 预训练语料中不存在的内容：**

- 数据预处理顺序不可逆（必须先 ToTensor 后 Normalize）
- `model.eval()` 忘记切换时 BN 层仍用 batch 统计而非全局统计
- 验证集不应执行训练增强
- ImageNet 归一化统计量被误用于其他数据集是收敛慢的常见原因

## 设计依据

1. **只保留信息增量。** 不写 Claude 已掌握的操作性知识。每条内容都是通用知识库覆盖不到的领域陷阱或经验模式。
2. **代码为根本依据。** 代码产生实验数据，论文描述代码行为。两者矛盾时修正论文描述。
3. **描述触发条件，不总结工作流。** 每个 `SKILL.md` 的 description 只写使用场景，不写工作流步骤。
4. **触发词覆盖中英文。** description 中包含中英双语关键词。

## 文件结构

```
├── README.md
├── README_EN.md
├── paper-revision/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── verify_cross_refs.py        # 检查 LaTeX 未定义引用和重复标签
│   │   ├── semantic_diff.py            # 按章节对比两版 .tex 文件
│   │   ├── validate_docx_fonts.py      # 检测 .docx 字号和字体不一致
│   │   └── fix_docx_fonts.py           # 自动修复 .docx 字号不一致
│   └── references/
│       ├── reviewer-response-patterns.md
│       └── latex-table-patterns.md
└── code-debug/
    ├── SKILL.md
    ├── scripts/
    │   ├── check_env.py                # 输出 PyTorch/CUDA/cv2 环境信息
    │   ├── verify_checkpoints.py       # 检测 .pt 残桩/空文件
    │   └── check_data_integrity.py     # 检测冻结值、时间戳碰撞、不可能零值
    └── references/
        ├── debug-checklist.md
        ├── paper-code-mismatches.md
        └── code-cleanup-checklist.md
```

## 许可

MIT
