#!/usr/bin/env python3
"""
Шаг 2 Пайплайна: Анализ FASTA-аннотаций и детекция генов антибиотикорезистентности (AMR).
Генерирует бинарную матрицу присутствия/отсутствия генов и карточки Obsidian.
"""

import os
import logging
import pandas as pd
from Bio import SeqIO

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
REFS_DIR = os.path.join(BASE_DIR, "data", "refs")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")
VAULT_DIR = os.path.join(BASE_DIR, "obsidian_vault")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(VAULT_DIR, exist_ok=True)
    
    logging.info("--- Шаг 2: Анализ FASTA и детекция генов ---")
    
    # 1. Загрузка метаданных штаммов
    metadata_path = os.path.join(OUTPUT_DIR, "combined_metadata.csv")
    if not os.path.exists(metadata_path):
        logging.error(f"Метаданные не найдены! Сначала запустите parse_data.py")
        return
    combined_genomes = pd.read_csv(metadata_path, dtype={'Genome ID': str})

    # 2. Загрузка целевых генов
    genes_file = os.path.join(REFS_DIR, "target_resistance_genes.csv")
    if not os.path.exists(genes_file):
        logging.error(f"Файл референсных генов не найден: {genes_file}")
        return
    genes_df = pd.read_csv(genes_file)
    genes_dict = dict(zip(genes_df['Gene_Name'], genes_df['Function']))
    target_genes = genes_df['Gene_Name'].tolist()

    # Инициализация профиля резистентности (по умолчанию False/0)
    resistance_profile = {
        gid: {gene: 0 for gene in target_genes} for gid in combined_genomes['Genome ID']
    }

    # 3. Парсинг FASTA
    fasta_path = os.path.join(RAW_DIR, "annotation.feature_dna.fasta")
    if not os.path.exists(fasta_path):
        logging.error(f"Файл FASTA {fasta_path} не найден!")
        return

    logging.info(f"Парсинг {os.path.basename(fasta_path)} через Biopython...")
    for record in SeqIO.parse(fasta_path, "fasta"):
        header = record.description
        
        # Поиск Genome ID в заголовке
        current_gid = None
        for gid in resistance_profile.keys():
            if gid in header:
                current_gid = gid
                break
        
        if current_gid:
            for gene in target_genes:
                if gene.lower() in header.lower():
                    # Присваиваем 1 (присутствие гена)
                    resistance_profile[current_gid][gene] = 1

    logging.info("Анализ последовательностей успешно завершен.")

    # 4. Сохранение бинарной матрицы (AMR Matrix)
    matrix_df = pd.DataFrame.from_dict(resistance_profile, orient='index')
    matrix_df.index.name = 'Genome_ID'
    matrix_output_path = os.path.join(OUTPUT_DIR, "amr_presence_absence.csv")
    matrix_df.to_csv(matrix_output_path)
    logging.info(f"Бинарная матрица AMR сохранена в: {matrix_output_path}")

    # 5. Генерация карточек для Obsidian
    logging.info("Генерация карточек Obsidian...")
    for idx, row in combined_genomes.iterrows():
        gid = str(row.get('Genome ID', ''))
        if not gid:
            continue
            
        name = row.get('Genome Name', 'Staphylococcus aureus')
        country = row.get('Isolation Country', 'Не указана')
        source = row.get('Isolation Source', 'Не указан')
        year = row.get('Collection Year', 'Неизвестен')
        mlst = row.get('MLST', 'Не определен')
        
        safe_name = f"Strain_{gid.replace('.', '_')}"
        file_path = os.path.join(VAULT_DIR, f"{safe_name}.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"type: microorganism_card\n")
            f.write(f"genome_id: \"{gid}\"\n")
            f.write(f"country: \"{country}\"\n")
            f.write(f"source: \"{source}\"\n")
            f.write(f"mlst: \"{mlst}\"\n")
            f.write("---\n\n")
            
            f.write(f"# 🧫 {name}\n\n")
            f.write(f"## 📋 Общая информация\n")
            f.write(f"* **ID Генома:** `{gid}`\n")
            f.write(f"* **Страна изоляции:** {country}\n")
            f.write(f"* **Источник:** {source}\n")
            f.write(f"* **Год сбора:** {year}\n")
            f.write(f"* **MLST профиль:** `{mlst}`\n\n")
            
            f.write(f"## 🧬 Профиль антибиотикорезистентности\n")
            f.write(f"На основе геномных аннотаций:\n\n")
            
            for gene in target_genes:
                is_present = resistance_profile[gid][gene] == 1
                status = "🟢 **Обнаружен**" if is_present else "❌ Не найден"
                description = genes_dict.get(gene, "")
                f.write(f"* {status} — **{gene}** *({description})*\n")
                
            f.write("\n---\n")
            f.write(f"*Дата генерации профиля: 2026-07-14*")
            
    logging.info(f"Все карточки сохранены в: {VAULT_DIR}")

if __name__ == "__main__":
    main()