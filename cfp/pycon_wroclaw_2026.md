# PyCon Wrocław 2026

## Proposal title

DefinITely, the most boring learning content you will ever see!

## Session type

Talk (~30-40 minutes)

## Abstract

`(between 250 and 4100 characters)`

"Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away." - Antoine de Saint-Exupéry

DefinIT is a terminology structured into a directed acyclic graph (DAG). This open-source project invites community contributions to expand and refine it. DefinIT creates a hierarchy of precise, unambiguous definitions for knowledge fields and academic disciplines. The project aims to create the most boring learning content you will ever see. As the quote above suggests, the best learning content is not about adding more information, but about removing unnecessary complexity. DefinIT is about creating a learning content as simple and concise as possible, without any ambiguity or redundancy.

DefinIT can be understood as a kind of Knowledge Graph. The DAG structure constrains the possible connections between definitions. Directed “is based on” relation is the only kind of connection between definitions. The most fundamental definitions (roots) form the foundation of the hierarchy and are independent of any other terms. They can be clearly described without the use of other definitions. Definition dependencies define the definition level. Over time, the DAG can be updated with more precise and better placed definitions. It is a living, systematically curated terminology for a field of knowledge.

The terminology can be accessed and modified through Python modules. Each definition is represented as a Python object inside a dedicated module. Relations between definitions are created by importing and referencing other definitions. Python, together with an IDE, serves as a user-friendly interface for exploration and manipulation of the terminology. It allows for an easy integration of LLM-based systems to enhance the definitions and their interconnections. Although Python is not necessary for such terminology development, the language features facilitate the process. The use of Python makes the development and contribution processes more efficient and accessible, without extra tooling.

## Description

Exploring DefinIT: Open-source & Python-powered project aiming to create the most boring learning content you will ever see!

## Notes

Demo: https://k4liber.github.io/definit-dsa
