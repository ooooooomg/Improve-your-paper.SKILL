# Academic Skills for Claude Code

此技能从真实结合 AI 完成论文大修的实际经验中得出，希望能帮到从 0 开始科研的你。

## 安装

```bash
git clone https://github.com/your-username/academic-skills.git
cp -r academic-skills/paper-revision ~/.claude/skills/
cp -r academic-skills/code-debug ~/.claude/skills/
cp -r academic-skills/autodl-training ~/.claude/skills/
```

脚本依赖（按需安装）：
```bash
# autodl-training 需要 paramiko（SSH/SFTP）
pip install -r ~/.claude/skills/autodl-training/requirements.txt

# paper-revision 需要 lxml（docx 字体修复）
pip install -r ~/.claude/skills/paper-revision/requirements.txt
```

技能在触发条件匹配时自动加载。也可以显式调用 `/paper-revision`、`/code-debug` 或 `/autodl-training`。

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

## autodl-training — 云服务器训练部署与监控

用于在 AutoDL 或其他 SSH 可达的 GPU 服务器上部署并监控远程深度学习训练：代码/数据上传、环境配置、后台启动训练、每小时进度监控与微信推送。

**技能覆盖的问题：**

| 问题 | 方案 |
|------|------|
| 本机显存不够，需在云 GPU 上训练 | 完整部署流程：SSH 检查 → 环境配置 → 代码上传 → 权重/数据上传 → nohup 启动训练 |
| 大数据（10GB+）上传慢、易中断 | `scripts/upload_data.py` 分片断点续传，已传 shard 自动跳过 |
| Windows 下打包上传失败 | 用 python `tarfile` 而非 subprocess 调 tar（Windows tar 路径坑） |
| 训练要跑几十小时，想自动监控 | `scripts/monitor_server.py` 服务器端常驻，每小时间隔检查并推送 |
| 想及时知道训练是否异常 | 自动检测 OOM / NaN / Traceback / 梯度爆炸，微信推送 ⚠️ 警示 |
| 想把进度推到手机 | `scripts/wxpush.py` 封装 wxpusher API，一条命令推送 |
| 本机关机后训练进度丢失 | 训练和监控都用 nohup 跑在服务器上，独立于本机 |
| 想"配置一次后全流程自动" | `scripts/orchestrator.py` 一键：等传输完成 → 自动启动训练 → 自动启动监控推送 |

**技能中包含的 Claude 预训练语料中不存在的内容：**

- AutoDL 服务器 `python` 不在 PATH，须用 `/root/miniconda3/bin/python` 完整路径
- AutoDL 控制面板磁盘占用显示有刷新延迟，以服务器 `df -h` 为准
- 服务器镜像自带旧版 torch（如 1.10），训练代码需兼容而非升级服务器
- AutoDL 按量计费开机即扣费（含传输/空闲），余额只能在网页控制台查看

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
└── autodl-training/
    ├── SKILL.md
    ├── requirements.txt               # paramiko
    ├── scripts/
    │   ├── ssh_helper.py              # SSH/SFTP 连接、命令执行、文件传输
    │   ├── upload_data.py             # 分片数据上传（断点续传）
    │   ├── wxpush.py                  # wxpusher 微信推送
    │   ├── monitor_server.py          # 服务器端每小时训练监控（中文推送）
    │   ├── orchestrator.py            # 全自动编排：等传输→启动训练→启动监控
    │   └── start_train.sh             # 远程训练启动模板（nohup 后台）
    └── references/
        └── autodl-server-guide.md     # AutoDL 服务器管理速查（环境/磁盘/计费/常见坑）
```

## 许可

MIT

## 局限性

- **skill 是脚手架而非成品**：各 skill 提供的脚本是"工作流模板"，需按你的具体项目配置（路径、凭据、超参、产物命名）后才能运行，不保证开箱即用。
- **领域示例**：`autodl-training` 的评估章节以图像分割/检测类项目为例，其他领域需替换对应评估协议。
- **维护性**：随 Claude Code 版本演进，脚本所用 API 可能变化，使用前建议用 `-m py_compile` 或冒烟测试验证。

## 联系

本项目仍在改进中。如有建议、bug 报告或合作意向，欢迎联系作者：

**AshMe** — <AshMe37@outlook.com>
