# connection_to_db.R

# opens connection to Postgres database 'testform'
# reads links, races and results tables into R as dataframes

library(RPostgreSQL)
library(sqldf)

# sqldf requires these options to connect
options(sqldf.RPostgreSQL.user ="postgres", 
        sqldf.RPostgreSQL.password ="16albion",
        sqldf.RPostgreSQL.dbname ="testform",
        sqldf.RPostgreSQL.host ="localhost", 
        sqldf.RPostgreSQL.port =5432)

# We actually connect with the RpostgresSQL package
drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname="testform", host="localhost", user="postgres",password="16albion")

# Rather than working with the database directly it is wise 
# to produce copies of the tables in it as dataframes

links <- dbReadTable(con, "links")
races <- dbReadTable(con, "races")
results <- dbReadTable(con, "results")

# Alternatively we could use sqldf to do exactly the same thing:
# links <- sqldf("select * from testform.links")

# Since the data frames have been copied we can quickly
# disconnect all database connections with
dbDisconnect(con)

# We are free to analyse these dataframes now
# using either the R or the SQL language (via sqldf)

# How to write directly from R to the database - see:
# http://www.r-bloggers.com/r-and-postgresql-using-rpostgresql-and-sqldf/

# With the sqldf package, we can now use the data frames
# as if they were a database and use SQL directly.

# The sqldf function supports the full richness of the SQL language,
# but applied to data frames in R's memory. This includes:
# SELECT ... WHERE statements to select rows and columns 
# according to logical criteria
# CASE clauses, for queries with special cases
# ORDER BY statements, to sort the resulting data
# according to specified columns,
# and LEFT JOIN and INNER JOIN statements for merging data frames
