# 代码开源前整理检查清单

## 删除清单

### 构建产物
```bash
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.synctex.gz" | xargs rm -f
find . -name ".pytest_cache" -type d -exec rm -rf {} +
```

### 审稿人/论文框架标记（de-reviewer-ization）
**先 grep 定位全部命中、再逐文件修改、最后删除前确认。** 搜索关键词：
```bash
grep -rnE "R[0-9]Q[0-9]|paper_v[0-9] Table|Reviewer [0-9]|mandated by paper|per the response letter|paste into paper|Table [0-9] output" *.py *.sh *.md
```
**改写原则：** 描述代码自身做什么，不描述论文在何处引用。

**文件级重命名：** 文件名含审稿编号 → 功能描述名。重命名后 grep 更新所有代码中的旧名引用。

### 个人脚本与凭据
**先 grep 确认无任何代码引用，再删除。**
```bash
grep -rn "auto_finisher\|monitor_training\|notify_results\|repack\|auto_shutdown" . --include="*.py" --include="*.sh"
# 确认零引用后：
rm -f auto_finisher.* monitor_training.py monitor.log notify_results.py notify.log repack.*
```
```bash
# 搜索硬编码路径
grep -rn "/home/\|/Users/\|C:\\\\Users\\\\" . --include="*.py" --include="*.sh"
# 搜索硬编码凭据
grep -rn "password\|api_key\|token\|secret\|wechat\|wx" . --include="*.py" --include="*.sh"
# 搜索个人监控/通知脚本（含子目录）
find . -name "*monitor*" -o -name "*notify*" -o -name "*auto_finish*" -o -name "*auto_shutdown*" | grep -v vendor
```

### 死代码与重复实现
```bash
grep -rn "if False\|# TODO: remove\|# DEPRECATED" .
grep -rn "^def " *.py | awk -F: '{print $NF}' | sort | uniq -c | sort -rn | awk '$1 > 1'
```

## 补充清单

### .gitignore
```
results/
cache/
checkpoints/
eval_results/
outputs/
figs/
__pycache__/
*.pyc
.pytest_cache/
*.log
*.aux
*.out
*.synctex.gz
*.pt
```

**缺口检测：** 列出所有输出目录，逐个确认是否在 .gitignore 中：
```bash
ls -d */ | grep -v vendor | while read d; do grep -q "^$d" .gitignore || echo "MISSING: $d"; done
```

### 第三方/vendored 代码决策
- **保留并标注（vendor）：** README 中注明出处链接、LICENSE、是否修改过。对 vendored 代码中"审稿用语"残留不修改（第三方自带的不动）
- **按需克隆（.gitignore）：** 列入 .gitignore，在 setup 脚本中自动 git clone
- **一致性：** 避免部分 vendor 被 ignore、部分被提交的不一致状态

### README 必备内容
- [ ] 项目简介（1-2 句）
- [ ] 安装依赖：`pip install -r requirements.txt`
- [ ] 权重下载链接或脚本
- [ ] 数据准备说明
- [ ] 训练命令（最小可运行示例）
- [ ] 评测命令（对应论文每张表）
- [ ] 项目结构树（`tree -L 2` 实际输出，不凭记忆手写）
- [ ] 第三方代码来源声明（vendor 目录下各仓库的出处和许可）
- [ ] **只填有把握的数字**：未用代码验证的数据标 `—` 并指向论文/复现文档，不编造

### 命名规范
- [ ] 文件名描述功能（`test_compression.py`），不包含论文版本号或审稿人编号
- [ ] 注释描述代码做了什么（`"Compare seven methods"`），不以外部分类编号为基准
- [ ] 文档（含 runbook/复现文档）不引用审稿人编号或论文版本号；保留所有复现命令和预期值不变
- [ ] 脚本不含硬编码绝对路径（改用 argparse + 相对路径）

### 最终 grep 复查
```bash
# 搜索残留审稿/论文框架标记（排除 vendor 目录）
grep -rnE "R[0-9]Q[0-9]|paper_v[0-9]|Reviewer [0-9]|paper\.tex|Reviwer" . --include="*.py" --include="*.sh" --include="*.md" | grep -v vendor
# 搜索旧文件名残留（重命名后）
# 确认零命中
```
**命中分类：** 自有代码 → 修改；vendor 目录 → 不修改

### 可运行性验证
```bash
# 每个 eval 脚本可导入
for f in eval/eval_*.py; do python -c "import $(basename $f .py)" || echo "FAIL: $f"; done
# 每个 shell 脚本语法正确
for f in *.sh; do bash -n "$f" || echo "FAIL: $f"; done
# 测试全部通过
pytest tests/ -v
```
