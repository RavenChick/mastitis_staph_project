#!/usr/bin/env Rscript
# Шаг 3 Пайплайна: Построение тепловой карты профилей AMR с иерархической кластеризацией.

# Настройка путей
initial.options <- commandArgs(trailingOnly = FALSE)
file.arg.name <- "--file="
script.name <- sub(file.arg.name, "", initial.options[grep(file.arg.name, initial.options)])
script.dir <- dirname(script.name)

# Если запускаем интерактивно, берем текущую директорию
if (length(script.dir) == 0) {
  script.dir <- "scripts"
}

base_dir <- file.path(script.dir, "..")
matrix_path <- file.path(base_dir, "data", "processed", "amr_presence_absence.csv")
plot_output_dir <- file.path(base_dir, "results", "plots")

dir.create(plot_output_dir, showWarnings = FALSE, recursive = TRUE)

message("--- Шаг 3: Построение тепловой карты в R ---")

if (!file.exists(matrix_path)) {
  stop(paste("Матрица не найдена по пути:", matrix_path, "\nЗапустите сначала parse_annotation.py!"))
}

# Читаем данные (ID геномов делаем именами строк)
amr_data <- read.csv(matrix_path, header = TRUE, row.names = 1, check.names = FALSE)
amr_matrix <- as.matrix(amr_data)

# Проверяем, что матрица не пустая
if (ncol(amr_matrix) == 0 || nrow(amr_matrix) == 0) {
  stop("Матрица пуста или некорректно отформатирована.")
}

# Настройка вывода графика в PNG
output_image <- file.path(plot_output_dir, "amr_genes_heatmap.png")
png(filename = output_image, width = 1000, height = 800, res = 120)

# Цветовая палитра: белый (отсутствие) и сине-зеленый (присутствие)
colors <- c("#f0f0f0", "#1b9e77")

# Отрисовка тепловой карты с иерархической кластеризацией методом Уорда (Ward.D2)
heatmap(amr_matrix, 
        distfun = function(x) dist(x, method = "euclidean"),
        hclustfun = function(x) hclust(x, method = "ward.D2"),
        col = colors, 
        main = "Профили генов AMR штаммов S. aureus",
        xlab = "Целевые гены резистентности",
        ylab = "Штаммы (Genome ID)",
        margins = c(7, 7),
        scale = "none")

dev.off()
message(paste("Тепловая карта успешно сохранена в:", output_image))