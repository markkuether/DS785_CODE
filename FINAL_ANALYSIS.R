# rem

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

af_dw_delta <- acc_flts$DELTA_DW[acc_flts$DELTA_DW > -9]
af_bs_delta <- acc_flts$DELTA_BASE[acc_flts$DELTA_BASE > -9]
af_fn_delta <- acc_flts$DELTA_FINAL[acc_flts$DELTA_FINAL > -9]
af_vel_delta <- acc_flts$DELTA_VEL

nf_dw_delta <- norm_flts$DELTA_DW[norm_flts$DELTA_DW > -9]
nf_bs_delta <- norm_flts$DELTA_BASE[norm_flts$DELTA_BASE > -9]
nf_fn_delta <- norm_flts$DELTA_FINAL[norm_flts$DELTA_FINAL >-9]
nf_vel_delta <- norm_flts$DELTA_VEL

ap_dw_delta <- acc_plts$DELTA_DW[acc_plts$DELTA_DW >-9]
ap_bs_delta <- acc_plts$DELTA_BASE[acc_plts$DELTA_BASE > -9]
ap_fn_delta <- acc_plts$DELTA_FINAL[acc_plts$DELTA_FINAL > -9]
ap_vel_delta <- acc_plts$DELTA_VEL

np_dw_delta <- norm_plts$DELTA_DW[norm_plts$DELTA_DW > -9]
np_bs_delta <- norm_plts$DELTA_BASE[norm_plts$DELTA_BASE > -9]
np_fn_delta <- norm_plts$DELTA_FINAL[norm_plts$DELTA_FINAL >-9]
np_vel_delta <- norm_plts$DELTA_VEL


#Medians and Means
all_dw_delta_med <- median(all_dw_delta)
all_bs_delta_med <- median(all_bs_delta)
all_fn_delta_med <- median(all_fn_delta)
all_vel_delta_mean <- mean(all_vel_delta)

af_dw_delta_med <- median(af_dw_delta)
af_bs_delta_med <- median(af_bs_delta)
af_fn_delta_med <- median(af_fn_delta)
af_vel_delta_mean <- mean(af_vel_delta)

nf_dw_delta_med <- median(nf_dw_delta)
nf_bs_delta_med <- median(nf_bs_delta)
nf_fn_delta_med <- median(nf_fn_delta)
nf_vel_delta_mean <- mean(nf_vel_delta)

ap_dw_delta_med <- median(ap_dw_delta)
ap_bs_delta_med <- median(ap_bs_delta)
ap_fn_delta_med <- median(ap_fn_delta)
ap_vel_delta_mean <- mean(ap_vel_delta)

np_dw_delta_med <- median(np_dw_delta)
np_bs_delta_med <- median(np_bs_delta)
np_fn_delta_med <- median(np_fn_delta)
np_vel_delta_mean <- mean(np_vel_delta)


xlab_st = "Degrees Off Heading"
xlab_vel = "Knots From Desired Target"
ad = "All Data"
af = "Accident Flights"
naf = "Non-Accident Flights"
ap = "Accident Pilots"
nap = "Non-Accident Pilots"
dwstr = "Downwind\n"
bsstr = "Base\n"
fnstr = "Final\n"
velstr = "Velocity\n"

#historgram charts
hist(all_dw_delta, xlab=xlab_st, main=ad,xlim=c(0,25));abline(v=all_dw_delta_med,col="red",lwd=2)
hist(af_dw_delta, xlab=xlab_st, main=af,xlim=c(0,25));abline(v=af_dw_delta_med,col="red",lwd=2)
hist(nf_dw_delta,xlab=xlab_st, main=naf,xlim=c(0,25));abline(v=nf_dw_delta_med,col="red",lwd=2)
hist(ap_dw_delta,xlab=xlab_st, main=ap,xlim=c(0,25));abline(v=ap_dw_delta_med,col="red",lwd=2)
hist(np_dw_delta,xlab=xlab_st, main=nap,xlim=c(0,25));abline(v=np_dw_delta_med,col="red",lwd=2)

hist(all_bs_delta, xlab=xlab_st, main=ad,xlim=c(0,45));abline(v=all_bs_delta_med,col="red",lwd=2)
hist(af_bs_delta, xlab=xlab_st, main=af,xlim=c(0,45));abline(v=af_bs_delta_med,col="red",lwd=2)
hist(nf_bs_delta, xlab=xlab_st, main=naf,xlim=c(0,45));abline(v=nf_bs_delta_med,col="red",lwd=2)
hist(ap_bs_delta, xlab=xlab_st, main=ap,xlim=c(0,45));abline(v=ap_bs_delta_med,col="red",lwd=2)
hist(np_bs_delta, xlab=xlab_st, main=nap,xlim=c(0,45));abline(v=np_bs_delta_med,col="red",lwd=2)

hist(all_fn_delta, xlab=xlab_st, main=ad,xlim=c(0,25));abline(v=all_fn_delta_med,col="red",lwd=2)
hist(af_fn_delta, xlab=xlab_st, main=af,xlim=c(0,25));abline(v=af_fn_delta_med,col="red",lwd=2)
hist(nf_fn_delta, xlab=xlab_st, main=naf,xlim=c(0,25));abline(v=nf_fn_delta_med,col="red",lwd=2)
hist(ap_fn_delta, xlab=xlab_st, main=ap,xlim=c(0,25));abline(v=ap_fn_delta_med,col="red",lwd=2)
hist(np_fn_delta, xlab=xlab_st, main=nap,xlim=c(0,25));abline(v=np_fn_delta_med,col="red",lwd=2)

hist(all_vel_delta,xlab=xlab_vel, main=ad,xlim=c(-50,50));abline(v=all_vel_delta_mean ,col="blue",lwd=2)
hist(af_vel_delta, xlab=xlab_vel, main=af,xlim=c(-50,50));abline(v=af_vel_delta_mean ,col="blue",lwd=2)
hist(nf_vel_delta, xlab=xlab_vel, main=naf,xlim=c(-50,50));abline(v=nf_vel_delta_mean ,col="blue",lwd=2)
hist(ap_vel_delta, xlab=xlab_vel, main=ap,xlim=c(-50,50));abline(v=ap_vel_delta_mean ,col="blue",lwd=2)
hist(np_vel_delta, xlab=xlab_vel, main=nap,xlim=c(-50,50));abline(v=np_vel_delta_mean ,col="blue",lwd=2)

#Data Distribution
data_vals <- c(505,3975,1825,2655)
name_vals <- c("Accident Flights","Non-Accident Flights","Accident Pilots","Non-Accident Pilots")
barplot(data_vals,names.arg=name_vals,ylab="Number Of Records",main="Record Count per Category",ylim=c(0,4000))


