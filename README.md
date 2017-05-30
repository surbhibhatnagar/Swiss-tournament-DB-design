This is a database design example of how winner is determined based on swiss tournament.
Database connection with PostgresSQL is established using Python DB-API.
tournament.sql contains database and table creation information.
tournament.py contains query functions that help in determining player standings.
tournamen_test.py contains the unit tests that check proper functioning of db queries.
To run:
Pre-req: 
a. Python 2.7 or above
b. PostgreSQL 
1. Download zip file and unzip the project folder
2. Open terminal and got to project folder
3. Run following command to create db and tables required
	>psql
        >\i tournament.sql
4. Exit from psql prompt by entering CMD+D or exit()
5. Run tournament_test.py by running following command:
	python tournament_test.py   
