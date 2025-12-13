import pandas as pd

from ppc.helpers.pandas_helper import PandasHelper as pdHelper
from ppc.clusterized_dataframe import ClusterizedDataframe
from ppc.enums.super_kingdom import SuperKingdom
from ppc.enums.columns import PPC_Columns
from ppc.enums.clusters import PPC_Clusters

class PPC_Dataframe:
    """
    A class to load, process, and analyze protein data from a .tsv file.

    This class serves as a high-level wrapper around a pandas DataFrame,
    providing specialized methods for common bioinformatics analyses like
    filtering by enzyme class, clustering by domain, and identifying
    homogeneous (HISE) and heterogeneous (NISE) enzyme groups.
    """
    
    __df: pd.DataFrame
    
    def __init__(self, file_path: str = '', df: pd.DataFrame = None):
        """
        Initializes the ProteinDataset object.

        Args:
            file_path (str): The full path to the input data file.
            df (DataFrame, optional): Internal use to duplicate the ProteinDataframe
        """
        if file_path:
            self.__read_file(file_path)
        else:
            self.__df = df.copy()

        self.__initial_treatment()
    
    def __len__(self):
        return len(self.__df)
    
    def __getitem__(self, key: str):
        return self.__df[key]
    
    def __repr__(self):
        return repr(self.__df)
    
    def __read_file(self, filename):
        self.__df = pd.read_csv(
            filename,
            sep='\t',
            header=0,
        )
        
    def __initial_treatment(self):
        self.__df[PPC_Columns.ECNumber] = pdHelper.transform_col_in_tuple(self.__df[PPC_Columns.ECNumber], ';')
        self.__df[PPC_Columns.SuperFamily] = pdHelper.transform_col_in_tuple(self.__df[PPC_Columns.SuperFamily], ';')
        self.__df[PPC_Columns.PDB] = pdHelper.transform_col_in_tuple(self.__df[PPC_Columns.PDB], ';')
        
        self.__df[PPC_Columns.SuperKingdom] = self.__df[PPC_Columns.TaxonomicLineage].apply(self.__extract_superkingdom)
        self.__df[PPC_Columns.IsECComplete] = self.__df[PPC_Columns.ECNumber].apply(self.__has_ec_complete)
    
    def to_tsv(self, path: str):
        self.__df.to_csv(path, sep='\t', encoding='utf-8', index=False, header=True)
    
    @property
    def cols(self):
        return list(self.__df)
    
    @property
    def ec_complete(self):
        filter = self.__df[PPC_Columns.IsECComplete]
        return PPC_Dataframe(df = self.__df[filter])
    
    @property
    def no_ec(self):
        filter = self.__df[PPC_Columns.ECNumber].str.len() < 1
        return PPC_Dataframe(df = self.__df[filter])
    
    @property
    def has_ec(self):
        filter = self.__df[PPC_Columns.ECNumber].str.len() > 0
        return PPC_Dataframe(df = self.__df[filter])
        
    @property
    def not_promiscuous(self):
        filter = self.__df[PPC_Columns.ECNumber].str.len() == 1
        return PPC_Dataframe(df = self.__df[filter])
    
    @property
    def promiscuos(self):
        filter = self.__df[PPC_Columns.ECNumber].str.len() > 1
        return PPC_Dataframe(df = self.__df[filter])
    
    @property
    def exploded_ec_clusters(self):
        exploded_supfam = self.__df.explode(PPC_Columns.ECNumber)
        
        clusters_df = pdHelper.clusterize_col(exploded_supfam, PPC_Columns.ECNumber)
        
        return clusters_df
    
    @property
    def ec_clusters(self):
        return pdHelper.clusterize_col(self.__df, PPC_Columns.ECNumber)
    
    def get_cluster(self, prop: PPC_Clusters):
        match prop:
            case PPC_Clusters.single_enzymes_clusters:
                return self.single_enzymes_clusters
            case PPC_Clusters.multiple_enzymes_clusters:
                return self.multiple_enzymes_clusters
            case PPC_Clusters.homologous_ec_clusters:
                return self.homologous_ec_clusters
            case PPC_Clusters.non_homologous_ec_clusters:
                return self.non_homologous_ec_clusters
    
    @property
    def single_enzymes_clusters(self):      
        hise = self.__df.groupby(PPC_Columns.ECNumber).filter(
            lambda group: group[PPC_Columns.Entry].nunique() == 1
        )
        
        return ClusterizedDataframe(hise)
    
    @property
    def multiple_enzymes_clusters(self):      
        hise = self.__df.groupby(PPC_Columns.ECNumber).filter(
            lambda group: group[PPC_Columns.Entry].nunique() > 1
        )
        
        return ClusterizedDataframe(hise)
    
    @property
    def homologous_ec_clusters(self):      
        hise = self.__df.groupby(PPC_Columns.ECNumber).filter(
            lambda group: group[PPC_Columns.SuperFamily].nunique() == 1
        )
        
        return ClusterizedDataframe(hise)
    
    @property
    def non_homologous_ec_clusters(self):      
        nise = self.__df.groupby(PPC_Columns.ECNumber).filter(
            lambda group: group[PPC_Columns.SuperFamily].nunique() > 1
        )
        
        return ClusterizedDataframe(nise)
    
    @property
    def ec_value_counts(self):
        return self.__df[PPC_Columns.ECNumber].explode().value_counts()
    
    @property
    def no_supfam(self):
        filter = self.__df[PPC_Columns.SuperFamily].str.len() < 1
        return PPC_Dataframe(df = self.__df[filter])
    
    @property
    def has_supfam(self):
        filter = self.__df[PPC_Columns.SuperFamily].str.len() > 0
        return PPC_Dataframe(df = self.__df[filter])
    
    @property
    def single_supfam(self):
        filter = self.__df[PPC_Columns.SuperFamily].str.len() == 1
        return PPC_Dataframe(df = self.__df[filter])
    
    @property
    def multi_supfam(self):
        filter = self.__df[PPC_Columns.SuperFamily].str.len() > 1
        return PPC_Dataframe(df = self.__df[filter])
    
    @property
    def exploded_supfam_clusters(self):
        exploded_supfam = self.__df.explode(PPC_Columns.SuperFamily)
        
        clusters_df = pdHelper.clusterize_col(exploded_supfam, PPC_Columns.SuperFamily)
        
        return clusters_df
    
    @property
    def supfam_clusters(self):        
        return pdHelper.clusterize_col(self.__df, PPC_Columns.SuperFamily)
    
    @property
    def supfam_value_counts(self):
        return self.__df[PPC_Columns.SuperFamily].explode().value_counts()
    
    @property
    def supkingdom_value_counts(self):
        return self.__df[PPC_Columns.SuperKingdom].value_counts()
    
    
    @property
    def has_pdb(self):
        filter = self.__df[PPC_Columns.PDB].str.len() > 0
        return PPC_Dataframe(df = self.__df[filter])
    
    @property
    def bacteria(self):
        return self.__supkingdom_is(SuperKingdom.Bacteria)
    
    @property
    def eukaryota(self):
        return self.__supkingdom_is(SuperKingdom.Eukaryota)
    
    @property
    def archaea(self):
        return self.__supkingdom_is(SuperKingdom.Archaea)
    
    @property
    def viruses(self):
        return self.__supkingdom_is(SuperKingdom.Viruses)
    
    @property
    def oxidoreductases(self):
        return self.__ec_init_with('1')
    
    @property
    def transferases(self):
        return self.__ec_init_with('2')
    
    @property
    def hydrolases(self):
        return self.__ec_init_with('3')
    
    @property
    def lyases(self):
        return self.__ec_init_with('4')
    
    @property
    def isomerases(self):
        return self.__ec_init_with('5')
    
    @property
    def ligases(self):
        return self.__ec_init_with('6')
    
    @property
    def translocases(self):
        return self.__ec_init_with('7')
    
    def __ec_init_with(self, ec_filter: str):
        filter = self.__df[PPC_Columns.ECNumber].apply(lambda x: any(ec.startswith(ec_filter) for ec in x))
        return PPC_Dataframe(df = self.__df[filter])
    
    def __supkingdom_is(self, supkingdom: str):
        superKingdomColumn: str = f'{PPC_Columns.SuperKingdom}'
        filter = self.__df[superKingdomColumn].fillna('').str.lower() == supkingdom.lower()
        return PPC_Dataframe(df = self.__df[filter])
    
    def __extract_superkingdom(self, lineage: str):
        if pd.isna(lineage):
            return None
        
        parts = lineage.split(', ')
        parts[0] = parts[0].split(' ')[0]
        
        if parts[0].lower() == SuperKingdom.Viruses.lower():
            return SuperKingdom.Viruses
        
        if len(parts) > 1:
            parts[1] = parts[1].split(' ')[0]
            return parts[1]
        
        return None
    
    def __has_ec_complete(self, ec_list):
        return any(self.__is_ec_complete(ec) for ec in ec_list)
    
    def __is_ec_complete(self, ec: str):
        if pd.isna(ec):
            return False
        
        parts = ec.split('.')
        
        if (len(parts) < 4):
            return False
        
        return all(x.isdigit() for x in parts)
    
    