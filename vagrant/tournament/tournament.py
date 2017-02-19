#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2



def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    co = connect()
    cur = co.cursor()
    cur.execute("""DELETE FROM matches""")
    co.commit()
    co.close()

def deletePlayers():
    """Remove all the player records from the database."""
    co = connect()
    cur = co.cursor()
    cur.execute("""DELETE FROM players""")
    co.commit()
    co.close()

def countPlayers():
    """Returns the number of players currently registered."""
    print 1
    co = connect()
    cur = co.cursor()
    cur.execute("""SELECT COUNT(id) FROM players""")
    rows = cur.fetchone()
    co.close()
    return rows[0]

def registerPlayer(playername):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    co = connect()
    cur = co.cursor()
    cur.execute("INSERT INTO players VALUES ("%s")" ,(playername,))
    co.commit()
    co.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    co = connect()
    cur = co.cursor()
    cur.execute("""SELECT * FROM record""")
    rows = cur.fetchall()
    co.close()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    co = connect()
    cur = co.cursor()
    cur.execute("""INSERT INTO matches VALUES (%s, %s)""", (winner, loser) )
    co.commit()
    co.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    co = connect()
    cur = co.cursor()
    cur.execute("""SELECT * FROM matches""")
    data = cur.fetchall()
    co.close()
    record = playerStandings()
    print record[0]
    result, marked, size = [], {}, countPlayers()
    for detail in record:
        marked.update({detail[0] : False})
    for i in range(size/2):
        index = 0
        while marked[record[index][0]]:
            index += 1
        id1, name1 = record[index][0], record[index][1]
        index += 1
        isFound, id2, name2 = False, 0, ""
        while not isFound:
            while marked[record[index][0]]:
                index += 1
            id2, name2 = record[index][0], record[index][1]
            index += 1
            for match in data:
                if (match[0] == id1 and match[1] == id2) or \
                   (match[1] == id1 and match[0] == id2):
                    continue;
            isFound = True
        matchtuple = (id1, name1, id2, name2)
        result.append(matchtuple)
    return result


    
