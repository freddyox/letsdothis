# LetsDoThis
All marathons are the same distance; however, the courses vary dramatically in difficulty. The goal of this consulting project for <a href="https://www.letsdothis.com/">LetsDoThis</a> is to estimate the difficulty of a race in order to guide users to their next challenge. This project was done in 3 weeks as a part of <a href="https://www.insightdatascience.com">Insight Data Science Program. </a> in New York City. In the interest of memory, the scraped and cleaned data will not been uploaded.

### Data Scraping and Cleaning
Extensive scraping has been performed from two data sources:
1. GPS coordinates (longitude, latitude, and elevation) of races, which allows one to calculate the elevation gain/loss, the standard deviation in the mean elevation (measure of hilliness), and the number of hills. This data was difficult to get but was done using Strava; you must find a Strava member's profile with pubic permissions in order to download the relevant GPX file.
2. Race results from <a href="https://www.runbritainrankings.com/">runbritain</a> which includes finish times, personal information such as sex/age, and race metadata.

Data merging and cleaning was performed using stand-alone python scripts and jupyter notebooks. I limited the analysis to **road** races, which means I excluded trail/multi terrain races. Post cleaning results in about 60 MB (350 MB) of GPS (finish time) data.

### Difficulty Analysis 
* I focused on 10K and Marathon races due to GPS data concerns; scraping more GPS information was too time-intensive for the 3-4 week schedule at Insight, but the analysis in principle extends to any race type.
