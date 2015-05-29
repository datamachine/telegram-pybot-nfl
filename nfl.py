import plugintypes
import nflgame
import nfldb


class NflPlugin(plugintypes.TelegramPlugin):
    """
    Print and query NFL stats using the nflgame library
    """


    patterns = {
        "^!topqb (20[0-9]{2})": "top_qb",
    }

    usage = [
        "!topqb 20xx: get regular season top 10 qbs for year"
    ]

    def top_qb(self, msg, matches):
        try:
            year = int(matches.group(1))
        except:
            return "Year is malformed"

        if year > 2014 or year < 2009:
            return "Only 2009-2014 supported"

        text = "Top QBs:\n"
        db = nfldb.connect()
        q = nfldb.Query(db)

        q.game(season_year=year, season_type='Regular')
        for pp in q.sort('passing_yds').limit(5).as_aggregate():
            text += "{}: {}yds\n".format(pp.player, pp.passing_yds)

        return text
