# Active Hypotheses

Maintained by the Board of Directors process. Only hypotheses that survived investigation are
listed. Each carries evidence on both sides, a confidence level, and the cheapest next test that
would move that confidence. Update or retire entries as evidence changes; do not assume a prior
entry is still correct.

Last updated: 2026-06-18 (Report No. 1, Revision A audit)

---

## H1 — Structure-before-substance is Marcos's primary cognitive bottleneck

**Statement.** Marcos reliably builds elaborate structure (schemas, templates, repos, directory
systems) and defers the load-bearing substance (the thesis, the actual content, the decision).
The scaffolding feels like progress; the value stays latent.

**Status:** Active — strongly supported.
**Confidence:** High.

**Evidence For**
- `adversarial-diligence-framework/PROJECT_THESIS.md` is an unfilled template — every section is
  still `_(write here)_` — while 576 lines of skeleton code and 7 doc files already exist.
- The framework's agents and pipelines are all stubs (`NotImplementedError`/`pass`); the README
  itself says "no model calls, no network, no real data."
- The Ideas wiki has a ~200-line operating schema (`CLAUDE.md`) and a rich seed profile, but zero
  compiled wiki entries (`sources/`, `concepts/`, `entities/` effectively empty).
- The Board of Directors template existed before any analysis was ever run against it.
- Report No. 1 itself (written by Claude) committed the same error: an impressive narrative
  structure built on thin, second-hand evidence that did not survive a primary-source audit.

**Evidence Against**
- The finance-statement-agent and the Okavango deliverables are fully substantive and in use, so
  the pattern is not universal — it concentrates in self-directed "infrastructure" projects.
- "Foundation-first" is a genuine strength in software (data model before UI) and sometimes the
  structure is the correct first step.

**Recommended Next Test.** Ask Marcos to write the framework's one-paragraph thesis in plain prose
in under 30 minutes. If he cannot, the project is structure without substance and should be
shelved, not extended. Repeat the test on any new "infrastructure" project before code is written.

---

## H2 — Marcos's real economic edge is legacy-business + El Salvador, not generic AI building

**Statement.** His defensible advantage is access to a real legacy business with physical and
relational moats (his father's regional construction firm, Narváez Hinds; the El Salvador market;
on-the-ground operations) applied with AI — not competing in the saturated, fast-commoditizing
"young person who builds with LLMs" lane.

**Status:** Active — plausible, needs a real-world test.
**Confidence:** Medium.

**Evidence For**
- He himself tags `llm-legacy-business` as a knowledge domain and calls architecture/construction
  "the through-line connecting most of [his] other interests" (seed profile).
- His father runs Narváez Hinds, "growing rapidly into a regional powerhouse" — a rare, warm,
  defensible distribution channel most peers do not have.
- The skill he is accumulating fastest (prompting Claude to build tools) is also the skill the
  broader market is commoditizing fastest; it is weak differentiation on its own.

**Evidence Against**
- He states a clear preference for "straight startup" and staying in the US; the family firm is in
  El Salvador and may not match his stated geographic intent.
- No evidence yet that he has scoped or attempted any AI application inside the family business.

**Recommended Next Test.** Scope one concrete, narrow AI application for Narváez Hinds or a specific
El Salvador business he can actually reach, and check whether a real decision-maker would adopt it.
A single warm "yes" would sharply raise confidence; a shrug would lower it.

---

## H3 — Adversarial verification is a real disposition, but not yet a durable moat

**Statement.** Refute-first, source-backed verification is a genuine trait in how Marcos works and
thinks — but it currently appears concentrated in recent, verification-rewarding tasks and may be
partly driven by tooling, not a proven career-level differentiator.

**Status:** Active — confirmed as a trait, unproven as a moat.
**Confidence:** Medium-High that it is a real disposition; Low that it is a durable moat.

**Evidence For (real disposition)**
- Okavango ran genuine adversarial verification at scale (one fact-checker agent per company,
  refute-by-default, 133-agent verification pass — `AUDIT.md`, `EXPANSION.md`).
- World Cup model red-teamed every large edge and honestly reported the model loses to the market.
- He commissioned a steelmanned two-sided analysis of the Protestant–Catholic question and states
  a standing preference for correction over flattery (seed profile).

**Evidence Against (moat / stability)**
- In the framework, "adversarial verification" is template boilerplate over stubbed code, not a
  working capability.
- The pattern clusters in June work; diligence and betting inherently reward verification, so task
  selection — not personal signature — may explain it.
- Analyst-projection risk: the Board process itself is built on adversarial verification, which
  primes the analyst to over-detect the pattern.

**Recommended Next Test.** Look for adversarial verification in work that does *not* inherently
demand it (e.g., a creative or course project). If it shows up there too, it is a trait; if not, it
is task-driven.

---

## H4 — The most under-managed real risk is OFSL conduct probation, not immigration

**Statement.** The chapter is on OFSL conduct probation and runs unregistered events; that is the
live institutional risk. The "F-1 / deportation" framing of Report No. 1 was overstated — Marcos is
the law-abiding victim in the Castle dispute and holds the leverage.

**Status:** Active — supported, severity recalibrated downward from Report No. 1.
**Confidence:** Medium-High.

**Evidence For**
- Seed profile: "The chapter is on conduct probation from OFSL ... and runs unregistered
  post-midnight events weekly. High risk, low detection."
- The Castle letter shows Marcos as the documented victim, explicitly stating he has committed no
  crimes; his only conceded exposure is "we would likely lose the ability to host registered
  events" — a chapter sanction, not an immigration event.

**Evidence Against**
- Conduct probation plus repeated unregistered events could, in a bad-faith escalation, still draw
  individual scrutiny; the residual tail risk is non-zero.
- Okavango work authorization for an F-1 holder remains unverified (likely moot if performed from
  El Salvador, but unconfirmed).

**Recommended Next Test.** Confirm the exact terms and end date of the OFSL probation, and confirm
where the Okavango work is physically performed and whether it needs CPT. Two short factual checks.

---

## H5 — Marcos's "straight startup, don't force recruiting" self-narrative conflicts with his behavior

**Statement.** He describes his path as "straight startup ... not interested in forcing
[recruiting]," but his revealed behavior in 2026 is more conventional: a US PE-search-fund
internship (Okavango) plus active recruiting outreach (Sapien, AMCA). His actual path may be more
conventional than he believes — which is not bad, but the mismatch is worth surfacing.

**Status:** Active — supported by the gap between stated plan and revealed action.
**Confidence:** Medium.

**Evidence For**
- April seed profile: summer plan is "building LLM-driven platforms as a personal business or
  startup" in El Salvador; "US summer internship recruiting is constrained by GPA, and he's not
  interested in forcing it."
- June reality: he is the engineer/intern on a deliverable for Okavango Holdings (Francois Stassen
  / Luke Baker), and ran tailored recruiting outreach to Sapien (Apr) and AMCA (May).

**Evidence Against**
- The Okavango internship may itself be the "monetizable agent service" plan in disguise, or a
  deliberate stepping-stone; the two are not strictly contradictory.

**Recommended Next Test.** Ask directly: is Okavango a paid internship, equity, or a favor, and does
he see it as a step toward the startup path or a detour from it? His answer resolves the tension.
