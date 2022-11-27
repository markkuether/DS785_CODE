#This script generates a simple CSV
#with an airport identifiers and 
#the N number for an accident airplane.
#The letter "N" is appended to the number
#from the original data file.
#This is used for later analysis.

wd="C:/Users/Mark/Documents/By_Subject/Data Science Masters/DS785/Code_Scripts/Input_Data/"
setwd(wd)

input_file = "LANDING ACCIDENT DATA WITH N NUMBERS.csv"
output_file = "LANDING_PLANE_AIRPORT_COMBO.CSV"
accidents <- read.csv(input_file)
keep <- c("ev_nr_apt_id","N_Number")

accidents <- accidents[,keep]
accidents$N_Number <- as.character(accidents$N_Number)
accidents$N_Number <- paste("N",accidents$N_Number,sep="")
write.csv(accidents,output_file,row.names = FALSE)
