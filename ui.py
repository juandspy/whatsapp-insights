import streamlit as st
from io import StringIO

from reader import chat_to_df

st.title("Whatsapp Insights")

demo_mode = st.checkbox(
    "Demo mode (uncheck me for uploading your own files)",
    value = True )

if demo_mode:
    with open("input.txt", "r", encoding="utf8") as f:
        df = chat_to_df(f)
else:
    uploaded_file = st.file_uploader("Choose a Whatsapp chat")

    with st.expander("Don't know how to export a chat?"):
        st.write("Visit https://faq.whatsapp.com/android/chats/how-to-save-your-chat-history")

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

    st.write("These are the most common words:")
    max_words = st.number_input(
        "Max words", 
        min_value=10, 
        max_value=500, 
        value=100, 
        step=1)
    from ploter import plot_wordcloud
    wordcloud = plot_wordcloud(df["message"].str.cat(sep=' '), max_words)
    st.image(wordcloud, use_column_width=True)