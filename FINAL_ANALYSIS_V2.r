library(ggpubr)
#This script is used to calculate final
#statistics for analysis

mywd <- "D:/output/csv_unfiltered/v24"
setwd(mywd)

#Get flight data categorized with a Landing_Phase
all_data <- read.csv("all_data_v4.csv")
flight_data <- all_data[all_data$Landing_phase!="",]
rm(all_data)

#Separate accident from non-accident flights
acc_flts <- flight_data[flight_data$acc_flight==TRUE,]
norm_flts <- flight_data[flight_data$acc_flight==FALSE,]

#Separate accident pilots form non-acc pilots
acc_plts <- flight_data[flight_data$acc_pilot=="YES",]
norm_plts <- flight_data[flight_data$acc_pilot=="NO",]

#distribution of delta's for all flights
#delta for downwind
all_dw_delta <- flight_data$DELTA_DW[flight_data$DELTA_DW > -9]
all_bs_delta <- flight_data$DELTA_BASE[flight_data$DELTA_BASE > -9]
all_fn_delta <- flight_data$DELTA_FINAL[flight_data$DELTA_FINAL > -9]
all_vel_delta <- flight_data$DELTA_VEL
all_data <- list(all_dw_delta,all_bs_delta,all_fn_delta,all_vel_delta)

af_dw_delta <- acc_flts$DELTA_DW[acc_flts$DELTA_DW > -9]
af_bs_delta <- acc_flts$DELTA_BASE[acc_flts$DELTA_BASE > -9]
af_fn_delta <- acc_flts$DELTA_FINAL[acc_flts$DELTA_FINAL > -9]
af_vel_delta <- acc_flts$DELTA_VEL
all_data[5:8] <- list(af_dw_delta,af_bs_delta,af_fn_delta,af_vel_delta)

nf_dw_delta <- norm_flts$DELTA_DW[norm_flts$DELTA_DW > -9]
nf_bs_delta <- norm_flts$DELTA_BASE[norm_flts$DELTA_BASE > -9]
nf_fn_delta <- norm_flts$DELTA_FINAL[norm_flts$DELTA_FINAL >-9]
nf_vel_delta <- norm_flts$DELTA_VEL
all_data[9:12] <- list(nf_dw_delta,nf_bs_delta,nf_fn_delta,nf_vel_delta)

ap_dw_delta <- acc_plts$DELTA_DW[acc_plts$DELTA_DW >-9]
ap_bs_delta <- acc_plts$DELTA_BASE[acc_plts$DELTA_BASE > -9]
ap_fn_delta <- acc_plts$DELTA_FINAL[acc_plts$DELTA_FINAL > -9]
ap_vel_delta <- acc_plts$DELTA_VEL
all_data[13:16] <- list(ap_dw_delta,ap_bs_delta,ap_fn_delta,ap_vel_delta)

np_dw_delta <- norm_plts$DELTA_DW[norm_plts$DELTA_DW > -9]
np_bs_delta <- norm_plts$DELTA_BASE[norm_plts$DELTA_BASE > -9]
np_fn_delta <- norm_plts$DELTA_FINAL[norm_plts$DELTA_FINAL >-9]
np_vel_delta <- norm_plts$DELTA_VEL
all_data[17:20] <- list(np_dw_delta,np_bs_delta,np_fn_delta,np_vel_delta)


all <- c(1:4)
af <- c(5:8)
nf <- c(9:12)
ap <- c(13:16)
np <- c(17:20)
dw <- c(1,5,9,13,17)
bs <- c(2,6,10,14,18)
fn <- c(3,7,11,15,19)
vel <- c(4,8,12,16,20)
sspos <- 1
phpos <- 2
estpos <- 3
lclpos <- 4
uclpos <- 5

qq_ap_vel <- ggqqplot(ap_vel_delta) + 
  ggtitle("Accident Pilots\nVelocity") +
  theme(plot.title = element_text(hjust=0.5))
qq_ap_vel

qq_np_vel <- ggqqplot(np_vel_delta) + 
  ggtitle("Non-Accident Pilots\nVelocity") +
  theme(plot.title = element_text(hjust=0.5))
qq_np_vel



#BOXPLOTS
xlabs <- c("Non-Accident Pilot","Accident Pilot")
boxplot(np_dw_delta,ap_dw_delta,names=xlabs,
        ylab="Difference in Degrees",main="Heading Delta\nDownwind Phase")

boxplot(np_bs_delta,ap_bs_delta,names=xlabs,
        ylab="Difference in Degrees",main="Heading Delta\nBase Phase")

boxplot(np_fn_delta,ap_fn_delta,names=xlabs,
        ylab="Difference in Degrees",main="Heading Delta\nFinal Phase")

boxplot(np_vel_delta,ap_vel_delta,names=xlabs,
        ylab="Difference in Knots",main="Relative Velocity\nAll Phases")

#WILCOX SUM TEST
wilcox.test(ap_dw_delta,np_dw_delta,conf.int = TRUE, conf.level = .95)
wilcox.test(ap_bs_delta,np_bs_delta,conf.int = TRUE, conf.level = .95)
wilcox.test(ap_fn_delta,np_fn_delta,conf.int = TRUE, conf.level = .95)
wilcox.test(ap_vel_delta,np_vel_delta,conf.int = TRUE, conf.level = .95)

wilcox.test(ap_dw_delta,np_dw_delta,conf.int = TRUE, conf.level = .95,
            alternative = "greater")
wilcox.test(ap_bs_delta,np_bs_delta,conf.int = TRUE, conf.level = .95,
            alternative = "greater")
wilcox.test(ap_fn_delta,np_fn_delta,conf.int = TRUE, conf.level = .95,
            alternative = "greater")
wilcox.test(ap_vel_delta,np_vel_delta,conf.int = TRUE, conf.level = .95,
            alternative = "greater")

