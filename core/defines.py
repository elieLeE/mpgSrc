# coding=utf-8

from enum import Enum


class Position(Enum):
    GOAL = "Gardien"
    DEF_CENTRAL = "Def. Cen."
    DEF_LATERAL = "Def. Lat."
    MILIEU_DEFENSIF = "Mil. Def."
    MILIEU_OFFENSIF = "Mil. Off"
    ATTAQUANT = "Attaquant"


class ChampName(Enum):
    LIGUE_1 = "LIGUE 1"
    LIGUE_2 = "LIGUE 2"
    LIGA = "LIGA"
    PREMIER_LEAGUE = "PREMIER LEAGUE"
    SERIE_A = "SERIE A"

    @staticmethod
    def items():
        return ChampName.__members__.items()
