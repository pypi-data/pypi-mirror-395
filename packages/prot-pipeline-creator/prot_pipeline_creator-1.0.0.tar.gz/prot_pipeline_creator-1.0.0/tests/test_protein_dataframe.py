import unittest
import pandas as pd
from ppc.protein_dataframe import PPC_Dataframe
from ppc.enums.columns import PPC_Columns
from ppc.enums.super_kingdom import SuperKingdom

class TestPPCDataframe(unittest.TestCase):

    def setUp(self):
        # Simulated "raw" data as it would come from the CSV
        self.raw_data = {
            PPC_Columns.Entry: ['P1', 'P2', 'P3', 'P4'],
            PPC_Columns.EntryName: ['Prot1', 'Prot2', 'Prot3', 'Prot4'],
            # Complete, Incomplete, Promiscuous, Empty
            PPC_Columns.ECNumber: ['1.1.1.1', '2.1.-.-', '3.1.1.1; 4.2.2.2; 5.2.-.-; 6.2.4.-; 7.1.2.-', ''],
            PPC_Columns.SuperFamily: ['SupA', 'SupB', 'SupA; SupC', ''],
            PPC_Columns.TaxonomicLineage: [
                # Archaea
                'cellular organisms (no rank), Archaea (domain), Thermoproteati (kingdom), Thermoproteota (phylum), Thermoprotei (class), Sulfolobales (order), Sulfolobaceae (family), Saccharolobus (genus)',
                # Bacteria
                'cellular organisms (no rank), Bacteria (domain), Pseudomonadati (kingdom), Pseudomonadota (phylum), Alphaproteobacteria (class), Hyphomicrobiales (order), Rhizobiaceae (family), Shinella (genus), unclassified Shinella (no rank)', 
                # Eukaryota
                'cellular organisms (no rank), Eukaryota (domain), Opisthokonta (clade), Fungi (kingdom), Dikarya (subkingdom), Ascomycota (phylum), saccharomyceta (clade), Pezizomycotina (subphylum), leotiomyceta (clade), sordariomyceta (clade), Sordariomycetes (class), Hypocreomycetidae (subclass), Hypocreales (order), Hypocreaceae (family), Trichoderma (genus), Hypocrea jecorina (species)',
                # Viruses
                'Viruses (no rank), Duplodnaviria (realm), Heunggongvirae (kingdom), Peploviricota (phylum), Herviviricetes (class), Herpesvirales (order), Orthoherpesviridae (family), Betaherpesvirinae (subfamily), Muromegalovirus (genus), Muromegalovirus muridbeta1 (species), Murid herpesvirus 1 (no rank)'
            ],
            PPC_Columns.PDB: ['1ABC;', '', '1ARO;1LBA;', ';']
        }
        self.df_mock = pd.DataFrame(self.raw_data)

    def test_initialization_and_treatment(self):
        ppc = PPC_Dataframe(df=self.df_mock)
        
        self.assertEqual(len(ppc), 4)

        # Test 1: EC Number become a tuple
        self.assertTrue(isinstance(ppc[PPC_Columns.ECNumber][0], tuple))
        self.assertEqual(ppc[PPC_Columns.ECNumber][0], ('1.1.1.1',))
        self.assertEqual(ppc[PPC_Columns.ECNumber][1], ('2.1.-.-',))
        self.assertEqual(ppc[PPC_Columns.ECNumber][2], ('3.1.1.1', '4.2.2.2', '5.2.-.-', '6.2.4.-', '7.1.2.-'))
        self.assertEqual(ppc[PPC_Columns.ECNumber][3], ())
        
        # Test 2: SuperKingdom Extraction
        self.assertEqual(ppc[PPC_Columns.SuperKingdom][0], SuperKingdom.Archaea)
        self.assertEqual(ppc[PPC_Columns.SuperKingdom][1], SuperKingdom.Bacteria)
        self.assertEqual(ppc[PPC_Columns.SuperKingdom][2], SuperKingdom.Eukaryota)
        self.assertEqual(ppc[PPC_Columns.SuperKingdom][3], SuperKingdom.Viruses)

        # Test 3: IsECComplete column generated correctly?
        # P1 (1.1.1.1) is True, P2 (2.1.-.-) is False, P3 ('3.1.1.1', '3.2.2.2') is true, P4 () is false
        self.assertTrue(ppc[PPC_Columns.IsECComplete][0])
        self.assertFalse(ppc[PPC_Columns.IsECComplete][1])
        self.assertTrue(ppc[PPC_Columns.IsECComplete][2])
        self.assertFalse(ppc[PPC_Columns.IsECComplete][3])
        
        # Test 4: PDB become a tuple
        self.assertTrue(isinstance(ppc[PPC_Columns.PDB][0], tuple))
        self.assertEqual(ppc[PPC_Columns.PDB][0], ('1ABC',))
        self.assertEqual(ppc[PPC_Columns.PDB][1], ())
        self.assertEqual(ppc[PPC_Columns.PDB][2], ('1ARO', '1LBA'))
        self.assertEqual(ppc[PPC_Columns.PDB][3], ())
        
        self.assertEqual(len(ppc.has_pdb), 2)
        

    def test_kindom_logic(self):
        ppc = PPC_Dataframe(df=self.df_mock)
        
        self.assertEqual(len(ppc.archaea), 1)
        self.assertEqual(len(ppc.bacteria), 1)
        self.assertEqual(len(ppc.eukaryota), 1)
        self.assertEqual(len(ppc.viruses), 1)
        
        self.assertEqual(ppc.archaea[PPC_Columns.Entry].iloc[0], 'P1')
        self.assertEqual(ppc.bacteria[PPC_Columns.Entry].iloc[0], 'P2')
        self.assertEqual(ppc.eukaryota[PPC_Columns.Entry].iloc[0], 'P3')
        self.assertEqual(ppc.viruses[PPC_Columns.Entry].iloc[0], 'P4')
        

    def test_supfam_logic(self):
        ppc = PPC_Dataframe(df=self.df_mock)
        
        self.assertEqual(len(ppc.no_supfam), 1)
        self.assertEqual(len(ppc.has_supfam), 3)
        self.assertEqual(len(ppc.single_supfam), 2)
        self.assertEqual(len(ppc.multi_supfam), 1)
        
        self.assertEqual(ppc.no_supfam[PPC_Columns.Entry].iloc[0], 'P4')
        self.assertEqual(ppc.multi_supfam[PPC_Columns.Entry].iloc[0], 'P3')
        

    def test_ec_logic(self):
        ppc = PPC_Dataframe(df=self.df_mock)

        self.assertEqual(len(ppc.ec_complete), 2) 
        self.assertEqual(len(ppc.no_ec), 1) 
        self.assertEqual(len(ppc.has_ec), 3) 

        self.assertEqual(len(ppc.promiscuos), 1)
        # Note: P4 has no ec, so it not enter in this count 
        self.assertEqual(len(ppc.not_promiscuous), 2)
        self.assertEqual(ppc.promiscuos[PPC_Columns.Entry].iloc[0], 'P3')
        
        oxidoreductases = ppc.oxidoreductases
        self.assertEqual(len(oxidoreductases), 1)
        self.assertEqual(oxidoreductases[PPC_Columns.Entry].iloc[0], 'P1')

        transferases = ppc.transferases
        self.assertEqual(len(transferases), 1)
        self.assertEqual(transferases[PPC_Columns.Entry].iloc[0], 'P2')
        
        hydrolases = ppc.hydrolases
        self.assertEqual(len(hydrolases), 1)
        self.assertEqual(hydrolases[PPC_Columns.Entry].iloc[0], 'P3')
        
        lyases = ppc.lyases
        self.assertEqual(len(lyases), 1)
        self.assertEqual(lyases[PPC_Columns.Entry].iloc[0], 'P3')
        
        isomerases = ppc.isomerases
        self.assertEqual(len(isomerases), 1)
        self.assertEqual(isomerases[PPC_Columns.Entry].iloc[0], 'P3')
        
        ligases = ppc.ligases
        self.assertEqual(len(ligases), 1)
        self.assertEqual(ligases[PPC_Columns.Entry].iloc[0], 'P3')
        
        translocases = ppc.translocases
        self.assertEqual(len(translocases), 1)
        self.assertEqual(translocases[PPC_Columns.Entry].iloc[0], 'P3')

if __name__ == '__main__':
    unittest.main()