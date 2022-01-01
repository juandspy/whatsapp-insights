import streamlit as st
from io import StringIO

from reader import chat_to_df

st.title("Whatsapp Insights")

uploaded_file = st.file_uploader("Choose a file")
@st.cache
def load_data():
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        df = chat_to_df(stringio)
        return df
    uploaded_file
df = load_data()

stacked_bars = st.checkbox("Select this if you want the graphs to be stacked by user")

if df is not None:
    with st.expander("These are all the messages I gathered:"):
        st.dataframe(df)

    from ploter import plot_pie
    st.write("This is the participation per user:")
    vc = df["user"].value_counts()
    fig = plot_pie(
        labels = vc.keys().tolist(),
        values= vc.tolist()
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("This is the number of messages during all this time:")
    from ploter import plot_historical_chat
    fig = plot_historical_chat(df, stacked_bars)
    st.plotly_chart(fig, use_container_width=True)

    st.write("This is the time of the day when you talk the most:")
    from ploter import plot_daily_chat
    fig = plot_daily_chat(df, stacked_bars)
    st.plotly_chart(fig, use_container_width=True)    