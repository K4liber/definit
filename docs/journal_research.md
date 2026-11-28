# Target Journal Research for a DefinIT Paper

Date: 2026-11-12

## Recommendation

### 🥇 Best fit: *Knowledge Organization* (KO)

- Website: https://www.imrpress.com/journal/KO — journal of the International Society for Knowledge Organization (ISKO), published open access by IMR Press. The ISKO portal (https://portal.isko.org/) is the parent society, not a journal itself.
- Scope explicitly covers: concept systems, classification, thesauri, ontologies, semantic relations, and theoretical papers about how concepts should be structured — exactly DefinIT's "concept-first, single acyclic 'is based on' relation" story.
- Regularly publishes position/theory papers in the Wüsterian tradition, sociocognitive and frame-based approaches — all already cited in the README literature review, so the paper speaks the journal's language.
- Notes: humanities/social-science orientation, moderate review speed (~6 days to first decision, ~98 days submission-to-acceptance per journal page), indexed in Scopus and SSCI (IF 0.5). **APC: 1800 USD** (open access, IMR Press) — full waivers available for unfunded authors, but must be requested *before* submission via apcs@imrpress.com (~27–32% of content gets waivers yearly); see https://www.imrpress.com/journal/KO/page/apc and https://www.imrpress.com/page/article-processing-charges.

Suggested framing: *"DefinIT: an operationalization of definitional regress and concept systems as a versioned, machine-processable DAG with a single acyclic relation."* The README sections on terminology science, philosophy of definitions, and symbol grounding map almost 1:1 to this journal's readership.

### 🥈 Strong alternative: *Terminology* (John Benjamins)

- Website: https://benjamins.com/catalog/term — Editors: Kyo Kageura & Rita Temmerman (Temmerman's sociocognitive approach is reference [11] in the README).
- Verified scope (from publisher): "problems of ambiguity, reference… knowledge representation and transfer, information technology tools, expert systems and terminological databases."
- Metrics: Impact Factor 1.0 (5-year: 1.2), CiteScore 2.2, SJR 0.343.
- Better fit if the paper frames DefinIT as a *terminological resource / concept-system engineering* contribution rather than a knowledge-organization theory paper. Linguistics-oriented audience.
- Cost: subscription-based, no mandatory page charges / APC for regular issues — effectively free to publish (green OA self-archiving allowed).

## Other options considered (less fitting)

| Journal | Publisher / Link | Why less fitting |
|---|---|---|
| *Semantic Web* | IOS Press, https://www.semantic-web-journal.net/ (IF ~3, open access, open transparent reviews) | Attractive if emphasizing the machine-processable/LLM-training-data angle and formal KG aspects; but DefinIT is deliberately *not* an OWL/RDF ontology, which reviewers there will likely challenge |
| *Journal of Documentation* | Emerald | Possible, but expects user studies or informometrics evaluation |
| *JASIST* | Wiley | Same expectation of empirical information-science evaluation |
| *International Journal of Lexicography* | OUP | Dictionary-focused; DefinIT is not a lexicographic work |

## Case study asset: `definit-db`

The "data structures and algorithms" concept database built on DefinIT (~/Desktop/projects/definit-db: `computer_science`/`mathematics` fields, `defs.json`, GUI, word analysis of non-definition words) is a strong asset for this venue — KO values concrete KOS implementations. Consider adding a case-study section demonstrating the `computer_science/data_structure` DAG and the word-analysis workflow.

## Strategy

1. Submit to *Knowledge Organization* (IMR Press), framing the paper around concept-system theory (definitional regress, symbol grounding kernel, single-relation discipline), citing the KO-ecosystem works now blended into the README Literature Review (Hjørland 2026; Alwis 2026; Amirhosseini 2026; Dahlberg; Szostak 2026).
2. Keep *Terminology* as backup if the framing leans more toward LSP communication and terminological databases.
