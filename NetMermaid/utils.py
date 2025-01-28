# Utility functions for NetMermaid (e.g., IP parsing, time formatting)

def parse_time(time_str):
    # Simple function to parse and format time (can be expanded if necessary)
    from datetime import datetime
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
