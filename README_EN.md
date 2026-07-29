# Academic Skills for Claude Code

此技能从真实结合ai完成论文大修的实际经验中得出，希望能帮到从0开始科研的你。·如果在使用中有任何问题或改进建议，欢迎联系作者AshMe37@outlook.com

## Installation

```bash
git clone https://github.com/your-username/academic-skills.git
cp -r academic-skills/paper-revision ~/.claude/skills/
cp -r academic-skills/code-debug ~/.claude/skills/
```

Skills load automatically when trigger conditions match. Can also be invoked explicitly: `/paper-revision` or `/code-debug`.

## paper-revision — Paper Revision

For responding to reviewer comments, editing LaTeX manuscripts, generating highlighted diff PDFs, fixing .docx response letter formatting, verifying cross-references, synchronizing bilingual papers, and preparing camera-ready or final resubmission packages.

**Problems covered:**

| Problem | Solution |
|------|------|
| Math formulas in .docx render as garbled text | Root causes of three OMML silent-corruption modes + step-by-step repair; `scripts/fix_docx_fonts.py` auto-fixes font size inconsistency |
| latexdiff crashes with `TeX capacity exceeded` | Root cause of soul/ulem infinite recursion with `\cite{}`; `\textcolor` workaround |
| Response letter cites a section/table that doesn't exist | RIRO principle: every `\ref{}` and section name must be grep-verified; `scripts/verify_cross_refs.py` for full scan before submission |
| Need a structure for responding to reviewer comments | 12 reviewer comment patterns with bilingual (EN/ZH) response templates |
| Response letter reads like AI-generated text | AI-pattern phrase replacement list |
| English and Chinese paper versions out of sync | Five-step bilingual sync workflow; `scripts/semantic_diff.py` for section-level diff |
| .docx font size or face inconsistency | `scripts/validate_docx_fonts.py` detects; `scripts/fix_docx_fonts.py` automatically repairs |
| Paper version confusion and lost modifications | Version naming convention, commit discipline, lost-modification recovery procedures |
| Infinite loops caused by repeated commands | Same command max 3 retries; read .log to diagnose before recompiling |

**Knowledge not present in Claude's pretraining corpus:**

- python-docx's `paragraph.text =` assignment silently deletes all OMML math objects
- Word stores font size in half-points; 11pt = `w:sz="22"`
- soul's `\hl{}` enters infinite `\SOUL@eval` recursion when encountering `\cite{}`

## code-debug — Code Debugging

For debugging ML training crashes (NaN, OOM, shape mismatch, gradient issues), verifying paper-code formula consistency, refactoring research code without changing outputs, and cleaning up code for open-source release.

**Problems covered:**

| Problem | Solution |
|------|------|
| Training crashes mid-epoch with NaN | Five-step diagnosis: lr → log/div-by-zero → gradient clipping → AMP → data pipeline |
| Paper formula doesn't match code numerically | Seven general paper-code mismatch patterns with detection workflow |
| Source files and comments named after reviewer IDs | Code-first naming principles and open-source cleanup checklist |
| Subtle, recurring ML code bugs | Seven ML bug pattern quick reference |
| Results not reproducible despite fixed seed | Full determinism lock: manual_seed + cudnn.deterministic + benchmark + hashseed |
| CUDA OOM or driver version mismatch | `scripts/check_env.py` outputs complete environment info |
| Checkpoint loads all zeros or random weights | `scripts/verify_checkpoints.py` distinguishes real checkpoints from stubs/empty files |
| Identical numeric values across experiment result files | `scripts/check_data_integrity.py` detects frozen values, timestamp collisions, and impossible zeros |
| Results diverge from expectation but code logic seems correct | `scripts/check_env.py` identifies environment-level causes |

**Knowledge not present in Claude's pretraining corpus:**

- Data preprocessing order is irreversible (ToTensor must precede Normalize)
- Forgetting `model.eval()` leaves BN using per-batch statistics instead of running estimates
- Validation set must not receive training augmentations
- Reusing ImageNet normalization statistics on custom datasets causes slow convergence

## Design Principles

1. **Information-delta only.** Nothing already known to Claude is included. Every line is a domain trap or experience pattern absent from general training data.
2. **Code is ground truth.** Code produces experimental numbers; the paper describes them. When they conflict, fix the paper.
3. **Description = triggers, not workflow.** Each `SKILL.md` description field states only when to use the skill, never what steps it contains.
4. **Bilingual trigger coverage.** Description fields include both English and Chinese keywords.

## File Structure

```
├── README.md
├── README_EN.md
├── paper-revision/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── verify_cross_refs.py        # Scan LaTeX for undefined refs, duplicate labels, unmatched cites
│   │   ├── semantic_diff.py            # Compare two .tex files section by section
│   │   ├── validate_docx_fonts.py      # Check .docx for font size/face inconsistency
│   │   └── fix_docx_fonts.py           # Auto-fix .docx font size inconsistency
│   └── references/
│       ├── reviewer-response-patterns.md
│       └── latex-table-patterns.md
└── code-debug/
    ├── SKILL.md
    ├── scripts/
    │   ├── check_env.py                # Print PyTorch/CUDA/cv2 environment for diagnostics
    │   ├── verify_checkpoints.py       # Distinguish real .pt files from stubs and empty files
    │   └── check_data_integrity.py     # Detect frozen values, timestamp collisions, impossible zeros
    └── references/
        ├── debug-checklist.md
        ├── paper-code-mismatches.md
        └── code-cleanup-checklist.md
```

## License

MIT
