#This code generates a separate
#CSV file with only the N number of
#The accident aircraft and the date
#of the accident. The tail number is
#appended with the letter "N".
#Used for later queries on these
#aircraft.

wd="C:/Users/Mark/Documents/By_Subject/Data Science Masters/DS785/Code_Scripts/Input_Data/"
setwd(wd)

input_file = "LANDING ACCIDENT DATA WITH N NUMBERS.csv"
output_file = "LANDING_DATE_PLANE_COMBO.CSV"
accidents <- read.csv(input_file)
keep <- c("ev_date","N_Number")

accidents <- accidents[,keep]
accidents$N_Number <- as.character(accidents$N_Number)
accidents$N_Number <- paste("N",accidents$N_Number,sep="")
write.csv(accidents,output_file,row.names = FALSE)
