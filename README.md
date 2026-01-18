# DefinIT

## What?

DefinIT is a way of representing knowledge as a hierarchy of precise (unambiguous) definitions (or concepts).

Hierarchy of definitions is a Knowledge Graph[1] with a DAG (directed acyclic graph) structure.

When it comes to knowledge representation type, the definitions have procedural 
representation (explaining the behaviour) and DAGs have structural representation, 
showing the relations between different definitions. Dependency is the only kind of relation
between definitions.

The most fundamental concepts make up the very bottom of the hierarchy of definitions. 
The ground level definitions do not have any references to other definitions. 
The are purely describe without usage of other concepts. 

The higher a concept is placed in the hierarchy, the higher level definitions it can reference to. 
A definition can only reference to another definition from a lower level. 

Over time, the DAG can be updated with more precise and better placed definitions. 
It is a kind of living, systematic creation of scientific terminology for a specific field.

## Why?

First principles thinking is the act of boiling a process down to the 
fundamental parts that you know are true and building up from there.
It is a way of understanding the world by breaking down complex problems into their most basic elements.

The original idea behind "DefinIT" was to create a knowledge representation for the field of computer science. 
In the early stages of the field, the importance of a unambiguous expert language has been highlighted. 
In 1954, Grace Hopper, a pioneer in computer programming, wrote a "First Glossary of Programming Terminology"[2].
She was working on first programming language to express operations using English-like statements. The language was later called FLOW-MATIC, originally known as B-0 (Business Language version 0). She recognized the need for a standardized vocabulary
to facilitate communication among programmers and engineers.
This glossary was one of the first attempts to create a common language for computer science,
and it laid the groundwork for future efforts to standardize terminology in the field.

In the 1960s, the Association for Computing Machinery (ACM) established a committee to develop a standardized vocabulary for computer science.
In 1964, the committee produced the "ACM Computing Classification System"[3], which provided a hierarchical classification of computing topics and terms.
The current version (from 2012) of the "ACM Computing Classification System" is widely used in academic publishing and research to categorize computer science literature. It has a tree structure with a set of classes and subclasses that cover various areas of computer science, including algorithms, programming languages, software engineering, and artificial intelligence.

In the 1970s, the IEEE (Institute of Electrical and Electronics Engineers) also recognized the need for standardized terminology in computer science and engineering.
They established the "IEEE Standard Glossary of Software Engineering Terminology"[4], which provided definitions for key terms in software engineering.

In the 1980s and 1990s, as computer science and technology continued to evolve rapidly,
there were numerous efforts to create standardized vocabularies and glossaries in various subfields of computer science.
For example, the Object Management Group (OMG) developed the Unified Modeling Language (UML)[5],
which included a standardized set of terms and symbols for modeling software systems.
In the 2000s and beyond, the rise of the internet and online resources led to the creation of numerous glossaries and dictionaries for computer science terminology.
Many universities and organizations began to publish their own glossaries and dictionaries,
and online platforms like Wikipedia became valuable resources for finding definitions and explanations of computer science terms.

Then why do we need "DefinIT"? What new thing does it bring to the current state of affairs? The target is to build a knowledge model when one can start learning from 
foundamental concepts and easily climb to higher levels in hierarchy. 
Picking a single definition, the descendent nodes indicate what should be 
firstly understood to fully understand the chosen definition.

Keeping the DAG structure enforce us to build a definition on top of the more general concepts. 
It makes it clear how specific is the concept of our interest. 
Going down in the hierarchy we reach a low level definitions that are more general and fundamental. 
Climping up on the DAG we learn more specific, high level concepts 
(see 'trie' dependencies DAG on Figure 1. as an example).

!['trie' dependencies DAG](./dag_definition_trie.png)  
Figure 1. 'trie' dependencies DAG.

The DAG is going to be precise and well arranged knowledge representation. 
It can be used by humans for example to learn a new field of knowledge.
Specyfing an unambiguous language that experts in a field use to communicate with each other 
will improve the quality and clarity of the communication.
It can also be used by LLMs (Language Models) as a solid training/tuning data or part of prompting.

If one would like to learn a specific part of the knowledge,
the "Track" concept can be used. Figure 2-3. show DAG representation of track's definitions.

!['data_structures' DAG](./dag_track_data_structures.png)  
Figure 2. Circular DAG visualization of 'data_structures' track.

!['algorithms' DAG](./dag_track_algorithms.png)  
Figure 3. Circular DAG visualization of 'algorithms' track.

## How?

It is a tedious process to create such knowledge structure since one need to have 
a good undestanding of an abstraction level for each definition. 
AI language models can automate some part of the work. 
On the other hand, the creation process allows for a deep understanding 
of the concepts and their unambiguous definitions.

## Mentioned materials

1. "A Common Sense View of Knowledge Graphs", Mike Bergman, https://www.mkbergman.com/2244/a-common-sense-view-of-knowledge-graphs/

2. "Report to ACM: First Glossary of Programming Terminology", Grace Hopper, https://archive.computerhistory.org/resources/text/Knuth_Don_X4100/PDF_index/k-8-pdf/k-8-u2741-2-ACM-Glossary.pdf

3. "ACM Computing Classification System", Association for Computing Machinery, https://dl.acm.org/ccs

4. "IEEE Standard Glossary of Software Engineering Terminology", IEEE, https://ieeexplore.ieee.org/document/159342

5. "Unified Modeling Language", Object Management Group, https://www.omg.org/spec/UML

## Related materials

I. "What is Knowledge Representation in Artificial Intelligence?", 
Sumeet Bansal, https://www.analytixlabs.co.in/blog/what-is-knowledge-representation-in-artificial-intelligence

II. "Ontology", wikipedia, https://en.wikipedia.org/wiki/Ontology

III. "Theory of categories", wikipedia, https://en.wikipedia.org/wiki/Theory_of_categories

IV. "Universal (metaphysics)", wikipedia, https://en.wikipedia.org/wiki/Universal_(metaphysics)

V. "Class (philosophy)", wikipedia, https://en.wikipedia.org/wiki/Class_(philosophy)

VI. "KBpedia", https://kbpedia.org/

VII. "Charles Sanders Peirce", wikipedia, https://en.wikipedia.org/wiki/Charles_Sanders_Peirce

VIII. "A Knowledge Representation Practionary", Michael K. Bergman, https://www.mkbergman.com/a-knowledge-representation-practionary/

## Installation

`uv sync --extra dev`

## Build

`uv build`

## Deploy

`uv publish --token <pypi_token>`
