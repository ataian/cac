---
name: cac
description: Use when writing or compressing agent text in CAC.
version: 1.0.0
author: Max, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cac, notation, authoring, compression, handoff]
    related_skills: [tas]
---

# CAC: Compact Artifact & Communication Notation

Write the shortest complete version of existing agent text, preserving authority, obligation, evidence, and exact literals.
This package contains the CAC notation and its Codex variant. It needs no Maker, network service, or TAS/Caveman installation.

## When to Use

- The user requests CAC, including work outside the notation's source project.
- Draft, revise, compress, or review agent-facing text: SOULs, skills, references, technical documents, tickets, findings, and agent-to-agent messages.
- Propose compact wording before an authorized file edit.

## Prerequisites

Use a file-reading capability and access to the commissioned source text.
Resolve package paths relative to this `SKILL.md`, not the current working directory.
If a required file is missing or unreadable, report its path and stop the affected step.

## Procedure

1. Read [the CAC notation](references/cac-notation.md) completely on every invocation.
2. When the commissioned text is Codex-facing, also read [the CAC Codex variant](references/cac-codex.md) completely before rewriting.
3. Read [the compact artifact contract](references/cac-authoring-contract.md) for the fidelity check, the obligation details, and the audience rule.
4. Read the target's applicable instructions and current text. Identify the requested result, authorized scope, audience, and existing approval gates.
5. Rewrite section by section. Preserve actors, obligation strength (`MUST` / `SHOULD` / `MAY`), conditions, exceptions, order, scope, and uncertainty.
6. Keep identifiers, paths, commands, code symbols, quoted values, numbers, and units exact.
7. Compare old and new wording for an ordinary case and for the failing or exceptional case. Restore every lost distinction before reporting savings.
8. Report the result briefly. State unresolved decisions, unverified claims, and concrete blockers explicitly.

## Boundaries

CAC governs writing and representation only.
It defines no roles, permissions, procedures, approval gates, workflows, or status transitions, and it changes none of them.
Examples in the references are notation samples, not new rules or required fields.

Keep existing syntax contracts intact: skill frontmatter, JSON schemas, APIs, placeholders, native commands, and required output literals. CAC does not format source code.
Agent-to-agent and internal development text uses compact technical English. Human-facing communication uses clear prose in the recipient's language; a role that owns the human contact writes that language, while roles that never address the human audience stay in technical English.
Explain consequential choices, risks, and warnings in ordinary sentences.

This writing standard grants no installation, file-edit, commit, publication, deployment, or infrastructure permission.
Other agents receive CAC only through instructions they actually load; package availability alone does not activate it for them.

## Verification

- Preserve actors, actions, inputs, triggers, conditions, approval owners, exceptions, and required results.
- Keep required, optional, unknown, and absent distinct; a valid zero is not missing and a present null is not an absent field.
- Distinguish observed facts from assumptions, and written, tested, reviewed, approved, published, and deployed states.
- Verify that every compressed pointer resolves to retrievable evidence for its recipient.
- Use plain prose when compression would obscure meaning, a condition, a sequence, a risk, or a safety boundary.
