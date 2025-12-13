"""
Sample data for the mock FOGIS API server.

This module contains sample data structures that mimic the responses from the FOGIS API.
The data is anonymized but follows the same structure as real API responses.
"""

# Sample match list
SAMPLE_MATCH_LIST = {
    "matcher": [
        {
            "matchid": 12345,
            "matchnr": "123456",
            "datum": "2023-09-15",
            "tid": "19:00",
            "hemmalag": "Home Team FC",
            "bortalag": "Away Team United",
            "hemmalagid": 1001,
            "bortalagid": 1002,
            "arena": "Sample Arena",
            "status": "Fastställd",
            "domare": "Referee Name",
            "ad1": "Assistant 1",
            "ad2": "Assistant 2",
            "fjarde": "",
            "matchtyp": "Serie",
            "tavling": "Sample League",
            "grupp": "Division 1",
            "hemmamal": None,
            "bortamal": None,
            "publik": None,
            "notering": None,
            "rapportstatus": "Ej påbörjad",
            "matchstart": None,
        },
        {
            "matchid": 12346,
            "matchnr": "123457",
            "datum": "2023-09-16",
            "tid": "15:00",
            "hemmalag": "Another Home FC",
            "bortalag": "Another Away United",
            "hemmalagid": 1003,
            "bortalagid": 1004,
            "arena": "Another Arena",
            "status": "Fastställd",
            "domare": "Referee Name",
            "ad1": "Assistant 1",
            "ad2": "Assistant 2",
            "fjarde": "",
            "matchtyp": "Serie",
            "tavling": "Sample League",
            "grupp": "Division 1",
            "hemmamal": None,
            "bortamal": None,
            "publik": None,
            "notering": None,
            "rapportstatus": "Ej påbörjad",
            "matchstart": None,
        },
    ]
}

# Sample match details
SAMPLE_MATCH = {
    "matchid": 12345,
    "matchnr": "123456",
    "datum": "2023-09-15",
    "tid": "19:00",
    "hemmalag": "Home Team FC",
    "bortalag": "Away Team United",
    "hemmalagid": 1001,
    "bortalagid": 1002,
    "arena": "Sample Arena",
    "status": "Fastställd",
    "domare": "Referee Name",
    "ad1": "Assistant 1",
    "ad2": "Assistant 2",
    "fjarde": "",
    "matchtyp": "Serie",
    "tavling": "Sample League",
    "grupp": "Division 1",
    "hemmamal": None,
    "bortamal": None,
    "publik": None,
    "notering": None,
    "rapportstatus": "Ej påbörjad",
    "matchstart": None,
    "halvtidHemmamal": None,
    "halvtidBortamal": None,
}

# Sample match players
SAMPLE_MATCH_PLAYERS = {
    "hemmalag": [
        {
            "personid": 2001,
            "fornamn": "Player",
            "efternamn": "One",
            "smeknamn": None,
            "tshirt": "1",
            "position": "Målvakt",
            "positionid": 1,
            "lagkapten": False,
            "spelareid": 3001,
            "licensnr": "ABC123",
        },
        {
            "personid": 2002,
            "fornamn": "Player",
            "efternamn": "Two",
            "smeknamn": None,
            "tshirt": "2",
            "position": "Försvarare",
            "positionid": 2,
            "lagkapten": True,
            "spelareid": 3002,
            "licensnr": "ABC124",
        },
        {
            "personid": 2003,
            "fornamn": "Player",
            "efternamn": "Three",
            "smeknamn": None,
            "tshirt": "10",
            "position": "Mittfältare",
            "positionid": 3,
            "lagkapten": False,
            "spelareid": 3003,
            "licensnr": "ABC125",
        },
        {
            "personid": 2004,
            "fornamn": "Player",
            "efternamn": "Four",
            "smeknamn": None,
            "tshirt": "9",
            "position": "Anfallare",
            "positionid": 4,
            "lagkapten": False,
            "spelareid": 3004,
            "licensnr": "ABC126",
        },
    ],
    "bortalag": [
        {
            "personid": 2005,
            "fornamn": "Player",
            "efternamn": "Five",
            "smeknamn": None,
            "tshirt": "1",
            "position": "Målvakt",
            "positionid": 1,
            "lagkapten": False,
            "spelareid": 3005,
            "licensnr": "DEF123",
        },
        {
            "personid": 2006,
            "fornamn": "Player",
            "efternamn": "Six",
            "smeknamn": None,
            "tshirt": "4",
            "position": "Försvarare",
            "positionid": 2,
            "lagkapten": True,
            "spelareid": 3006,
            "licensnr": "DEF124",
        },
        {
            "personid": 2007,
            "fornamn": "Player",
            "efternamn": "Seven",
            "smeknamn": None,
            "tshirt": "8",
            "position": "Mittfältare",
            "positionid": 3,
            "lagkapten": False,
            "spelareid": 3007,
            "licensnr": "DEF125",
        },
        {
            "personid": 2008,
            "fornamn": "Player",
            "efternamn": "Eight",
            "smeknamn": None,
            "tshirt": "11",
            "position": "Anfallare",
            "positionid": 4,
            "lagkapten": False,
            "spelareid": 3008,
            "licensnr": "DEF126",
        },
    ],
}

# Sample match officials
SAMPLE_MATCH_OFFICIALS = {
    "hemmalag": [
        {
            "personid": 4001,
            "fornamn": "Coach",
            "efternamn": "One",
            "roll": "Tränare",
            "rollid": 1,
        },
        {
            "personid": 4002,
            "fornamn": "Assistant",
            "efternamn": "Coach",
            "roll": "Assisterande tränare",
            "rollid": 2,
        },
    ],
    "bortalag": [
        {
            "personid": 4003,
            "fornamn": "Coach",
            "efternamn": "Two",
            "roll": "Tränare",
            "rollid": 1,
        },
        {
            "personid": 4004,
            "fornamn": "Team",
            "efternamn": "Manager",
            "roll": "Lagledare",
            "rollid": 3,
        },
    ],
}

# Sample match events
SAMPLE_MATCH_EVENTS = [
    {
        "matchhandelseid": 5001,
        "matchid": 12345,
        "handelsekod": 6,  # Goal
        "handelsetyp": "Mål",
        "minut": 23,
        "lagid": 1001,
        "lag": "Home Team FC",
        "personid": 2003,
        "spelare": "Player Three",
        "assisterande": "Player Two",
        "assisterandeid": 2002,
        "period": 1,
        "mal": True,
        "resultatHemma": 1,
        "resultatBorta": 0,
    },
    {
        "matchhandelseid": 5002,
        "matchid": 12345,
        "handelsekod": 6,  # Goal
        "handelsetyp": "Mål",
        "minut": 42,
        "lagid": 1002,
        "lag": "Away Team United",
        "personid": 2008,
        "spelare": "Player Eight",
        "assisterande": "Player Seven",
        "assisterandeid": 2007,
        "period": 1,
        "mal": True,
        "resultatHemma": 1,
        "resultatBorta": 1,
    },
    {
        "matchhandelseid": 5003,
        "matchid": 12345,
        "handelsekod": 1,  # Yellow card
        "handelsetyp": "Gult kort",
        "minut": 56,
        "lagid": 1001,
        "lag": "Home Team FC",
        "personid": 2002,
        "spelare": "Player Two",
        "period": 2,
    },
    {
        "matchhandelseid": 5004,
        "matchid": 12345,
        "handelsekod": 7,  # Substitution
        "handelsetyp": "Byte",
        "minut": 65,
        "lagid": 1002,
        "lag": "Away Team United",
        "personid": 2008,  # Player going out
        "spelare": "Player Eight",
        "assisterande": "Player Nine",  # Player coming in
        "assisterandeid": 2009,
        "period": 2,
    },
]

# Sample match result
SAMPLE_MATCH_RESULT = {
    "matchid": 12345,
    "hemmamal": 2,
    "bortamal": 1,
    "halvtidHemmamal": 1,
    "halvtidBortamal": 1,
}
