# Mastitis Staph AMR Analysis Pipeline

A toolkit for the automated bioinformatic analysis of Staphylococcus aureus genomes isolated from clinical bovine mastitis cases.
The pipeline transforms raw metadata and annotations (BV-BRC) into a structured knowledge base (Obsidian) and provides visualized antimicrobial resistance (AMR) profiles.

## 🧬 Project Objectives
*  **Data Consolidation:** An ETL process for cleaning and deduplicating metadata for 26+ strains.
*  **Genomic Screening:** Automated searching for target AMR loci within FASTA annotations.
*  **Knowledge Integration:** Automated generation of Obsidian strain cards (Markdown/YAML) containing metadata and AMR screening results.
*  **Visualization:** Construction of hierarchical heatmaps to identify hidden pathogen subpopulations.

## 📂 Project Structure
Plaintext
├── data/               # Raw and processed data (metadata, references)
├── notebooks/          # Jupyter notebooks for exploratory data analysis
├── results/            # Final visualizations and tables
├── scripts/            # Modular data processing pipeline
│   ├── parse_data.py         # Step 1: Metadata cleaning
│   ├── parse_annotation.py   # Step 2: Gene analysis and report generation
│   └── build_heatmap.R       # Step 3: Statistical visualization
├── obsidian_vault/     # Generated strain cards
└── README.md
## 🚀 Quickstart
1. Requirements and Installation
The pipeline requires Python 3.8+ and R (for generating final plots).
Clone the repository and install the dependencies:

```bash
git clone https://github.com/RavenChick/mastitis_staph_project.git
cd mastitis_staph_project
pip install -r requirements.txt
```

Инструментарий для автоматизированного биоинформатического анализа геномов *Staphylococcus aureus*, выделенных из клинических случаев мастита КРС. 

Пайплайн позволяет трансформировать сырые метаданные и аннотации (BV-BRC) в структурированную базу знаний (Obsidian) и визуализированные профили антибиотикорезистентности (AMR).

## 🧬 Основные задачи проекта
*   **Консолидация данных:** ETL-процесс для очистки и дедупликации метаданных 26+ штаммов.
*   **Геномный скрининг:** Автоматизированный поиск целевых локусов антибиотикорезистентности в FASTA-аннотациях.
*   **Интеграция знаний:** Автоматическая генерация карточек штаммов для Obsidian (Markdown/YAML) с метаданными и результатами AMR-скрининга.
*   **Визуализация:** Построение иерархических тепловых карт для идентификации скрытых субпопуляций патогенов.

## 📂 Структура проекта
```text
├── data/               # Сырые и обработанные данные (метаданные, референсы)
├── notebooks/          # Jupyter-ноутбуки для исследовательского анализа данных
├── results/            # Итоговые визуализации и таблицы
├── scripts/            # Модульный пайплайн обработки данных
│   ├── parse_data.py         # Шаг 1: Очистка метаданных
│   ├── parse_annotation.py   # Шаг 2: Анализ генов и генерация отчетов
│   └── build_heatmap.R       # Шаг 3: Статистическая визуализация
├── obsidian_vault/     # Сгенерированные карточки штаммов
└── README.md
```
## 🚀 Быстрый старт

### 1. Требования и установка
Для работы пайплайна требуются Python 3.8+ и R (для построения финальных графиков). 
Клонируйте репозиторий и установите зависимости:

```bash
git clone https://github.com/RavenChick/mastitis_staph_project.git
cd mastitis_staph_project
pip install -r requirements.txt
```
