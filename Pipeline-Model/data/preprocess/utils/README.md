<pre>
<code>

usage: question2table.py [-h] -j JSON -d DATA

optional arguments:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  path for json data to parse
  -d DATA, --data DATA  path for data directory that contains directories
                        containing table.csv

                        
python3 utils/question2table.py -j ../../data/sayhearfall2018_train.json -d ../../data/sayhearfall2018_train/
>> Please input indexs of the questions (seperated by comma): 23,35,46
>> Show table?(y/n): y
>>
>> Question 23: Alexa  what is the current price of Bitcoin 
+------------+---------------+
| Key        | Value         |
+------------+---------------+
| last price | $  7,509.08   |
+------------+---------------+
| %          | -5.67 %       |
+------------+---------------+
| 24 high    | 7,981.52      |
+------------+---------------+
| 24 low     | 7,350.47      |
+------------+---------------+
| 24 volume  | $ 812,332,917 |
+------------+---------------+
| # coins    | 16.94m        |
+------------+---------------+
| market cap | 127.14b       |
+------------+---------------+
>>
>> Question 35: Alexa  what is the name of the last Harry Potter movie 
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
| url        | Motion_pic | Release_da | UK        | USA_&_Can | Other_cou | Worldwide | Budget    |
|            | ture       | te         |           | ada       | ntries    |           |           |
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
| https://en | Harry      | 16         | £66,096,0 | $317,575, | $657,179, | $974,755, | $125      |
| .wikipedia | Potter and | November   | 60        | 550       | 821       | 371       | million   |
| .org/wiki/ | the Philos | 2001 (2001 |           | (55,976,2 |           |           |           |
| Harry_Pott | opher's    | -11-16)    |           | 00)       |           |           |           |
| er_(film_s | Stone      |            |           |           |           |           |           |
| eries)#Fil |            |            |           |           |           |           |           |
| ms         |            |            |           |           |           |           |           |
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
| https://en | Harry      | 14         | £54,780,7 | $261,988, | $616,991, | $878,979, | $100      |
| .wikipedia | Potter and | November   | 31        | 482       | 152       | 634       | million   |
| .org/wiki/ | the        | 2002 (2002 |           | (44,978,9 |           |           |           |
| Harry_Pott | Chamber of | -11-14)    |           | 00)       |           |           |           |
| er_(film_s | Secrets    |            |           |           |           |           |           |
| eries)#Fil |            |            |           |           |           |           |           |
| ms         |            |            |           |           |           |           |           |
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
| https://en | Harry      | 31 May     | £45,615,9 | $249,541, | $547,147, | $796,688, | $130      |
| .wikipedia | Potter and | 2004 (2004 | 49        | 069       | 480       | 549       | million   |
| .org/wiki/ | the        | -05-31)    |           | (40,183,7 |           |           |           |
| Harry_Pott | Prisoner   |            |           | 00)       |           |           |           |
| er_(film_s | of Azkaban |            |           |           |           |           |           |
| eries)#Fil |            |            |           |           |           |           |           |
| ms         |            |            |           |           |           |           |           |
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
| https://en | Harry      | 18         | £48,328,8 | $290,013, | $606,898, | $896,911, | $150      |
| .wikipedia | Potter and | November   | 54        | 036       | 042       | 078       | million   |
| .org/wiki/ | the Goblet | 2005 (2005 |           | (45,188,1 |           |           |           |
| Harry_Pott | of Fire    | -11-18)    |           | 00)       |           |           |           |
| er_(film_s |            |            |           |           |           |           |           |
| eries)#Fil |            |            |           |           |           |           |           |
| ms         |            |            |           |           |           |           |           |
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
| https://en | Harry      | 11 July    | £49,136,9 | $292,004, | $647,881, | $939,885, | $150      |
| .wikipedia | Potter and | 2007 (2007 | 69        | 738       | 191       | 929       | million   |
| .org/wiki/ | the Order  | -07-11)    |           | (42,442,5 |           |           |           |
| Harry_Pott | of the     |            |           | 00)       |           |           |           |
| er_(film_s | Phoenix    |            |           |           |           |           |           |
| eries)#Fil |            |            |           |           |           |           |           |
| ms         |            |            |           |           |           |           |           |
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
| https://en | Harry      | 15 July    | £50,713,4 | $301,959, | $632,457, | $934,416, | $250      |
| .wikipedia | Potter and | 2009 (2009 | 04        | 197       | 290       | 487       | million   |
| .org/wiki/ | the Half-  | -07-15)    |           | (40,261,2 |           |           |           |
| Harry_Pott | Blood      |            |           | 00)       |           |           |           |
| er_(film_s | Prince     |            |           |           |           |           |           |
| eries)#Fil |            |            |           |           |           |           |           |
| ms         |            |            |           |           |           |           |           |
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
| https://en | Harry      | 19         | £52,364,0 | $295,983, | $664,300, | $960,283, | Less than |
| .wikipedia | Potter and | November   | 75        | 305       | 000       | 305       | $250      |
| .org/wiki/ | the        | 2010 (2010 |           | (37,503,7 |           |           | million ( |
| Harry_Pott | Deathly    | -11-19)    |           | 00)       |           |           | official) |
| er_(film_s | Hallows –  |            |           |           |           |           |           |
| eries)#Fil | Part 1     |            |           |           |           |           |           |
| ms         |            |            |           |           |           |           |           |
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
| https://en | Harry      | 15 July    | £73,094,1 | $381,011, | $960,500, | $1,341,51 | Less than |
| .wikipedia | Potter and | 2011 (2011 | 87        | 219       | 000       | 1,219     | $250      |
| .org/wiki/ | the        | -07-15)    |           | (48,046,8 |           |           | million ( |
| Harry_Pott | Deathly    |            |           | 00)       |           |           | official) |
| er_(film_s | Hallows –  |            |           |           |           |           |           |
| eries)#Fil | Part 2     |            |           |           |           |           |           |
| ms         |            |            |           |           |           |           |           |
+------------+------------+------------+-----------+-----------+-----------+-----------+-----------+
>>
>> Question 46: What are the AR points for The Last Kids on Earth and the Zombie Parade 
+--------------------+----------------------------------------------------------------------+
| Key                | Value                                                                |
+--------------------+----------------------------------------------------------------------+
| atos book level:   | 4                                                                    |
+--------------------+----------------------------------------------------------------------+
| interest level:    | middle grades (mg 4-8)                                               |
+--------------------+----------------------------------------------------------------------+
| ar points:         | 4                                                                    |
+--------------------+----------------------------------------------------------------------+
| rating:            |                                                                      |
+--------------------+----------------------------------------------------------------------+
| word count:        | 30484                                                                |
+--------------------+----------------------------------------------------------------------+
| fiction/nonfiction | fiction                                                              |
+--------------------+----------------------------------------------------------------------+
| topic - subtopic:  | adventure-survival; fantasy/imagination-monsters; humor/funny-funny; |
+--------------------+----------------------------------------------------------------------+
| series:            | last kids on earth;                                                  |
+--------------------+----------------------------------------------------------------------+
>>
>> Please input indexs of the questions (seperated by comma): 

</code>
</pre>