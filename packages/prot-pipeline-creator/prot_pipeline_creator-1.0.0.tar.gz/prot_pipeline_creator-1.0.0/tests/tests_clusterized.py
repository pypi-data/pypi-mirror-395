import unittest
import pandas as pd
import json

from ppc.clusterized_dataframe import ClusterizedDataframe
from ppc.enums.columns import PPC_Columns, PPC_ClusterizedColumns

class TestClusterizedDataframe(unittest.TestCase):

    def test_clustering_aggregation(self):
        # Scenario: 4 Proteins.
        # EC 1.1.1.1 has 3 proteins divided into 2 families:
        #   - Family A: P1 and P2
        #   - Family B: P3
        # EC 2.2.2.2 has 1 protein and 1 family:
        #   - Family C: P4
        data = {
            PPC_Columns.Entry: ['P1', 'P2', 'P3', 'P4'],
            PPC_Columns.ECNumber: ['1.1.1.1', '1.1.1.1', '1.1.1.1', '2.2.2.2'],
            PPC_Columns.SuperFamily: ['FamA', 'FamA', 'FamB', 'FamC'],
            PPC_Columns.ProteinNames: ['N1', 'N2', 'N3', 'N4'] 
        }
        df = pd.DataFrame(data)

        # Initialize the ClusterizedDataframe
        cluster_df = ClusterizedDataframe(df)

        # We should have 2 rows now (one for 1.1.1.1 and another for 2.2.2.2)
        self.assertEqual(len(cluster_df), 2)

        group_1 = cluster_df._ClusterizedDataframe__df[
            cluster_df._ClusterizedDataframe__df[PPC_Columns.ECNumber] == '1.1.1.1'
        ].iloc[0]
        self.assertEqual(group_1[PPC_ClusterizedColumns.ProteinCount], 3)
        self.assertEqual(group_1[PPC_ClusterizedColumns.SuperFamilyCount], 2)

        group_2 = cluster_df._ClusterizedDataframe__df[
            cluster_df._ClusterizedDataframe__df[PPC_Columns.ECNumber] == '2.2.2.2'
        ].iloc[0]
        self.assertEqual(group_2[PPC_ClusterizedColumns.ProteinCount], 1)
        self.assertEqual(group_2[PPC_ClusterizedColumns.SuperFamilyCount], 1)
        
        
        raw_json = group_1[PPC_ClusterizedColumns.Entries]
        
        # Test 1: Entries is a String
        self.assertIsInstance(raw_json, str)
        
        details_dict = json.loads(raw_json)
        # Test 2: It must be a DICTIONARY (Object), not a list
        self.assertIsInstance(details_dict, dict)
        # Test 3: Has 2 SupFam
        self.assertEqual(len(details_dict), 2)
        
        # Test 4: Verify content of each SupFam
        self.assertIn("FamA", details_dict)
        self.assertEqual(details_dict["FamA"], ['P1', 'P2'])
        
        self.assertIn("FamB", details_dict)
        self.assertEqual(details_dict["FamB"], ['P3'])
        
        # Test 5: Same for the other group
        group_2 = cluster_df._ClusterizedDataframe__df[
            cluster_df._ClusterizedDataframe__df[PPC_Columns.ECNumber] == '2.2.2.2'
        ].iloc[0]
        
        details_dict_2 = json.loads(group_2[PPC_ClusterizedColumns.Entries])
        self.assertIn("FamC", details_dict_2)
        self.assertEqual(details_dict_2["FamC"], ['P4'])
        

    def test_count_proteins_property(self):
        # The total unique proteins in the clusterized dataset must match the input
        data = {
            PPC_Columns.Entry: ['P1', 'P2'],
            PPC_Columns.ECNumber: ['1.1', '1.1'],
            PPC_Columns.SuperFamily: ['A', 'A'],
            PPC_Columns.ProteinNames: ['N1', 'N2']
        }
        df = pd.DataFrame(data)
        cluster_df = ClusterizedDataframe(df)
        
        self.assertEqual(cluster_df.count_proteins, 2)

if __name__ == '__main__':
    unittest.main()