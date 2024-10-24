import numpy as np
import plotly.graph_objects as go
from math import *
import mpmath
from ipywidgets import interact, widgets, Text, Layout

formula = Text(value='(1 - cos(((4)/2)*x))/2', layout=Layout(width='100%'),description='⚪ᗩ⚪ᙁ⚪ᑎ⚪ᙏ⚪ᴥ⚪Ⓞ⚪ꗳ⚪◌⚪◌⚪◌⚪◌⚪◌⚪◌⚪ꗳ⚪Ⓞ⚪ᴥ⚪ᙏ⚪ᑎ⚪ᙁ⚪ᗩ⚪')
N_slider = widgets.IntSlider(min=1, max=16, value=8,layout=Layout(width='100%'),readout_format='.256f',description='⚪ᴥ⚪ᗱᗴ⚪ᗯ⚪Ⓞ⚪ߦ⚪◯⚪ᴥ⚪ᗱᗴ⚪⚭⚪ᙏ⚪ᑎ⚪ИN⚪◯⚪✤⚪ИN⚪ꖴ⚪Ⓞ⚪ᑫᑭ⚪◌⚪◌⚪◌⚪◌⚪◌⚪◌⚪ᑫᑭ⚪Ⓞ⚪ꖴ⚪ИN⚪✤⚪◯⚪ИN⚪ᑎ⚪ᙏ⚪⚭⚪ᗱᗴ⚪ᴥ⚪◯⚪ߦ⚪Ⓞ⚪ᗯ⚪ᗱᗴ⚪ᴥ⚪')
RANGE_FROM_SLIDER=widgets.FloatSlider(min=0, max=4*(4*atan(1)), value=0*(4*atan(1)), step=(4*atan(1))/4, layout=Layout(width='100%'),readout_format='.256f',description='⚪ᙏ⚪Ⓞ⚪ᴥ⚪ꗳ⚪◯⚪ᗱᗴ⚪ᕤᕦ⚪ИN⚪ᗩ⚪ᴥ⚪◌⚪◌⚪◌⚪◌⚪◌⚪◌⚪ᴥ⚪ᗩ⚪ИN⚪ᕤᕦ⚪ᗱᗴ⚪◯⚪ꗳ⚪ᴥ⚪Ⓞ⚪ᙏ⚪')
RANGE_TO_SLIDER=widgets.FloatSlider(min=0, max=4*(4*atan(1)), value=4*(4*atan(1)),step=(4*atan(1))/4, layout=Layout(width='100%'),readout_format='.256f',description='⚪Ⓞ⚪✤⚪◯⚪ᗱᗴ⚪ᕤᕦ⚪ИN⚪ᗩ⚪ᴥ⚪◌⚪◌⚪◌⚪◌⚪◌⚪◌⚪ᴥ⚪ᗩ⚪ИN⚪ᕤᕦ⚪ᗱᗴ⚪◯⚪✤⚪Ⓞ⚪')

def clamp(x):
    return max(min(1, x), -1)
def kappa(formula, x):
    func_dict = {fn: eval(f'lambda *args: mpmath.{fn}(*args)') for fn in dir(mpmath)}
    return float(eval(formula, {'x': x, 'clamp': clamp, **func_dict}))
def plot(formula='(1 - cos(((4)/2)*x))/2', RANGE_FROM=0*(4*atan(1)), RANGE_TO=4*(4*atan(1)), N=8):
    num_points = 1+2**N

    # Generate x values with the specified number of points
    x_vals = np.linspace(RANGE_FROM, RANGE_TO, num_points)

    # Compute kappa values
    kappa_vals = np.array([kappa(formula, x_val) for x_val in x_vals])

    theta_vals = np.cumsum(kappa_vals) * (x_vals[1]-x_vals[0]) if num_points > 1 else np.array([0])
    x_coords_ = np.cumsum(np.cos(theta_vals)) * (x_vals[1] - x_vals[0]) if num_points > 1 else np.array([0])
    y_coords_ = np.cumsum(np.sin(theta_vals)) * (x_vals[1] - x_vals[0]) if num_points > 1 else np.array([0])

    # Check if the first point is zero, if not, add it manually
    if x_coords_[0] != 0 or y_coords_[0] != 0:
        x_coords = np.insert(x_coords_, 0, 0)
        y_coords = np.insert(y_coords_, 0, 0)
    else:
        x_coords = x_coords_
        y_coords = y_coords_

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_coords,y=y_coords,mode='lines',line=dict(color='#CECECE'),name='',hovertemplate ='X:%{x:.256f}'+'<br>Y:%{y:.256f}'))

    fig.update_layout(
        autosize=True,
        xaxis=dict(scaleanchor='y',scaleratio=1,gridcolor='#CECECE',zeroline=True,zerolinecolor='#CECECE',tickfont=dict(color='#9C9C9C')),
        yaxis=dict(                             gridcolor='#CECECE',zeroline=True,zerolinecolor='#CECECE',tickfont=dict(color='#9C9C9C')),
        hoverlabel=dict(bgcolor="#FFFFFF",font_color='#9C9C9C',bordercolor="#CECECE"),plot_bgcolor='#FFFFFF'
        )
        
    fig.show()

# Create the interactive plot
interact(plot, formula=formula, RANGE_FROM=RANGE_FROM_SLIDER, RANGE_TO=RANGE_TO_SLIDER, N=N_slider);