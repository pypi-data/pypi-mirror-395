#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
dat_file <- args[1]
plot_dir <- args[2]

library(ggplot2)

# Load data
df <- read.table(dat_file, header=TRUE, sep="\t")

# Parameters
binwidth <- 0.01
breaks <- seq(0, 1, by=binwidth)
breaks_mid <- head(breaks, -1) + binwidth/2

# Function to compute counts per bin
compute_counts <- function(df_sub, value_col="gap_fraction") {
  df_sub$bin <- cut(df_sub[[value_col]], breaks=breaks, include.lowest=TRUE, right=FALSE)
  tab <- as.data.frame(table(df_sub$bin))
  names(tab) <- c("bin", "count")
  tab$mid <- breaks_mid[match(as.character(tab$bin), levels(df_sub$bin))]
  return(tab)
}

# --- Plot 1: per Feature, RF vs no_x ---
tab_list <- lapply(split(df, df$feature), function(sub_df) {
  counts_rf <- compute_counts(sub_df[sub_df$rf == "x",])
  counts_no <- compute_counts(sub_df[sub_df$rf != "x",])
  counts_rf$rf <- "x"
  counts_no$rf <- "no_x"
  counts_rf$feature <- sub_df$feature[1]
  counts_no$feature <- sub_df$feature[1]
  rbind(counts_rf, counts_no)
})
tab1 <- do.call(rbind, tab_list)

p1 <- ggplot(tab1, aes(x = mid, y = count, color = rf)) +
  geom_line() +
  facet_wrap(~feature, scales="free_y") +
  labs(x="Gap fraction per column",
       y=paste0("Number of columns per bin (binwidth=", binwidth,")"),
       color="RF annotation") +
  ggtitle("Distribution of gap fractions per feature") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))
ggsave(file.path(plot_dir, "gapfractions_per_feature.png"), p1, width=12, height=6, bg="white")

# --- Plot 2: all Features summed, RF: x vs no_x ---
tab_list2 <- lapply(split(df, df$rf), function(sub_df) compute_counts(sub_df))
tab2 <- do.call(rbind, tab_list2)
tab2$rf <- rep(names(split(df, df$rf)), each=length(breaks_mid))

p2 <- ggplot(tab2, aes(x = mid, y = count, color = rf, fill = rf)) +
  geom_line(size=0.8) +
  labs(x="Gap fraction per column",
       y=paste0("Number of columns per bin (binwidth=", binwidth,")"),
       color="RF annotation",
       fill="RF annotation") +
  ggtitle("Distribution of gap fractions, summed over all features") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))
ggsave(file.path(plot_dir, "gapfractions_sum.png"), p2, width=10, height=5, bg="white")
