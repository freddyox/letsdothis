# letsdothis
While all true marathons are the same distance, the races are not created equal! The goal of this consulting project for <a href="https://www.letsdothis.com/">LetsDoThis</a> is to assign a difficulty index to races in order to guide users to their next challenge. This project was done as a part of NYC Insight Data Science program. In the interest of space, the scraped and cleaned data has not been uploaded.

The data-scraping and cleaning was time intensive, and has been done in multiple stages as follows: for the runner finish time tables, which have been scraped from <a href="https://www.runbritainrankings.com//">runbritain</a>, the pipeline is:
* scrape with spider/spider.py
* collect and merge all json tables with build_tables.ipynb
* clean the output of build_tables.ipynb with clean_build_tables.ipynb. Also, this is where a terrain is chosen in addition to cross-referencing the race course with GPS data (elevation profile information)
* analyze the cleaned and GPS cross-referenced output with analysis.ipynb, and build all functions to be used in the flask application with flask_code.ipynb. Important model results are located within **inputs**

GPS data:
* Read the GPX format and build a table of features for each course with gpx_analysis.py, output is gpx_elevation_map_new.csv
