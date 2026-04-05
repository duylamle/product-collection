# Phase 10 — Skill Absorption

You don't need to be an expert in every domain to build great skills. You need a method for finding what already works and making it yours.

---

## The Problem

When you need a skill for a new domain — code review, data analysis, content marketing, test planning — you face a cold start problem. You don't know what best practices exist, what edge cases to handle, or what output structure works best. Building from scratch means reinventing wheels that others have already built.

---

## The Pattern: Skill Absorption

Instead of starting from zero or blindly copying someone else's work, use this 6-step pattern to bootstrap and grow any skill.

### Step 1 — Bootstrap

Tell Claude what you need. Describe the task, who it's for, and what good output looks like.

```
"I need a skill for code review. It should check for security issues,
performance problems, and readability. Output should be a structured
report with severity levels. The reviewer is a senior engineer persona."
```

Claude proposes and creates a basic agent + skill based on your requirements. This gives you a working starting point — not perfect, but functional.

### Step 2 — Research

Search for existing skills in the same domain:

```bash
npx skills find code-review
npx skills find security-review
npx skills find pull-request
```

Browse results on [skills.sh](https://skills.sh). Install promising ones:

```bash
npx skills add <owner/repo@skill-name> -y
```

Install 2-3 that look relevant. You're not committing to any of them — you're gathering reference material.

### Step 3 — Gap Analysis

Compare your bootstrapped skill against each community skill, side by side. Look for:

- **Scripts** they have that you don't (automation, API calls, formatters)
- **Templates** with better structure or more comprehensive sections
- **Checklists** covering edge cases you didn't think of
- **Patterns** for handling tricky situations (error recovery, fallbacks)
- **Constraints** that prevent common mistakes

Read their files thoroughly — SKILL.md, guides, templates, examples, scripts. Don't skim.

### Step 4 — Absorb

Extract the good parts and integrate them into YOUR skill. This is not copy-paste — it's adaptation.

- Take their edge case handling and add it to your constraints
- Take their template sections and merge with yours (keeping your conventions)
- Take their scripts and adapt to your project structure
- Take their checklist items and add to your quality criteria

**Key decisions during absorption:**
- Does this addition serve your actual workflow? If not, skip it.
- Does it conflict with your existing conventions? If so, adapt it.
- Does it add value beyond what you already have? If not, skip it.

### Step 5 — Review

After absorbing, review your upgraded skill holistically:

- Did you miss anything from the community skills?
- Does the combined result still make sense as a coherent skill?
- Are there any contradictions between absorbed parts and your original design?
- Would your skill handle edge cases the community skill handles?

### Step 6 — Cleanup

Delete the community skills you installed. Keep only yours, now upgraded.

```bash
# Remove installed community skills
rm -rf .claude/skills/community-code-review/
```

Your skill is now the single source of truth. No external dependencies.

> **Why This Matters:** Community skills are teaching material, not production dependencies. Using someone else's skill as-is means inheriting their conventions, their assumptions, and their limitations. Absorbing the best parts into your own skill means you understand every line and it fits your system perfectly.

---

## Example Walkthrough: Building a "Code Review" Skill

**Day 1 — Bootstrap:**
You tell Claude: "I need a code review skill. Focus on Python. Check security, performance, maintainability. Output a report with findings by severity."

Claude creates:
```
.claude/skills/code-review/
  SKILL.md          (basic: input, output, constraints)
  report/TEMPLATE.md (simple severity-based report)
```

You use it for 2-3 real reviews. It works but misses some things.

**Day 3 — Research + Gap Analysis:**
```bash
npx skills find code-review
# Found: alice/dev-tools@code-review, bob/workflows@pr-review
npx skills add alice/dev-tools@code-review -y
npx skills add bob/workflows@pr-review -y
```

You read both skills thoroughly. Findings:
- Alice's skill has a security checklist covering OWASP Top 10 — yours doesn't
- Bob's skill has a "review by file type" pattern — checks different things for tests vs production code
- Alice's template includes a "positive feedback" section — good for team morale
- Bob's skill has a script that auto-extracts changed files from a PR

**Day 3 — Absorb:**
You integrate:
- OWASP checklist items into your constraints
- File-type-aware review pattern into your guide
- Positive feedback section into your template
- Adapted version of Bob's script into your skill's scripts folder

You skip:
- Alice's JavaScript-specific rules (you work in Python)
- Bob's CI/CD integration (you don't need it yet)

**Day 3 — Cleanup:**
```bash
rm -rf .claude/skills/community-code-review/
rm -rf .claude/skills/community-pr-review/
```

Your code-review skill is now significantly better than any individual community skill — because it's tailored to your needs and enriched by the best of what's out there.

---

## Applies to Any Domain

This pattern is not limited to engineering skills:

| Domain | Bootstrap prompt | Research queries |
|---|---|---|
| Content writing | "I need a skill for blog posts targeting developers" | `npx skills find blog-writing`, `npx skills find content` |
| Data analysis | "I need a skill for SQL analysis with visualization recommendations" | `npx skills find data-analysis`, `npx skills find sql` |
| Testing | "I need a skill for writing test plans from PRDs" | `npx skills find test-plan`, `npx skills find qa` |
| Documentation | "I need a skill for API documentation" | `npx skills find api-docs`, `npx skills find documentation` |
| Marketing | "I need a skill for product launch planning" | `npx skills find gtm`, `npx skills find launch` |

You don't need domain expertise upfront. The bootstrap step leverages Claude's general knowledge, and the absorption step leverages the community's specialized experience.

---

## Commands Reference

| Command | Purpose |
|---|---|
| `npx skills find [query]` | Search skills.sh for skills matching your query |
| `npx skills add <owner/repo@skill> -y` | Install a community skill into your project |
| `npx skills` | List installed skills |
| Browse [skills.sh](https://skills.sh) | Discover skills visually |

---

## Key Principle

**Don't use someone else's skill as-is — use it as a benchmark to level up your own.**

Community skills are written for their author's context, conventions, and needs. Your skill should be written for yours. The absorption pattern lets you benefit from others' experience without inheriting their limitations.
