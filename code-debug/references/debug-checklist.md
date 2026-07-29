# 调试排查清单

训练崩溃、结果异常、数值不一致的系统排查步骤。

## 训练崩溃排查

### NaN / Inf 值
```bash
# 定位 NaN 首次出现的位置
torch.autograd.set_detect_anomaly(True)
# 或在可疑位置插入
assert not torch.isnan(tensor).any(), f"NaN at {name}"
```

检查顺序：
1. 学习率是否过大（尝试 ÷10）
2. 损失函数中是否有 log(0) 或除零
3. 梯度裁剪是否生效
4. 混合精度训练中是否有梯度下溢（检查 loss scale）
5. 输入数据是否包含 NaN（数据加载阶段检查）

### CUDA Out of Memory
1. 减小 batch size
2. 检查是否有张量未释放（`del tensor; torch.cuda.empty_cache()`）
3. 检查是否有梯度累积逻辑导致的隐式扩大
4. 使用 `torch.cuda.memory_summary()` 查看显存分配

### 形状不匹配
```python
# 在出错行前插入
print(f"tensor1: {tensor1.shape}, tensor2: {tensor2.shape}")
# 常见原因：缺少/多余的维度、通道顺序错误、broadcast 不符合预期
```

## 结果与预期不符排查

### 锁定随机性
```python
import torch
import numpy as np
import random
SEED = 42
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
np.random.seed(SEED)
random.seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
```

### 逐模块对比
1. 保存参考实现和新实现的中间层输出
2. 逐层计算差异（相对误差/绝对误差）
3. 定位差异首次放大的位置 → 该层即为问题所在

### 梯度检查
```python
# 确认梯度是否正常传播
for name, param in model.named_parameters():
    if param.grad is None:
        print(f"WARNING: {name} has no gradient")
    elif param.grad.abs().mean() < 1e-8:
        print(f"WARNING: {name} gradient near zero, mean={param.grad.abs().mean()}")
```

## 数值精度问题

### 检查混合精度
```python
# 确认哪些操作在 fp32 下执行
torch.cuda.amp.autocast(enabled=True)
# 查看 loss scale 是否在下降（暗示梯度下溢）
```

### 检查数值范围
```python
# 统计张量的数值分布
print(f"min={tensor.min():.6f}, max={tensor.max():.6f}, std={tensor.std():.6f}")
# 异常信号：极小的 std → 可能梯度消失；极大的 max → 可能梯度爆炸
```

## 训练产物数据完整性检查

以下检查针对已完成的训练输出（非运行时崩溃），用于发现伪造或损坏的训练数据。

### 跨文件/跨实验数值等价检测
```python
import json, glob
from collections import defaultdict
values_by_key = defaultdict(list)
for f in glob.glob("results/**/*.json", recursive=True):
    data = json.load(open(f))
    for k, v in data.items():
        if isinstance(v, (int, float)):
            values_by_key[k].append((f, v))
# 警报：3+ 个独立方法间同一指标值完全相同
for k, entries in values_by_key.items():
    vals = [v for _, v in entries]
    if len(vals) >= 3 and len(set(vals)) == 1:
        print(f"FROZEN: {k}={vals[0]} across {len(vals)} files")
```

### 数值量级合理性检查
- 损失值是否在合理范围内？(MSE: 0.001-0.1，非百万量级)
- 指标值是否在 [0, 1] 内？（交并比/精度类指标不应超出此范围）
- 标准差是否有负值？（std 必 >= 0）
- epoch 时间是否与 GPU 型号匹配？（ 单个 epoch 通常数百到数万秒，非零秒）

### 领域排序约束检查
- 难度排序：简单数据集 > 困难数据集
- 提示信息量排序：多点提示 > 单点提示 > 无提示
- 数据规模排序：5% 数据 >= 2% 数据 >= 1% 数据
- 违反这些排序可能表明数据未真实运行

### 时间序列单调性
- `time_elapsed_s` 是否严格递增？（epoch 边界不应重置）
- 每个 epoch 的 `end_time_utc` 是否 > `start_time_utc`？

### 内部数据源交叉验证
对每个 checkpoint 目录，以下文件必须内部一致：
- `train.log` 的 epoch 均值 ≈ `epoch_summary.json` ≈ `train_summary.json`
- `steps.jsonl` 的每步 loss 平均值应接近 `epoch_summary.json` 的 epoch loss
- 多个文件声称同一指标时，差异应在 <1% 以内
- **矛盾是最高信号**——一个数据源正确不代表另一个也正确

### 时间戳与时间线合理性
```bash
grep -rh "timestamp_utc" results/ --include="*.json" | sort | uniq -c | sort -rn
# 任何 count > 1 = 多个文件声称在同一时刻完成（不可能）
```
- 每个评测需要数分钟到数小时，完成时刻应各不相同
- 时间戳精度应匹配硬件（CUDA 计时通常 1-2 位小数，15-17 位小数表明是合成数据）
- 总训练时间应 = 各 epoch 时间之和（误差 < 1%）

```bash
# Windows GBK 控制台下 Unicode 字符（✓ ✗ 等）会导致 print 崩溃
# Fix: 改用 ASCII 标记 [OK] [FAIL] 或只输出英文
# 检查文件路径分隔符（Windows \ vs Linux /）
# 检查 multiprocessing 的 spawn/ fork 模式差异
```
