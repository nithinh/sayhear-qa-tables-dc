# sayhear-fall2018

The objective of SayHear is to answer qusetions from tables collected on the web. 

Here are the specific problems we are trying to solve this semester:

1. source-select: pick the source that has the answer - this automatically gives the relation name and data.

2. determine structure of source
  Type: entity instance, key-value pairs
  Classify columns as ordered or not

3. pick the project clause attribute names
  Classify based on question pick the where clause attribute names
  Classify based on likely constants (a sequence labeling problem on the query) and proximity match to value in table

4. pick the order by clause attribute name, direction
  Classify by source and question (source typically uses order by) no query so far has both where and order by, but we shouldn't make this assumption into the model

5. pick the structure of the sql at a high level - e.g., number of attributes, where clause, order by/limit, etc., copy of input to output for proximity 
  Use the probabilities of matches from attribute models, order by models
  Use fact that relation names are ordered, likelihood of an order by as given by prior queries on source generate the query, including perhaps external data like the current year, or location during execution, match the query constants with the data constants

6. Rerun entire pipeline, but obscure the column headers of the extracted data sources

Each problem has a dedicated folder with a more detailed description and the solution we will come up with.