-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE DATABASE tournament;

\c tournament;



CREATE TABLE players (
    ID      serial PRIMARY KEY,
    Name    varchar(50) NOT NULL
);



CREATE TABLE matches ( 
    WinnerID   integer,
    LoserID    integer 
);



CREATE VIEW record AS 
    (SELECT players.ID AS ID, players.Name AS Name, Mule.wins AS Wins, Mule.matches AS Matches
     FROM (SELECT Temp1.ID AS ID, Temp1.wins AS wins, Temp1.wins + Temp2.loses AS matches
	  FROM (SELECT WinnerID AS ID, COUNT(*) AS wins
                FROM matches 
                GROUP BY WinnerID) AS Temp1,
               (SELECT LoserID AS ID, COUNT(*) AS loses
                FROM matches
                GROUP BY LoserID) AS Temp2
          WHERE Temp1.ID = Temp2.ID) AS Mule, players
     WHERE Mule.ID = players.ID)
    UNION
    (SELECT players.ID AS ID, players.Name AS Name, 0 AS Wins, 0 AS Matches
     FROM players
     WHERE players.ID NOT IN ((SELECT WinnerID FROM matches)
                               UNION
                              (SELECT LoserID FROM matches)))
    ORDER BY Wins, Matches DESC;
