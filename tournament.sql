-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--Drop database if it exists before
DROP DATABASE IF EXISTS tournament;
--Create new database
CREATE DATABASE tournament;
--Connect to database
\c tournament
--Create Players table
CREATE TABLE players(
	p_id serial,
	player_name varchar(20),
	primary key (p_id)
);
--Create match table
CREATE TABLE match(
	m_id serial,
	winner integer,
	loser integer,
	Foreign Key(winner) references players(p_id),
	Foreign Key(loser) references players(p_id),
        primary key (m_id)
);
--Create view for standings
CREATE VIEW standings AS 
SELECT p_id, player_name,
(SELECT COUNT(*) FROM match where p_id=winner)as wins,
(SELECT COUNT(*) FROM match where p_id in (winner,loser))as matches
FROM players
GROUP BY p_id
ORDER BY wins;  

