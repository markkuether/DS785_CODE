#This code re-orderes the CSV files
#by airplane ID, then by time to allow
#easy identification of landing
#pattern leg in other scripts

my_wd <- "D:/OUTPUT/CSV_UNFILTERED/V5/"
v6 <- "D:/OUTPUT/CSV_UNFILTERED/V6/"

setwd(my_wd)

file_list <- list.files(path=my_wd, pattern=".csv", all.files=FALSE,
             full.names=FALSE)
for(in_file in file_list){
  this_df <- read.csv(in_file)
  sorted_df <- this_df[order(this_df$icao24, this_df$time),]
  strlen <- nchar(in_file)
  end_pos = strlen-7
  out_file <- substr(in_file,1,end_pos)
  out_file <- paste(out_file,"_v6.csv",sep="")
  full_name <- paste(v6,out_file,sep="")
  write.csv(sorted_df,full_name,row.names=FALSE,quote=FALSE)
}

