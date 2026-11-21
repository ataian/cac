# CAC — Compact Artifact & Communication Notation

A standalone skill for compact, precise agent text. CAC writes the shortest version that still lets the recipient take the same action, for the same reason, within the same authority.

CAC is a writing and representation convention. It defines no roles, permissions, procedures, approval gates, or workflows, and it changes none of them.

## Use from a checkout

Give your agent the path to this repository's `SKILL.md`:

> Read `./SKILL.md` and its required local references. Apply CAC to `./AGENTS.md`. Preserve actors, obligations, conditions, exceptions, and exact literals. Change only the commissioned text.

Resolve `./SKILL.md` against this checkout. Resolve the target file against the project you commissioned.
Reading the skill and authorizing a file edit are separate actions.

## Install as a skill

Register the complete repository directory as `cac` through your agent's supported local-skill mechanism.
Keep `SKILL.md`, `references/`, and `third_party/` together; copying only the entrypoint is incomplete.
If another skill named `cac` exists, select the intended implementation before installation rather than merging them.

The skill uses file-reading capabilities, not a particular agent API. It needs no Maker checkout, TAS or Caveman installation, API key, package installation, or network access during use.

## Included files

- [SKILL.md](SKILL.md): triggers, loading procedure, scope, and verification.
- [CAC notation](references/cac-notation.md): principle, notation selection, syntax conventions, examples, agent-to-agent messages, and audience adaptation.
- [CAC Codex variant](references/cac-codex.md): the Codex-facing style, message shapes, and code/document boundaries.
- [Compact artifact contract](references/cac-authoring-contract.md): obligations, evidence discipline, state distinctions, placement, audience rule, and fidelity check.
- [Source inventory](sources.json): pinned origins, per-file checksums, and the exact adaptations.
- [Attribution and adaptations](NOTICE.md): license boundaries and changes from the source documents.

## Relation to TAS and Caveman

CAC replaces TAS and Caveman as the *writing convention* in the Maker that produces them; it does not replace their content, and this package needs neither.

- **TAS** remains a separate standard and a separate package. It supplies what CAC leaves to its consumers: the separation of authority from procedure, source grounding, verifiable completion criteria, and the requirement that moved instructions stay reachable. CAC keeps those outcomes as preserved obligations instead of restating the method. A project that wants the full authoring method still loads TAS.
- **Caveman** remains a third-party style source with its own packaging. CAC carries its durable direction — answer first, exact payload, concise findings, clarity exceptions — inside the notation itself, so neither Caveman nor a review variant is a required load. CAC is not a Caveman mode and has no activation, persistence, or routing commands.
- **CAC** is narrower than both: it fixes how existing information is written down. It cannot grant or move authority, cannot change a procedure, and cannot authorize a delivery change. Removing a style skill from a deployment is a delivery decision outside this package.

Caveman's Auto-Clarity originally excused verbosity for onboarding contexts where the author is new and needs the reason. CAC keeps the underlying rule — explain a consequential choice or a non-obvious correction — as a property of the finding, not as an audience exception. Whether a reason is needed depends on whether the recipient can act without it.

## Verify the package

Python 3.9 or newer, from the repository root:

```sh
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

Checks cover the skill frontmatter, the reference links in `SKILL.md`, the packaged checksums in `sources.json`, the declared adaptations, private machine paths, and relocation into a fresh directory.
These offline checks validate the package, not live model behavior, measured token savings, or the compliance of any text that was rewritten with it.

## Maintain and publish

This repository is the CAC package upstream. The notation itself is maintained in the `generic-devteam` Maker, where it is the operative writing convention.
Source updates here are deliberate package maintenance, not automatic pulls from the Maker.
Update references, provenance, and checks together. Preserve upstream notices.

Commit, remote publication, and live installation remain separate actions. A consuming project's pin names a committed revision, not unpublished working-tree changes.

## License

New CAC package material is [MIT-licensed](LICENSE).
The adapted notation, Codex variant, and artifact contract retain the [generic-devteam MIT notice](third_party/generic-devteam/LICENSE).
See [NOTICE.md](NOTICE.md) for attribution and exact scope.
