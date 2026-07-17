# Foundation review protocol and evidence extraction

## Scope and evidence hierarchy

This bounded review supports foundation items 1–10: repository, developer
documentation, architecture, dependency locking, automated controls, environment
configuration, owner identity, approval responsibility, audiences and ranked
goals. It does not assert implementation of later content modules.

Evidence is used in this order:

1. supplied project specifications for project intent and required behavior;
2. formal standards and government publications for normative quality and
   security guidance;
3. peer-reviewed research for academic-homepage and scholarly-identity
   observations;
4. official project/service documentation for component behavior; and
5. explicitly labelled reviewer inference for architecture synthesis.

Vendor documentation establishes capability, not independent comparative
superiority.

## Run record

- Review date: 2026-07-17
- Timezone: Asia/Baku
- PDF inspection tools: `pdfinfo`, `pdftotext`, `sha256sum`
- Bibliographic discovery endpoint: Crossref REST API
- DOI deduplication: lowercase DOI string
- Official-document discovery: targeted domain searches followed by direct
  inspection of the official page

## Supplied-document integrity

| Document                                              | SHA-256                                                            | Physical pages | Page mapping                                                               | Foundation locations                                                                                                                 |
| ----------------------------------------------------- | ------------------------------------------------------------------ | -------------: | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `personal_academic_professional_website_srs.pdf`      | `976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7` |            324 | numbered body pages 1–316 are physical pages 9–324; physical = printed + 8 | printed pp. 1–3 purpose/boundary/language; 6–7 actors/invariants; 15–23 identity governance; 33–41 homepage goals; 315 bibliography  |
| `personal_academic_website_backend_specification.pdf` | `1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5` |             65 | numbered content is one physical page later; physical = printed + 1        | printed pp. 4–7 scope/conformance/components/deployment; 22–27 security/search; 32–35 deployment/testing/completion; 64 deliverables |

Repository citations use printed page numbers explicitly. An unqualified page
number would be ambiguous.

## Exact scholarly-discovery requests

The review executed three bounded Crossref requests and screened the first 20
relevance-ordered records from each:

```text
GET https://api.crossref.org/works?query.title=academic%20homepages%20scholarly%20identity&filter=type:journal-article&rows=20&select=DOI,title,author,published,container-title,score
GET https://api.crossref.org/works?query.title=researchers%20online%20visibility%20trust%20reputation&filter=type:journal-article&rows=20&select=DOI,title,author,published,container-title,score
GET https://api.crossref.org/works?query.title=scholarly%20identity%20social%20networking%20sites&filter=type:journal-article&rows=20&select=DOI,title,author,published,container-title,score
```

Exact retained records were checked with:

```text
GET https://api.crossref.org/works/{URL-encoded-DOI}
```

Crossref's changing global `total-results` value is not treated as a stable
count. The bounded returned set defines the reproducible procedure, while future
relevance ordering may still change.

### Screening criteria

A record was retained when it directly examined personal/academic homepages,
owner-controlled academic identity, researchers' online visibility/trust/
reputation, or academic social-network use with a material implication for an
owner-controlled scholarly hub.

Generic self-esteem, consumer reputation, shopping, student self-concept,
political identity, general social-media use and institution-only homepages were
excluded.

### Screening ledger

| Stage                                                                 | Count | Disposition                                                                                                                |
| --------------------------------------------------------------------- | ----: | -------------------------------------------------------------------------------------------------------------------------- |
| Crossref records returned                                             |    60 | 20 per exact query                                                                                                         |
| Unique lowercase DOI strings                                          |    60 | no duplicates across returned sets                                                                                         |
| Excluded at relevance screen                                          |    53 | outside direct scope                                                                                                       |
| Retained from Crossref                                                |     7 | directly relevant                                                                                                          |
| Additional unique records seeded from the supplied SRS/current review |     4 | Döring; Papacharissi; Thoms and Thelwall; Bar-Ilan et al.                                                                  |
| Final identity evidence set                                           |    11 | nine peer-reviewed DOI records, one peer-reviewed record without a verified DOI, one contextual preprint/conference record |

This is a bounded evidence review, not an exhaustive systematic review of every
bibliographic database.

## Exact official-source discovery queries

```text
site:iso.org ISO IEC 29148 requirements engineering official
site:iso.org ISO IEC 25010 product quality model official
site:iso.org ISO IEC 25012 data quality model 2008 official
site:rfc-editor.org RFC 2119 RFC 8174 BCP 14 official
site:w3.org/TR/WCAG22 conformance full pages complete processes official
site:owasp.org ASVS 5.0 official
site:nist.gov SP 800-218 SSDF official
site:orcid.org public API reading ORCID records official
site:crossref.org documentation REST API retrieve metadata official
site:schema.datacite.org DataCite Metadata Schema current official
site:credit.niso.org contributor roles taxonomy 14 roles official
site:go-fair.org FAIR principles official
site:schema.org ProfilePage Person official
site:scholar.google.com scholar inclusion crawlable URLs bibliographic metadata
site:docs.djangoproject.com/en/5.2 templates security admin deployment official
site:postgresql.org/docs/18 full text search GIN pg_trgm unaccent official
site:docs.aws.amazon.com SQS at-least-once dead-letter visibility timeout official
site:docs.aws.amazon.com S3 encryption versioning CloudFront origin access control official
site:docs.aws.amazon.com ECS Fargate RDS Multi-AZ backups official
```

Official pages were purposefully sampled, so no unstable search-result
denominator is claimed.

## Evidence appraisal

| Evidence class                                | Permitted use                                                   | Principal limitation                                                |
| --------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------- |
| Supplied PDFs                                 | scope, actors, behavior, priorities, state boundaries           | internally authored; not independent empirical validation           |
| ISO, RFC and W3C                              | requirement language, quality models, accessibility conformance | accessible ISO summaries do not justify claims beyond visible text  |
| NIST and OWASP                                | secure lifecycle and verification structure                     | tailoring is required; citation does not prove compliance           |
| Peer-reviewed studies                         | audience needs, identity tensions, common content and risks     | samples can be old, small, discipline-specific or platform-specific |
| Scholarly-infrastructure/search documentation | API fields, metadata behavior and crawler conditions            | cannot prove imported data correctness or guarantee indexing        |
| Framework/cloud documentation                 | component capability and operational facts                      | vendor-authored, not comparative proof                              |
| Weighted matrices                             | transparent selection inference                                 | ordinal judgment, not measurement or a price quote                  |

## Scholarly-identity extraction

| Source                                                                                             | Method/sample                                                 | Relevant extraction                                                                                       | Limitation and decision use                                        |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Döring, [DOI](https://doi.org/10.1111/j.1083-6101.2002.tb00152.x)                                  | review of about 30 personal-homepage studies                  | production, content, self-presentation and reception interact; ownership/authenticity matter              | broad and old; supports owner control, not modern feature ranks    |
| Papacharissi, [DOI](https://doi.org/10.1177/107769900207900307)                                    | personal-homepage content study                               | layout and publishing tools influence self-presentation                                                   | early-web context; supports deliberate structure only              |
| Thoms and Thelwall, [article](https://firstmonday.org/ojs/index.php/fm/article/download/1302/1222) | qualitative analysis of 20 academic homepages                 | institution-managed presentation may suppress individual identity; owner-managed pages allow more control | small interpretive sample; peer-reviewed context, no verified DOI  |
| Hyland, [DOI](https://doi.org/10.1016/j.esp.2011.04.004)                                           | 100 academic homepages across two fields, ranks and genders   | text, design and links jointly construct credibility and scholarly identity                               | two disciplines/2011; supports structured identity and evidence    |
| Hyland, [DOI](https://doi.org/10.1016/j.compcom.2012.10.002)                                       | paired university/personal pages for 50 academics             | self-managed pages can preserve individuality beyond institutional profiles                               | identity, not usability, research                                  |
| Dumont and Frindte, [DOI](https://doi.org/10.1016/j.chb.2004.02.001)                               | 350 content observations; 86 questionnaires in four countries | research activities/publications dominated; teaching and scholarly links were common                      | one discipline and early-web period; does not prove exact ranks    |
| Bar-Ilan et al., [record](https://arxiv.org/abs/1205.5611)                                         | web-presence study of 57 conference presenters                | scholarly presence is distributed across homepages and external profiles                                  | small convenience sample/preprint context only                     |
| Kjellberg and Haider, [DOI](https://doi.org/10.1108/OIR-07-2017-0211)                              | focus-group study                                             | formal outputs continue to scaffold online trust and reputation                                           | public abstract limits sample-level generalization                 |
| Radford et al., [DOI](https://doi.org/10.1002/pra2.2018.14505501044)                               | 30 semi-structured interviews                                 | connection/dissemination benefits coexist with ethical, commercial, time and context-collapse risks       | exploratory/self-selected; supports restrained owner control       |
| Radford et al., [DOI](https://doi.org/10.1108/JD-04-2019-0074)                                     | analysis of 30 self-selected participants                     | benefits coexist with platform, copyright, confusion and reputation risks                                 | demographic/geographic limits; supports local authority/provenance |
| Yan and Zhang, [DOI](https://doi.org/10.2478/dim-2020-0050)                                        | scoping review of 115 works                                   | discovery and sharing are major academic-network motivations, varying geographically                      | social-network rather than personal-site evidence                  |

These sources support owner control, research/output prominence,
discoverability, provenance and restrained claims. They do not empirically prove
the exact audience or goal order; that order remains a recorded product
decision.

## Standards and scholarly infrastructure

1. [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) supports
   identifiable, testable and traceable requirements; it does not prescribe Git,
   Django or AWS.
2. [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) supplies
   product-quality characteristics used as comparison criteria.
3. [ISO/IEC 25012:2008](https://www.iso.org/standard/35736.html), confirmed in
   2025, adds a structured-data quality model relevant to identity, dates,
   identifiers, visibility and publication metadata.
4. [RFC 2119](https://www.rfc-editor.org/info/rfc2119) and
   [RFC 8174](https://www.rfc-editor.org/info/rfc8174) assign special meanings
   only to uppercase BCP 14 terms; they do not define project priority.
5. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) uses full-page and complete-process
   conformance, so isolated component checks are insufficient.
6. [OWASP ASVS 5.0.0](https://owasp.org/www-project-application-security-verification-standard/)
   and [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) support
   lifecycle security and reviewable verification evidence.
7. The
   [ORCID Public API](https://info.orcid.org/what-is-orcid/services/public-api/)
   can retrieve public data; imported data remains provenance-labelled and
   owner-reviewed.
8. The
   [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
   exposes deposited/trusted-source metadata; imports are candidates, not
   automatically authoritative facts.
9. [DataCite Metadata Schema 4.7](https://schema.datacite.org/meta/kernel-4.7/),
   released 2026-03-03, is the current vocabulary baseline; imported records
   retain their source/schema version.
10. [CRediT](https://credit.niso.org/contributor-roles-defined/) supplies 14
    contribution roles but does not determine authorship or author order.
11. The [FAIR principles](https://doi.org/10.1038/sdata.2016.18) support
    identifiers, rich metadata, licences, provenance and access conditions for
    research objects. They do not make the whole site FAIR by default.
12. [Schema.org `ProfilePage`](https://schema.org/ProfilePage) and
    [Google ProfilePage guidance](https://developers.google.com/search/docs/appearance/structured-data/profile-page)
    support a visible owner profile; markup must match visible content and does
    not guarantee a search feature.
13. [Google Scholar inclusion guidance](https://scholar.google.com/intl/en/scholar/inclusion.html)
    calls for a separate crawlable URL per paper, simple links, visible complete
    abstracts or full text and bibliographic meta tags. It also expects an
    included collection to be primarily scholarly articles. Publication pages
    should be compatible without promising site acceptance or indexing.

## Foundation decision trace

| Item | Evidence-to-decision boundary                                                                    | Verification                                       |
| ---: | ------------------------------------------------------------------------------------------------ | -------------------------------------------------- |
|    1 | backend version-control requirement and SSDF controlled change; Git is the engineering mechanism | valid `main`, initial commit, fresh-clone check    |
|    2 | reproducibility/maintainability requirements; exact README/local procedure                       | documented bootstrap and live probe                |
|    3 | backend component profile plus quality/security evidence; one coherent selection                 | ADR and weighted matrices                          |
|    4 | reproducible release plus official `npm ci`/`uv sync --frozen` behavior                          | manifests, complete locks, read-only lock check    |
|    5 | quality, accessibility, security and backend verification requirements                           | single `make check` gate and CI                    |
|    6 | Django deployment checklist, SSDF and secret boundaries                                          | safe examples, strict parser, production check     |
|    7 | SRS one-owner model plus owner-directed/local identity evidence                                  | versioned owner/provenance record                  |
|    8 | distinct acceptance evidence for six quality domains                                             | six named roles and decision-record contract       |
|    9 | SRS actors plus identity research                                                                | sourced audience hypotheses                        |
|   10 | SRS purpose/home requirements plus identity/discovery evidence                                   | explicit ordinal method, goals and revisit trigger |
