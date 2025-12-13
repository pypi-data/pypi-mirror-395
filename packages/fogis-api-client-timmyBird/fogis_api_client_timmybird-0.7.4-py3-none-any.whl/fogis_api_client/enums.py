from enum import Enum


class MatchStatus(Enum):
    INTERRUPTED = "avbruten"
    POSTPONED = "uppskjuten"
    CANCELLED = "installd"
    COMPLETED = "genomford"  # Assuming 'arslutresultat' implies completed
    NOT_STARTED = "ej_startad"  # Status for not started matches


class AgeCategory(Enum):
    UNDEFINED = 1
    CHILDREN = 2
    YOUTH = 3
    SENIOR = 4
    VETERANS = 5


class Gender(Enum):
    MALE = 2
    FEMALE = 3
    MIXED = 4


class FootballType(Enum):
    FOOTBALL = 1
    FUTSAL = 2
