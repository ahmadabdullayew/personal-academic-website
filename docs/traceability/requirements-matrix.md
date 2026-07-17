# Requirement applicability, dependency, and ownership matrix

`config/requirements-matrix.json` is the machine-readable row-for-row control
record for foundation item 23. It contains all 264 functional-requirement cards
from the reviewed SRS and cross-checks their order and priority against Appendix
A of the reviewed backend specification.

## Audited source identity

| Source                                                | PDF pages | SHA-256                                                            |
| ----------------------------------------------------- | --------: | ------------------------------------------------------------------ |
| `personal_academic_professional_website_srs.pdf`      |       324 | `976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7` |
| `personal_academic_website_backend_specification.pdf` |        65 | `1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5` |

All matrix page references are printed page numbers shown inside the PDFs, not
PDF-viewer indices. Every row records the detailed SRS card-heading page, the
SRS table-of-contents target page, and the backend Appendix A trace page.

## Completeness result

| Control                                                | Audited result |
| ------------------------------------------------------ | -------------: |
| Unique requirement rows                                |            264 |
| SRS modules / dependency profiles                      |        20 / 20 |
| P0 - MUST                                              |            148 |
| P1 - SHOULD                                            |             62 |
| P2 - CONDITIONAL                                       |             52 |
| P2 - MAY                                               |              2 |
| Applicable in baseline 2.0.0                           |            222 |
| Not applicable in baseline 2.0.0                       |             42 |
| Explicit cross-requirement ID edges in the source PDFs |              0 |
| Backend `Direct backend` rows                          |            179 |
| Backend `Shared contract` rows                         |             70 |
| Backend `Frontend-led` rows                            |             15 |

The 222 applicable rows comprise all 148 P0 rows, all 62 P1 rows retained by the
full-build profile, and 12 explicitly activated P2 rows:

1. `FR-CONTENT-10`
2. `FR-CONTACT-03`
3. `FR-ADMIN-08`
4. `FR-ADMIN-11`
5. `FR-ADMIN-14`
6. `FR-ADMIN-16`
7. `FR-SEC-02`
8. `FR-SEC-04`
9. `FR-SEC-05`
10. `FR-SEC-06`
11. `FR-SEC-09`
12. `FR-OPS-03`

The other 42 P2 rows have explicit dormant decisions, rationales, and activation
conditions copied from `config/product-baseline.json`; they are not unresolved
or silently deferred.

## Module and owner reconciliation

| Prefix     | Module                                               | Rows | SRS accountable roles                               |
| ---------- | ---------------------------------------------------- | ---: | --------------------------------------------------- |
| `GOV`      | Identity and Content Governance                      |    8 | Product Owner; Academic Content Owner               |
| `SHELL`    | Global Shell and Navigation                          |    8 | Frontend Lead; UX Owner                             |
| `HOME`     | Homepage                                             |    8 | Product Owner; Academic Content Owner               |
| `ABOUT`    | About and Professional Identity                      |   10 | Academic Content Owner                              |
| `RES`      | Research Profile                                     |   10 | Academic Content Owner; Research Lead               |
| `PUB`      | Publications and Scholarly Outputs                   |   42 | Academic Content Owner; Scholarly Metadata Steward  |
| `PROJ`     | Projects, Software, and Research Data                |   14 | Academic Content Owner; Technical Portfolio Owner   |
| `CAREER`   | Education, Experience, and Expertise                 |   14 | Academic Content Owner                              |
| `ACADEMIC` | Teaching, Mentoring, Recognition, Talks, and Service |   12 | Academic Content Owner                              |
| `CONTENT`  | News, Public Scholarship, and Media                  |   10 | Academic Content Owner; Communications Owner        |
| `DOC`      | Curriculum Vitae and Public Documents                |    8 | Academic Content Owner; Document Steward            |
| `CONTACT`  | Contact and Collaboration                            |   12 | Product Owner; Privacy Owner; Backend Lead          |
| `SEARCH`   | Search and Discovery                                 |    8 | Frontend Lead; Content Architecture Owner           |
| `INT`      | Scholarly Identity and External Integrations         |   10 | Integration Owner; Scholarly Metadata Steward       |
| `SEO`      | Machine-Readable Metadata and Discoverability        |   14 | Technical SEO Owner; Content Architecture Owner     |
| `ACC`      | Accessibility Functions                              |   20 | Accessibility Owner; Frontend Lead                  |
| `I18N`     | Internationalization and Multilingual Content        |    6 | Content Localization Owner; Frontend Lead           |
| `ADMIN`    | Content Administration and Editorial Workflow        |   16 | Product Owner; Technical Administrator              |
| `SEC`      | Authentication, Security, and Privacy                |   18 | Security Owner; Privacy Owner; Backend Lead         |
| `OPS`      | Errors, Operations, Legal, and Data Quality          |   16 | Technical Owner; Content Owner; Legal/Privacy Owner |

Each row preserves those source roles and assigns the named project-accountable
person, Ahmad Abdullayev, through the product-baseline owner record.

## Dependency interpretation

The SRS expresses dependencies as card preconditions. Within each module, the
non-title preconditions are identical, producing 20 lossless dependency
profiles. Every row additionally retains its exact title-specific scope-approval
precondition.

Neither reviewed PDF names another `FR-*` identifier as a dependency from inside
a requirement card. Consequently, every `requirement_ids` array is deliberately
empty. This means “no explicit source edge,” not “no semantic relationship.” The
matrix prohibits inferred edges so an apparently plausible relationship cannot
be mistaken for source fact.

## Printed-page discrepancy retained

The SRS table of contents and the physical detailed-card heading differ by one
printed page for 31 requirements. Both values are retained:

| Requirement      | TOC page | Card-heading page |
| ---------------- | -------: | ----------------: |
| `FR-GOV-01`      |       15 |                16 |
| `FR-SHELL-02`    |       25 |                26 |
| `FR-HOME-05`     |       37 |                38 |
| `FR-ABOUT-08`    |       49 |                50 |
| `FR-RES-09`      |       61 |                62 |
| `FR-PUB-06`      |       69 |                70 |
| `FR-PUB-13`      |       77 |                78 |
| `FR-PUB-20`      |       85 |                86 |
| `FR-PUB-27`      |       93 |                94 |
| `FR-PUB-34`      |      101 |               102 |
| `FR-PUB-41`      |      109 |               110 |
| `FR-PROJ-08`     |      119 |               120 |
| `FR-CAREER-04`   |      130 |               131 |
| `FR-CAREER-14`   |      141 |               142 |
| `FR-ACADEMIC-12` |      154 |               155 |
| `FR-CONTENT-09`  |      164 |               165 |
| `FR-CONTACT-02`  |      176 |               177 |
| `FR-CONTACT-09`  |      184 |               185 |
| `FR-SEARCH-04`   |      192 |               193 |
| `FR-INT-06`      |      203 |               204 |
| `FR-SEO-04`      |      212 |               213 |
| `FR-SEO-13`      |      222 |               223 |
| `FR-ACC-08`      |      232 |               233 |
| `FR-ACC-18`      |      243 |               244 |
| `FR-ADMIN-01`    |      253 |               254 |
| `FR-ADMIN-10`    |      263 |               264 |
| `FR-SEC-02`      |      272 |               273 |
| `FR-SEC-09`      |      280 |               281 |
| `FR-SEC-16`      |      288 |               289 |
| `FR-OPS-05`      |      296 |               297 |
| `FR-OPS-13`      |      305 |               306 |

Within the SRS extraction, no duplicate or missing ID, title, module, priority,
owner, normative statement, or precondition field was found. Appendix A of the
backend specification has exactly 264 row starts on printed pages 38–63; its
priority-level sequence is identical to the SRS sequence, and every row's
backend responsibility class is retained.

## Reproduction and validation

The committed matrix does not require the external PDFs at runtime. A source
audit can regenerate it from the exact reviewed files. Source regeneration
requires Poppler `pdftotext` 24.02.0 or later; verify the installed extractor
first with `pdftotext -v`:

```shell
python3 scripts/build_requirements_matrix.py \
  --srs-pdf /path/to/personal_academic_professional_website_srs.pdf \
  --backend-pdf /path/to/personal_academic_website_backend_specification.pdf
```

The builder rejects different PDF hashes, wrong page counts, missing or
reordered cards, a priority mismatch between PDFs, and an incomplete P2 decision
ledger. The standalone release check is:

```shell
python3 scripts/validate_requirements_matrix.py
```

The validator applies the JSON Schema and independently pins the source ledger
digest `505e956ebbd194265668aa2e74d9b0856d2a14c73939ac1a7ff0c362fe824a81` and
decision ledger digest
`a17de332330a6f1e379381eed3b30ad4f1e59f4e8ded324d0f38aaf9f6c2a1cc`.
