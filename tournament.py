#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    	"""Remove all the match records from the database."""
        c = connect()
	cursor = c.cursor()
	query = "DELETE FROM match"
	cursor.execute(query)
	c.commit()
	c.close()
	return

def deletePlayers():
    	"""Remove all the player records from the database."""
	c = connect()
        cursor = c.cursor()
        query = "DELETE FROM players"
        cursor.execute(query)
        c.commit()
        c.close()
        return 	

def countPlayers():
    	"""Returns the number of players currently registered."""
	c = connect()
        cursor = c.cursor()
        query = "SELECT count(*) AS count FROM players"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        c.close()
        return count     

def registerPlayer(name):
	"""Adds a player to the tournament database
	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)  
	Args:
	name: the player's full name (need not be unique). """
	c = connect()
	cursor = c.cursor()
	clean = bleach.clean(name, strip=True)
        query = "INSERT INTO players(player_name) values (%s)"
	cursor.execute(query, (clean,))
	c.commit()
	c.close()
	return 


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
    c = connect()
    cursor = c.cursor()
    query = "SELECT * FROM standings"
    cursor.execute(query)
    results = cursor.fetchall()
    #Check for tie and execute query to re-arrange order
    query = "SELECT p_id, player_name, wins, matches FROM standings" \
                       "ORDER BY (cast(wins AS DECIMAL)/matches) DESC;"
    if(results[0][2] > 0) and (results[0][2] == results[1][2]):
	cursor.execute(query)
        results = cursor.fetchall()
    c.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c = connect()
    cursor = c.cursor()
    cursor.execute("INSERT INTO match(winner,loser) values (%s,%s)", (winner,loser))
    c.commit()
    c.close()
    return 
 
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
    pairings =[]
    results = playerStandings()
    #Stepping loop iterator by 2 to makee pairs
    for i in range(0, len(results)-1, 2):
	p_list = (results[i][0],results[i][1],results[i+1][0],results[i+1][1])
        pairings.append(p_list)
    return pairings
