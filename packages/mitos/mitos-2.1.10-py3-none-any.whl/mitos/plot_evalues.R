#!/usr/bin/env Rscript

# creates a stacked bar plot of Best vs Discarded HMMER E-values.
# Usage: Rscript plot_evalues.R <best_file> <discarded_file> <output_dir> [outfile.png] [plot_title]

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) stop("Usage: plot_evalues.R <best_file> <discarded_file> <output_dir> [outfile.png] [plot_title]")

best_file      <- args[1]
discarded_file <- args[2]
output_dir     <- args[3]
outfile        <- if (length(args) >= 4) file.path(output_dir, args[4]) else file.path(output_dir, "evalues.png")
plot_title     <- if (length(args) >= 5) args[5] else "Distribution of HMMER E-values"

suppressPackageStartupMessages({
  library(ggplot2)
  library(scales)
})

# --- Load data ---
best_values <- scan(best_file, quiet = TRUE)
discarded_values <- scan(discarded_file, quiet = TRUE)

best <- data.frame(
  evalue = best_values,
  type = rep("best hits", length(best_values))
)
discarded <- data.frame(
  evalue = discarded_values,
  type = rep("discarded hits", length(discarded_values))
)

data <- rbind(best, discarded)

# Handle zero e-values
if (any(data$evalue == 0)) {
  min_nonzero <- min(data$evalue[data$evalue > 0])
  data$evalue[data$evalue == 0] <- min_nonzero
}

data$log10e <- log10(data$evalue)

# --- Prepare legend labels with total counts ---
total_best <- nrow(best)
total_discarded <- nrow(discarded)
data$type <- factor(data$type, levels = c("best hits", "discarded hits"))
levels(data$type) <- c(
  paste0("best hits (n=", total_best, ")"),
  paste0("discarded hits (n=", total_discarded, ")")
)

# --- 50 bins ---
bins <- seq(min(data$log10e), max(data$log10e), length.out = 51)
data$bin <- cut(data$log10e, breaks = bins, include.lowest = TRUE, labels = FALSE)

# --- Count per bin and type ---
counts <- as.data.frame(table(bin = data$bin, type = data$type))
names(counts)[3] <- "count"

# --- X-axis: integer exponents, max 7 ---
log_min <- floor(min(data$log10e))
log_max <- ceiling(max(data$log10e))
ticks <- seq(log_min, log_max, length.out = 7)
tick_bins <- sapply(ticks, function(x) which.min(abs(bins[-length(bins)] - x)))
tick_labels <- sapply(round(ticks), function(x) bquote(10^.(x)))
tick_labels <- parse(text = tick_labels)

# --- Plot ---
p <- ggplot(counts, aes(x = as.numeric(bin), y = count, fill = type)) +
  geom_bar(stat = "identity", position = position_stack(reverse = TRUE), color = "black", linewidth = 0.2) +
  scale_fill_manual(values = c("#619CFF", "#F8766D")) +
  scale_x_continuous(breaks = tick_bins, labels = tick_labels, expand = c(0, 0)) +
  theme_minimal(base_size = 13) +
  theme(axis.text.x = element_text(hjust = 0.5), legend.position = "top") +
  labs(title = plot_title, x = "E-value", y = "Count", fill = "")

ggsave(outfile, p, width = 8, height = 6, dpi = 150, bg = "white")
