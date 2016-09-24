#!/usr/bin/Rscript
library(data.table)
library(ggplot2)

args = commandArgs(trailingOnly=TRUE)
if(length(args)==0){
    stop("You have to provide a file name.")
}
filename=args[1]

factor<-1
if(length(args)>1 & args[2]=="invert"){
    factor=-1
}
print(factor)

data <- read.csv(paste(filename,".csv", sep=""))
data$timestamp=round(data$timestamp/1000)
data$value=factor*data$value

lo <- loess(data$value~data$timestamp)
minTime=min(data$timestamp)
maxTime=max(data$timestamp)
smoothedTime=seq(minTime, maxTime, 1)
smoothedValues=predict(lo, smoothedTime)

data$timestamp <- as.POSIXct(data$timestamp, origin="1970-01-01")
smoothedTimestamp=as.POSIXct(smoothedTime, origin="1970-01-01")

png(paste(filename, ".png", sep=""))
qplot(data$timestamp, data$value)+geom_point(aes(x=smoothedTimestamp, y=smoothedValues))
dev.off()

dt1=data.table(data)
setkey(dt1, timestamp)
dt2=data.table(timestamp=smoothedTimestamp, valueSmoothed=smoothedValues)
setkey(dt2, timestamp)

merged<-dt1[dt2,]
analysed<-merged[,list(
    timestamp=timestamp,
    value=ifelse(is.na(value), valueSmoothed, value)
)]

png(paste(filename, "_analysed.png", sep=""))
qplot(analysed$timestamp, analysed$value)
dev.off()

write.csv(analysed, paste(filename, "_analysed.csv", sep=""))
