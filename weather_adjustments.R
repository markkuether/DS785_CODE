#This code reads the compiled weather data
#and filters out records where the wind speed
#or direction are not available.
#It also filters out records where the original
#metar data displayed "\\\" as the wind direction.
#This caused the regular expression to identify
#wind speed and the letter "G" as the wind direction.
#With these unknowns filtered out, all weather data 
#has all records and can be synchronized with the 
#fligth data.

mywd <- "C:/Users/Mark/Documents/By_Subject/Data Science Masters/DS785/Code_Scripts/Output_data/"
setwd(mywd)

weather_df <- read.csv("all_weather_data_comp_4.csv")
summary(weather_df)
new_df <- weather_df[!is.na(weather_df$wind_spd) | length(weather_df$wind_dir)==0,]
new_df2 <- new_df[!(substr(new_df$wind_dir,3,3)=="G"),]
new_df2$wind_dir <- droplevels(new_df2$wind_dir)
new_df2$est_wind_dir <- droplevels((new_df2$est_wind_dir))
write.csv(new_df2,"all_weather_data_comp_5.csv",row.names=FALSE,quote=FALSE)

