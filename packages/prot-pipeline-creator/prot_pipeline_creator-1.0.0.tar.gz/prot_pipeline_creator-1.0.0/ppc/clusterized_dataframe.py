import pandas as pd
import json

from ppc.enums.columns import PPC_Columns, PPC_ClusterizedColumns

class ClusterizedDataframe:
    __df: pd.DataFrame
    
    def __init__(self, df: pd.DataFrame = None):
        self.__initial_treatment(df)
    
    def __len__(self):
        return len(self.__df)
    
    def __getitem__(self, key: str):
        return self.__df[key]
    
    def __repr__(self):
        return repr(self.__df)
        
    def __initial_treatment(self, df: pd.DataFrame):
        if df.empty:
            self.__df = pd.DataFrame(columns=[
                PPC_Columns.ECNumber, 
                PPC_ClusterizedColumns.SuperFamilyCount,
                PPC_ClusterizedColumns.ProteinCount,
                PPC_ClusterizedColumns.Entries
            ])
            return

        temp_df = df.copy()
        
        family_groups = temp_df.groupby([
            PPC_Columns.ECNumber, PPC_Columns.SuperFamily
        ])[PPC_Columns.Entry].apply(list).reset_index()
        
        def build_family_dict(group):
            result = {}
            for _, row in group.iterrows():
                key = str(row[PPC_Columns.SuperFamily])
                value = row[PPC_Columns.Entry]
                result[key] = value
            return json.dumps(result)

        detailed_entries = family_groups.groupby(PPC_Columns.ECNumber).apply(build_family_dict).reset_index()
        
        detailed_entries.columns = [PPC_Columns.ECNumber, PPC_ClusterizedColumns.Entries]

        stats_df = temp_df.groupby(PPC_Columns.ECNumber).agg(
            SuperFamilyCount=(PPC_Columns.SuperFamily, 'nunique'),
            ProteinCount=(PPC_Columns.Entry, 'nunique')
        ).reset_index()

        self.__df = pd.merge(stats_df, detailed_entries, on=PPC_Columns.ECNumber, how='left')
    
    def to_tsv(self, path: str):
        self.__df.to_csv(path, sep='\t', encoding='utf-8', index=False, header=True)
    
    @property
    def cols(self):
        return list(self.__df)
    
    @property
    def count_proteins(self):
        return self.__df[PPC_ClusterizedColumns.ProteinCount].sum()
    
    
    