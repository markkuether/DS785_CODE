#This file filters out all airplanes except for Cessna 172's.
#It then identifies which planes are accident planes
#using the title and callsign

library(stringr)
library(lubridate)
library(dplyr)

mywd <- "D:/output/csv_unfiltered/v24/"
setwd(mywd)

out_file <- "all_data_out.csv"
whole_file <- read.csv("all_data.csv")
summary(whole_file)

#Make sure all text is in upper case
whole_file$mfr <- toupper(whole_file$mfr)
whole_file$model <- toupper(whole_file$model)
whole_file$callsign <- toupper(whole_file$callsign)
whole_file$file_planeid <- toupper(whole_file$file_planeid)

#Make sure all text has spaces stripped
whole_file$mfr <- str_trim(whole_file$mfr,"right")
whole_file$mfr <- str_trim(whole_file$mfr,"left")
whole_file$callsign <- str_trim(whole_file$callsign,"right")
whole_file$callsign <- str_trim(whole_file$callsign,"left")
whole_file$file_planeid <- str_trim(whole_file$file_planeid,"right")
whole_file$file_planeid <- str_trim(whole_file$file_planeid,"left")
whole_file$model <- str_trim(whole_file$model,"right")
whole_file$model <- str_trim(whole_file$model,"left")

whole_file$mfr <- as.factor(whole_file$mfr)
whole_file$callsign <- as.factor(whole_file$callsign)
whole_file$file_planeid <- as.factor(whole_file$file_planeid)
whole_file$model <- as.factor(whole_file$model)

#only keep cessna 172 data
only_cessna <- whole_file[whole_file$mfr == "CESSNA",]
only_cessna <- only_cessna[grep("172",only_cessna$model),]

#clean out old data
rm(whole_file)

only_cessna$mfr <- droplevels(only_cessna$mfr)
only_cessna$callsign <- droplevels(only_cessna$callsign)
only_cessna$file_planeid <- droplevels(only_cessna$file_planeid)
only_cessna$model <- droplevels(only_cessna$model)

only_cessna$file_apt <- as.factor(only_cessna$file_apt)
only_cessna$acc_plane <- only_cessna$callsign %in% only_cessna$file_planeid
only_cessna$time_gmt <- lubridate::as_datetime(only_cessna$time)

#new column is 23rd column.  Place next to first column
col_order <- c(1,23)
col_order <- c(col_order,seq(from=2,to=22,by=1))
only_cessna <- only_cessna[,col_order]
summary(only_cessna)
#levels(only_cessna$callsign)
#levels(only_cessna$file_planeid)

write.csv(only_cessna,out_file,row.names=FALSE,quote=FALSE)


