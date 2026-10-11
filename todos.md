# DefinIT TODOs

As much as possible, the items should be prioritized in order of importance. We split the items into 4 buckets:
- IN PROGRESS: Items that are currently being worked on.
- TODO: Items that are planned to be implemented in the future.
- DONE: Items that have been completed.
- ABANDONED: Items that are no longer being pursued, but are kept for historical purposes.

Each item should have a title, a description, and a list of tasks to be completed. The tasks should be checkboxes that can be checked off as they are completed. Each item should also have a category [feature, bug, docs, devops, or other] to indicate the type of work being done. If a task depends on another task, it should be indicated next to the category e.g. [FEATURE, depends on #1].

## IN PROGRESS

### 7. [docs] Re-do the literature review and update the README with the new references

Survey the literature beyond the historical CS glossaries (Hopper, ACM CCS, IEEE, UML) to position DefinIT against existing concepts, and refresh the README references.

- [x] Review terminology science (Wüster's General Theory of Terminology and later schools).
- [x] Review philosophy of definitions (SEP: real/nominal, stipulative/descriptive/explicative, conservativeness & eliminability).
- [x] Review symbol grounding (Harnad; Blondin Massé et al. reachable sets) as the formal basis for roots/kernels.
- [x] Review prerequisite structures in education (Ausubel, Novak's concept maps, knowledge space theory).
- [x] Review knowledge organization systems (semantic networks, WordNet, SKOS, Gene Ontology DAG).
- [x] Review formal mathematics (Metamath) for the axioms/roots analogy.
- [x] Rewrite the README literature review with thematic subsections and a positioning statement.
- [x] Extend "Mentioned materials" (refs 7-22) and "Related materials" (IX-XVI).
- [ ] Review the changes [HUMAN] and update the README accordingly.

## TODO

### 4. [docs] Update the README to reflect last changes

### 5. [devops] Github Action to deploy the package to PyPI

### 6. [devops] Github Action to deploy the documentation to GitHub Pages

## DONE

### 3. [feature] Introduce Definition Groups

Some very simple API to group definitions together. It will be used in the definit-dsa package to group all created definitions into "Data Structures and Algorithms" group that later can be chosen by the user to filter the definitions while learning.

- [x] Add `DefinitionGroup` to the definition data model.
- [x] Serialize/parse groups in the markdown database (`groups.md`).
- [x] Filter `get_index` by group.

### 2. [feature] Introduce definition aliases

When a definition has more than one synonym/alias, we should collect all of them.

- [x] Add aliases to the definition data model.

### 1. [feature] Remove the category (sub-category) concept from the definition data model

The `field` remains the only grouping level of definitions. Definition files are stored directly under `definitions/<field>/`.

- [x] Remove `sub_categories` from `DefinitionKey`.
- [x] Simplify `full_path` to `field/name` and update `from_full_path`.
- [x] Update the markdown database and tests.

## ABANDONED
