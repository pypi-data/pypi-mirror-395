import numpy as np
import plotly.graph_objects as go

# Function to calculate integer points based on equations
def calculate_points(equation_id, t_max, u_max):
    points = []
    for t in range(1, t_max + 1):
        for u in range(1, u_max + 1):
            if equation_id == 1:
                n = 6 * t * u + t + u
            elif equation_id == 2:
                n = 6 * t * u - t - u
            elif equation_id == 3:
                n = 6 * t * u + t - u
            elif equation_id == 4:
                n = 6 * t * u - t + u
            points.append((t, u, n))
    return points

# Function to add traces for points and lines
def add_traces(fig, points, color, label, show_t_lines=False, show_u_lines=False):
    t_vals, u_vals, n_vals = zip(*points)

    # Add points trace
    fig.add_trace(
        go.Scatter3d(
            x=t_vals,
            y=u_vals,
            z=n_vals,
            mode="markers",
            marker=dict(size=5, color=color),
            name=f"{label} Points",
            legendgroup=label,
            hovertemplate="t: %{x}<br>u: %{y}<br>n: %{z}<extra></extra>",
        )
    )

    # Add lines for each t value
    if show_t_lines:
        for t in range(1, max(t_vals) + 1):
            t_line_points = [(t, u, n) for t_, u, n in points if t_ == t]
            if len(t_line_points) > 1:
                t_vals_line, u_vals_line, n_vals_line = zip(*t_line_points)
                fig.add_trace(
                    go.Scatter3d(
                        x=t_vals_line,
                        y=u_vals_line,
                        z=n_vals_line,
                        mode="lines",
                        line=dict(color=color, width=2),
                        name=f"{label} t={t} Line",
                        legendgroup=label,
                        showlegend=False,
                    )
                )

    # Add lines for each u value
    if show_u_lines:
        for u in range(1, max(u_vals) + 1):
            u_line_points = [(t, u, n) for t, u_, n in points if u_ == u]
            if len(u_line_points) > 1:
                t_vals_line, u_vals_line, n_vals_line = zip(*u_line_points)
                fig.add_trace(
                    go.Scatter3d(
                        x=t_vals_line,
                        y=u_vals_line,
                        z=n_vals_line,
                        mode="lines",
                        line=dict(color=color, width=2, dash="dot"),
                        name=f"{label} u={u} Line",
                        legendgroup=label,
                        showlegend=False,
                    )
                )

# Function to plot equations
def plot_equations(t_max, u_max):
    colors = ["red", "blue", "green", "purple"]
    labels = [
        "n = 6t.u + t + u",
        "n = 6t.u - t - u",
        "n = 6t.u + t - u",
        "n = 6t.u - t + u",
    ]

    fig = go.Figure()

    for equation_id in range(1, 5):
        points = calculate_points(equation_id, t_max, u_max)
        add_traces(fig, points, colors[equation_id - 1], labels[equation_id - 1], show_t_lines=True, show_u_lines=True)

    fig.update_layout(
        scene=dict(
            xaxis_title="t",
            yaxis_title="u",
            zaxis_title="n",
        ),
        title="3D Plot of Integer Points with Toggleable Lines and Points",
        legend=dict(
            title="Toggle Visibility",
            itemsizing="constant",
        ),
    )

    fig.show()

# Example usage
plot_equations(t_max=100, u_max=100)
