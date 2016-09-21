# amend_wintimes.R

library(dplyr)

wintimes <- age_wintimes
min_wintimes <- aggregate(wintimes$wintime, by=list(wintimes$distance, wintimes$racecourse, wintimes$raceclass), FUN=min)
mean_wintimes <- aggregate(wintimes$wintime, by=list(wintimes$distance, wintimes$racecourse, wintimes$raceclass), FUN=mean)
wintimes_95 <- aggregate(wintimes$wintime, by=list(wintimes$distance, wintimes$racecourse, wintimes$raceclass), function(x) quantile(c(x),probs=c(0,.05), na.rm=TRUE))

# write.csv(wintimes_95, 'wintimes_95.csv')
