def generate_mermaid_graph(graph):
    """
    Generate Mermaid syntax from a NetworkX graph
    """
    mermaid = 'graph TD\n'
    
    for node in graph.nodes:
        # Assuming the flags are in node attributes
        flag = graph.nodes[node].get('country_flag', '')
        mermaid += f'    {node}["{node} {flag}"]\n'
    
    for u, v, data in graph.edges(data=True):
        time = data.get('time', '')
        protocol = data.get('protocol', '')
        mermaid += f'    {u} -->|{protocol}, {time}| {v}\n'
    
    return mermaid
