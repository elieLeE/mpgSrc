# coding=utf-8

from enum import Enum


MAX_SUM_PRIZE_TEAM = 500


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
        if realPos == Position.GOAL.value:
            return Position.GOAL.value
        if realPos in [Position.CENTRAL_DEFENDER.value, Position.LATERAL_DEFENDER.value]:
            return Position.DEFENDER.value
        if realPos in [Position.MILIEU_DEFENSIVE.value, Position.MILIEU_OFFENSIVE.value]:
            return Position.MILIEU.value
        return Position.STRIKER.value


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
    TAG_BUY_PRIZE = "buyPrize"
    TAG_PERCENT_TIT = "percentTit"


class EXT_FILES(Enum):
    CSV = ".csv"
    XML = ".xml"
