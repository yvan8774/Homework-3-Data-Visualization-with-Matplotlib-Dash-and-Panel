import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Provided data for x, y, and z
x_values = [-21, -15, -9, -9, -13, -9, -1, -15, -7, -13, -11, -7, -9, -9, -11, -13, 
            -11, -25, -19, -19, 0, -17, -9, -9, -17, -17, -11, -11, -19]

y_values = [9, 19, 23, 27, 17, 21, 23, 21, 31, 19, 15, 21, 23, 31, 35, 31, 
            19, 15, 21, 21, 9, 17, 9, 25, 23, 9, 11, 15, 21]

z_values = [-1011, -1011, -1020, -1013, -1020, -1024, -1016, -1016, -1015, -1018, 
            -1020, -1028, -1018, -1013, -1024, -1016, -1018, -1026, -1022, -1013, 
            -1018, -1015, -1016, -1016, -1018, -1026, -1026, -1018, -1013]

# Create a DataFrame
df = pd.DataFrame({'x': x_values, 'y': y_values, 'z': z_values})

# 1. Histogram of x, y, z distributions
plt.figure(figsize=(12, 6))
plt.hist(df['x'], bins=10, alpha=0.5, color='blue', label='x values')
plt.hist(df['y'], bins=10, alpha=0.5, color='green', label='y values')
plt.hist(df['z'], bins=10, alpha=0.5, color='red', label='z values')
plt.title("The X- Y- and Z-axes of the accelerometer (Bosch CISS Sensor) ")
plt.xlabel("accelerometer x_axis")
plt.ylabel("accelerometer y_axis")
plt.legend()
plt.show()

# 2. 3D Scatter Plot of x, y, z with color and size based on z and y values
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot with x, y, and z; color by z and size by y
scatter = ax.scatter(df['x'], df['y'], df['z'], c=df['z'], s=(df['y'] * 10), cmap='viridis', alpha=0.7)
ax.set_title("3D Scatter Plot of x, y, and z")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
fig.colorbar(scatter, label='z value')

plt.show()


# Initialize the Dash app
app = dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Interactive 3D Scatter Plot"),
    
    # Dropdown for selecting x-axis
    html.Label("Select X-axis:"),
    dcc.Dropdown(
        id='x-axis',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='x'
    ),
    
    # Dropdown for selecting y-axis
    html.Label("Select Y-axis:"),
    dcc.Dropdown(
        id='y-axis',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='y'
    ),
    
    # Dropdown for selecting color dimension
    html.Label("Select Color Dimension:"),
    dcc.Dropdown(
        id='color-dimension',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='z'
    ),
    
    # Slider for point size scaling
    html.Label("Adjust Point Size:"),
    dcc.Slider(
        id='point-size',
        min=5,
        max=50,
        step=5,
        value=15
    ),
    
    # Scatter plot
    dcc.Graph(id='scatter-plot')
])

# Callback to update the scatter plot based on user selections
@app.callback(
    Output('scatter-plot', 'figure'),
    [
        Input('x-axis', 'value'),
        Input('y-axis', 'value'),
        Input('color-dimension', 'value'),
        Input('point-size', 'value')
    ]
)
def update_scatter_plot(x_axis, y_axis, color_dimension, point_size):
    fig = px.scatter(df, x=x_axis, y=y_axis, color=color_dimension, 
                     size=[point_size] * len(df), title=f'Scatter Plot: {x_axis} vs {y_axis} with Color {color_dimension}')
    fig.update_layout(transition_duration=500)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
 
   