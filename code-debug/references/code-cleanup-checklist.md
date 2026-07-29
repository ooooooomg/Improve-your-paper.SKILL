# 代码开源前整理检查清单

## 删除清单

### 构建产物
```bash
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.synctex.gz" | xargs rm -f
find . -name ".pytest_cache" -type d -exec rm -rf {} +
```

### 个人脚本与凭据
```bash
# 搜索硬编码路径
grep -rn "/home/\|/Users/\|C:\\\\Users\\\\" . --include="*.py" --include="*.sh"
# 搜索硬编码凭据
grep -rn "password\|api_key\|token\|secret\|wechat\|wx" . --include="*.py" --include="*.sh"
# 搜索个人监控/通知脚本
ls *monitor* *notify* *auto_finish* 2>/dev/null
```

### 死代码与重复实现
```bash
# 找不可达分支（if False / if total < target 但条件永假）
grep -rn "if False\|# TODO: remove\|# DEPRECATED" .
# 找重复函数定义
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

### README 必备内容
- [ ] 项目简介（1-2 句）
- [ ] 安装依赖：`pip install -r requirements.txt`
- [ ] 权重下载链接或脚本
- [ ] 数据准备说明
- [ ] 训练命令（最小可运行示例）
- [ ] 评测命令（对应论文每张表）
- [ ] 项目结构树（`tree -L 2` 输出）
- [ ] 第三方代码来源声明（vendor 目录下各仓库的出处和许可）

### 命名规范
- [ ] 文件名描述功能（`test_compression.py`），不包含论文版本号或审稿人编号
- [ ] 注释描述代码做了什么（`"Compare seven methods"`），不以外部分类编号为基准
- [ ] 文档不引用审稿人编号或论文版本号
- [ ] 脚本不含硬编码绝对路径（改用 argparse + 相对路径）

### 可运行性验证
```bash
# 每个 eval 脚本可导入
for f in eval/eval_*.py; do python -c "import $(basename $f .py)" || echo "FAIL: $f"; done
# 每个 shell 脚本语法正确
for f in *.sh; do bash -n "$f" || echo "FAIL: $f"; done
# 测试全部通过
pytest tests/ -v
```
