from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px


data = pd.read_csv('top_movies_by_gender.csv')
data.head()

data2 = data.values.tolist()
lista_gen = []
for row in data2:
    if row[0] not in lista_gen:
        lista_gen.append(row[0])

conta_gen = len(lista_gen) * [0]
for movie in data2:
    ix = 0
    while ix < len(lista_gen):
        if (lista_gen[ix] == movie[0]):
            break
        ix += 1
    conta_gen[ix] += 1

indice = 0
lista_gen_qtd = []
while indice < len(lista_gen):
    fil_bil = [lista_gen[indice], conta_gen[indice]]
    lista_gen_qtd.append(fil_bil)
    indice += 1

df = pd.DataFrame(lista_gen_qtd, columns=['Gêneros', 'Quantidade'])

grafico = px.bar(df, x='Gêneros', y='Quantidade', color="Gêneros",
                 title='GÊNEROS MAIS BEM AVALIADOS NO MUNDO(>95%)',
                 color_discrete_sequence=px.colors.qualitative.Bold,
                 template='plotly_dark')

app = Dash(__name__)

app.layout = html.Main([
    html.Div(className="vertical-container", children=[
        html.H1("Dash - Gêneros mais bem avaliados do mundo"),
    ]),
    html.Div(children=[
        html.Div(className='horizontal-container', children=[
            html.Label('Selecione o intervalo de quantidade:'),
            dcc.RangeSlider(min=0, max=100, step=10, value=[0, 100],
                            id='slider-quantidade', className='slider'),
        ]),
        dcc.Graph(
            id='generos-avaliados'
        )
    ])
])


@app.callback(
    Output('generos-avaliados', 'figure'),
    Input('slider-quantidade', 'value')
)
def update_graph(range_value):
    valores_filtrados = []
    menor_valor, maior_valor = range_value

    for gen in conta_gen:
        if gen > menor_valor and gen < maior_valor:
            valores_filtrados.append(gen)

    generos_filtrados = []
    for gen_qtd in lista_gen_qtd:
        if gen_qtd[1] > menor_valor and gen_qtd[1] < maior_valor:
            generos_filtrados.append(gen_qtd[0])

    indice = 0
    lista_gen2_qtd2 = []
    while indice < len(generos_filtrados):
        gen_60 = [generos_filtrados[indice], valores_filtrados[indice]]
        lista_gen2_qtd2.append(gen_60)
        indice += 1

    df2 = pd.DataFrame(lista_gen2_qtd2, columns=[
                       'Gêneros', 'Frequência'])

    grafico = px.bar(df2, x='Gêneros', y='Frequência', color="Gêneros",
                     title=f'GÊNEROS ENTRE {menor_valor} E {maior_valor} FILMES APROVADOS',
                     color_discrete_sequence=px.colors.qualitative.Set1,
                     template='plotly_dark')
    return grafico


if __name__ == '__main__':
    app.run_server(debug=True)
