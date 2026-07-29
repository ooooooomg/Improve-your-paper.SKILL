# 学术论文 LaTeX 表格格式化参考

## 通用学术表格模板

```latex
\begin{table}[t!]
\centering
\caption{表格标题。}
\label{tab:xxx}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{l c c c}
\toprule
\multirow{2}{*}{Method} & \multicolumn{2}{c}{Dataset A} & Dataset B \\
\cmidrule(lr){2-3}\cmidrule(lr){4-4}
& Metric 1 & Metric 2 & Metric 3 \\
\midrule
Method A & \textbf{92.3} & 85.1 & \underline{78.4} \\
Method B & 90.1 & \textbf{86.2} & \textbf{80.1} \\
Method C & \underline{91.5} & \underline{85.0} & 76.3 \\
\bottomrule
\end{tabular}
\end{table}
```

## 格式化规范

- **最优结果：** `\textbf{42.4}`（粗体）
- **次优结果：** `\underline{41.8}`（下划线）
- **新增最优行时：** 旧 `\textbf{}` 降级为 `\underline{}`，移除旧的 `\underline{}`
- **脚注：** `\multicolumn{列数}{c}{$^{\dagger}$脚注内容。}`
- **列对齐：** 用 `@{}` 去除列两侧多余间距，用 `c`/`l`/`r` 控制对齐
- **行距：** `\renewcommand{\arraystretch}{1.2}` 到 `1.5` 视表格密度而定
- **横线：** `\toprule`/`\midrule`/`\bottomrule`（booktabs风格），`\cmidrule(lr){列范围}` 用于分组

## 常见表格模式

### 多数据集多指标

```latex
\begin{tabular}{l|c c c|c c c}
\toprule
\multirow{2}{*}{Method} & \multicolumn{3}{c|}{Dataset A} & \multicolumn{3}{c}{Dataset B} \\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}
& M1 & M2 & M3 & M1 & M2 & M3 \\
\midrule
...
```

### 多种配置对比

列分组按配置类型（如不同输入分辨率、不同训练数据比例等）。

### 消融实验

通常单列方法名 + 多列指标。方法排序：本方法 → 竞争性数值方法（按预期性能降序）。

## 新增行检查清单

1. 新增行使用与现有行相同的列数
2. `\cmidrule`/`\midrule` 模式保持一致
3. 粗体/下划线层级正确（仅一个最优值）
4. 数值格式统一（如分类精度 1位小数、交并比 2位小数）
5. 脚注标记与表格正文/标题对应
6. `\multirow` 单元格的行数正确
