from typing import Tuple, Iterable, Union
from jaxtyping import Float, Integer
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as psub
from plotly.figure_factory._quiver import _Quiver
from ..plotting.image_utils import image_type, normalize, to_color
    
def visualize_2d(
    pointsets: Iterable[Tuple[str,Union[Float[np.ndarray, "N 2"],Float[np.ndarray, "N 3"]]]]=None,
    vectors: Float[np.ndarray, "N 4"]=None,
    paths: Iterable[Tuple[str,Float[np.ndarray, "N 2"]]]=None,
    title: str="Manifold",
    x_label: str="X",
    y_label: str="Y",
    save_name: str=None,
    show: bool=False,
    fig_size: Tuple[int, int]=(800,800),
    cmap: str="Viridis",
    marker_size: Union[int,Iterable[int]]=8,
    marker_opacity: Union[float,Iterable[float]]=1.,
    vector_scale: float=0.1,
    vector_opacity: float=1.0,
    vector_arrow_scale: float=0.5,
    vector_arrow_angle: float=np.pi/9,
    vector_arrow_width: int=2,
    path_width: Union[int,Iterable[int]]=3,
    path_marker_size: Union[int,Iterable[int]]=10,
) -> go.Figure:
    fig = go.Figure()
    color_count = 0
    if pointsets is not None:
        colorbar_offset = 0
        for i,pointset in enumerate(pointsets):
            label, data = pointset
            fig.add_trace(go.Scatter(
                x=data[:,0],
                y=data[:,1],
                mode='markers',
                marker=dict(
                    size=marker_size[i] if isinstance(marker_size,Iterable) else marker_size,
                    color=data[:,2] if data.shape[1]>2 else px.colors.qualitative.Dark24[color_count],
                    colorscale=cmap if data.shape[1]>2 else None,
                    colorbar=dict(title=label, x=1.2+0.2*colorbar_offset) if data.shape[1]>2 else None,
                ),
                opacity=marker_opacity[i] if isinstance(marker_opacity,Iterable) else marker_opacity,
                customdata=data[:,2] if data.shape[1]>2 else None,
                hovertemplate=(
                    'x: %{x:.4g}<br>' +
                    'y: %{y:.4g}<br>' +
                    ('v: %{customdata:.4g}<br>' if data.shape[1]>2 else '')
                ),
                name=label
            ))
            if data.shape[1]==2:
                color_count+=1
            else:
                colorbar_offset+=1
    if vectors is not None:  
        quiver_obj = _Quiver(vectors[:, 0], vectors[:, 1], vectors[:, 2], vectors[:, 3], scale=vector_scale, arrow_scale=vector_arrow_scale, angle=vector_arrow_angle)
        barb_x, barb_y = quiver_obj.get_barbs()
        arrow_x, arrow_y = quiver_obj.get_quiver_arrows()
        angles = np.arctan2(vectors[:, 3], vectors[:, 2]) * (180 / np.pi)
        for i in range(len(barb_x) // 3):
            fig.add_trace(go.Scatter(
                x=barb_x[i * 3:(i + 1) * 3],
                y=barb_y[i * 3:(i + 1) * 3],
                mode='lines',
                line=dict(color=f'hsl({angles[i]}, 100%, 50%)', width=vector_arrow_width),
                showlegend=False,
                legendgroup='Vector Field',
            ))
        for i in range(len(arrow_x) // 4):
            fig.add_trace(go.Scatter(
                x=arrow_x[i * 4:(i + 1) * 4],
                y=arrow_y[i * 4:(i + 1) * 4],
                mode='lines',
                line=dict(color=f'hsl({angles[i]}, 100%, 50%)', width=vector_arrow_width),
                opacity=vector_opacity,
                legendgroup='Vector Field',
                name='Vector Field' if i == 0 else None,
                showlegend=(i == 0),
            ))
    if paths is not None:
        for i,path in enumerate(paths):
            label, steps = path
            color = px.colors.qualitative.Dark24[color_count]
            fig.add_trace(go.Scatter(
                x=steps[:,0],
                y=steps[:,1],
                mode='lines+markers',
                line=dict(width=path_width[i] if isinstance(path_width,Iterable) else path_width, color=color),
                marker=dict(size=path_marker_size[i] if isinstance(path_marker_size,Iterable) else path_marker_size, color=color, symbol="arrow-bar-up", angleref="previous"),
                name=label,
                legendgroup=label,
                showlegend=True,
            ))
            fig.add_trace(go.Scatter(
                x=[steps[0, 0], steps[-1, 0]],
                y=[steps[0, 1], steps[-1, 1]],
                mode='markers',
                marker=dict(size=path_marker_size[i] if isinstance(path_marker_size,Iterable) else path_marker_size, color=color, symbol='circle'),
                name=f'{label} Start',
                legendgroup=label,
                showlegend=False
            ))
            color_count+=1
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        xaxis=dict(scaleanchor="y", scaleratio=1),
        width=fig_size[0],
        height=fig_size[1],
        template="plotly_white",
    )
    if save_name:
        fig.write_html(f"{save_name}.html")
        fig.write_image(f"{save_name}.png")
    if show:
        fig.show()
    return fig

def visualize_3d(
    pointsets: Iterable[Tuple[str,Union[Float[np.ndarray, "N 3"],Float[np.ndarray, "N 4"]]]]=None,
    vectors: Float[np.ndarray, "num_scores 6"] = None,
    paths: Iterable[Tuple[str, Float[np.ndarray, "path_length 3"]]] = None,
    title: str = "Manifold",
    x_label: str = "X",
    y_label: str = "Y",
    z_label: str = "Z",
    save_name: str = None,
    show: bool = False,
    fig_size: Tuple[int, int] = (800, 800),
    cmap: str = "Viridis",
    marker_size: Union[int,Iterable[int]]=8,
    marker_opacity: Union[float,Iterable[float]]=1.,
    vector_scale: float = 0.1,
    vector_opacity: float = 1.0,
    path_width: Union[int,Iterable[int]]=3,
    path_marker_size: Union[int,Iterable[int]]=10,
) -> go.Figure:
    fig = go.Figure()
    color_count = 0
    if pointsets is not None:
        colorbar_offset = 0
        for i,pointset in enumerate(pointsets):
            label, data = pointset
            fig.add_trace(go.Scatter3d(
                x=data[:, 0],
                y=data[:, 1],
                z=data[:, 2],
                mode='markers',
                marker=dict(
                    size=marker_size[i] if isinstance(marker_size,Iterable) else marker_size,
                    color=data[:,3] if data.shape[1]>3 else px.colors.qualitative.Dark24[color_count],
                    colorscale=cmap if data.shape[1]>3 else None,
                    colorbar=dict(title=label, x=1.2+0.2*colorbar_offset) if data.shape[1]>3 else None,
                ),
                opacity=marker_opacity[i] if isinstance(marker_opacity,Iterable) else marker_opacity,
                name=label,
                customdata=data[:,3] if data.shape[1]>3 else None,
                hovertemplate=(
                    'x: %{x:.4g}<br>' +
                    'y: %{y:.4g}<br>' +
                    'z: %{z:.4g}<br>' +
                    ('v: %{customdata:.4g}<br>' if data.shape[1]>3 else '')
                ),
            ))
            if data.shape[1]==3:
                color_count+=1
            else:
                colorbar_offset+=1
    if vectors is not None:
        angles = np.arctan2(vectors[:, 5], vectors[:, 4]) * (180 / np.pi) + 360
        magnitude = np.linalg.norm(vectors[:,3:6]-vectors[:,:3],axis=1)
        for i in range(vectors.shape[0]):
            fig.add_trace(go.Cone(
                x=[vectors[i, 0]],
                y=[vectors[i, 1]],
                z=[vectors[i, 2]],
                u=[vectors[i, 3]],
                v=[vectors[i, 4]],
                w=[vectors[i, 5]],
                sizemode="absolute",
                sizeref=vector_scale*np.log(magnitude[i]+2),
                colorscale=[f'hsl({angles[i]}, 100%, 50%)',f'hsl({angles[i]}, 100%, 50%)'],
                opacity=vector_opacity,
                anchor="tail",
                showscale=False,
                legendgroup="Vector Field",
                name="Vector Field",
                showlegend=(i==0),
            ))
    if paths is not None:
        for i, path in enumerate(paths):
            label, steps = path
            color = px.colors.qualitative.Dark24[color_count]
            fig.add_trace(go.Scatter3d(
                x=steps[:, 0],
                y=steps[:, 1],
                z=steps[:, 2],
                mode='lines+markers',
                line=dict(width=path_width[i] if isinstance(path_width,Iterable) else path_width, color=color),
                marker=dict(size=path_marker_size[i] if isinstance(path_marker_size,Iterable) else path_marker_size, color=color, symbol="circle"),
                name=label,
                legendgroup=label,
                showlegend=True,
            ))
            for j in range(1,len(steps)):
                fig.add_trace(go.Cone(
                    x=[steps[j, 0]],
                    y=[steps[j, 1]],
                    z=[steps[j, 2]],
                    u=[steps[j, 0]-steps[j-1, 0]],
                    v=[steps[j, 1]-steps[j-1, 1]],
                    w=[steps[j, 2]-steps[j-1, 2]],
                    sizemode="absolute",
                    sizeref=path_marker_size/400.,
                    colorscale=[color,color],
                    showscale=False,
                    anchor="tail",
                    name=label,
                    legendgroup=label,
                    showlegend=False,
                ))
            color_count+=1
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=x_label,
            yaxis_title=y_label,
            zaxis_title=z_label,
            aspectmode='data',
        ),
        width=fig_size[0],
        height=fig_size[1],
        template="plotly_white",
    )
    if save_name:
        fig.write_html(f"{save_name}.html")
        fig.write_image(f"{save_name}.png")
    if show:
        fig.show()
    return fig

def visualize_image_grid(
    images: Union[
        Integer[np.ndarray, "N w h"],
        Integer[np.ndarray, "N w h 3"]
    ],
    rows: int,
    cols: int,
    title: str="Image Grid",
    labels: Iterable[str]=None,
    save_name: str=None,
    show: bool=False,
) -> go.Figure:
    """Plots the images in an image grid using plotly"""
    fig = psub.make_subplots(rows=rows, cols=cols, 
                             subplot_titles=[f"Image {i+1}" for i in range(len(images))] if labels is None else labels,
                             vertical_spacing=0.1, horizontal_spacing=0.1)
    for i, image in enumerate(images):
        row = i // cols + 1
        col = i % cols + 1
        if image_type(image)=="grayscale":
            image = to_color(normalize(image))
        fig.add_trace(
            go.Image(z=image),
            row=row, col=col
        )
    fig.update_layout(
        height=300*rows,
        width=300*cols,
        showlegend=False,
        title=title,
    )
    if save_name:
        fig.write_html(f"{save_name}.html")
        fig.write_image(f"{save_name}.png")
    if show:
        fig.show()
    return fig

def heatmap(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    z_col: str,
    title: str="Heatmap",
    x_label: str=None,
    y_label: str=None,
    z_label: str=None,
    cmap: str="Reds",
    save: str=None,
    origin: str="upper",
):
    heatmap_data = df.pivot(index=y_col, columns=x_col, values=z_col)

    plt.figure(figsize=(5, 4), dpi=150)
    plt.imshow(heatmap_data, cmap=cmap, aspect='equal', origin=origin)
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            value = heatmap_data.iloc[i, j]
            plt.text(j, i, f"{value:.3f}", ha='center', va='center', color=('white' if value > heatmap_data.values.max()/2 else 'black') if (cmap is None or cmap[-2:]!="_r") else ('white' if value < heatmap_data.values.max()/2 else 'black'))

    plt.xticks(ticks=np.arange(len(heatmap_data.columns)), labels=heatmap_data.columns)
    plt.yticks(ticks=np.arange(len(heatmap_data.index)), labels=heatmap_data.index)
    plt.title(title)
    plt.xlabel(x_label if x_label is not None else x_col)
    plt.ylabel(y_label if y_label is not None else y_col)
    plt.colorbar(label=z_label if z_label is not None else z_col)
    plt.tight_layout()

    if save:
        os.makedirs(os.path.dirname(save), exist_ok=True)
        plt.savefig(save)
    plt.show()