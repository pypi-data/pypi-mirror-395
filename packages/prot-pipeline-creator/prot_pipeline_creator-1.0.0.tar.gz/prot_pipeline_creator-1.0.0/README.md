# PPC - Prot Pipeline Creator

**PPC - Prot Pipeline Creator** is a Python-based tool designed for the bioinformatics processing and analysis of protein data. 

The system is engineered to ingest `.tsv` files from UniProt (UniProtKB), enabling the creation of automated analysis pipelines for filtering, clustering, and generating sub-datasets based on taxonomy (Super Kingdoms), enzymatic activity (EC numbers) and others.    

## 🛠️ Prerequisites

To run this project, you will need:

-   **Python 3.8+**
    
-   **Pandas**
    

## 🚀 Installation

1.  Clone the repository:
    
    Bash
    
    ```bash
    git clone https://github.com/emanuelumbelino/prot-pipeline-creator.git
    cd prot-pipeline-creator
    ```
    
2.  Install dependencies (using a virtual environment is recommended):
    
    Bash
    
    ```bash
    pip install pandas
    ```
    

## 💻 Usage

The project uses the concept of "Pipelines" to execute analyses. You can create your own script or use the templates in the `example/` folder.

### Basic Example

To run the default example included in the project, ensure you have a UniProt data file in the correct format and run:

Bash

```bash
python main.py data/file/path.tsv
```

### Creating a Custom Pipeline

You can use the `PPC_Dataframe` class directly in your Python scripts:

```py
from ppc.protein_dataframe import PPC_Dataframe
from ppc.helpers.printer_helper import PPC_Printer

# 1. Load the DataFrame
file_path = 'path/to/your/uniprot_file.tsv'
df = PPC_Dataframe(file_path)

# 2. Use the filters
bacterias_with_pdb = df.bacteria.has_pdb

# 3. Save all proteins filtered in a .tsv file
bacterias_with_pdb.to_tsv('output/my_analysis.tsv')

# 4. Use the Printer helper to print by ec class
PPC_Printer.print_by_ec_class(bacterias_with_pdb)
```

For a comprehensive list of currently implemented filters, please consult the **Wiki**. It is also possible to create new filters by following the existing ones. 

If you have improvements or suggestions, feel free to submit a **Pull Request** or open an **Issue**.

## 🔬 Available Pipelines

The project already includes three example pipelines in the `example/` folder:

1.  **KingdomPipeline**:
    
    -   Splits the original dataset into 4 `.tsv` files based on Super Kingdoms (Archaea, Bacteria, Eukaryota, Viruses).
        
    -   Generates statistics on sequence and enzyme counts per kingdom.
        
2.  **EnzymesPipeline**:
    
    -   Classifies and separates proteins into the 7 main enzyme classes (EC 1 to EC 7).
        
    -   Generates individual files for each class (e.g., `1_oxidoreductases.tsv`, `2_transferases.tsv`).
        
3.  **AnalogousPipeline**:
    
    -   Focuses on the analysis of **HISE** (Homologous Enzymes) and **NISE** (Non-Homologous/Analogous Enzymes).
        
    -   Clusters enzymes that share the same EC number, verifying if they belong to the same Superfamily or different ones.
        
    -   Filters datasets to contain only enzymes with complete EC numbers and PDB annotation.
        

## 📂 Project Structure

The project is organized as follows:

```
prot-pipeline-creator/
├── ppc/                     # Core source code
│   ├── enums/               # Enumerations for Kingdoms, Columns, and Clusters
│   ├── helpers/             # Helpers for Pandas and Printing
│   ├── clusterized_dataframe.py
│   └── protein_dataframe.py # Main class (Pandas Wrapper)
├── main.py                  # Main entry point
|
|
├── example/                 # Example pipelines and execution scripts
│   ├── output/              # Output directory for examples
│   ├── analogous_pipeline.py
│   ├── enzymes_pipeline.py
│   ├── kingdom_pipeline.py
│   └── example.py
└── LICENSE                  # Apache 2.0 License
```

## 📄 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for more details.

Copyright 2025 - Emanuel Umbelino
