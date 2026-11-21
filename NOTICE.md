# Attribution and adaptations

## CAC

CAC means Compact Artifact & Communication Notation.
The notation derives from the `generic-devteam` project's `docs/cac/CAC-HERMES.md`, `docs/cac/CAC-CODEX.md`, `docs/SPEC_2.10.1_CAC_v1.md`, and `references/cac-authoring.md`, by Max and the generic-devteam contributors.
The original MIT notice is retained in [third_party/generic-devteam/LICENSE](third_party/generic-devteam/LICENSE).
[Sources and checksums](sources.json) identify the repository revision, the source files, the packaged bytes, and every adaptation.

This package is an independent distribution of the notation, not an installation of the Maker and not a team template.
It bundles no roles, model routes, delivery procedure, updater, manifest, or generated-team instructions.
The Maker remains the place where CAC is applied to Team SOULs and handoffs.

## Adaptations

The notation and Codex references are separate reading copies with a visible provenance notice; the artifact contract is a reading copy with a heading and that notice.
The source titles, purpose statements, and scope paragraphs of the two notation references were rewritten so the texts address a package reader rather than the Maker's maintainers.
The notation reference adds one role-scoped audience bullet: only the role that owns the human contact writes in that language, and roles that never address the human audience write technical English to each other.
That bullet records the rule the Maker's generated teams actually apply, where Coder, Codex, and Reviewer never talk to the customer and only the Planner is bilingual.
The same reference escapes one pipe inside a table cell so the notation table keeps three columns.

Apart from that audience bullet, no rule was added, removed, or weakened by the packaging.
Examples remain notation samples, and no universal schema, parser, or word cap is implied.

## Relation to TAS

TAS is a separate standard with its own standalone package and its own revision history.
CAC replaces TAS *as a writing convention* in the Maker; it does not supersede the standard's method.
Authority separated from procedure, source grounding, verifiable completion, reachable pointers, and distinct state claims remain obligations of any CAC rewrite and are restated in the artifact contract.
A project that wants the full authoring method still loads TAS.
No TAS file is bundled here, and this package neither requires nor modifies the `tas` package.

## Relation to Caveman

Caveman is Julius Brussee's third-party style project, distributed separately.
CAC replaces it as a writing convention in the Maker and keeps its durable direction in its own rules: answer first, exact payload, concise findings, clarity exceptions.
No Caveman file, CLI, hook, font, or mode machinery is bundled, and CAC has no activation, deactivation, persistence, or routing commands.

Caveman's review guidance dropped terse mode for security findings, architectural disagreements, and onboarding contexts where the author is new and needs the "why".
CAC keeps the first two as properties of the finding and drops the onboarding exception: the recipient is a role, not a new employee.
Where a reason is needed to act, the finding carries it briefly; otherwise the observed fact, impact, and evidence suffice.

Copyright 2026 Julius Brussee. Caveman is referenced as an upstream style source, not bundled here, and is not the author or sponsor of CAC.

## Deliberate limits

The package tests validate files: frontmatter shape, links, checksums, provenance, and relocation.
They do not measure model behavior, token savings, or compliance of rewritten text.
Byte reductions reported for the Maker migration are offline UTF-8 measurements on instruction text, not billed tokens and not a promise for other projects.
