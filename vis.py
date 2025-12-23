import plotly.graph_objects as go
import numpy as np

def create_cube(x_center, y_center, width, depth, height, color, label, opacity=0.8):
    # Define corners
    x = [x_center - width/2, x_center + width/2, x_center + width/2, x_center - width/2] * 2
    y = [y_center - depth/2, y_center - depth/2, y_center + depth/2, y_center + depth/2] * 2
    z = [0, 0, 0, 0, height, height, height, height]
    
    # Define mesh triangles
    i = [0, 0, 4, 4, 0, 1, 2, 3, 0, 1, 2, 3]
    j = [3, 1, 7, 5, 1, 2, 6, 7, 4, 5, 6, 7]
    k = [4, 5, 6, 7, 3, 2, 6, 7, 1, 2, 3, 0] # correction for sides

    # Correct mesh definitions for a clean cube
    return go.Mesh3d(
        x=[x_center-width/2, x_center-width/2, x_center+width/2, x_center+width/2, x_center-width/2, x_center-width/2, x_center+width/2, x_center+width/2],
        y=[y_center-depth/2, y_center+depth/2, y_center+depth/2, y_center-depth/2, y_center-depth/2, y_center+depth/2, y_center+depth/2, y_center-depth/2],
        z=[0, 0, 0, 0, height, height, height, height],
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color=color,
        opacity=opacity,
        name=label,
        showscale=False
    )

def visualize_campus_system():
    fig = go.Figure()

    # --- 1. DEFINING THE 8 ZONES (Campus Architecture) ---
    # Layout: Engineering and Science on one side, Dorms on the other, Admin/Library central
    
    zones = [
        # x, y, w, d, h, color, name
        (0, 5, 3, 3, 4, 'red', 'Zone 1: Engineering (High Load)'),
        (5, 5, 3, 3, 3, 'blue', 'Zone 2: Library (Study)'),
        (5, 0, 2, 2, 2, 'gray', 'Zone 3: Admin'),
        (0, 0, 2.5, 2.5, 2, 'cyan', 'Zone 4: Science F1'),
        (0, 0, 2.5, 2.5, 4, 'cyan', 'Zone 5: Science F2 (Stacked)'), # Stacked visually by height
        (10, 5, 2, 4, 1.5, 'orange', 'Zone 6: Cafeteria'),
        (10, 0, 2, 2, 3, 'green', 'Zone 7: Dorms East'),
        (12, 0, 2, 2, 3, 'green', 'Zone 8: Dorms West'),
    ]

    for x, y, w, d, h, c, name in zones:
        fig.add_trace(create_cube(x, y, w, d, h, c, name))
        # Add a text label above the building
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[h + 0.5],
            mode='text', text=[name],
            textposition="top center", showlegend=False
        ))

    # --- 2. INPUTS (Solar & Grid) ---
    # Solar array visualization above buildings
    fig.add_trace(go.Mesh3d(
        x=[-2, 14, 14, -2], y=[-2, -2, 8, 8], z=[6, 6, 6, 6],
        color='yellow', opacity=0.1, name='Solar Potential (Input)'
    ))
    
    # Representing the Grid connection
    fig.add_trace(go.Scatter3d(
        x=[-5], y=[2.5], z=[0],
        mode='markers+text', marker=dict(size=10, color='black'),
        text=["GRID INPUT"], name="Main Grid Feed"
    ))

    # --- 3. THE SYSTEM BRAIN (Orchestrator Agent) ---
    # Central AI Node
    ai_x, ai_y, ai_z = 5, 2.5, 8
    fig.add_trace(go.Scatter3d(
        x=[ai_x], y=[ai_y], z=[ai_z],
        mode='markers+text', marker=dict(size=15, color='purple', symbol='diamond'),
        text=["<b>AI ORCHESTRATOR</b>"], textposition="top center",
        name='AI System Brain'
    ))

    # --- 4. DATA FLOWS (Inputs & Outputs) ---
    # Connect AI to all buildings (Monitoring & Control)
    for x, y, w, d, h, c, name in zones:
        # Line from AI to building roof
        fig.add_trace(go.Scatter3d(
            x=[ai_x, x], y=[ai_y, y], z=[ai_z, h],
            mode='lines', line=dict(color='purple', width=2, dash='dot'),
            hoverinfo='none', showlegend=False
        ))

    # --- LAYOUT SETTINGS ---
    fig.update_layout(
        title="3D Visualization: Multi-Zone University Energy System",
        scene=dict(
            xaxis=dict(title="East-West"),
            yaxis=dict(title="North-South"),
            zaxis=dict(title="Elevation/Load"),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    print("Generating 3D Visualization...")
    fig.show()

if __name__ == "__main__":
    visualize_campus_system()