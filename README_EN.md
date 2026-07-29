# Academic Skills for Claude Code

Two Claude Code skills distilled from a full revise-and-resubmit cycle (3 reviewers, 16 comments), covering paper revision and ML code debugging. Field-agnostic — no journal, dataset, or method lock-in.

## Installation

```bash
git clone https://github.com/your-username/academic-skills.git
cp -r academic-skills/paper-revision ~/.claude/skills/
cp -r academic-skills/code-debug ~/.claude/skills/
```

Skills load automatically when trigger conditions match. Can also be invoked explicitly: `/paper-revision` or `/code-debug`.

## paper-revision — Paper Revision

Use when responding to reviewer comments, editing LaTeX manuscripts, generating highlighted diff PDFs, fixing .docx response letter formatting, verifying cross-references, synchronizing bilingual (Chinese/English) papers, or preparing camera-ready / final resubmission packages.

**Problems covered:**

| Problem | Solution |
|------|------|
| Math formulas in .docx response letter render as garbled text | Root causes of three OMML silent-corruption modes and step-by-step repair |
| latexdiff crashes with `TeX capacity exceeded` | Root cause of soul/ulem infinite recursion with `\cite{}`; `\textcolor` workaround |
| Response letter cites a section or table that doesn't exist in the paper | RIRO principle (Reference In, Reference Out): every `\ref{}` and section name must be grep-verified against the manuscript; run `scripts/verify_cross_refs.py` for full scan before submission |
| Need a structure for responding to reviewer comments | 12 reviewer comment patterns with bilingual (EN/ZH) response templates |
| Response letter reads like AI-generated text | AI-pattern phrase replacement list |
| English and Chinese paper versions out of sync | Five-step bilingual sync workflow; `scripts/semantic_diff.py` for section-level diff |
| Font size or face inconsistency in .docx | `scripts/validate_docx_fonts.py` automatically checks the entire document |
| Cannot reliably diff two paper versions | `scripts/semantic_diff.py old.tex new.tex` reports semantic changes by section |

**Knowledge not present in Claude's pretraining corpus:**

- python-docx's `paragraph.text =` assignment silently deletes all OMML math objects
- Word stores font size in half-points; 11pt = `w:sz="22"`
- soul's `\hl{}` enters infinite `\SOUL@eval` recursion when it encounters `\cite{}`

## code-debug — Code Debugging

Use when debugging ML training crashes (NaN, OOM, shape mismatch, gradient issues), verifying paper-code formula consistency, refactoring research code without changing outputs, or cleaning up code for open-source release.

**Problems covered:**

| Problem | Solution |
|------|------|
| Training crashes mid-epoch with NaN | Five-step NaN diagnosis: lr → log/div-by-zero → gradient clipping → AMP → data pipeline |
| Paper formula doesn't match code numerically | Seven general paper-code mismatch patterns with detection workflow |
| Source files and comments named after reviewer IDs | Code-first naming principles and open-source cleanup checklist |
| Subtle, recurring ML code bugs | Seven ML bug pattern quick reference (zero_grad placement, BN mode, preprocessing order, etc.) |
| Results not reproducible despite fixed seed | Full determinism lock: manual_seed + cudnn.deterministic + benchmark + hashseed |
| CUDA OOM or driver version mismatch | `scripts/check_env.py` outputs complete environment info (CUDA/driver/PyTorch/GPU) |
| Checkpoint loads all zeros or random weights | `scripts/verify_checkpoints.py` distinguishes real checkpoints from stubs/empty files |
| Results diverge from expectation but code logic seems correct | `scripts/check_env.py` identifies environment-level differences causing numerical deviation |

**Knowledge not present in Claude's pretraining corpus:**

- Data preprocessing order is irreversible (ToTensor must precede Normalize)
- Forgetting `model.eval()` leaves BN using per-batch statistics instead of running estimates
- Validation set must not receive training augmentations, or metrics will be biased
- Reusing ImageNet normalization statistics on custom datasets is a common cause of slow convergence

## Design Principles

1. **Information-delta only.** Nothing already known to Claude (e.g., "run pdflatex three times to resolve cross-references") is included. Every line is a domain trap or experience pattern absent from general training data.
2. **Code is ground truth.** Code produces experimental numbers; the paper describes them. When they conflict, fix the paper — not verified, result-producing code.
3. **description = triggers, not workflow.** Each `SKILL.md` description field states only when to use the skill, never what steps it contains. This forces Claude to read the full body before acting.
4. **Bilingual trigger coverage.** Description fields include both English and Chinese keywords. A Chinese-only description will never match in an English conversation.

## File Structure

```
├── README.md
├── README_EN.md
├── paper-revision/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── verify_cross_refs.py        # Scan LaTeX for undefined refs, duplicate labels, unmatched cites
│   │   ├── semantic_diff.py            # Compare two .tex files section by section, ignoring noise
│   │   └── validate_docx_fonts.py      # Check .docx for font size and face inconsistency
│   └── references/
│       ├── reviewer-response-patterns.md
│       └── latex-table-patterns.md
└── code-debug/
    ├── SKILL.md
    ├── scripts/
    │   ├── check_env.py                # Print PyTorch/CUDA/cv2 environment for diagnostics
    │   └── verify_checkpoints.py       # Distinguish real .pt files from stubs and empty files
    └── references/
        ├── debug-checklist.md
        ├── paper-code-mismatches.md
        └── code-cleanup-checklist.md
```

## License

MIT
