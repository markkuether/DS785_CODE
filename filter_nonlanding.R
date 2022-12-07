
# This code uses the last five points in each flight
# to filter out flights that are not landing.
# The conditions that indicate a plane is landing are:
# - The plane is getting closer to the airport.
# - The plane is below 500 feet agl
# - The last point is within 200 feet of the minimum altitude.

test_landing <- function(five_pts,min_alt){
  is_landing = FALSE
  
  if (five_pts$apt_dst[5] < five_pts$apt_dst[1]){
    if (abs(five_pts$agl[5]) <= 500){
      if (! is.na(five_pts$baroaltitude[5])){
        if (abs(five_pts$baroaltitude[5]-min_alt) < 200){
          is_landing = TRUE
          
        }
        else{
          if (abs(five_pts$geoaltitude[5]-min_alt) < 200){
            is_landing = TRUE
          }
        }
      }
    }
  }
  return(is_landing)
}



my_wd <- "D:/OUTPUT/CSV_UNFILTERED/V20/"
v21 <- "D:/OUTPUT/CSV_UNFILTERED/V21_2/"

setwd(my_wd)


# headers = ["time", "icao24", "callsign"]
# headers += ["mfr", "model"]
# headers += ["lat", "lon", "velocity", "heading", "vertrate"]
# headers += ["baroaltitude", "geoaltitude"]
# headers += ["lastposupdate", "lastcontact"]
# headers += ["delta_time", "flt_num"]
# headers += ["apt_dst","agl"]

file_list <- list.files(path=my_wd, pattern=".csv", all.files=FALSE,
                        full.names=FALSE)
for(in_file in file_list){
  print(in_file)
  this_df <- read.csv(in_file)
  this_df$baroaltitude <- as.numeric(this_df$baroaltitude)

  vpos <- unlist(gregexpr("_V20",in_file,ignore.case=TRUE))[1]
  start_name = substr(in_file,1,vpos-1)
  out_name <- paste(start_name,"_v21.csv",sep="")
  out_file <- paste(v21,out_name,sep="")
  out_df <- data.frame(matrix(ncol = dim(this_df)[2],nrow=0))
  colnames(out_df) <- colnames(this_df)
  
  #planes <- sqldf("SELECT DISTINCT icao24 from this_df")
  planes <- unique(this_df$icao24)
  for (plane in planes){
    print(paste("  ",plane))
    flights <- unique(this_df$flt_num[this_df$icao24==plane])
    for (flight in flights){
       print(paste("     flight=",flight))
       flight_data <-  this_df[this_df$icao24==plane & this_df$flt_num==flight,]
       min_alt <- min(flight_data$baroaltitude)
       flight_len <-  dim(flight_data)[1]
       top <- flight_len-5
       if (top > 1){
         last_five <-  flight_data[top:flight_len,]
         is_landing <-  test_landing(last_five,min_alt)
         if(is_landing){
           out_df <- rbind(out_df,flight_data)
         }#if islanding
       }#if top
    }#for flight
  }#for plane
  write.csv(out_df,out_file,row.names = FALSE,quote=FALSE)
  
}#for file