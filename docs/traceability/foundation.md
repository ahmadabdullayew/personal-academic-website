# Foundation items 1–10 traceability

| Item | Required outcome                   | Primary implementation evidence                                  | Executable evidence                              |
| ---: | ---------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------ |
|    1 | Functioning source repository      | Git `main`, intentional initial commit, source tree              | fresh-clone `make check`                         |
|    2 | README and local development       | `README.md`, `docs/development/local-development.md`             | `make bootstrap`, live-stack probe               |
|    3 | Seven architecture selections      | ADR 0001 and foundation literature review                        | Django/Compose/build checks                      |
|    4 | Manifests and locks                | `pyproject.toml`, `uv.lock`, `package.json`, `package-lock.json` | `make lock-check`                                |
|    5 | Format/lint/type/test commands     | Makefile and package scripts                                     | format, lint, type and test targets              |
|    6 | Environment documentation/examples | examples and environment contract                                | environment/deployment checks and negative tests |
|    7 | Actual owner                       | product baseline owner record and governance provenance          | schema/cross-field validation                    |
|    8 | Named approvers                    | six domain assignments and decision-record contract              | schema/cross-field validation                    |
|    9 | Primary/secondary audiences        | audience document and machine baseline                           | schema/cross-field validation                    |
|   10 | Ranked visitor/owner goals         | ranked-goal document, method and evidence references             | schema/cross-field validation                    |

The supplied PDFs are external evidence inputs, not repository dependencies.
Their filenames, printed-page reference convention and SHA-256 digests are
recorded in the machine baseline so a reviewer can verify that references point
to the same documents.
