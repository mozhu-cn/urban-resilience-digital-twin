import osmnx as ox
import networkx as nx
import numpy as np
import pickle
import requests
import time
import os

def load_or_fetch_data(cfg):
    cache_file = cfg["cache_file"]
    if os.path.exists(cache_file):
        print(f"   -> [Cache Hit] Loading {cache_file}")
        with open(cache_file, 'rb') as f:
            G_proj, x_coords, y_coords, z_coords = pickle.load(f)
        nodes = list(G_proj.nodes())
        return G_proj, nodes, x_coords, y_coords, z_coords
    else:
        print("   -> [First Run] Fetching data from OpenStreetMap and Open-Meteo...")
        G = ox.graph_from_point(cfg["city_center"], dist=cfg["dist_meters"],
                                network_type="drive", simplify=True)
        nodes = list(G.nodes())
        # Fetch elevation
        chunk_size = 50
        for i in range(0, len(nodes), chunk_size):
            chunk = nodes[i:i+chunk_size]
            lats = [str(round(G.nodes[n]['y'], 5)) for n in chunk]
            lons = [str(round(G.nodes[n]['x'], 5)) for n in chunk]
            url = f"https://api.open-meteo.com/v1/elevation?latitude={','.join(lats)}&longitude={','.join(lons)}"
            for _ in range(3):
                try:
                    res = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                    if res.status_code == 200:
                        elevs = res.json().get('elevation', [])
                        for j, n in enumerate(chunk):
                            G.nodes[n]['elevation'] = max(0, elevs[j]) if elevs[j] is not None else 0
                        break
                except:
                    time.sleep(1)
            else:
                for n in chunk:
                    G.nodes[n]['elevation'] = 0
            print(f"   Download progress: {min(100, int((i+chunk_size)/len(nodes)*100))}%", end='\r')
        print()
        G_proj = ox.project_graph(G, to_crs="EPSG:6674")
        x_coords = np.array([G_proj.nodes[n]['x'] for n in nodes])
        y_coords = np.array([G_proj.nodes[n]['y'] for n in nodes])
        z_coords = np.array([G_proj.nodes[n]['elevation'] for n in nodes])
        with open(cache_file, 'wb') as f:
            pickle.dump((G_proj, x_coords, y_coords, z_coords), f)
        return G_proj, nodes, x_coords, y_coords, z_coords