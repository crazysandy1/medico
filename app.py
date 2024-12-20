from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

# Initialize Dash app
app = Dash(__name__)
app.layout = ...

if __name__ == '__main__':
    app.run_server(debug=True)

# Simulate drug response function
def simulate_drug_response(potency, specificity, toxicity, half_life, time_points=48):
    time = np.arange(time_points)
    viability = [1.0]
    resistance = [0.05]
    drug_concentration = [1.0]

    for t in range(1, time_points):
        current_concentration = drug_concentration[-1] * np.exp(-0.1 / half_life)
        drug_effect = potency * current_concentration * (1 - resistance[-1])
        viability.append(max(0, viability[-1] - drug_effect))
        resistance.append(resistance[-1] + drug_effect * 0.1)
        drug_concentration.append(current_concentration)

    return time, viability, resistance, drug_concentration

# Layout for Dash app
app.layout = html.Div([
    html.H1("Drug Response Simulation Dashboard", style={'textAlign': 'center'}),

    # Controls
    html.Div([
        html.Label("Drug Potency"),
        dcc.Slider(id='potency', min=0.1, max=1.0, step=0.05, value=0.85),
        
        html.Label("Drug Specificity"),
        dcc.Slider(id='specificity', min=0.1, max=1.0, step=0.05, value=0.9),

        html.Label("Drug Toxicity"),
        dcc.Slider(id='toxicity', min=0.0, max=0.5, step=0.05, value=0.1),

        html.Label("Drug Half-Life"),
        dcc.Slider(id='half_life', min=1, max=24, step=1, value=10),
    ], style={'width': '50%', 'margin': 'auto'}),

    # Graphs
    dcc.Graph(id='response-graph'),

    # Metrics
    html.Div(id='metrics', style={'textAlign': 'center', 'marginTop': '20px'})
])

# Callbacks for interactivity
@app.callback(
    [Output('response-graph', 'figure'),
     Output('metrics', 'children')],
    [Input('potency', 'value'),
     Input('specificity', 'value'),
     Input('toxicity', 'value'),
     Input('half_life', 'value')]
)
def update_graph(potency, specificity, toxicity, half_life):
    # Simulate drug response
    time, viability, resistance, drug_concentration = simulate_drug_response(
        potency, specificity, toxicity, half_life
    )

    # Create the graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=viability, mode='lines', name='Viability', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=time, y=resistance, mode='lines', name='Resistance', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=time, y=drug_concentration, mode='lines', name='Drug Concentration', line=dict(color='red')))
    fig.update_layout(title="Drug Response Over Time", xaxis_title="Time (hours)", yaxis_title="Proportion")

    # Calculate AUC and final metrics
    auc_score = np.trapz(1 - np.array(viability), dx=1)
    final_viability = viability[-1]
    final_resistance = resistance[-1]

    metrics = [
        html.P(f"Area Under Curve (AUC): {auc_score:.2f}"),
        html.P(f"Final Cell Viability: {final_viability:.2%}"),
        html.P(f"Final Resistance Level: {final_resistance:.3f}")
    ]

    return fig, metrics

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
