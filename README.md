# DefinIT

## What?

DefinIT is a way of representing knowledge as a hierarchy of precise (unambiguous) definitions (or concepts).

Hierarchy of definitions is a Knowledge Graph[1] with a DAG (directed acyclic graph) structure.

When it comes to knowledge representation type, the definitions have procedural 
representation (explaining the behaviour) and DAGs have structural representation, 
showing the relations between different definitions. 
A relation has always the same type: dependency.

First principles thinking is the act of boiling a process down to the 
fundamental parts that you know are true and building up from there.

The most fundamental concepts make up the very bottom of the hierarchy of definitions. 
The ground level definitions do not have any references to other definitions. 
The are purely describe without usage of other concepts. 

The higher a concept is placed in the hierarchy, the higher level definitions it can reference to. 
A definition can only reference to another definition from a lower level. 

## Why?

The target is to create a knowledge model when one can start learning from 
a foundamental concepts and climbing to higher level of hierarchy. 
Picking a single definition, the descendent nodes indicate what should be 
firstly understood to fully understand the chosen definition.

Over time, the DAG can be updated with more precise and better placed definitions. 
It is a kind of living, systematic knowledge representation of a specific field of knowledge.

Keeping the DAG structure enforce us to build a definition on top of the more general concepts. 
It makes it clear how specific is the concept of our interest. 
Going down in the hierarchy we reach a low level definitions that are more general and fundamental. 
Climping up on the DAG we learn more specific, high level concepts 
(see 'stack' dependencies DAG on Figure 1. as an example).

!['list' dependencies DAG](./dag_stack.png)  
Figure 1. 'stack' dependencies DAG.

The DAG is going to be precise and well arranged knowledge representation. 
It can be used by humans and artificial intelligence systems as well.

## How?

It is a tedious process to create such knowledge structure since one need to have 
a good undestanding of an abstraction level for each definition. 
AI language models can automate some part of the work. 
On the other hand, the creation process allows for a deep understanding 
of the concepts and their unambiguous definitions.

Money is a universal motivator and it could be involved in the creation process as well. 
One of ideas to involve money in the process is inspired by the blockchain technology. 
A single block is an update to the existing knowledge structure (a single commit). 
It is not clear yet who is going to be the judge if a specific update request 
should be accepted or rejected.

One of the ideas is to involve the current stake/knowledge holders 
with something similar to the Proof-of-Stake. 
The benefits for the knowledge update can be splitted between author(s) and reviewer(s). 
Removing part of the content is going to be rewarded as well. 
The current idea for the creation process is following:

- create a PR with proposed changes (additions, removals)
- selection of reviewers based on the current involvment on the content similar to the proposed one
- voting/corrections from the reviewers
- (if voted on) final decision from the project maintainer
- (if accepted) new knowledge coins are generated for the block (commit)
- (if accepted) new knowledge coins split between author(s) and reviewer(s)

The are several issue to be solved before introducing such process:
- what is the minimum amount of contribution (size of a minimum block/commit)?
- should the amount of generated knowledge coins be proportional to the number of signs being changed? 
- how to reduce spam/garbage PRs (there could be too many of bad quality PRs due to AI tool capabilities)?
- how does a transaction of knowledge coins corresponds to the knowledge coin mining?
- Is the mining only triggered on an PR merge or on transactions as well?

## Bibliography

1. "A Common Sense View of Knowledge Graphs", Mike Bergman, https://www.mkbergman.com/2244/a-common-sense-view-of-knowledge-graphs/

2. "What is Knowledge Representation in Artificial Intelligence?", 
Sumeet Bansal, https://www.analytixlabs.co.in/blog/what-is-knowledge-representation-in-artificial-intelligence

3. "Ontology", wikipedia, https://en.wikipedia.org/wiki/Ontology

4. "Theory of categories", wikipedia, https://en.wikipedia.org/wiki/Theory_of_categories

5. "Universal (metaphysics)", wikipedia, https://en.wikipedia.org/wiki/Universal_(metaphysics)

6. "Class (philosophy)", wikipedia, https://en.wikipedia.org/wiki/Class_(philosophy)

7. "KBpedia", https://kbpedia.org/

8. "Charles Sanders Peirce", wikipedia, https://en.wikipedia.org/wiki/Charles_Sanders_Peirce

9. "A Knowledge Representation Practionary", Michael K. Bergman, https://www.mkbergman.com/a-knowledge-representation-practionary/
