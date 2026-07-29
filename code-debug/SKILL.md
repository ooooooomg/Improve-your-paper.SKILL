---
name: code-debug
description: Use when debugging ML training code (NaN loss, CUDA OOM, shape mismatch, gradient explosion/vanishing, training crash), verifying paper-code formula consistency, refactoring research code without breaking results, cleaning up code for open-source or reviewer submission, or fixing reproducibility issues. 当需要调试机器学习训练代码、排查NaN/显存溢出/形状不匹配/梯度异常、核实论文公式与代码一致性、在不动功能前提下重构、或为开源/审稿整理代码时使用。触发词：debug NaN OOM CUDA error shape mismatch gradient training crash reproducibility 代码报错 训练崩溃 论文代码一致 重构 开源准备
---

# 代码调试与完善

## 概述

ML 研究代码的系统化调试与整理。核心原则：**代码为根本依据——代码产生实验数字，矛盾时改论文不改代码；修改最小化——只修根因，不加"顺便"改动。**

## 何时使用

- 训练中途崩溃（NaN/Inf/OOM）或结果与论文预期差异显著
- 论文公式与代码实现数值对不上，需逐行定位分歧
- 代码能跑但结构混乱、命名以审稿编号为基准、存在重复实现
- 准备开源或提交审稿，需在不改变任何输出前提下清理代码
- 需在不影响已有功能的前提下增加测试或重构

## 何时不用

- 从零写新功能或新实验 → 标准开发流程
- 撰写或修改论文正文 → `paper-revision`
- 通用代码 bug 审查 → `superpowers:requesting-code-review`

## 快速参考

| 症状 | 首选排查 | 详见 |
|------|----------|------|
| Loss=NaN | `torch.autograd.set_detect_anomaly(True)`; 检查 log(0)、除零、lr 过大 | debug-checklist §1 |
| CUDA OOM | 先跑 `scripts/check_env.py` 确认 CUDA/驱动/PyTorch 版本一致；`torch.cuda.memory_summary()`；检查梯度累积隐式扩 batch | debug-checklist §2 |
| 形状不匹配 | 在出错行前 `print(tensor.shape, tensor.dtype, tensor.device)` | debug-checklist §3 |
| 结果与预期不符 | `torch.manual_seed(42)` + `cudnn.deterministic=True` 锁随机性后逐模块 diff；也检查环境差异（`scripts/check_env.py`） | debug-checklist §4 |
| Checkpoint 可疑 | `scripts/verify_checkpoints.py checkpoints/` 区分真实文件 vs 空/残桩/过小 | — |
| **数据完整性可疑** | **`scripts/check_data_integrity.py results/` 检测冻结值、时间戳碰撞、不可能零值** | **debug-checklist §数据完整性** |
| 梯度异常 | 遍历 `named_parameters()` 检查 `grad is None` 或 `grad.abs().mean()≈0` | debug-checklist §5 |
| 论文-代码公式不一致 | 代入具体数值手算 vs 运行代码结果；始终改论文 | paper-code-mismatches.md |
| 重构风险 | 重构前 `pytest tests/` 全绿 → 改动 → 立即回归 | code-cleanup-checklist.md |

## 核心流程

### 定位论文-代码公式分歧

对每个论文关键公式，在代码中找到对应函数。检查清单：
- 数学运算：矩阵乘法方向（`@` 的左右）、求和 vs 求均值、是否有论文未声明的除法
- 张量形状：输入/输出维度与论文符号是否对应
- 归一化：损失函数是否除以了论文公式中没有的项
- 符号约定：单边投影 vs 双边投影、无偏 vs 有偏

**当代码产生实验数字时 → 改论文，不改代码逻辑。当代码确实有 bug → 最小化修复，加 test 锁死。**

### 代码整理（开源准备）

- 命名：描述功能（`test_compression_methods.py`），不描述论文位置或审稿人编号
- 删除：死代码分支、重复实现（保留规范版其余改 import）、硬编码绝对路径和凭据、构建产物
- 补充：`.gitignore`、README 含项目树和最小运行示例、所有硬编码配置改为 argparse

## 常见 ML 代码 Bug 模式

| 模式 | 表现 | 检查 |
|------|------|------|
| `zero_grad` 位置错误 | 梯度累积意外 | `optimizer.zero_grad()` 是否在 `loss.backward()` 之前 |
| `model.eval()` 忘切 | 推理时 BN 仍用 batch 统计 | 推理/评测前是否调用 `model.eval()` |
| 数据归一化统计量错 | 收敛慢或不收敛 | ImageNet 统计量是否误用于自定义数据集 |
| ToTensor→Normalize 顺序反 | 数值范围异常 | 先 ToTensor(0-1) 再 Normalize |
| 训练/验证预处理不一致 | 验证集 loss 偏高 | 验证集不应做训练增强 |
| `loss.backward()` 重复调用 | 梯度叠加非预期 | 是否循环中多次 `.backward()` |
| AMP 下梯度下溢 | loss scale 持续下降 | 检查 `GradScaler` 的 scale 变化趋势 |

## 配套文件

- `references/debug-checklist.md` — 训练崩溃、结果异常的系统排查清单
- `references/paper-code-mismatches.md` — 论文-代码公式不一致通用模式编目
- `references/code-cleanup-checklist.md` — 代码开源前整理检查清单
