from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from swissrugbystats.api import views


urlpatterns = patterns('',
    url(r'^$', views.api_root),
    url(r'^leagues/?$', views.LeagueList.as_view(), name="leagues"),
    url(r'^leagues/(?P<pk>[0-9]+)/?$', views.LeagueDetail.as_view(), name='leagues_detail'),

    url(r'^games/?$', views.GameList.as_view(), name="games"),
    url(r'^games/(?P<pk>[0-9]+)/?$', views.GameDetail.as_view()),

    url(r'^gameparticipations/?$', views.GameParticipationList.as_view(), name="game-participations"),
    url(r'^gameparticipations/(?P<pk>[0-9]+)/?$', views.GameParticipationDetail.as_view()),

    url(r'^clubs/?$', views.ClubList.as_view(), name="clubs"),
    url(r'^clubs/(?P<pk>[0-9]+)/?$', views.ClubDetail.as_view()),

    url(r'^teams/?$', views.TeamList.as_view(), name="teams"),
    url(r'^teams/(?P<pk>[0-9]+)/?$', views.TeamDetail.as_view()),

    url(r'^teams/(?P<pk>[0-9]+)/games/?$', views.GameSchedule.as_view(), name="game-schedule"),
    url(r'^teams/(?P<pk>[0-9]+)/games/next/?$', views.NextGameByTeamId.as_view(), name="next-game"),
    url(r'^teams/(?P<pk>[0-9]+)/games/last/?$', views.LastGameByTeamId.as_view(), name="last-game"),
    url(r'^teams/(?P<pk>[0-9]+)/games/season/(?P<season>[0-9]+)/?$', views.get_team_games_by_season, name="last-game"),

    url(r'^players/?$', views.PlayerList.as_view(), name="players"),
    url(r'^players/(?P<pk>[0-9]+)/?$', views.PlayerDetail.as_view()),

    url(r'^referees/?$', views.RefereeList.as_view(), name="referees"),
    url(r'^referees/(?P<pk>[0-9]+)/?$', views.RefereeDetail.as_view()),

    url(r'^seasons/?$', views.SeasonList.as_view(), name="seasons"),

    url(r'^competitions/?$', views.CompetitionList.as_view(), name="competitions"),

    url(r'^venues/?$', views.VenueList.as_view(), name="venues"),
    url(r'^venues/(?P<pk>[0-9]+)/?$', views.VenueDetail.as_view()),

    url(r'^users/?$', views.CreateUser.as_view(), name='create-user'),
    # url(r'^users/changePW$', views.CreateUser.as_view(), name='create-user'),
    url(r'^favorites/?$', views.CreateFavorite.as_view(), name='create-favorite'),


    # JWT Authentication
    url(r'^api-token-auth/?', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-refresh/?', 'rest_framework_jwt.views.refresh_jwt_token'),

)

urlpatterns = format_suffix_patterns(urlpatterns)