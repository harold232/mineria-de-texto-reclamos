from wordcloud import WordCloud

def generar_nube_palabras(df, columna):
    """Genera una nube de palabras a partir de una columna de texto"""
    text = " ".join(df[columna].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
