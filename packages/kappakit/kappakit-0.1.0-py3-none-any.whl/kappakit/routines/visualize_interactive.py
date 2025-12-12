import os
import jsonargparse
from datasets import load_dataset, DatasetDict, Dataset
import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
from kappakit.curvature.curvature import *
from kappakit.plotting.visualize import visualize_3d

# Initialize the Dash app
app = dash.Dash(__name__)

# Dash layout
app.layout = html.Div([
    # Header div
    html.Div([
        html.H1("KappaKit: Estimating Curvature of a Manifold from Data", style={
            'textAlign': 'center',
            'marginBottom': '20px',
            'color': '#333',
            'fontFamily': 'Helvetica, sans-serif',
            'fontSize': '36px'
        }),
        html.P("Harvard Geometric ML Lab", style={
            'textAlign': 'center',
            'color': '#333',
            'fontFamily': 'Helvetica, sans-serif',
            'fontSize': '24px'
        }),
    ], style={
        'backgroundColor': '#eaeaea',
        'padding': '30px 10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),

    # Input div
    html.Div([
        html.P("This visualization tool looks at each point's curvature results. Remember that positive curvature indicates more spherical and negative curvature indicates more hyperbolic. \
                Please input objects to visualize as a comma-separated lines in the form 'kind,label,size,path'. Kind can be one of 'dataset', 'scalar', 'mean', 'gaussian', 'principal1', 'principal2', 'vectors', or 'path'. \
                Label is the string to associate the object with. Suggested sizes are 8 for pointsets, 0.1 for vectors, and 10 for paths. Path is the local or HF path to the object. \
                E.g., dataset,sphere,8,data/unit_sphere", style={
            'textAlign': 'left',
            'color': '#333',
            'fontFamily': 'Helvetica, sans-serif',
            'fontSize': '18px'
        }),

        dcc.Textarea(
            id='textarea-input',
            placeholder='',
            style={'width': '100%', 'height': '150px', 'padding': '10px', 'borderRadius': '8px', 'fontSize': '16px'}
        ),

        html.Div([
            html.Button("Visualize", id="visualize-button", n_clicks=0, style={
                'padding': '10px 20px',
                'fontSize': '16px',
                'borderRadius': '8px',
                'backgroundColor': '#007BFF',
                'color': 'white',
                'border': 'none',
                'cursor': 'pointer'
            })
        ], style={'textAlign': 'center', 'marginTop': '20px'}),

        html.P(id='error-message', style={'color': 'red', 'marginTop': '10px', 'fontFamily': 'Helvetica, sans-serif',}),
    ], style={
        'padding': '10px 20px',
        'borderRadius': '8px',
    }),

    # Figure div
    html.Div([
        html.Div([
            dcc.Graph(id='scatter-plot', config={
                'toImageButtonOptions': {
                    'format': 'png',  # one of png, svg, jpeg, webp
                    'filename': 'plot',
                    'height': None,
                    'width': None,
                    'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
                }
            }),
        ], style={
            'flex': '1',
            'marginRight': '20px'
        }),
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'margin': '20px',
        'flexWrap': 'wrap'
    }),
], style={
    'fontFamily': 'Helvetica, sans-serif',
    'margin': '0 auto',
    'width': '80%',
    'maxWidth': '1200px',
    'backgroundColor': '#f7f7f7',
    'paddingBottom': '1em',
})

# Callback to update graph based on text input
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('error-message', 'children')],
    Input('visualize-button', 'n_clicks'),
    State('textarea-input', 'value')
)
def update_data(n_clicks: int, text_input: str) -> go.Figure:
    if n_clicks == 0:
        return go.Figure(), ""
    try:
        pointsets = []
        vectors = None
        paths = []
        marker_sizes = []
        vector_scale = None
        path_sizes = []
        for line in text_input.split("\n"):
            kind, label, size, path = line.split(",")
            if kind=="dataset":
                if os.path.exists(path):
                    manifold = DatasetDict.load_from_disk(path)["manifold"].with_format("numpy")["points"]
                else:
                    manifold = load_dataset(path)["manifold"].with_format("numpy")["points"]
                pointsets.append((label,manifold))
                marker_sizes.append(float(size))
            elif kind=="scalar":
                if os.path.exists(path):
                    curvature = Dataset.load_from_disk(path).with_format("numpy")
                else:
                    curvature = load_dataset(path)["train"].with_format("numpy")
                pointsets.append((label,np.concatenate([curvature["points"],[[scalar_from_sff(sff)] for sff in curvature["sffs"]]],axis=1)))
                marker_sizes.append(float(size))
            elif kind=="mean":
                if os.path.exists(path):
                    curvature = Dataset.load_from_disk(path).with_format("numpy")
                else:
                    curvature = load_dataset(path)["train"].with_format("numpy")
                pointsets.append((label,np.concatenate([curvature["points"],[[mean_from_sff(sff,[1.])] for sff in curvature["sffs"]]],axis=1)))
                marker_sizes.append(float(size))
            elif kind=="gaussian":
                if os.path.exists(path):
                    curvature = Dataset.load_from_disk(path).with_format("numpy")
                else:
                    curvature = load_dataset(path)["train"].with_format("numpy")
                pointsets.append((label,np.concatenate([curvature["points"],[[gaussian_from_sff(sff,[1.])] for sff in curvature["sffs"]]],axis=1)))
                marker_sizes.append(float(size))
            elif kind=="principal1":
                if os.path.exists(path):
                    curvature = Dataset.load_from_disk(path).with_format("numpy")
                else:
                    curvature = load_dataset(path)["train"].with_format("numpy")
                pointsets.append((label,np.concatenate([curvature["points"],[[principal_from_sff(sff,[1.])[0]] for sff in curvature["sffs"]]],axis=1)))
                marker_sizes.append(float(size))
            elif kind=="principal2":
                if os.path.exists(path):
                    curvature = Dataset.load_from_disk(path).with_format("numpy")
                else:
                    curvature = load_dataset(path)["train"].with_format("numpy")
                pointsets.append((label,np.concatenate([curvature["points"],[[principal_from_sff(sff,[1.])[1]] for sff in curvature["sffs"]]],axis=1)))
                marker_sizes.append(float(size))
            elif kind=="vectors":
                vectors = DatasetDict.load_from_disk(path)["vectors"].with_format("numpy")["points"]
                vector_scale = float(size)
            elif kind=="path":
                if os.path.exists(path):
                    geodesic = DatasetDict.load_from_disk(path)["geodesic"].with_format("numpy")["points"]
                else:
                    geodesic = load_dataset(path)["geodesic"].with_format("numpy")["points"]
                paths.append((label,geodesic))
                path_sizes.append(float(size))
            else:
                raise ValueError("Unexpected value for 'kind'")
        fig = visualize_3d(
            pointsets=pointsets,
            vectors=vectors,
            paths=paths,
            marker_size=marker_sizes,
            vector_scale=vector_scale,
            path_marker_size=path_sizes,
        )
        return fig, ""
    except Exception as e:
        return go.Figure(), f"Error: {str(e)}"


# Run the app
if __name__ == '__main__':
    parser = jsonargparse.ArgumentParser()
    parser.add_argument("--config", action="config")
    parser.add_argument("--host", type=str, required=False, default="127.0.0.1", help="Host to launch webapp")
    parser.add_argument("--port", type=str, required=False, default="8050", help="Port to launch webapp")
    parser.add_argument("--debug", type=bool, required=False, default=False, help="Debug mode")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)
