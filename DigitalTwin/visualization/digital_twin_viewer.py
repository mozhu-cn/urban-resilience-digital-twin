import plotly.graph_objects as go
import numpy as np
import random
from ..data.terrain_processing import get_xyz

def create_animation(G_proj, grid_x, grid_y, grid_z, frame_data_list,
                     dependency_edges, comm_nodes, nodes, power_nodes, cfg):
    # ... 其余代码不变 ...
    print(">>> Generating 4D animation...")
    random.seed(cfg.get("seed", 42))
    fig = go.Figure()

    # Terrain
    land_colorscale = [[0.0, '#759b66'], [0.4, '#c8c58f'], [0.7, '#a98056'], [1.0, '#664d36']]
    fig.add_trace(go.Surface(x=grid_x, y=grid_y, z=grid_z, colorscale=land_colorscale,
                             opacity=1.0, hoverinfo='skip', showscale=False))

    # Base water (lowlands)
    base_water = np.where(grid_z <= 1.5, 1.5, np.nan)
    fig.add_trace(go.Surface(x=grid_x, y=grid_y, z=base_water,
                             colorscale=[[0, '#1c4587'], [1, '#1c4587']],
                             opacity=0.9, showscale=False, hoverinfo='skip'))

    # Roads (subsampled)
    rx, ry, rz = [], [], []
    for u, v in list(G_proj.edges())[::5]:
        rx.extend([G_proj.nodes[u]['x'], G_proj.nodes[v]['x'], None])
        ry.extend([G_proj.nodes[u]['y'], G_proj.nodes[v]['y'], None])
        rz.extend([G_proj.nodes[u]['elevation']+0.5, G_proj.nodes[v]['elevation']+0.5, None])
    fig.add_trace(go.Scatter3d(x=rx, y=ry, z=rz, mode='lines',
                               line=dict(color='rgba(255,255,255,0.4)', width=1), hoverinfo='skip'))

    # Urban buildings (safe random sample)
    all_nodes = set(nodes)
    exclude_ids = set(comm_nodes) | set(power_nodes)
    urban_pool = list(all_nodes - exclude_ids)
    sample_size = min(400, len(urban_pool))
    urban_sample = random.sample(urban_pool, sample_size) if sample_size > 0 else []
    bx, by, bz = get_xyz(G_proj, urban_sample)
    fig.add_trace(go.Scatter3d(x=bx, y=by, z=[z+1 for z in bz], mode='markers',
                               marker=dict(size=2.5, color='#aaaaaa', symbol='square'),
                               hoverinfo='skip'))

    # Dependency lines
    dx, dy, dz = [], [], []
    for p, c in dependency_edges:
        dx.extend([G_proj.nodes[p]['x'], G_proj.nodes[c]['x'], None])
        dy.extend([G_proj.nodes[p]['y'], G_proj.nodes[c]['y'], None])
        dz.extend([G_proj.nodes[p]['elevation'], G_proj.nodes[c]['elevation'], None])
    fig.add_trace(go.Scatter3d(x=dx, y=dy, z=dz, mode='lines',
                               line=dict(color='#32cd32', width=1.5, dash='dot'),
                               hoverinfo='skip'))

    # Initial dynamic traces (frame 0)
    fd0 = frame_data_list[0]
    fig.add_trace(go.Surface(x=grid_x, y=grid_y, z=fd0['water_z'],
                             colorscale='Blues', opacity=0.85, hoverinfo='skip', showscale=False))
    fig.add_trace(go.Scatter3d(x=fd0['sx'], y=fd0['sy'], z=fd0['sz'], mode='markers',
                               marker=dict(size=8, color='red', symbol='square'), name='Active Power'))
    fig.add_trace(go.Scatter3d(x=fd0['fx'], y=fd0['fy'], z=fd0['fz'], mode='markers',
                               marker=dict(size=11, color='black', symbol='x'), name='Flooded Power'))
    fig.add_trace(go.Scatter3d(x=fd0['repairx'], y=fd0['repairy'], z=fd0['repairz'], mode='markers',
                               marker=dict(size=10, color='orange', symbol='diamond'), name='Repairing'))
    fig.add_trace(go.Scatter3d(x=fd0['rx'], y=fd0['ry'], z=fd0['rz'], mode='markers',
                               marker=dict(size=10, color='#00ff00', symbol='square',
                                           line=dict(color='white', width=2)), name='Restored'))
    fig.add_trace(go.Scatter3d(x=fd0['fleet_x'], y=fd0['fleet_y'], z=fd0['fleet_z'],
                               mode='markers', marker=dict(size=12, color='#ffd700', symbol='circle',
                                                           line=dict(color='black', width=1)),
                               name='Repair Fleet'))
    fig.add_trace(go.Scatter3d(x=get_xyz(G_proj, comm_nodes)[0],
                               y=get_xyz(G_proj, comm_nodes)[1],
                               z=get_xyz(G_proj, comm_nodes)[2],
                               mode='markers',
                               marker=dict(size=6, color=fd0['cc'],
                                           colorscale=[[0,'#404040'],[1,'#00ffff']],
                                           cmin=0, cmax=1, symbol='diamond'),
                               name='Comm Base'))

    # Build frames
    frames = []
    for step, fd in enumerate(frame_data_list):
        frames.append(go.Frame(data=[
            go.Surface(z=fd['water_z']),
            go.Scatter3d(x=fd['sx'], y=fd['sy'], z=fd['sz']),
            go.Scatter3d(x=fd['fx'], y=fd['fy'], z=fd['fz']),
            go.Scatter3d(x=fd['repairx'], y=fd['repairy'], z=fd['repairz']),
            go.Scatter3d(x=fd['rx'], y=fd['ry'], z=fd['rz']),
            go.Scatter3d(x=fd['fleet_x'], y=fd['fleet_y'], z=fd['fleet_z']),
            go.Scatter3d(marker=dict(color=fd['cc']))
        ], traces=[5,6,7,8,9,10,11], name=f'F{step}'))
    fig.frames = frames

    # Layout
    fig.update_layout(
        title="Resilience Digital Twin: Physics + Delayed Cascades + Adaptive Restoration",
        scene=dict(
            xaxis_title='Easting', yaxis_title='Northing', zaxis_title='Elevation',
            aspectratio=dict(x=1, y=1, z=0.15),
            camera=dict(eye=dict(x=-1.3, y=-1.6, z=0.9)),
            xaxis=dict(showgrid=False, showbackground=False, zeroline=False),
            yaxis=dict(showgrid=False, showbackground=False, zeroline=False),
            zaxis=dict(showgrid=True, showbackground=True)
        ),
        legend=dict(x=0.85, y=0.9, bgcolor='rgba(255,255,255,0.7)'),
        updatemenus=[dict(
            type='buttons', showactive=False, y=0.1, x=0.05, xanchor='left', yanchor='top',
            buttons=[
                dict(label='▶ RUN', method='animate',
                     args=[None, dict(frame=dict(duration=400, redraw=True),
                                      fromcurrent=True, mode='immediate')]),
                dict(label='⏸ PAUSE', method='animate',
                     args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate')])
            ]
        )],
        sliders=[dict(
            steps=[dict(method='animate', args=[[f'F{step}'],
                    dict(mode='immediate', frame=dict(duration=200, redraw=True))],
                    label=f'{step}') for step in range(len(frame_data_list))],
            active=0, transition=dict(duration=0), x=0.2, y=0,
            currentvalue=dict(font=dict(size=14), prefix="Frame: ")
        )],
        margin=dict(l=0, r=0, b=0, t=40)
    )
    return fig