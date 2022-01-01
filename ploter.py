import plotly.graph_objects as go
from streamlit import cache as st_cache

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

from wordcloud import WordCloud, STOPWORDS

SPANISH_STOPWORDS = {'estuviésemos', 'estuviesen', 'tengo', 'estábamos', 'tuya', 'algunos', 'el', 'nuestras', 'hayas', 'ese', 'tuviéramos', 'estuvierais', 'hubiéramos', 'nuestra', 'ya', 'os', 'has', 'fuesen', 'tuvieseis', 'sea', 'sí', 'hubieron', 'era', 'fueron', 'tus', 'estamos', 'estando', 'desde', 'somos', 'poco', 'tiene', 'seré', 'tuyas', 'cual', 'estaremos', 'yo', 'esos', 'todo', 'habríamos', 'tanto', 'tuvisteis', 'hubiera', 'estas', 'sobre', 'habiendo', 'nada', 'teníais', 'hubiesen', 'estaríais', 'otro', 'te', 'tu', 'tuvo', 'fueseis', 'estuvieron', 'tendrá', 'ella', 'tendríamos', 'sin', 'tendrías', 'esas', 'hubieran', 'esté', 'sintiendo', 'este', 'estaba', 'tuvimos', 'tendría', 'siente', 'tengan', 'hayamos', 'nuestro', 'mis', 'teníamos', 'tendrán', 'eres', 'se', 'mía', 'fueras', 'fueses', 'seremos', 'esa', 'ante', 'seríamos', 'también', 'y', 'qué', 'hubimos', 'muy', 'estáis', 'no', 'tuvieses', 'sois', 'estuve', 'mío', 'serías', 'soy', 'serían', 'suyo', 'habían', 'estaré', 'habré', 'éramos', 'a', 'muchos', 'seamos', 'pero', 'fuimos', 'vuestros', 'las', 'otras', 'tuve', 'estará', 'estuvimos', 'del', 'tendrían', 'por', 'más', 'porque', 'como', 'que', 'habido', 'tenido', 'seas', 'tuvierais', 'con', 'estaréis', 'hay', 'donde', 'hayan', 'para', 'sería', 'estadas', 'hubieras', 'tuviera', 'hube', 'tuviésemos', 'hubisteis', 'le', 'serán', 'cuando', 'ellos', 'otra', 'tuyos', 'haya', 'ha', 'he', 'será', 'tuvieran', 'ti', 'quien', 'nos', 'habías', 'estarías', 'ni', 'fueran', 'hubieseis', 'uno', 'estaríamos', 'otros', 'estad', 'durante', 'estoy', 'seríais', 'estuviste', 'tuvieras', 'me', 'fuese', 'tengas', 'estén', 'antes', 'todos', 'habida', 'habríais', 'lo', 'estuvieseis', 'estada', 'tendréis', 'estuvieran', 'estuviera', 'les', 'algo', 'estés', 'estarían', 'habidos', 'estéis', 'sentidos', 'tú', 'tenía', 'suya', 'esto', 'tendré', 'los', 'habréis', 'han', 'estarán', 'estemos', 'hubierais', 'estás', 'estuviese', 'están', 'en', 'de', 'habría', 'fuerais', 'la', 'estarás', 'suyas', 'e', 'o', 'tienes', 'una', 'su', 'erais', 'tenida', 'nuestros', 'al', 'fuésemos', 'estuviéramos', 'sentidas', 'tenías', 'habremos', 'vuestras', 'tendríais', 'habíamos', 'suyos', 'vuestra', 'entre', 'fuéramos', 'habíais', 'tendrás', 'mi', 'quienes', 'vosotros', 'estuvo', 'vosotras', 'habrá', 'hubieses', 'tuvieron', 'un', 'estos', 'algunas', 'tenidos', 'vuestro', 'fui', 'es', 'sus', 'eso', 'había', 'habrían', 'mías', 'fuisteis', 'eras', 'tendremos', 'habidas', 'tenéis', 'estados', 'hubo', 'sentida', 'estabas', 'fue', 'sentid', 'fuera', 'tenían', 'serás', 'eran', 'fuiste', 'tenga', 'habrías', 'nosotros', 'habéis', 'está', 'hubiste', 'habrán', 'ellas', 'son', 'tuviste', 'sean', 'contra', 'mucho', 'teniendo', 'estuvieras', 'tengáis', 'tenidas', 'estuvieses', 'hubiese', 'hayáis', 'él', 'esta', 'nosotras', 'tienen', 'hasta', 'tengamos', 'estuvisteis', 'estabais', 'tenemos', 'hemos', 'estaría', 'tuviesen', 'tuyo', 'sentido', 'míos', 'unos', 'estar', 'tened', 'seréis', 'hubiésemos', 'estaban', 'habrás', 'mí', 'estado', 'tuviese', 'seáis'}

@st_cache
def generate_wordcloud(text, max_words):
    # Remove multimedia messages
    text = text.replace("<Multimedia omitido>", "")  # TODO: Make it language-independent
    
    stopwords=set(STOPWORDS)
    stopwords = set.union(stopwords, SPANISH_STOPWORDS)

    # Create and generate a word cloud image:
    wordcloud = WordCloud(
        max_words=max_words,
        stopwords=stopwords,
        background_color="white",
    ).generate(text)
    return wordcloud

def plot_wordcloud(text, max_words):
    wordcloud = generate_wordcloud(text, max_words)
    return wordcloud.to_image()