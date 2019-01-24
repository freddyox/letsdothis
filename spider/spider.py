import scrapy

crawled_urls = []


class RunBritainResultsSpider(scrapy.Spider):
    """
    """
    
    name = 'runbritainresults'

    start_urls = [
        #events_5
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Apr-2017&dateto=31-Apr-2017',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Mar-2017&dateto=31-Mar-2017',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Feb-2017&dateto=31-Feb-2017',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jan-2017&dateto=31-Jan-2017',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Dec-2016&dateto=31-Dec-2016',
        #events_6
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Nov-2016&dateto=31-Nov-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Oct-2016&dateto=31-Oct-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Sep-2016&dateto=31-Sep-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Aug-2016&dateto=31-Aug-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jul-2016&dateto=31-Jul-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jun-2016&dateto=31-Jun-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-May-2016&dateto=31-May-2016',
         #events_7
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Apr-2016&dateto=31-Apr-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Mar-2016&dateto=31-Mar-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Feb-2016&dateto=31-Feb-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jan-2016&dateto=31-Jan-2016',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Dec-2015&dateto=31-Dec-2015',
        #events_8
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Nov-2015&dateto=31-Nov-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Oct-2015&dateto=31-Oct-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Sep-2015&dateto=31-Sep-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Aug-2015&dateto=31-Aug-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jul-2015&dateto=31-Jul-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jun-2015&dateto=31-Jun-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-May-2015&dateto=31-May-2015',
        #events_9
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Apr-2015&dateto=31-Apr-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Mar-2015&dateto=31-Mar-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Feb-2015&dateto=31-Feb-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jan-2015&dateto=31-Jan-2015',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Dec-2014&dateto=31-Dec-2014',
        #events_10
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Nov-2014&dateto=31-Nov-2014',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Oct-2014&dateto=31-Oct-2014',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Sep-2014&dateto=31-Sep-2014',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Aug-2014&dateto=31-Aug-2014',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jul-2014&dateto=31-Jul-2014',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jun-2014&dateto=31-Jun-2014',
        #'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-May-2014&dateto=31-May-2014',
        #events_11
        'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Apr-2014&dateto=31-Apr-2014',
        'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Mar-2014&dateto=31-Mar-2014',
        'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Feb-2014&dateto=31-Feb-2014',
        'https://www.runbritainrankings.com/results/resultslookup.aspx?datefrom=1-Jan-2014&dateto=31-Jan-2014',
    ]
    
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'

    def css_extract_first(self, response, selector):
        # Strip strings from selectors
        string = response.css(selector).extract_first()
        if string and len(string) > 0:
            return string.strip()
        return None

    def parse(self, response):
        # Follow all "Full" results pages
        # for row in response.css('a:contains("Full")'):
        for row in response.css('#cphBody_dgMeetings tr'):
            results_link = row.css('a:contains("Full")::attr(href)').extract_first()
            if results_link:
                terrain = row.css('td:nth-last-child(3)::text').extract_first()
                href = '%s&pagenum=1' % results_link
                yield response.follow(href, self.parse_results, meta={'terrain': terrain})

    def parse_results(self, response):
        # Retain list of crawled urls
        print(response.url)
        crawled_urls.append(response.url)

        event_title = response.css('#cphBody_lblMeetingDetails b::text').extract_first()
        [results_link, event_location, event_date, *_] = response.css('#cphBody_lblMeetingDetails::text').extract()

        # Follow all paginated results pages, avoiding previously visited
        for href in response.css('#cphBody_lblTopPageLinks a'):
            if href not in crawled_urls:
                yield response.follow(href, self.parse_results, meta=response.meta)

        # Aggregate results from table rows
        results = []

        # Races are determined by mid-table "headings" (which aren't actual th elements)
        race_title = ''

        for result in response.css('#cphBody_gvP tr'):
            if len(result.css('td')) == 1:
                table_heading = result.css('a[name^=r]')

                # Update race heading for following rows
                if table_heading:
                    race_title = self.css_extract_first(result, 'a[name^=r] + b::text')

            if len(result.css('td:nth-child(1) input')):
                results.append({
                    'terrain': response.meta['terrain'],
                    'race_title': race_title,
                    'position': self.css_extract_first(result, 'td:nth-child(2)::text'),
                    'gun_time': self.css_extract_first(result, 'td:nth-child(3)::text'),
                    'chip_time': self.css_extract_first(result, 'td:nth-child(4)::text'),
                    'name': self.css_extract_first(result, 'td:nth-last-child(10) a::text')
                    or self.css_extract_first(result, 'td:nth-last-child(10)::text'),
                    'strava_profile': self.css_extract_first(
                        result, 'td:nth-last-child(10) a[href*="strava"]::attr(href)'),
                    'age_group': self.css_extract_first(result, 'td:nth-last-child(8)::text'),
                    'sex': self.css_extract_first(result, 'td:nth-last-child(7)::text'),
                    'club': self.css_extract_first(result, 'td:nth-last-child(6)::text'),
                    'rb_season_best': self.css_extract_first(result, 'td:nth-last-child(5)::text'),
                    'rb_personal_best': self.css_extract_first(result, 'td:nth-last-child(4)::text'),
                    'rb_handicap': self.css_extract_first(result, 'td:nth-last-child(3)::text'),
                })

        # Output
        yield {
            'event_url': response.url,
            'event_title': event_title,
            'event_location': event_location,
            'event_date': event_date,
            'results': results,
        }
