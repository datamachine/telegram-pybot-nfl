from telex.plugin import TelexPlugin
import argparse
import nflgame
import nfldb


class NflPlugin(TelexPlugin):
    """
    Print and query NFL stats using the nflgame library
    """


    patterns = {
        "^!nfl playerquery (.*)": "nfldb_playerquery",
    }

    usage = [
        "!nfl playerquery .*: TODO: DOCUMENT"
    ]

    def nfldb_playerquery(self, msg, matches):
        args = matches.group(1)

        parser = argparse.ArgumentParser(description='Query the nfldb for stats', prog="!nfl playerquery")
        parser.add_argument('-w','--week', dest='week', metavar="WEEK", type=int, help="Week to query")
        parser.add_argument('-y','--year', dest='year', metavar="YEAR", type=int, default=2014, help="Year to query")
        parser.add_argument('-p','--position', dest='position', metavar="POSITION", help="Position to query")
        parser.add_argument('-s','--stat', dest='stat', metavar="STAT", help="Stat to query")
        parser.add_argument('-c','--count', dest='count', metavar="COUNT", type=int, default=5, help="How many results to return (Max: 20)")
        parser.add_argument('-t','--team', dest='team', metavar="TEAM", help="Team to query, use short name i.e. NE")

        pargs = parser.parse_args(args.split())

        print(pargs)

        if pargs.position == None and pargs.stat == None:
            return "Either position, stat, or both must be specified"

        db = nfldb.connect()
        q = nfldb.Query(db)

        q.game(season_year=pargs.year)


        if pargs.position:
            q.player(position=pargs.position)

        if pargs.team:
            q.game(team=pargs.team)

        if pargs.stat:
            q.sort(pargs.stat)

        text = "Results:\n"
        for pp in q.limit(pargs.count).as_aggregate():
            text += "{}: {}\n".format(pp.player, getattr(pp, pargs.stat))

        return text
