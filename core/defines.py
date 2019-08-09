# coding=utf-8

from enum import Enum


class Position(Enum):
    GOAL = "Gardien"
    DEFENDER = "Defenseur"
    CENTRAL_DEFENDER = "Def. Cen."
    LATERAL_DEFENDER = "Def. Lat."
    MILIEU = "Milieu"
    MILIEU_DEFENSIVE = "Mil. Def."
    MILIEU_OFFENSIVE = "Mil. Off"
    STRIKER = "Attaquant"

    @staticmethod
    def getGloBasPos(realPos):
        if realPos == Position.GOAL:
            return Position.GOAL
        if realPos in [Position.CENTRAL_DEFENDER, Position.LATERAL_DEFENDER]:
            return Position.DEFENDER
        if realPos in [Position.MILIEU_DEFENSIVE, Position.MILIEU_OFFENSIVE]:
            return Position.MILIEU
        return Position.STRIKER


class ChampName(Enum):
    LIGUE_1 = "LIGUE 1"
    LIGUE_2 = "LIGUE 2"
    LIGA = "LIGA"
    PREMIER_LEAGUE = "PREMIER LEAGUE"
    SERIE_A = "SERIE A"

    @staticmethod
    def items():
        return ChampName.__members__.items()


class XML(object):
    ATTR_GLOBAL_DATA_BASE = "GlobalDataBase"
    ATTR_CHAMP = "champ"
    ATTR_DAY_NUMBER = "dayNumber"
    ATTR_TEAM = "team"
    ATTR_PLAYER = "player"

    TAG_VERSION = "version"
    TAG_ID = "id"
    TAG_NAME = "name"
    TAG_POSITION = "pos"
    TAG_EVAL = "eval"
    TAG_GOAL_NUMBER = "goalNumber"
    TAG_PRIZE = "prize"
    TAG_PERCENT_TIT = "percentTit"


