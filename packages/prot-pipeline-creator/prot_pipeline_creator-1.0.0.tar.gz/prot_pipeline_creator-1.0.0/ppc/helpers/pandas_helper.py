import pandas as pd

from ppc.enums.columns import PPC_Columns

class PandasHelper:
    @staticmethod
    def plot_full():
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)  
        # pd.set_option('display.max_colwidth', None) 
        
    @staticmethod
    def transform_col_in_tuple(col_df: pd.DataFrame, sep: str = None):
        col_s = col_df.fillna('')
        return col_s.apply(PandasHelper.__str_to_clear_tuple, args=(sep,))
    
    @staticmethod
    def clusterize_col(df: pd.DataFrame, col: str):
        clusters_df = df.groupby(col).agg(
            ProteinEntries=(PPC_Columns.Entry, list),
            MemberCount=(PPC_Columns.Entry, 'nunique')
        ).reset_index()
        return clusters_df
    
    def __str_to_clear_tuple(val, sep: str = None):
        if isinstance(val, tuple):
            return val
        
        str_val = str(val) if val else ''
        if not str_val:
            return ()
        
        list = str_val.split(sep)
        clean = [x.strip() for x in list]
        filtered = [x for x in clean if x]
        filtered.sort()
        
        return tuple(filtered)
    