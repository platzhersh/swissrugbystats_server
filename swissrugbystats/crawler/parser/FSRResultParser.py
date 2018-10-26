import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from swissrugbystats.core.models import Team, Game, GameParticipation, Venue, \
    Referee
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser import FSRAbstractParser
from swissrugbystats.crawler.parser.FSRGameParser import FSRGameParser


class FSRResultParser(FSRAbstractParser):

    @staticmethod
    def something(row, cells):
        logger = None
        # get host and guest team
        teams = cells[2].find(text=True)        # teams
        teams2 = teams.split(' - ')

        host = Team.objects.filter(name=teams2[0].strip())
        if not host:
            logging.error(u"Hostteam not found: {}".format(teams2[0].strip()))
            logging.error(row)
            logger.log(u"Hostteam not found: {}".format(teams2[0].strip()))
            return False
        else:
            host = host[0]
        guest = Team.objects.filter(name=teams2[1].strip())
        if not guest:
            logging.error(u"Guestteam not found: {}".format(teams2[1].strip()))
            logging.error(row)
            logger.log(u"Guestteam not found: {}".format(teams2[1].strip()))
            return False
        else:
            guest = guest[0]

        # check if game is already stored, if so, update the existing one
        fsrUrl = cells[0].find('a')['href']
        if not Game.objects.filter(fsrUrl=fsrUrl):
            game = Game()
            hostParticipant = GameParticipation(team=host)
            guestParticipant = GameParticipation(team=guest)
        else:
            game = Game.objects.filter(fsrUrl=fsrUrl)[0]
            hostParticipant = game.host
            guestParticipant = game.guest


        # parse date and set timezone
        date = cells[1].find(text=True)
        d1 = timezone.get_current_timezone().localize(datetime.strptime(date, '%d.%m.%Y %H:%M'))
        d2 = d1.strftime('%Y-%m-%d %H:%M%z')
        game.date = d2

        game.competition = competition
        game.fsrID = cells[0].find(text=True)
        game.fsrUrl = cells[0].find('a')['href']

        # Game details & team logos

        # make new request to game detail page
        r2 = requests.get(game.fsrUrl, headers=FSRAbstractParser.get_request_headers())
        soup2 = BeautifulSoup(r2.text, "html.parser")
        table2 = soup2.find('table', attrs={'class': None})
        rows = table2.findAll('tr')

    @staticmethod
    def parse_row(row, competition):
        """

        :param row:
        :return:
        """
        logger = CrawlerLogger.get_logger_for_class(FSRResultParser)

        cells = row.findAll('td')
        if len(cells) > 0:
            # check if game is already stored, if so, update the existing one
            fsr_url = cells[0].find('a')['href']

            logger.log("Crawl Game Details: " + fsr_url);

            # Game details & team logos

            # make new request to game detail page
            r = requests.get(fsr_url, headers=FSRAbstractParser.get_request_headers())
            soup = BeautifulSoup(r.text, "html.parser")
            game_detail_table = soup.find('table', attrs={'class': None})

            rows = game_detail_table.findAll('tr')

            if FSRGameParser.parse_rows(rows, fsr_url):
                # logger.log(u"GameFixture {} created / updated".format(Game.objects.get(id=game.id)))
                # increment game counter
                return True
            else:
                return False