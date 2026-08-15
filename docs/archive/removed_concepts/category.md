# Category (Sub-category)

> **Status:** Removed concept (archived).

## Description

The *category* (also referred to as *sub-category*) concept was an early part of the DefinIT definition data model. In addition to the *field* — the main and only required grouping of definitions — a definition could optionally be assigned one or more sub-categories. Sub-categories formed intermediate grouping levels between the field and the definition itself.

A definition was then identified by a full path of the form:

```
<field>/<sub_category_1>/.../<sub_category_n>/<name>
```

For example, a definition named `set` in the `mathematics` field with the sub-category chain `fundamental` had the full path `mathematics/fundamental/set`.

## Purpose

Sub-categories were intended for:

- Grouping and navigating through related definitions within a field.
- Organizing the markdown database on disk, where each sub-category corresponded to a nested directory (`definitions/<field>/<sub_category>/.../<name>.md`).
- Visualizing category-level DAGs, e.g. all definitions under `mathematics/fundamental`.

## Why it was removed

The concept introduced redundancy and complexity without adding unique information:

- The unique definition identifier (`<field>/<name>`) did not include sub-categories, so they were not part of the definition identity.
- Sub-categories duplicated a role that is better served by the DAG structure itself: the "is based on" relations between definitions already express grouping and hierarchy in a precise, non-redundant way.
- The extra path segments complicated the data model (`DefinitionKey.sub_categories`), the markdown database serialization, and parsing.

After removal, the *field* remains the only grouping level of definitions, and definition files are stored directly under `definitions/<field>/<name>.md`.
