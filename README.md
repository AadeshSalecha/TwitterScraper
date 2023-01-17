# Twitter_Scraper
Twitter scraper that bypasses normal API limitations. 

This repository was a predecessor to the work that was used in the paper - *Detecting fake news spreaders in social networks using inductive representation learning*. This paper was published in the IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining (ASONAM) 2020. 

Please note that the code is still in a maintenance state.

If you find this code or paper useful in your research, please consider citing:

Please cite this paper:

```
@inproceedings{rath2020detecting,
  title={Detecting fake news spreaders in social networks using inductive representation learning},
  author={Rath, Bhavtosh and Salecha, Aadesh and Srivastava, Jaideep},
  booktitle={2020 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining (ASONAM)},
  pages={182--189},
  year={2020},
  organization={IEEE}
}
```

Change Log:
```
(05.13.2019) Global parellelism instead of level parellelism
(05.12.2019) Updated friends.py
(05.12.2019) General Code Cleanup
(05.12.2019) Added ability to resume code and -reset flag
(05.10.2019) Ram optimization to reduce follower array overhead
(05.09.2019) Added assertions to ensure all followers are scraped
(05.09.2019) Parellelize and Multithread code
(05.09.2019) Print out diagnostic information - user being scraped, timestamp, number of followers
(05.08.2019) Added exception handling for delted users
(05.07.2019) Changed output formatting
(05.07.2019) Added support for friends scraping
(04.23.2019) Initial followers scraper
```

TO DO (Code)
```
1. Add Resume functionality to avoid recomputation
```

TO DO (Others):
```
1. Go over Spread of News paper
2. Go ove TSM paper
2. Start collecting AltNews articles
3. Test a few AltNews articles to check density
```

Dropped:
```
Disk-based Hashtable would have to coded and right now, the RAM overhead is acceptable
Explore memory mapping to reduce RAM overhead of hashtable - Priority 3, Urgency 1
```
