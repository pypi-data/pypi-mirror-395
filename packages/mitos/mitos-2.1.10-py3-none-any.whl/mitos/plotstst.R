#!/usr/bin/env Rscript
# parameters
# 1. stst.dat
# 2. output directory

library(ggplot2)
library(reshape2)
library(scales)

asinh_breaks <- function(x) {
  br <- function(r) {
    lmin <- round(log10(r[1]))
    lmax <- round(log10(r[2]))
    lbreaks <- seq(lmin, lmax, by = 1)
    breaks <- 10 ^ lbreaks
  }
  p.rng <- range(x[x > 0], na.rm = TRUE)
  breaks <- br(p.rng)
  if (min(x) <= 0) {breaks <- c(0, breaks)}
  if (sum(x < 0) > 1) { #more negative values that expected from expanding scale that includes zero
    n.rng <- rev(-range(x[x < 0], na.rm = TRUE))
    breaks <- c(breaks, -br(n.rng))
  }
  return(sort(breaks))
}

asinh_trans <- function() {
  trans_new("asinh",
            transform = asinh,
            inverse   = sinh,
            breaks = asinh_breaks)
}



args<-commandArgs(T)

t <- read.table(args[1], col.names= c("start", "stop", "gene", "strand", "begin","end","pvalue","value" , "ci" , "qi" , "di" , "fi" , "mi" , "cj" , "qj" , "dj" , "fj" , "mj"), stringsAsFactors=FALSE)


#t$pvalue=1+t$pvalue
#t$value=1+t$value


pdf(paste(args[2],"/stst-value.pdf" ,sep="" ), width=4.5, height=3)

for(g in unique(t$gene)){
	T<-subset(t, gene==g)
	for(p in unique(T$start)){
		P <- T[ which(T$start==p), ]
		# plot top 100 values
		Q<-(subset(P, value>0))
		if(nrow(Q) == 0){
			next
		}
#		pdf(paste(args[2],"/", g, "-",p,"-value.pdf" ,sep="" ))
		plot <- ggplot(Q)+
# 			geom_tile(aes(x=factor(begin), y=factor(end), fill=log(value+sqrt(value^2 +1))))+
			geom_tile(aes(x=factor(begin), y=factor(end), fill=value), color="black")+
			scale_x_discrete(name="start")+
			scale_y_discrete(name="stop")+
#			scale_fill_gradientn(colours = rainbow(7), name="V")+
#			scale_fill_gradientn(colours = rainbow(7))+
			scale_fill_gradient( low="white", high="black", name="p")+
			theme_bw(base_size=15)+
			theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
			ggtitle(paste( g, p ))
		print(plot)
#		x<-dev.off()


	}
}
x<-dev.off()

t$ashpval <- log10(t$pvalue+sqrt(t$pvalue^2 +1))

pdf(paste(args[2],"/stst-pvalue.pdf" ,sep="" ), width=4.5, height=3)
for(g in unique(t$gene)){
	T<-subset(t, gene==g)
	for(p in unique(T$start)){
		P <- T[ which(T$start==p), ]
		Q<-(subset(P, value>0))
		if(nrow(Q) == 0){
			next
		}
		plot <- ggplot(Q)+
			geom_tile(aes(x=factor(begin), y=factor(end), fill=pvalue), color="black")+
			scale_x_discrete(name="start")+
			scale_y_discrete(name="stop")+
#			scale_fill_gradientn( colours = rainbow(7), name="p")+
			scale_fill_gradient( low="white", high="black", name="p")+
			theme_bw(base_size=15)+
			theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
			ggtitle(paste( g, p ))
		print(plot)
	}
}
x<-dev.off()

a<-subset(t, select=c("gene","strand","start","stop","begin","ci","fi","qi","di","mi" ))
if(nrow(a)>0){
	a$region<-"begin"
	a<-unique(a)
	names(a)<-c("gene", "strand", "start","stop", "p", "codon","codfreq","quality","distance", "tmalus", "region")
}

b<-subset(t, select=c("gene","strand","start","stop","end","cj","fj","qj","dj","mj" ))
if(nrow(b)>0){
	b$region<-"end"
	b<-unique(b)
	names(b)<-c("gene", "strand", "start","stop", "p", "codon","codfreq","quality","distance", "tmalus", "region")
}

t<-rbind(a,b)

pdf(paste(args[2],"/stst.pdf" ,sep="" ), height=9, width=19)
for(g in unique(t$gene)){
	T<-subset(t, gene==g & codfreq > 0)
#	print(T)
	for(p in unique(T$start)){
		Q <- T[ which(T$start==p), ]

		q <- melt(Q, id=c("gene","strand", "start","stop", "p","codon","codfreq","quality","distance", "tmalus"))
		q$iquality <- q$quality > 0
# 		print(paste(g,p))
# 		print(q)
		#pdf(paste(args[2],"/", g, "-",p,".pdf" ,sep="" ), width=30)
  		plot <- ggplot(q) +
			geom_bar( aes(x=factor(p), y=codfreq ), stat="identity", width=1, color="black", fill="lightgray")+
#			geom_point( aes(x=p, y=quality ), show.legend = FALSE)+
			geom_point( aes(x=factor(p), y=distance ))+
# 			geom_text( aes(x=p, label=p), y=0.75, angle=90, size=4 )+
			geom_text( aes(x=factor(p), label=codon), y=0.28, angle=90, size=5 )+
			facet_wrap( ~value, ncol=1, scales="free_x" )+
			ggtitle(paste(g,p)) +
			# scale_x_continuous(name="position")
			scale_x_discrete( name = "position") +
			theme_bw( base_size = 30 ) +
			theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
			#+
			#scale_y_continuous(breaks=1:10/10)
		print(plot)
		#x<-dev.off()
	}
}
x<-dev.off()

# warnings()
