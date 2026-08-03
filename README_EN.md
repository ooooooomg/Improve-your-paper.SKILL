# Academic Skills for Claude Code

Three Claude Code skills distilled from a full revise-and-resubmit cycle (3 reviewers, 16 comments), covering paper revision, ML code debugging, and remote GPU training deployment/monitoring. Field-agnostic — no journal, dataset, or method lock-in.


## Installation

```bash
git clone https://github.com/your-username/academic-skills.git
cp -r academic-skills/paper-revision ~/.claude/skills/
cp -r academic-skills/code-debug ~/.claude/skills/
cp -r academic-skills/autodl-training ~/.claude/skills/
```

Script dependencies (install as needed):
```bash
# autodl-training needs paramiko (SSH/SFTP)
pip install -r ~/.claude/skills/autodl-training/requirements.txt

# paper-revision needs lxml (docx font repair)
pip install -r ~/.claude/skills/paper-revision/requirements.txt
```

Skills load automatically when trigger conditions match. Can also be invoked explicitly: `/paper-revision`, `/code-debug` or `/autodl-training`.

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

## autodl-training — Cloud GPU Training Deployment & Monitoring

For deploying and monitoring remote deep-learning training on AutoDL or any SSH-reachable GPU server: code/data upload, environment setup, background training launch, hourly progress monitoring, and WeChat push notifications.

**Problems covered:**

| Problem | Solution |
|------|------|
| Not enough local VRAM; need cloud GPU training | Full deployment flow: SSH check → env setup → code upload → weights/data upload → nohup training launch |
| Large data (10GB+) upload is slow and interrupt-prone | `scripts/upload_data.py` sharded upload with resume; already-verified shards are skipped |
| Packing fails on Windows | Use python `tarfile`, not subprocess `tar` (Windows tar path pitfall) |
| Training runs for dozens of hours; want automated monitoring | `scripts/monitor_server.py` runs server-side, checks hourly and pushes |
| Want to know immediately if training goes wrong | Auto-detects OOM / NaN / Traceback / gradient explosion, pushes ⚠️ alert to WeChat |
| Want progress pushed to phone | `scripts/wxpush.py` wraps the wxpusher API, one-command push |
| Losing training progress when local machine powers off | Training and monitoring both run server-side via nohup, independent of the local machine |
| Want "configure once, run the whole pipeline automatically" | `scripts/orchestrator.py` one-shot: wait for uploads → auto-start training → auto-start monitor |

**Knowledge not present in Claude's pretraining corpus:**

- AutoDL server `python` is not on PATH; must use full path `/root/miniconda3/bin/python`
- AutoDL console disk-usage display lags; trust server `df -h` instead
- Server images ship older torch (e.g. 1.10); adapt training code to the server, don't upgrade the server
- AutoDL is pay-as-you-go, billed from boot (including transfer/idle time); balance is only viewable in the web console

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
└── autodl-training/
    ├── SKILL.md
    ├── requirements.txt               # paramiko
    ├── scripts/
    │   ├── ssh_helper.py              # SSH/SFTP connect, command exec, file transfer
    │   ├── upload_data.py             # Sharded data upload with resume
    │   ├── wxpush.py                  # wxpusher WeChat push
    │   ├── monitor_server.py          # Server-side hourly training monitor (Chinese push)
    │   ├── orchestrator.py            # Full pipeline: wait uploads → start training → start monitor
    │   └── start_train.sh             # Remote training launch template (nohup background)
    └── references/
        └── autodl-server-guide.md     # AutoDL server quick reference (env/disk/billing/pitfalls)
```

## License

MIT

## Limitations

- **Skills are scaffolding, not turnkey products**: the scripts are workflow templates that must be configured for your specific project (paths, credentials, hyperparameters, artifact naming). They are not guaranteed to run out of the box.
- **Domain examples**: the evaluation section of `autodl-training` uses image segmentation/detection as an example; other domains need their own evaluation protocol.
- **Maintenance**: as Claude Code evolves, the APIs used by the scripts may change. Verify with `-m py_compile` or a smoke test before relying on them.

## Contact

This project is under active improvement. For suggestions, bug reports, or collaboration, contact the author:

**AshMe** — <AshMe37@outlook.com>

