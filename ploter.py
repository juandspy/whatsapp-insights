import plotly.graph_objects as go


def plot_pie(labels, values):
    return go.Figure(
        data=[go.Pie(labels=labels, values=values, hole=.3)])

def plot_historical_chat(df, stacked=True):
    users = df["user"].unique()
    data = [
        go.Histogram(x=df[df["user"] == user]["date"], name=user) for user in users
    ]
    fig = go.Figure(data)
    if stacked:
        fig.update_layout(barmode='stack')
    return fig

def plot_daily_chat(df, accumulative=True):
    temp_df = df.copy()
    temp_df["date"] = temp_df["date"].dt.hour
    return plot_historical_chat(temp_df, accumulative)

