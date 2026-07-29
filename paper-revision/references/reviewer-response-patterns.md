# 审稿意见应对模式

学术论文修订中常见审稿意见类型的通用回复结构。

## 前置步骤：回复-论文一致性验证

**在写任何回复之前，必须先确认论文中是否真的有对应的修改。** 否则会出现回复声称已添加某对比/实验，但论文表格中数据为占位符或整行缺失的情况——审稿人复核时直接拒稿。

检查方法：
- 对回复中声称的每个修改，在论文 `.tex` 文件中 grep 对应的小节标题、表格行、新增引用
- 若声称"在表X中增加了某方法的对比"，必须确认表格中存在该行且有真实数值（非 `xx.x`、`—`、占位符）
- 若声称"补充了某小节的理论分析"，必须确认该 `\subsection` 确实存在且内容完整
- 若论文中找不到对应修改 → 补论文，或调整回复措辞，绝不声称做了实际上没有的修改

此步骤应在处理每条审稿意见前执行。

## 模式 1：缺少理论分析

1. 新增了什么：小节名称和位置
2. 涵盖内容：理论框架 + 可检验预测
3. 诚实的范围声明
4. 交叉引用实验验证

> We added §X.Y "[Section Title]." It derives testable predictions from [framework], then evaluates them in Table Z. The analysis provides structural motivation rather than a formal optimality proof.

> 我们在第X.Y节新增了"[小节标题]"。该节从[框架]导出了可检验的预测，并在表Z中实验评估。

## 模式 2：增加与某方法的对比

1. 调研结果
2. 加入位置（表号/节号）
3. 关键数字
4. 实验协议差异（如有）及处理方式
5. 可复现性风险提示（如无官方权重）

> We added [Method] to the [task] comparison (Table X). Key metric: [value]. Protocol note: [Method] uses [different component]; documented via table footnote.

## 模式 3：增加设计选择的消融实验

1. 新增表号/节号
2. 包含的方法及原因
3. 排除的方法及学术理由
4. 关键发现

> We added Table X comparing K variants at matched configuration: [list]. [Excluded variant] is excluded because it [introduces external factors not present in other variants].

## 模式 4：扩展到更大数据集

1. 做了什么规模
2. 增益幅度 + 递减证据
3. 不做更大规模的理由

> We trained on N× more data. Gains are X-Y points, with diminishing returns evident from the progression. Comparable methods all use the same base data scale.

## 模式 5：缺少实现细节

补充完整的超参数清单：优化器、学习率、权重衰减、批次大小、输入尺寸、初始化方式、训练轮数、混合精度设置、硬件型号。

## 模式 6：弱化过度宣称的表述

1. 具体被替换的措辞（摘引原文）
2. 位置（摘要/引言/理论节）
3. 新增的限定语

> We replaced "[overclaimed phrase]" with "[qualified phrase]". In the theory section, we added an explicit caveat that the analysis should be understood as heuristic structural motivation.

## 模式 7：某个指标差距 / 局限性讨论

1. 直接陈述数据——不用"承认""同意"等姿态词
2. 结构性原因（我方机制 vs 对方机制）
3. 论文中何处讨论（实验节 + 结论）
4. 具体缓解策略

> In [task], our method [metric]=[value] vs [competitor]=[value] (gap [magnitude]). [Competitor] uses [specialized component] for [property]; our [simpler design] captures [global property] but may not preserve [fine-grained property] to the same degree. We discuss this trade-off in §X and propose [1-2 strategies] as future work.

## 模式 8：缺少与相关工作的对比讨论

1. 在 Related Work 中新增了哪些对比
2. 与每项工作的关系（补充/正交/超越/不同假设）
3. 在何处明确论述了差异

> We expanded the related work discussion of [topic] in §II. Specifically: [Work A] addresses [different setting]; [Work B] is complementary (our method can be combined); [Work C] shares [component] but differs in [key aspect].

## 模式 9：创新性/贡献辩护

1. 逐一重述每条贡献
2. 对应每条的支撑证据（理论节/消融表/对比表）
3. 与最相关工作的区分

> Our contributions are: (1) [contribution 1], supported by [evidence]; (2) [contribution 2], supported by [evidence]. The key distinction from [closest work] is [difference in assumption/method/scope].

## 模式 10：实验公平性辩护

1. 明确指出质疑的对比条件
2. 说明控制变量的具体措施
3. 承认不可控因素（如对方用不同预训练权重）及对结论的影响评估

> All methods in Table X are evaluated under identical conditions: same input resolution, same evaluation protocol, same hardware. The [factor reviewer questioned] is held constant: [specific control measure]. One unavoidable difference: [factor]. We assess its impact as [minor/moderate] because [reasoning].

## 模式 11：写作质量问题

1. 逐段说明重写位置和改动
2. 具体改动内容（拆分长句、重组段落、补过渡句）
3. 可请审稿人直接看新版对应章节

> We substantially revised the writing throughout. Key changes: §II restructured into thematic subsections; §III-B simplified the notation and added intermediate steps; long sentences in §IV split for readability. The revised manuscript has been proofread by a native English speaker / professional editing service.

## 模式 12：补充统计显著性检验

1. 做了什么检验（多次运行/error bars/统计检验）
2. 结果：主要结论的显著性水平
3. 为什么选择该检验方法

> We conducted [N] independent runs with different random seeds and report mean ± std in [Table X]. The key comparisons (ours vs [baseline]) are statistically significant at p < 0.01 (paired t-test / Wilcoxon). We chose [test] because [assumption: normality / non-parametric].

## 措辞指南

**避免（AI 痕迹标志）：**
- "We fully recognize..." / "We sincerely appreciate..." → 删除
- "comprehensive investigation" → "we examined"
- "明确承认" / "我们承认" → 直接陈述数据
- "insightful comment" → 删除

**正确回复结构：** (1) 可选：一句客观陈述 (2) 具体改动 (3) 关键结果 (4) 论文位置
