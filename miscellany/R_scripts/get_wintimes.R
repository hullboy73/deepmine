# get_wintimes.R

library(RPostgreSQL)
library(sqldf)

options(sqldf.RPostgreSQL.user ="postgres", 
        sqldf.RPostgreSQL.password ="16albion",
        sqldf.RPostgreSQL.dbname ="testform",
        sqldf.RPostgreSQL.host ="localhost", 
        sqldf.RPostgreSQL.port =5432)
drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname="testform", host="localhost", user="postgres",password="16albion")

uniqrcds <- dbGetQuery(con, 
"select racecourse, distance, COUNT(distance)
from links
group by racecourse, distance
order by racecourse, distance, count(distance);")

wintimes <- dbGetQuery(con, 
"SELECT links.racecourse, links.distance, links.disttext, links.racedate, races.raceid, races.going, races.racetype2, races.agerange, races.raceclass, races.wintime 
FROM links
INNER JOIN races
ON links.raceid = races.raceid
ORDER BY links.racecourse, links.distance, races.raceclass, races.wintime;")

# restricted to 3yo+ and 4yo+ races
age_wintimes <- subset(wintimes, agerange == "3yo+" | agerange == "4yo+")

# write.csv(uniqrcds, "uniq_racecourse_dists.csv")
write.csv(age_wintimes, "age_wintimes.csv")

crs_dist_cls_times <- sqldf(
"SELECT racecourse, disttext, raceclass, COUNT(raceclass)
FROM age_wintimes
GROUP BY racecourse, disttext, raceclass
ORDER BY racecourse, disttext, raceclass, COUNT(raceclass)")

# write.csv(crs_dist_cls_times, "crs_dist_clas_times.csv")

dbDisconnect(con)
