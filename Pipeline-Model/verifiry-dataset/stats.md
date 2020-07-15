# Stats on verified dataset

## Analysis of not working examples (train set)

Computed with `verified_dataset_stats.py`, see [README](https://github.com/CMU-RERC-APT/sayhear-fall2018/blob/lucile/projection/verifiry_dataset/README.md) for details.

	STATS:

	238 examples have been verified:
	191 (80.25%) are valid (working),
	47 (19.75%) are not.

	If we use only word vector similarities (strategy 4) and none of the other heuristics we usually apply bfore using similarity scores:
	238 examples have been verified:
	182 (76.47%) are valid (working),
	56 (23.53%) are not.


Classification for examples not working:

| Problem                                            | # of examples affected | Examples' IDs                                                                             |
|----------------------------------------------------|------------------------|-------------------------------------------------------------------------------------------|
| Word vectors don't work                            | 15                     | 6, 9, 26, 90, 92, 111, 145<sup>1</sup>, 146, 209, 219 [91, 93, 101, 185, 206]<sup>2</sup> |
| Table too complexe for word vectors                | 5                      | 41, 48, 192, 196, 214,                                                                    |
| Table needs further pre processing (e.g. for date) | 4                      | 17, 35, 54, 123                                                                           |
| Answer retrieved but requires further reasoning    | 2                      | 34, 107                                                                                   |
| _Badly transposed table_                           | _9_                    | _63, 100, 115, 118, 125, 149, 154, 197, 221_                                              |
| "external" operator                                | 2                      | 96, 108                                                                                   |
| Broken examples                                    | 10                     | 12, 28, 68, 87, 95, 138, 151, 176, 211, 222                                               |

<sup>1</sup> We are looking for an exact match to city "Dallas" in the table and word2vec returns the closest value ("Huston").

<sup>2</sup> "a" and "1" are not related in word2vec.

## Details train set

	Examples not working:

	6
	Question: Alexa  what is the best ergonomic mouse
	SQL: SELECT "mouses" FROM Best_Ergonomic_Mouse WHERE "keys" ~ "best"
	Expected answer: logitech marathon mouse m705
	Note: Is expected to select from "our pick" column but best maps to "Also great"

	9
	Question: how often to wash sweater
	SQL: SELECT "Duration" FROM "Table_1" WHERE "Type" ~ "sweater"
	Expected answer: 5 wears
	Note: Bad mapping. Ideal solution is to look for sweater in the table and focus on that row.

	12
	Question: how much does an average golden retriever weigh
	SQL: SELECT Average FROM "Table_1" WHERE "Age" ~ "average"
	Expected answer: 70 lbs
	Note: The query returns the good result but obviously by luck.

	17
	Question: Who will be in the 2018 super bowl
	SQL: SELECT "Team_one", "Team_two" FROM Super_Bowl ORDER_BY "Season" DESCENDING LIMIT_1;
	Expected answer: new england patriots, philadelphia eagles
	Note: The order by column has text (roman numbers) so it cannot work unless we do further preprocessing.

	26
	Question: which is the current president of United States
	SQL: SELECT "President" FROM US_Presidents WHERE "President" ~ "current president"
	Expected answer: donald trump
	Note: I have no idea why the closest word2vec to "current president" is "Ulysses S. Grant". It does not work with just "president" either.

	28
	Question: Who s the actor from the Matrix
	SQL: SELECT "Actor" FROM "Table_1" WHERE "Character" LIKE "%%Agent Smith%"
	Expected answer: hugo weaving
	Note: Query returns the expected answer but just does not make sense.

	34
	Question: Is Jefe a Jewish name
	SQL: SELECT "Origin" from "Definition_of_Jefe" WHERE "Word" ~ "Jefe"
	Expected answer: no
	Note: requires further reasonning to obtain short answer from table...

	35
	Question: Alexa  what is the name of the last Harry Potter movie
	SQL: SELECT "Motion_picture" FROM Harry_Potter_Movies ORDER_BY "Release_date" DESCENDING LIMIT_1
	Expected answer: harry potter and the deathly hallows part 2
	Note: Requires preprocessing of CSV table to produce accurate SQL table with dates (for the ORDER BY) instead of simple text --> First, would need to recognize column as containing dates.

	41
	Question: How do I get a refund for Social Security Tax erroneously withheld
	SQL: SELECT "Product_Number" FROM "Table_1" WHERE "Title" ~ "refund"
	Expected answer: form 843
	Note: I am not even sure how the labeler knew which one to select. I don't see any simple way to make the query work.

	48
	Question: Siri  when are you able to file federal taxes for 2018
	SQL: SELECT "2018_Deadline" FROM "Table_1" WHERE "Activity" ~ "file"
	Expected answer: 29-jan
	Note: Can't see how to make this one work. Requires world knowledge.

	54
	Question: Alexa  is there a Jewish holiday on January 31st
	SQL: SELECT "Name" FROM "Table_1" WHERE "DATE" LIKE "January 31st"
	Expected answer: tu bishvat
	Note: "January 31st" appears as "Jan 31st" in the table. Would require more preprocessing of the table to work.

	63
	Question: what are the feature of nokia 8
	SQL: SELECT "Features" FROM "table_1"
	Expected answer: geo-tagging, touch focus, face detection, hdr, panorama
	Note: Table has been badly transposed. Need for correction.

	68
	Question: Alexa  what day is easter on this year
	SQL: SELECT "Date" FROM Easter_Info ORDER BY "Year" DESCENDING LIMIT_1
	Expected answer: april 1st
	Note: The newsql was written with the assumption that the table would stop at the current year, which is not the case.

	87
	Question: How long do dogs live
	SQL: SELECT "Value" FROM Dog_Info WHERE "Property" ~ "long"
	Expected answer: 10-13 years
	Note: Table is about dogs but does not correspond to the SQL query that has been written.

	90
	Question: Alexa  what is the distance between England and the US
	SQL: SELECT "Distance_(mi)" from "Distance_from_United_States_to_Other_Countries" WHERE "Country" ~ "England"
	Expected answer: 4244 miles
	Note: ~ operator does not work. For some reason, "england" maps to "Distance from Spain to United States" rather that to "united kingdom"

	91
	Question: Alexa  how many ounces are in a gallon
	SQL: SELECT "Ounce" FROM "Table_1" WHERE "Gallon" LIKE "a"
	Expected answer: 128 ounces
	Note: ~ operator does not work. Letter "a" cannot map to 1.

	92
	Question: Alexa  what is the best ergonomic keyboard
	SQL: SELECT "keyboards" FROM Best_Ergonomic_Keyboard WHERE "keys" ~ "best"
	Expected answer: microsoft sculpt ergo
	Note: Same problem as with #6. We expect "best" to map to "our pick" but of course it maps to "also great".

	93
	Question: Alexa  how many feet are in a meter
	SQL: SELECT "Feet" FROM "Table_1" WHERE "Meters" ~ "a"
	Expected answer: 3.28084 ft
	Note: Character "a" cannot map to 1. Would need special rules...which would seem like cheating.

	95
	Question: Alexa  is there a passively cooled GTX 1060
	SQL: SELECT Count ( "Product_Name" ) FROM Graphics_Card_Cooler WHERE "NVIDIA" LIKE "%%GTX%" AND "NVIDIA" LIKE "%%1060%";
	Expected answer: yes. by using accelero s3
	Note: Does not have a ~ operator. Query would give a better result by just returning "product name" and not "count(product name" as the expected answer is yes/no + the name of a product, not a number.

	96
	Question: Alexa  when was Groundhog Day released
	SQL: SELECT "Release_date", "Country" FROM "Groundhog_Day_Release_Info" WHERE "Country" ~ external ( "country_location" )
	Expected answer: 2/4/1993, 2/13/1993
	Note: 'external' is another invented operator that I don't know how to implement. Should we just simplify for now and replace with "USA"? ---> Anthony's note about external: interesting - requires external country information, invent syntax where external(attribute) provides the persons information. external('country location'), external('date'), external('city location') - external words backward from the data to retrieve the relevant type of data. so if location column is countries supply usa (or whatever is relevant), if location is us cities, supply pittsburgh (or whatever is relevant)

	100
	Question: Alexa  how much does an iPhone X cost
	SQL: SELECT "Price" FROM "table_1"
	Expected answer: $999, $1149
	Note: badly transposed table.

	101
	Question: Alexa  how many pounds are in a stone
	SQL: SELECT "Pound" FROM Pound_To_Stone_Table WHERE "Stone" ~ "a"
	Expected answer: 14
	Note: Again, "a' cannot map to 1.

	107
	Question: How much does Straight Talk cell phone service cost
	SQL: SELECT * FROM phone_networks WHERE "network" ~ "Straight_Talk"
	Expected answer: 30-55$
	Note: requires further processing of the answer returned by the query (list of prices ---> we want an range).

	108
	Question: how much does amazon prime cost
	SQL: SELECT "Annual_Price" from "Amazon_Prime_Rates" WHERE "Country" ~ "external ( "country_location" ) "
	Expected answer: $99
	Note: External operator pb.

	111
	Question: Who played Flash in The Flash
	SQL: SELECT "Actor" FROM "Table_1" WHERE "Character" ~ "Flash"
	Expected answer: grant gustin
	Note: Also returns the name of the actor who played "kid flash" ......... Actually that may be the right full answer. I don't know.

	115
	Question: what are the feature of Samsung Galaxy Note 8  Midnight Black
	SQL: SELECT "Features" FROM "table_1"
	Expected answer: geo-tagging, simultaneous 4k video and 9mp image recording, touch focus, face/smile detection, auto hdr, panorama
	Note: Badly transposed table.

	118
	Question: Alexa  what is the Meredith Corporation
	SQL: SELECT "Products" FROM "meredith_corporation"
	Expected answer: media, newspapers; magazines; television; educational services; websites
	Note: table badly transposed.

	123
	Question: which is the most common language in the world
	SQL: SELECT "Language" FROM Native_Speaker_Ranking ORDER_BY "Rank" ASCENDING LIMIT_1
	Expected answer: mandarin
	Note: Would require that the Rank column contains INT and not TEXT? not sure.

	125
	Question: When does Red Dead Redemption 2 release
	SQL: SELECT "Release" FROM "table_1"
	Expected answer: 26-oct-18
	Note: table badly transposed

	138
	Question: Alexa  who became president after John Kennedy
	SQL: SELECT "President" FROM "List_of_Presidents_of_the_United_States" WHERE "Number" > ( SELECT "Number" FROM "List_of_Presidents_of_the_United_States" WHERE "President" ~ "John_Kennedy" ) ) ORDER_BY "Number" ASCENDING LIMIT_1
	Expected answer: lyndon b johnson
	Note: Too complicated.

	145
	Question: Alexa  when is taylor swift coming to dallas
	SQL: SELECT "Date", "Market" FROM Taylor_Swift WHERE "Market" ~ "Dallas";
	Expected answer: False
	Note: In this particular case we are looking only for exact match.

	146
	Question: when can i get masters on amazon turk
	SQL: SELECT "Answer" FROM "MTurk_Master_Worker" WHERE "Question" ~ "masters"
	Expected answer: mechanical turk automatically grants the masters qualification based on statistical models that analyze worker performance based on several requester-provided and marketplace data points. those who score the highest across these key data points are granted the masters qualification. workers cannot apply for this status. to receive the masters qualification, try tasks across a variety of requesters and consistently submit a lot of high quality work.
	Note: Here we retreive 2 cells, the second one is about master qualification being revoked. We want only the 1st cell retreived.

	149
	Question: Alexa  when is the premier of the Black Panther movie
	SQL: SELECT "Release_Date" FROM "black_panther"
	Expected answer: february 16, 2018
	Note: Table badly transposed.

	151
	Question: Alexa  what are the vegan pizza spots in St  Charles
	SQL: SELECT "Name" FROM St_Charles_Vegan WHERE "Category_List_Text" ~ "vegan" AND "Snippet" ~ "Pizza"
	Expected answer: frida's
	Note: This example is broken. The question asks for something vegan, but the labeler returned a vegetarian restaurant. There is no vegan pizza place in this table...

	154
	Question: where is kennesaw georgia
	SQL: SELECT "County;_County" FROM "table_1"
	Expected answer: cobb
	Note: Badly transposed table.

	176
	Question: local antiques stores
	SQL: SELECT "Biz_Name_Click" FROM "Table_1" WHERE "Search_Result" ~ "1."
	Expected answer: west end antiques mall
	Note: Changed `LIKE` with `~`. But it does not seem like a good ~ query: `SELECT "Biz_Name_Click" FROM "Table_1" WHERE "Search_Result" ~ "1."` `1` never appears in the question (`local antiques stores`), and the query does not return the expected answer if we change `1.` with just `1`.  Besides, the question asks for stores (plural) but we return only one name. So I reject this example.

	185
	Question: Alexa  how many seconds are there in a year
	SQL: SELECT "Seconds" FROM "Table_1" WHERE "Years" ~ a
	Expected answer: 31,556,952
	Note: "a" is not close to "1" with word vectors.

	192
	Question: Alexa  where can I but Fallout
	SQL: SELECT "Store" FROM Fallout_Search_Result WHERE "Product" LIKE "%%Fallout 4%" LIMIT 1
	Expected answer: from 2 stores
	Note: The entire table is about fallout. I don't see how we can select the right row.

	196
	Question: what day are taxes due in 2018
	SQL: SELECT "Deadline" FROM "Table_1" WHERE "Type_of_Income_Tax_Return" ~ "taxes"
	Expected answer: 17-apr-18
	Note: All rows are about taxes, so word vectors don't allow us to select the right one. (the right one is the first one...)

	197
	Question: what are the feature of iphone 7plus
	SQL: SELECT "Features" FROM "table_1"
	Expected answer: geo-tagging, simultaneous 4k video and 8mp image recording, touch focus, face/smile detection, hdr (photo/panorama)
	Note: badly transposed table

	206
	Question: What is a labor camp
	SQL: SELECT "Definition" from "Labor_Camp_Definitions" WHERE "Number" ~ "a"
	Expected answer: a penal colony where inmates are forced to work.
	Note: No correspondance between "1" and "a" un pre trained word2vec.

	209
	Question: What is the transatlantic luggage allowance with Aer Lingus
	SQL: SELECT "Weight" FROM "Table_1" WHERE "Baggage_Type" ~ "luggage"
	Expected answer: 23kg
	Note: Word2vec maps "luggage" to "cabin baggage" instead of "checked baggage"

	211
	Question: What is the weather in Ingleside  Il
	SQL: SELECT "Hight", "Low" FROM Ingleside_Il_Weather WHERE "Day" LIKE "%%Tonight%"
	Expected answer: 40 degrees
	Note: Does not use the ~ operator

	214
	Question: What is a normal heart rate
	SQL: SELECT "Normal_heart_rate_(bpm)", "Age" FROM "Table_1"
	Expected answer: 70-190 for babies, 60-100 for adults
	Note: Basicallt retrieves the whole table. Would need a sum up method to get a better answer... Unless we consider it good enough?

	219
	Question: Alexa  what s the kilometer to mile conversion
	SQL: SELECT "Miles" FROM "Table_1" WHERE "Kilometers" ~ "kilometer"
	Expected answer: 0.6214 mi
	Note: For some reason word2vec map "kilometer" to "10 km" instead of "1 km"

	221
	Question: What is the fertility rate in iran
	SQL: SELECT "Fertility_rate,_total_(births_per_woman)" FROM "Iran_-_Health"
	Expected answer: 1.69
	Note: Badly transposed tables

	222
	Question: what happened during the recent oscars 2018
	SQL: SELECT "Best_Picture;_Best_Picture" FROM "table_1"
	Expected answer: shape of water
	Note: This is obviously a broken example.

## Details test set

	239
	Question: What day is Chinese New Years
	SQL: SELECT "Dates" FROM "Table_1" ORDER_BY "Years" DESCENDING LIMIT_1
	Expected answer: feb. 16, 2018 (friday)
	Note: Assumption that the last year of the table is the current year. It is not the case.

	241
	Question: Alexa  how many stars are in the Milky Way Galaxy
	SQL: SELECT "Number_of_stars" FROM "Table_1"
	Expected answer: 100–400 billion (2.5 × 1011 ± 1.5 × 1011)[6][7][8]
	Note: Badly transposed table.

	248
	Question: Alexa  what is Google Adsense
	SQL: SELECT "Type" FROM "Table_1"
	Expected answer: online advertising
	Note: Badly transposed table.

	256
	Question: Alexa what is the price of jio 4G Net pack 3Gb per day month Pack
	SQL: SELECT "price" FROM jio WHERE "Plan_Heading" ~ "3Gb per day"
	Expected answer: 299
	Note: Word vectors pb. For some reason "3Gb per day" maps to "1 GB/DAY 1.5 GB/DAY PACKS" instead of "2 GB/DAY 3 GB/DAY PACKS"

	257
	Question: Where do I find the best condoms in Miami
	SQL: SELECT "Name" FROM "Table_1" WHERE "Search_Result" ~ "best"
	Expected answer: happy supermarket
	Note: Word vector problem. "best" does not map to serach result #1 as expected. (Maps to "Ad").

	260
	Question: Alexa  what year did the knights Templar exist
	SQL: SELECT "max(year)", "min(year)" FROM TemplarTimePeriod
	Expected answer: 1119-1314
	Note: Wrong query preprocessing.

	263
	Question: Alexa  how old are the pyramids
	SQL: SELECT "Date_of_Construction" from "Wonders" WHERE "Name" ~ "pyramid"
	Expected answer: about 4500 years old
	Note: Needs further reasoning.

	266
	Question: When are taxes due
	SQL: SELECT "Date" FROM US_Tax_Day ORDER_BY "Year" DESCENDING LIMIT_1
	Expected answer: apr 17
	Note: Again, assumption that last year of table is current year. It is not the case.

	267
	Question: Alexa  does Swagbucks work
	SQL: SELECT "VERDICT:_LEGIT" FROM "Swagbucks"
	Expected answer: legit
	Note: Example was working but I don't understand the question / the answer. I guess maybe the webpage was giving context? --> with hust this table I think it does not make sense so I reject this example.

	268
	Question: Alexa  who is the actress that plays Sheldon s mother
	SQL: SELECT "Portrayed_by" FROM "Character_Appearances" WHERE "Character" ~ "Sheldon s mother";
	Expected answer: laurie metcalf
	Note: Word vector wrong mapping.

	269
	Question: What time does Best Buy close
	SQL: SELECT "Close" from "Store_Hours" WHERE "Weekday" ~ "external ( "day_of_week" ) "
	Expected answer: 9:00 pm
	Note: Uses "external" operator.

	270
	Question: Alexa  what s the screen resolution of Iphone X
	SQL: SELECT "Resolution" FROM "Table_1"
	Expected answer: 5.8-inch (diagonal)
	Note: Table badly transposed

	273
	Question: Does a loan from my 401k count as taxable income
	SQL: SELECT "401kloan" FROM loans WHERE "info" ~ "taxable_income"
	Expected answer: no
	Note: Note sure if answer requires further reasoning or if we have a wrong mapping with wrd2vec.

	287
	Question: Are there any science jobs in Rochester  NY
	SQL: SELECT COUNT ( Title ) FROM "Table_1" WHERE "Location" ~ "Rochester NY"
	Expected answer: 22
	Note: Question: "Rochester NY" table: "Rochester, NY". The "," breaks the example...

	290
	Question: When does Squashbusters gym close
	SQL: SELECT "Close_Time" from "SquashBusters_Hours" WHERE "Day" ~ "external ( "day_of_week" ) "
	Expected answer: 9:15 pm
	Note: "external" operator

	292
	Question: Alexa  what is my weight in kilograms
	SQL: SELECT "Kilograms" FROM "Table_1" WHERE "Pounds" = "100.00lb";
	Expected answer: 65 kilograms
	Note: Broken example. Turker asks for his weight in kg. labeler took it as a conversion question for lb to kg, but no weight in lb is given in the question.

	295
	Question: How many states have signed onto the 270 compact
	SQL: SELECT COUNT ( State ) FROM "National_Popular_Vote_-_Bills_receiving_floor_votes_in_previous_sessions" WHERE "Outome" ~ "states signed"
	Expected answer: 11
	Note: "states signed" is not in table. Usually (without COUNT operator), the ~ operator recieves feedback for its different trials (wheather or not the query executes). But because of COUNT, the query will execute and return something even if the key words in the ~ operator never appear in the table --> it will count 0 of such elements.I don't see any easy way around that problem.