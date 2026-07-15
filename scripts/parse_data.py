#!/usr/bin/env python3
"""
Шаг 1 Пайплайна: Консолидация и очистка метаданных штаммов из BV-BRC.
"""

import os
import glob
import logging
import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Настройка путей относительно корня проекта
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
REFS_DIR = os.path.join(BASE_DIR, 'data', 'refs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True) 
    logging.info("--- Шаг 1: Консолидация метаданных ---")

    # Поиск файлов метаданных
    bvbrc_files = glob.glob(os.path.join(RAW_DIR, "BVBRC_genome*.csv"))
    if not bvbrc_files:
        logging.error(f"Файлы BVBRC_genome*.csv не найдены в {RAW_DIR}")
        return

    logging.info(f"Найдено файлов для объединения: {len(bvbrc_files)}")
    
    # Объединение таблиц
    dfs = []
    for file_path in bvbrc_files:
        try:
            df = pd.read_csv(file_path, dtype={'Genome ID': str})
            dfs.append(df)
            logging.info(f"  Успешно прочитан: {os.path.basename(file_path)}")
        except Exception as e:
            logging.warning(f"Ошибка при чтении {os.path.basename(file_path)}: {e}")

    if not dfs:
        logging.error("Не удалось прочитать ни одного файла метаданных.")
        return

    combined_genomes = pd.concat(dfs, ignore_index=True)
    total_raw = len(combined_genomes)

    # Дедупликация
    combined_genomes.drop_duplicates(subset=['Genome ID'], inplace=True)
    total_unique = len(combined_genomes)
    logging.info(f"Объединение завершено: {total_raw} строк -> {total_unique} уникальных штаммов.")

    # Сохранение результатов
    output_file = os.path.join(OUTPUT_DIR, "combined_metadata.csv")
    combined_genomes.to_csv(output_file, index=False)
    logging.info(f"Чистые метаданные сохранены в: {output_file}")

if __name__ == "__main__":
    main()