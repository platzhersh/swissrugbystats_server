from swissrugbystats.core.models import Competition
from swissrugbystats.crawler.crawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.models import CrawlerLogMessage
from swissrugbystats.crawler.parser import FSRAbstractParser, FSRResultParser


class ResultCrawler(AbstractCrawler):

    @classmethod
    def crawl_per_league(cls, url, follow_pagination=False):
        """
        Fetch all the results of a specific league.

        TODO: crawl also special tables like finals / semi finals
        :param url: the url of the league to crawl
        :param follow_pagination: follow pagination?
        :return:
        """
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)

        try:
            logger.log("crawl per league {}".format(url))
            tables = FSRAbstractParser.get_tables(url)
            competition = Competition.objects.get(id=url[2])

            for table in tables:
                for row in table.findAll('tr'):
                    try:
                        if FSRResultParser.parse_row(row, competition):
                            count = count + 1

                    except Exception as e:
                        msg = u'ResultCrawler: Exception: {}'.format(e)
                        CrawlerLogMessage.objects.create(
                            message_type=CrawlerLogMessage.ERROR,
                            message=u"crawl_results_per_league, {}".format(msg)
                        )
            if follow_pagination:
                # recursively parse all next sites if there are any
                pagination = FSRAbstractParser.get_pagination(url)
                if pagination:
                    current = pagination.find('span',
                                              attrs={'class': 'current'})
                    if current and int(current.find(text=True)) == 1:
                        logger.log(u"Follow pagination, {} pages.".format(len(pagination)))
                        for page in pagination.findAll('a', attrs={'class': 'inactive'}):
                            logger.log(u"Page: {}, Current: {}".format(int(page.find(text=True)),
                                                                       int(current.find(text=True))))
                            if int(page.find(text=True)) > int(current.find(text=True)):
                                nextUrl = [(competition.league.shortcode, page['href'], competition.id)]
                                logger.log(u"visit {}".format(nextUrl))
                                count = count + cls.crawl(nextUrl)

        except Exception as e:
            msg = u'Type: {}, Args: {}, Str: {}'.format(e.__name__, e.args, e.__str__())
            CrawlerLogMessage.objects.create(
                message_type=CrawlerLogMessage.ERROR,
                message=u"crawl_results_per_league, {}".format(msg)
            )

        # TODO: statistics
        # if lock:
        #     with lock:
        #         self.statistics['results'] += count
        # else:
        #     self.statistics['results'] += count

        return count
