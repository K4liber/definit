## EuroPython 2026

### Proposal title

Terminology structured into a directed acyclic graph

### Session type

Talk (30 minutes)

### Track

Community Building, Education, Outreach

### Abstract

`(between 250 and 4100 characters)`

DefinIT is a terminology structured into a directed acyclic graph (DAG). This open-source project invites community contributions to expand and refine it. DefinIT creates a hierarchy of precise, unambiguous terms for knowledge fields and academic disciplines, removing ambiguity and redundancy in concept definitions across domains.

Definitions use procedural representations to explain behaviors. Each definition is general. It can be a word or a phrase that represents a broad category or concept rather than a specific instance or entity. For example, car, list, human, country represent general terms. My car, your todo list, Albert Einstein, Poland are singular instances of these general terms or so-called singular terms. DefinIT does not examine singular terms. In an analogy to object-oriented programming, DefinIT examines definitions or classes, but not instances.

DefinIT can also be understood as a kind of Knowledge Graph. The DAG structure constrains the possible connections between definitions. Directed “is based on” relation is the only kind of connection between definitions. The most fundamental definitions (roots) form the foundation of the hierarchy and are independent of any other terms. They can be clearly described without the use of other definitions. Definition dependencies define the definition level. Over time, the DAG can be updated with more precise and better placed definitions. It is a kind of living, systematic creation of a terminology for a specific field.

The terminology can be accessed and modified through Python modules. Each definition is represented as a Python object inside a dedicated module. Relations between definitions are created by importing and referencing other definitions. Structure of the project enables categorization and organization of definitions in a meaningful way. Python, together with an IDE, serves as a user-friendly interface for exploration and manipulation of the terminology. It allows for an easy integration of LLM-based systems to enhance the definitions and their interconnections. Although Python is not necessary for such terminology development, the language features facilitate the process. The use of Python makes the development and contribution processes more efficient and accessible, without extra tooling.

### Outline

`(Describe a rough structure of your proposal, including the time per topic. Please do not include any personally identifiable information here. Please write between 100 and 2000 characters.)`

1. First-principles thinking in defining terms (~10 minutes)
- What is first-principles thinking?
- Bottom-up and divide-and-conquer approaches to knowledge representation.
- The basic building block of knowledge.
- How first-principles thinking can help in creating more precise definitions.

2. Role of directed acyclic graphs in structuring terminology (~5 minutes)
- What is a directed acyclic graph (DAG)?
- DAGs as a differentiator for terminology.
- Significance for efficient curriculum design.
- Implementation challenges.
- How Python facilitates DAG-based terminology.

3. Practical applications and use cases (~10 minutes)
- Data Structures and Algorithms (DSA) curriculum overview.
- Learning new fields.
- Deepening topic understanding.
- Pre-reading/watching exercise for books/lectures.
- Unambiguous expert communication.
- Glossaries for companies/teams/projects.
- LLM training/tuning/input enhancement.

### Why am I qualified to speak about this topic?

`(Descriptions of previous professional or personal projects about your proposal, previous talks or blog posts, or links to repos containing code about your project are all helpful to show this.)`

I've worked on DefinIT for the past year, reviewing existing terminology approaches and identifying improvements. It's the result of my efforts for more structured, precise terminology. See the project README: https://github.com/K4liber/definit/blob/main/README.md.

A DSA curriculum demo is at: https://k4liber.github.io/definit-dsa/.

### Abstract as a short post

`(Short description of your abstract one could tweet. Speaker twitter handles will be added automatically. Please write between 60 and 150 characters.)`

Exploring DefinIT: DAG-structured terminology for precise, unambiguous knowledge representation. Open-source & Python-powered!
