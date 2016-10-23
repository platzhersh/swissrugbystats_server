# -*- coding: utf-8 -*-
import datetime
from django_admin_conf_vars.global_vars import config
import logging
from swissrugbystats.crawler.crawler import SRSCrawler, SRSAsyncCrawler
from swissrugbystats.crawler.models import CrawlerLogMessage
from swissrugbystats.core.models import Competition, Season, Team

# create logger
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s- %(message)s', datefmt='%d.%m.%Y %I:%M:%S ')


def update_all(deep_crawl=True, season=config.CURRENT_SEASON, log_to_db=True):
    """
    Crawl suisserugby.com for the latest data.
    :param deep_crawl: crawl through pagination
    :return: none
    """
    current_season = Season.objects.get(id=season)
    logging.info("update started for season {}".format(current_season))

    if log_to_db:
        CrawlerLogMessage.objects.create(
            message="Update started for season {}. Deep crawl = {}.".format(current_season, deep_crawl),
        )

    # get current timestamp to calculate time needed for script exec
    start_time = datetime.datetime.now()

    print "------------------------------------------------------------------"
    print ""

    print "Getting data from suisserugby.com for season {}".format(Season.objects.filter(id=season).first())
    if deep_crawl:
        print "    deep_crawl = True - following pagination"
    else:
        print "    deep_crawl = False (default) - not following pagination"

    print ""
    print "------------------------------------------------------------------"
    print ""

    crawler = SRSCrawler()
    #crawler = SRSAsyncCrawler()

    # update team table
    print("crawl Teams")
    teams_count = crawler.crawl_teams([(c.league.shortcode, c.get_league_url(), c.id) for c in Competition.objects.filter(season=current_season)])

    # update game table with fixtures
    print("current season:" + config.CURRENT_SEASON)
    fixtures_count = crawler.crawl_fixtures([(c.league.shortcode, c.get_fixtures_url(), c.id) for c in Competition.objects.filter(season=current_season)], deep_crawl)

    # update game table with results
    result_count = crawler.crawl_results([(c.league.shortcode, c.get_results_url(), c.id) for c in Competition.objects.filter(season=current_season)], deep_crawl)

    print ""
    print "------------------------------------------------------------------"
    print ""
    print "{} {}".format(teams_count, "teams crawled")
    print "{} {}".format(result_count, "results crawled")
    print "{} {}".format(fixtures_count, "fixtures crawled")

    print ""
    print "{} {}".format("Time needed:", (datetime.datetime.now() - start_time))
    print ""

    if log_to_db:
        CrawlerLogMessage.objects.create(
            message="Crawling completed.\n{0} teams crawled\n{1} results crawled\n{2} fixtures crawled\nTime needed: {3}".format(teams_count, result_count, fixtures_count, (datetime.datetime.now() - start_time))
        )

def update_statistics(log_to_db=True):
    """

    :param log_to_db:
    :return:
    """
    teams = Team.objects.all()

    for t in teams:
        try:
            print(u"update {}".format(t.name))
            t.update_statistics()
        except Exception as e:
            print("Exception! {}".format(e))