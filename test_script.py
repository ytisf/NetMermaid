import sys
import os
from NetMermaid import NetMaid

# Add Flaggle and NetMermaid to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Flaggle')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'NetMermaid')))

# Path to the example CSV file
csv_file_path = 'examples/C2_FullFlows.csv'

def main():
    # Initialize the NetMermaid class with the example CSV file
    netmermaid = NetMaid(csv_file_path)
    
    # Step 1: Create the graph
    netmermaid.create_graph()
    
    # Step 2: Visualize the graph (this will open a Matplotlib window)
    netmermaid.visualize()
    
    print("Generated Mermaid Syntax:")

if __name__ == "__main__":
    main()
