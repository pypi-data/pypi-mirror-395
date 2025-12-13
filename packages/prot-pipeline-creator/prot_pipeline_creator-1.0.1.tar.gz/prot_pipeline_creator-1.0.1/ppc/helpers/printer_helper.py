import sys

from ppc.protein_dataframe import PPC_Dataframe
from ppc.enums.clusters import PPC_Clusters

class PPC_Printer():
    
    def print_in_file(path: str, df: PPC_Dataframe, f):
        original_stdout = sys.stdout
        try: 
            print()
            print(f"Initiate print in file: {path}.")
            with open(path, 'w', encoding='utf-8') as file_output:
                sys.stdout = file_output
                f(df)
            sys.stdout = original_stdout
            print(f"File Writing completed successfully!")
        except FileNotFoundError:
            sys.stdout = original_stdout
            print(f"Error: The file ({path}) was not found.")
        except Exception as e:
            sys.stdout = original_stdout
            raise e
            
        sys.stdout = original_stdout
        

    def analysis_by_kingdom(df: PPC_Dataframe, f, *args):
        print(f"ARCHAEA")
        f(df.archaea, *args)
        
        print()
        print(f"BACTERIA")
        f(df.bacteria, *args)
        
        print()
        print(f"EUKARYA")
        f(df.eukaryota, *args)
        
        print()
        print(f"VIRUSES")
        f(df.viruses, *args)   

    def print_by_kingdom(df: PPC_Dataframe):
        print(f"            EC \t\t SEQ")
        print(f"archaea     {len(df.archaea.ec_value_counts)} \t {len(df.archaea)}")
        print(f"bacteria    {len(df.bacteria.ec_value_counts)} \t {len(df.bacteria)}")
        print(f"eukaryota   {len(df.eukaryota.ec_value_counts)} \t {len(df.eukaryota)}")
        print(f"viruses     {len(df.viruses.ec_value_counts)} \t\t {len(df.viruses)}")
        print(f"total       {len(df.ec_value_counts)} \t {len(df)}")
    
    def print_cluster_by_ec_class(df: PPC_Dataframe, prop: PPC_Clusters):
        oxidoreductases = df.oxidoreductases.get_cluster(prop)
        transferases = df.transferases.get_cluster(prop)
        hydrolases = df.hydrolases.get_cluster(prop)
        lyases = df.lyases.get_cluster(prop)
        isomerases = df.isomerases.get_cluster(prop)
        ligases = df.ligases.get_cluster(prop)
        translocases = df.translocases.get_cluster(prop)
        total = df.get_cluster(prop)
        
        print(f"                  EC \t SEQ")
        print(f"oxidoreductases   {len(oxidoreductases)} \t {oxidoreductases.count_proteins}")
        print(f"transferases      {len(transferases)} \t {transferases.count_proteins}")
        print(f"hydrolases        {len(hydrolases)} \t {hydrolases.count_proteins}")
        print(f"lyases            {len(lyases)} \t {lyases.count_proteins}")
        print(f"isomerases        {len(isomerases)} \t {isomerases.count_proteins}")
        print(f"ligases           {len(ligases)} \t {ligases.count_proteins}")
        print(f"translocases      {len(translocases)} \t {translocases.count_proteins}")
        print(f"total             {len(total)} \t {total.count_proteins}")

    def print_by_ec_class(df: PPC_Dataframe):
        print(f"                  EC \t SEQ")
        print(f"oxidoreductases   {len(df.oxidoreductases.ec_value_counts)} \t {len(df.oxidoreductases)}")
        print(f"transferases      {len(df.transferases.ec_value_counts)} \t {len(df.transferases)}")
        print(f"hydrolases        {len(df.hydrolases.ec_value_counts)} \t {len(df.hydrolases)}")
        print(f"lyases            {len(df.lyases.ec_value_counts)} \t {len(df.lyases)}")
        print(f"isomerases        {len(df.isomerases.ec_value_counts)} \t {len(df.isomerases)}")
        print(f"ligases           {len(df.ligases.ec_value_counts)} \t {len(df.ligases)}")
        print(f"translocases      {len(df.translocases.ec_value_counts)} \t {len(df.translocases)}")
        print(f"total             {len(df.ec_value_counts)} \t {len(df)}")