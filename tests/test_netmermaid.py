import unittest
from NetMermaid.netmermaid import NetMermaid

class TestNetMermaid(unittest.TestCase):
    
    def setUp(self):
        # Example CSV file path for testing
        self.csv_file_path = "example.csv"
        self.netmermaid = NetMermaid(self.csv_file_path)
    
    def test_ingest_csv(self):
        self.assertFalse(self.netmermaid.df.empty, "CSV ingestion failed")
    
    def test_flags(self):
        # Test if flags are being added for IPs (we'll assume some valid IPs)
        self.assertTrue(self.netmermaid.df['src_flag'].notna().all(), "Flags for source IPs are missing")
        self.assertTrue(self.netmermaid.df['dst_flag'].notna().all(), "Flags for destination IPs are missing")
    
    def test_graph_creation(self):
        self.netmermaid.create_graph()
        self.assertGreater(len(self.netmermaid.graph.nodes), 0, "Graph nodes were not created")
        self.assertGreater(len(self.netmermaid.graph.edges), 0, "Graph edges were not created")
    
    def test_mermaid_generation(self):
        self.netmermaid.create_graph()
        mermaid_syntax = generate_mermaid_graph(self.netmermaid.graph)
        self.assertTrue(mermaid_syntax.startswith('graph TD'), "Mermaid graph syntax generation failed")
        
if __name__ == "__main__":
    unittest.main()
