import pycountry
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime


class NetMaid:
	def __init__(self, csv_file_path):
		self.csv_file_path = csv_file_path
		self.df = self._ingest_csv(csv_file_path)
		self.graph = nx.DiGraph()  # Directed graph for communications

	def _ingest_csv(self, csv_file_path):
		# Step 1: Ingest the CSV
		df = pd.read_csv(csv_file_path)

		# Select relevant columns
		df = df[['start_time', 'src_ip_addr', 'dst_ip_addr', 'src_cc', 'dst_cc', 'proto', 'src_port', 'dst_port',
				 'num_pkts']]
		return df

	def create_graph(self):
		# Convert the start_time to a numeric format (e.g., timestamp)
		self.df['start_time'] = pd.to_datetime(self.df['start_time'])
		self.df['timestamp'] = self.df['start_time'].astype(int) / 10 ** 9  # Convert to Unix timestamp in seconds

		for _, row in self.df.iterrows():
			src_ip = row['src_ip_addr']
			dst_ip = row['dst_ip_addr']
			start_time = row['start_time']
			timestamp = row['timestamp']
			proto = row['proto']
			dst_port = row['dst_port']
			src_port = row['src_port']
			packets = row['num_pkts']

			source_name_display = self._get_flag(row['src_cc']) + f' {src_ip}'
			destination_name_display = self._get_flag(row['dst_cc']) + f' {dst_ip}'

			connection_information = f'{src_port}-->{dst_port} ({packets} packets)'

			# Add nodes (IP addresses) with port as Y-position
			if not self.graph.has_node(source_name_display):
				self.graph.add_node(source_name_display, timestamp=timestamp, port=src_port, ip=src_ip,
									country=row['src_cc'])
			if not self.graph.has_node(destination_name_display):
				self.graph.add_node(destination_name_display, timestamp=timestamp, port=dst_port, ip=dst_ip,
									country=row['dst_cc'])

			# Add edge (communication between IPs)
			self.graph.add_edge(source_name_display, destination_name_display,
								connection_information=connection_information)

	def _get_flag(self, country_code):
		# Convert country code to its respective flag using Unicode (emoji)
		try:
			country = pycountry.countries.get(alpha_2=country_code)
			flag_unicode = chr(0x1F1E6 + ord(country.alpha_2[0]) - ord('A')) + chr(
				0x1F1E6 + ord(country.alpha_2[1]) - ord('A'))
			return flag_unicode
		except AttributeError:
			return "🏳️"  # Return a generic flag if not found

	def visualize(self):
		# Prepare node positions based on timestamps (X-axis is time, Y-axis is port)
		pos = {}
		for node in self.graph.nodes():
			timestamp = self.graph.nodes[node].get('timestamp', 0)
			src_port = self.graph.nodes[node].get('port', 0)  # Source port for the left Y-axis
			dst_port = self.graph.nodes[node].get('dst_port', 0)  # Destination port for the right Y-axis
			pos[node] = (timestamp, src_port)  # X: timestamp, Y: source port

		# Get min and max timestamps to adjust the X-axis range dynamically
		min_timestamp = min([self.graph.nodes[node]['timestamp'] for node in self.graph.nodes()])
		max_timestamp = max([self.graph.nodes[node]['timestamp'] for node in self.graph.nodes()])

		# Format the timestamp on the x-axis
		timestamp_range = max_timestamp - min_timestamp
		if timestamp_range < 3600:  # Less than 1 hour
			xaxis_tickformat = "%Y-%m-%d %H:%M:%S"
		elif timestamp_range < 86400:  # Less than 1 day
			xaxis_tickformat = "%Y-%m-%d %H:%M"
		else:  # More than 1 day
			xaxis_tickformat = "%Y-%m-%d"

		# Create the Plotly figure
		edge_x = []
		edge_y = []
		edge_text = []

		# Extract edges for Plotly
		for edge in self.graph.edges():
			x0, y0 = pos[edge[0]]
			x1, y1 = pos[edge[1]]
			edge_x.append(x0)
			edge_y.append(y0)
			edge_x.append(x1)
			edge_y.append(y1)
			edge_text.append(self.graph[edge[0]][edge[1]]['connection_information'])

		# Create the edge traces
		edge_trace = go.Scatter(
			x=edge_x, y=edge_y,
			line=dict(width=0.5, color='gray'),
			hoverinfo='text',
			text=edge_text,
			mode='lines'
		)

		node_x = []
		node_y = []
		node_text = []

		# Extract nodes for Plotly
		for node in self.graph.nodes():
			x, y = pos[node]
			node_x.append(x)
			node_y.append(y)

			# Add IP address and country flag to node text
			country_flag = self._get_flag(self.graph.nodes[node]["country"])
			node_text.append(f'{country_flag} {self.graph.nodes[node]["ip"]}')

		# Create the node traces
		node_trace = go.Scatter(
			x=node_x, y=node_y,
			mode='markers',
			hoverinfo='text',
			marker=dict(
				showscale=True,
				colorscale='YlGnBu',
				size=20,
				color=node_x,  # Use the x-axis position for coloring nodes
				colorbar=dict(thickness=15, title='Timestamp', xanchor='left', titleside='right')
			),
			text=node_text  # Adding IP addresses and flags to the hover text
		)

		# Create the layout for the figure


		min_timestamp = min([self.graph.nodes[node]['timestamp'] for node in self.graph.nodes()])
		max_timestamp = max([self.graph.nodes[node]['timestamp'] for node in self.graph.nodes()])

		tickvals = [min_timestamp + i * (max_timestamp - min_timestamp) / 5 for i in range(6)]
		ticktext = [datetime.utcfromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S') for val in tickvals]

		layout = go.Layout(
			title='IP Communication Graph',
			titlefont_size=16,
			showlegend=False,
			hovermode='closest',
			xaxis=dict(
				title='Timestamp',
				tickmode='array',  # Use custom tick values
				tickvals=[min_timestamp + i * (max_timestamp - min_timestamp) / 5 for i in range(6)],
				# Define your tick values
				ticktext=[datetime.utcfromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S') for val in
						  [min_timestamp + i * (max_timestamp - min_timestamp) / 5 for i in range(6)]],
				# Format them as readable dates
			),
			yaxis=dict(title='Port'),  # Limit y-axis range for ports
			plot_bgcolor='white'
		)

		# Create the figure with edges and nodes
		fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

		# Show the interactive graph
		fig.show()
