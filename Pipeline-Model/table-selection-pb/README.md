# Identifying data source

The first problem to solve is, given a new question, to identify wheather we have a data source (SQL table) we can use to answer that question.

## Information retrieval approach

In the informnation retrieval approach, you can use all sources of information at your disposal to identify the table that can answer the new question.

Those sources of information are:
* the tables,
* the DOM tree of the pages from which we collected the tables,
* the other questions we already answered.

## ML approach

In the ML approach, you should use only:
* the tables and
* the DOM tree of the pages from which we collected the tables

to identify a data source (table) for the new question.

__See subfolders for specific instructions.__