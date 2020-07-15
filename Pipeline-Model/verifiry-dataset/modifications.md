# Modifications made while manually verifying the dataset

## Analysis of modifications

For the train set:

|                                                   |                                              | Total examples | IDs of examples                                    |
|---------------------------------------------------|----------------------------------------------|----------------|----------------------------------------------------|
| __Made modifications to the example__ <sup>1</sup>                                                                                                                     |
| Modified uery                                     | Modification in SELECT clause                | 8              | 18, 21, 60, 80, 98, 99, 148, 168                   |
|                                                   | Modification in WHERE clause                 | 1              | 27                                                 |
|                                                   | Replaced * in query                          | 1              | 37                                                 |
|                                                   | Replaced SQL operator in WHERE clause this ~ | 4              | 92, 157, 182, 223                                  |
|                                                   | Replaced table name                          | 1              | 163                                                |
|                                                   | Total                                        | 13             |                                                    |
| Modified expected answer                          |                                              | 11             | 37, 38, 61, 106, 114, 150, 156, 188, 198, 207, 225 |
| ___Total examples modified___                     |                                              | ___24 (10%)___ |                                                    |
| __Other notes__                                                                                                                                                        |
| Query without ~ operator                          |                                              | 2              | 33, 52                                             |
| Returned answer is too long (non exhaustive list) |                                              | 11             | 42, 58, 79, 94, 131, 143, 193, 213, 214, 218, 228  |

<sup>1</sup> 2 different kinds of modifications:
* Query did not exectue without modification
* Query did execute without modification but we obtain a better answer by modifying the query.

I made other comments for individul examples that are not represented in this table. The Details below, examples with __ID in bold__.

## Details train set

_I may have made some other modifications that I forgot to list here..._

_Also note that I did NOT check the long answer. But I glanced at a few of them, and some are not good. e.g. #207, long answer does not correspond to short answer._

#18:
Added column in select. Changed the expected answer so that it matches with the question / table... even though the answer is not as good anymore.

#21:
Added column in select.

#27:
Change query from
`SELECT "Address", "City" FROM "WilliWaste" WHERE "Name" ~ "Willimantic Waste"`
to
`SELECT "Address", "City" FROM "WilliWaste" WHERE "Name" ~ "Willimantic Waste" AND "Description" ~ "waste"`
to because first query returns 2 results...

#__28__: 
Query does not make sense. We don't know from the question what character to select.

Question: Who s the actor from the Matrix

Query:
`SELECT "Actor" FROM "Table_1" WHERE "Character" ~ "Agent Smith"`

Isn't Neo the most famous character from this movie?
I tried with "Matrix" instead of "Agent Smith" and it does not work.
I did NOT validate this example even though, given the query, it returns the expected answer.

#33:
The SQL query does not use the ~ operator. Shouldn't it?


Question: Siri  what was the best video game of 2017

`SQL: SELECT "Game" FROM "Table_1" WHERE "Rank" = 1`

(Example validated anyway)

#37:
Changed short answer. It had nothing in common with the table!
Also changed the query...

#38:
Modified expected short answer. Also had elements that are not in the selected cell.

#52: Does not have the ~ operator.

We also have several examples where the expected answer is a span of the selected cell. e.g. # 42. (I considered those examples as valid here... but google would do a better job at answering some of those questions - e.g. #42)

#58: 
Good answer but waaaay to long. Need to cut it.

#60:
Changed SQL from `SELECT "begins" FROM "e3_2018"` to `SELECT "begins", "ends" FROM "e3_2018"` to get expected answer.

#61: 
Changed expected answer from `spy novelist` to `writer, spy novelist, CIA, officer` so that it mathces what you get from the table (and the long answer as well).

#72:
Table with duplicate items.

#79: 
Gives a super long answer detailing the water inake for all age/gender, when the expected answer is just `between 0.7 and 3.8 liters`. Validated anyway...

#80:
Changed the SQL from `SELECT "Performer", "Year" FROM "Table_1" ORDER BY "Year" DESC LIMIT 1` to `SELECT "Performer" FROM "Table_1" ORDER BY "Year" DESC LIMIT 1` so that the answer returned matches exactly the expected answer.

#__88__:
Not really a table but a list...

#92:
Replaced `LIKE` with `~` in query. 

#94:
Answer would be a span of cell.

#98:
Replaced `SELECT * FROM oatmeal WHERE "benefits" ~ "Asthma"` with `SELECT "benefits" FROM oatmeal WHERE "benefits" ~ "Asthma"` to avoid returning a URL in the answer.

#99:
Replaced `SELECT "Full-nane" FROM "Computer_Science:_Abbreviations" WHERE "Abbreviation" ~ "USB"` with `SELECT "Full_Name" FROM "Computer_Science:_Abbreviations" WHERE "Abbreviation" ~ "USB"` (labeler's nistake).

#106:
Changed the expected answer from `transfers power` to `extends the range of a power source` so that it actually corresponds to something in the table.

#114: 
Changed expected answer from `august 13, 1959;november 21, 1964` to `august 13, 1959` so that it corresponds better to the query (we have no construction end date in the table... the labeler took the open date).

#131:
Expected answer is some kind of summary of returned answer.

#143:
Expected answer is a span of cell.

#__146__:
Given question `Alexa  when is taylor swift coming to dallas`, changed:
`"short_a": "oct. 6, 2018", 
 "long_a": "taylor swift will be playing next in arlington, tx on october 6, 2018", 
`
to:
`"short_a": "False", 
"long_a": "taylor swift will not be coming to dallas.", `
We still don't get the right answer as word2vec allows replacement of "dallas" by "Houston".

#148:
Changed SQL from `SELECT "Max Size ~1" FROM "horned nerite snail"` to `SELECT "Max_Size_~1" FROM "Horned_Nerite_Snail"` AND pre-processed CSVs to get ride of double quotes within column headers.

#150:
Slightly changed functioning of ~ operator...
Also changed expected answer from `https://en.wikipedia.org/wiki/list_of_cryptocurrencies` (did not make sense) to `The first decentralized ledger currency. Cryptocurrency with the most famous, popular, notable and highest market capitalization.`

#__152__:
Validated the example, even though the expected answer is `yes` and we actually return `shadow`...

#156:
Changed expected answer from `$13,499` (does not appear in the table) to `$27,775`.

#157:
Replaced `SELECT "Rank" FROM "Table_1" WHERE "Team" LIKE "Steeler"` (did not work - the word in the table is Steelers not Steeler) with `SELECT "Rank" FROM "Table_1" WHERE "Team" ~ "Steeler"`.

#__158__:
Expected answer is `bmi>40`, but we can only retreive from the table `>40`... Validated anyway.

#163:
Changed `SELECT "time:" FROM "how_to_watch_super_bowl_52"` with `SELECT "time:" FROM "Superbowl_2018"` (actual name of the table).

#168:
Changed `SELECT "Antonyms" FROM "table_1"` with `SELECT "Synonyms" FROM "table_1"` since the question is about synonyms.

#__169__:
Validated example, but I think the given answer does not really answer the question. Question is `What is AP BIo about` and answer is `Comedy`.

#182: 
Changed `LIKE` with `~` (query did not work with LIKE).

#188:
Changed expected answer from `10-jul` to `7` (question: `What did Cloverfield get on IMDB` --> we select a rating, it seems to make sense).

#193:
Validated, but expected answer is a sum up of the answer from the table.

#198:
Changed expected answer from `no 1 april 1` to `april 1` (for question `When is Easter 2018`)

#201:
Corrected `LIMT_1` --> `LIMIT_1`

#207:
Changed expected answer from `the closest place is maui` ("maui" does nit appear in the table) with a span of a cell of the table (the cell that the SQL query returns... ): `the first and best place to experience them is in hawai`

#213
Answer is a span of the cell (long text in cell).

#214:
Same.

#218:
Same.

#223:
Query had no ~ operator (and for some reason did not execute with `LIKE`. 
Changed `SELECT "From_Euro_to_Currency" FROM "Euro_conversion" WHERE "Currency" LIKE "US Dollars"` to `SELECT "From_Euro_to_Currency" FROM "Euro_conversion" WHERE "Currency" ~ "US Dollars"`

#225:
Changed extected answer (`10200 baltimore ave` is not in the table) to `beaverdam and sheep roads, beltsville, md 20705`.

#228:
Answer is a span of the cell (long text in cell).

## Details test set

#238: 
Changed `DESENDING` with `ASCENDING`.

#240: 
Replaced `SELECT [...] ORDER BY ASCENDING "Ranking" LIMIT_1` with `SELECT [...] ORDER BY  "Ranking" ASCENDING LIMIT_1`. 

#245
Replaced `LIKE` with `~`.

#247:
Extrat inforation in retrieved answer.

#249:
Modified expected answer (Got ride of `friendly with people needs a firm leader` --> dit not make sense as a beginning of answer, and was not part of cell about differences - question `What s the difference between a Siberian Husky and a Malamute`)

#250:
Modified query to use `~` operator: `SELECT "Ingredients" FROM "Table_1" WHERE "Name" LIKE "%%Three%Ingredient%Peanut%Butter%Cookie%"` --> `SELECT "Ingredients" FROM "Table_1" WHERE "Name" ~ "3 ingredient peanut butter cookies"`

#252: 
Answer has extrat information.

#255:
Retrieved answer has extrat information (a lot! Long text).

#257:
Changed it so that i has ~ operator, but does not work with ~ operator.

#261: 
Answer would need further reasoning (validated anyway): 
* question = `Alexa  Did the Groundhog see his shadow in 2018`
* expected answer: `yes`
* predicted answer: `[('Shadow at 7:20 AM; 9\xc2\xba cloudy skies with -7\xc2\xba Wind Chill.',)]`

#268 (REJECTED)
Original:
* question: `Alexa  who is the actress that plays Sheldon s mother`
* query: `SELECT "Portrayed_by" FROM "Character_Appearances" WHERE "Character" LIKE "%%Mary Cooper%"`
* problem: no ~ operator and extrat knowledge is necessary to translate question to SQL query (Sheldon's mother --? Mary Cooper)
Modification:
* query: `SELECT "Portrayed_by" FROM "Character_Appearances" WHERE "Character" ~ "Sheldon s mother"`
--> Word vectors wrong mapping. 

#274:
Changed `SELECT "location" FROM "Cheesecake_Factory_at_Barton_Creek_Mall"` to `SELECT "address" FROM "Cheesecake_Factory_at_Barton_Creek_Mall"`

#277:
Changed `SELECT "_release_date_" FROM "Gosford_Park"` to `SELECT "release_date" FROM "Gosford_Park"`

#282:
Modified expected answer:
* question: `What is the superbowl being televised on channel in new england`
* expected anwer: `nbc 6:30pm` ---> `nbc`

#289:
Replace `LIKE` with `~`.

#294:
Same.






