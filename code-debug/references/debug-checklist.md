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

## 平台兼容性

```bash
# Windows GBK 控制台下 Unicode 字符（✓ ✗ 等）会导致 print 崩溃
# Fix: 改用 ASCII 标记 [OK] [FAIL] 或只输出英文
# 检查文件路径分隔符（Windows \ vs Linux /）
# 检查 multiprocessing 的 spawn/ fork 模式差异
```
