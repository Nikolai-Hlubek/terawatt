#!/usr/bin/Rscript
library(data.table)
library(ggplot2)

data <- read.csv('pv_wirk.csv')
data$value <- -1*data$value
data$timestamp=round(data$timestamp/1000)

lo <- loess(data$value~data$timestamp)
minTime=min(data$timestamp)
maxTime=max(data$timestamp)
smoothedTime=seq(minTime, maxTime, 1)
smoothedValues=predict(lo, smoothedTime)

data$timestamp <- as.POSIXct(data$timestamp, origin="1970-01-01")
smoothedTimestamp=as.POSIXct(smoothedTime, origin="1970-01-01")

png("pv_wirk.png")
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

png("pv_wirk_analysed.png")
qplot(analysed$timestamp, analysed$value)
dev.off()

write.csv(analysed, "pv_wirk_analysed.csv")
