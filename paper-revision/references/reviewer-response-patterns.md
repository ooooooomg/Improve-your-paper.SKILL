# 审稿意见应对模式

学术论文修订中常见审稿意见类型的通用回复结构。每种模式包含：回复结构、学术英语措辞示例、中文措辞示例。

## 模式 1：缺少理论分析

**回复结构：**
1. 新增了什么：小节名称和位置
2. 涵盖内容：理论框架 + 可检验预测
3. 诚实的范围声明："提供结构动机而非形式化最优性证明"
4. 交叉引用实验验证（消融表）

**英文学术措辞：**
> We added §X.Y "[Section Title]." It derives two testable predictions from [theoretical framework], then evaluates them in Table Z. The analysis provides structural motivation rather than a formal optimality proof, which the ablation table supplies empirically.

**中文学术措辞：**
> 我们在第X.Y节新增了"[小节标题]"。该节从[理论框架]导出了两个可检验的预测，并在表Z中进行了实验评估。分析提供的是结构动机而非形式化最优性证明——后者由消融实验提供实证支持。

## 模式 2：增加与某方法的对比

**回复结构：**
1. 调研结果：发现了该方法的什么信息
2. 加入位置：哪张表/哪一节
3. 关键数字（1-2个）
4. 实验协议差异（如有）及处理方式
5. 可复现性风险提示（如该方法无官方权重/仓库）

**英文学术措辞：**
> We added [Method Name] to the [task] comparison (Table X). Its key metric of [value] lies [above/below/between] the baselines. Protocol note: [Method] uses [different detector/backbone]; this is documented via table footnote. We note that [Method] has no official open-source release; our reproduction follows the published description and the achievable performance may differ from the authors' reported numbers.

**中文学术措辞：**
> 我们将[方法名]加入了[任务]的对比实验（表X）。其关键指标为[数值]，处[于基线之间/高于基线/低于基线]。协议说明：[方法]使用了[不同检测器/骨干]，已通过表格脚注记录。我们注意到[方法]无官方开源版本；我们的复现基于已发表的描述，达到的性能可能与原论文报告值略有差异。

## 模式 3：增加设计选择的消融实验

**回复结构：**
1. 新增了什么消融：表号、节号
2. 包含了哪些方法以及原因
3. 排除了哪些方法以及原因（给出学术理由）
4. 关键发现（1-2句）

**英文学术措辞：**
> We added Table X comparing K compression operators at matched dimension: [list methods in performance order]. [Excluded method] is excluded because it [introduces learnable parameters / relies on external supervision / violates the controlled-comparison premise], placing it in a different category outside the scope of this parameter-free comparison.

**中文学术措辞：**
> 我们在表X中增加了在相同压缩维度下K种压缩算子的对比：[按性能降序列出方法]。[被排除的方法]未被纳入，因为它[引入了可学习参数/依赖外部监督/破坏了受控对比的前提]，属于不同类别，不在本无参数对比的范围内。

## 模式 4：扩展到更大数据集

**回复结构：**
1. 做了什么：数据扩展的具体规模
2. 结果：增益幅度 + 递减证据
3. 为什么不做更大规模：算力限制 + 同行研究的数据使用惯例

**英文学术措辞：**
> We trained on N× more data and evaluated across all tasks. Gains are 0.X-Y points over the previous setting, with marginal diminishing returns evident from the progression. Comparable methods in the literature all train on the same base dataset size. The diminishing-returns pattern suggests further scaling would yield marginal improvements.

**中文学术措辞：**
> 我们在N倍更大数据规模上进行了训练并在全部任务上评估。相比之前设置，增益为X-Y个百分点，从递进趋势中可观察到边际递减。文献中的可比方法均使用相同的基础数据规模。递减规律表明进一步扩展带来的额外收益将十分有限。

## 模式 5：缺少实现细节

**回复结构：**
1. 新增了什么：完整的超参数清单
2. 关键数值：优化器、学习率、权重衰减、批次大小、输入尺寸、初始化方式、训练轮数、混合精度、GPU型号

**英文学术措辞：**
> We expanded the Implementation Details subsection to include: [optimizer], fixed lr=[value], weight decay=[value], batch size=[value], input resolution, weight initialization from [pretrained checkpoint], training epochs, AMP optional, single [GPU model] GPU.

**中文学术措辞：**
> 我们在实现细节小节中补充了完整的超参数清单：[优化器]、固定学习率、权重衰减、批次大小、输入分辨率、预训练权重初始化、训练轮数、可选的混合精度训练、单卡[GPU型号]。

## 模式 6：弱化过度宣称的表述

**回复结构：**
1. 改了什么：具体被替换的措辞（摘引原文）
2. 改在哪里：摘要、引言、理论节等位置
3. 新增了什么限定语

**英文学术措辞：**
> We replaced "[overclaimed phrase]" with "[qualified phrase]" in the abstract and introduction. In the theory section, we added an explicit caveat stating that the analysis should be understood as heuristic structural justification rather than a formal optimality proof. All absolute superiority claims have been removed or qualified.

**中文学术措辞：**
> 我们将摘要和引言中的"[原过度措辞]"替换为"[限定措辞]"。在理论分析节中增加了明确的免责声明，指出分析应理解为启发式结构论证而非形式化最优性证明。所有绝对性优势声明已被移除或加限定。

## 模式 7：某个指标差距 / 局限性讨论

**回复结构：**
1. 直接陈述数据（我方数值、对比方数值、差距大小）——不用"承认"
2. 结构性原因（我方方法的机制 vs 对方方法的机制）
3. 论文中何处讨论（实验节 + 结论）
4. 未来缓解策略（1-2个具体方案）

**英文学术措辞：**
> In [task], our method achieves [value] vs [competitor]=[value] (gap of [magnitude]). [Competitor] uses [specialized mechanism] that provides finer [property]; our method uses [simpler/general mechanism] that captures [global/holistic property] but may not preserve [fine-grained property] to the same degree. We added a paragraph in the experiment section discussing this structural trade-off with a cross-reference to the Conclusion, where we propose [1-2 specific mitigation strategies] as future work.

**中文学术措辞：**
> 在[任务]中，我们的方法[指标]=[数值]，[对比方法]=[数值]，差距[幅度]。[对比方法]采用了[专用机制]来保留[细粒度属性]；我们的方法使用[通用机制]通过[全局方法]迁移知识——这一过程高效捕捉[全局属性]，但操作的抽象层级可能对[细粒度属性]有所衰减。我们在实验节末尾增加了讨论段落并交叉引用结论部分，在结论中提出[1-2个具体缓解策略]作为未来工作方向。

## 措辞指南

**避免以下AI痕迹标志（英文）：**
- "We fully recognize..." → 删除，直接陈述操作
- "We sincerely appreciate the reviewer's insightful comment..." → 删除，直接回应
- "comprehensive investigation" → "we examined" / "we compared"
- "immediately conducted" → "we conducted" / "we performed"
- "theoretically demonstrate the inherent superiority" → "provide structural motivation"
- "It is worth noting that..." → 删除，直接陈述

**避免以下AI痕迹标志（中文）：**
- "我们完全理解审稿人的关切" → 删除
- "我们衷心感谢这一建设性意见" → 删除
- "进行了全面深入的调研" → "调研了" / "比较了"
- "立刻开展了相关工作" → "开展了" / "完成了"
- "明确承认" / "我们承认" → 直接陈述实验数据
- "从理论上证明了本方法的固有优越性" → "提供了结构动机"
- "值得一提的是" → 删除

**正确的回复结构（每条意见）：**
1. (可选) 一句话点出关注的合理性——不做姿态性的"感谢"或"同意"
2. 做了什么：具体章节、表格、段落
3. 关键结果或发现：1-2句
4. 论文中位置：交叉引用
