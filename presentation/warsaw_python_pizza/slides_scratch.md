# Knowledge representation for efficient learning and communication

- Author: Jan Bielecki
- Event: Warsaw Python Pizza
- Date: 20260509

# Gamification of a learning process

- Its fun to create games.
- Its fulfilling to make something useful.
- Duolingo as an example of gamification in learning.

# Different learning platforms

- Codecademy
- Leetcode
- Brilliant
- Coursera
- edX
- Khan Academy
- Udacity

- Some of the platforms have a gamification element to enhance the learning experience.

# Let's create the universal platform!

- standards.png

# Basic building block of a knowledge representation

- What is the smallest unit of knowledge that can be checked as "learned" and we can move forward to the next one?

# First principles thinking

- Divide and conquer.

# Definition as the smallest unit of knowledge

- Examples of definitions.
- Literature overview.
-- "First Glossary of Programming Terminology"
-- "IEEE Standard Glossary of Software Engineering Terminology"
-- UML, Internet, Wikipedia ...

# Definition properties

- Key (definition name, field Why? Two same names can exist in different fields.)
- Value (content, dependencies: definitions can rely on other definitions)

# Structure of definitions

- DAG.

# Using Python as a platform for creating and managing knowledge representations

- Strict format for definitions
- Github Copilot helps with the content creation.
- Tests, visualizations.
- Serializers.

# POC - Data Structures and Algorithms (DSA)

- https://k4liber.github.io/definit-dsa/

# Why it exists?

- Efficient learning - by breaking down complex topics into smaller, manageable units.
- DAG structure implies where to start.
-- from the low-level definitions.
-- from the set of descendant definitions of a given definition.
- A living, qualitative and structured glossary for any field of knowledge.
- Improved quality and clarity of training data for machine learning models.

# What is wrong with such approach?

- A lot of effort to create a qualitative knowledge representation.
- Who decides a definition content and dependencies?
- DAG structure is an assumption that all knowledge can be represented in a hierarchical manner.
- "Brain rot" content is more addictive then a well-structured knowledge representation.
- "In theory, there is no difference between theory and practice. But in practice, there is."~Benjamin Brewster
-- The brain learns most effectively through active, deliberate practice, and a static knowledge representation may not provide the necessary engagement and feedback for optimal learning.

# What's next?

- Explore more high-level concepts (uv, compilation, architecture).
- Creating a more engaging learning experience (questions, active and deliberate practice, tasks).
