import plotly.graph_objects as go

def criar_grafico_barras_verticais(valores_corrente, valores_anterior, titulo):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=['Mês Corrente', 'Mês Anterior'],
        y=[valores_corrente, valores_anterior],
        marker=dict(color=['#212b2c', '#536c6f']),
        text=[valores_corrente, valores_anterior],
        textposition='auto'
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title='Mês',
        yaxis_title='Valores',
        plot_bgcolor='lightgrey',
        paper_bgcolor='lightgrey',
        font=dict(color='black'),
        title_font=dict(color='black'),
        xaxis=dict(
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        legend=dict(font=dict(color='black')),
        autosize=True,
        margin=dict(l=100, r=20, t=50, b=50)
    )

    return fig

# def criar_grafico_barra_horizontal(data, title):
#     fig = go.Figure(go.Bar(
#         x=data.values,
#         y=data.index,
#         orientation='h',
#         marker=dict(
#             color='#212b2c',
#             line=dict(color='black', width=0.9)
#         )
#     ))

#     fig.update_layout(
#         title=title,
#         xaxis_title='Média',
#         yaxis_title='Dia da Semana',
#         plot_bgcolor='lightgrey',
#         paper_bgcolor='lightgrey',
#         font=dict(color='black'),
#         title_font=dict(color='black'),
#         xaxis=dict(
#             title_font=dict(color='black'),
#             tickfont=dict(color='black')
#         ),
#         yaxis=dict(
#             title_font=dict(color='black'),
#             tickfont=dict(color='black')
#         ),
#         legend=dict(font=dict(color='black')),
#         margin=dict(l=100, r=20, t=50, b=50)
#     )

#     return fig


def criar_grafico_barra_horizontal(data, title):
    # Mapeamento dos valores de 0 a 6 para os nomes dos dias da semana
    dias_semana = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}
    
    # Substituindo os valores pelos nomes dos dias
    data.index = data.index.map(dias_semana)

    fig = go.Figure(go.Bar(
        x=data.values,
        y=data.index,
        orientation='h',
        marker=dict(
            color='#212b2c',
            line=dict(color='black', width=0.9)
        )
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Média',
        yaxis_title='Dia da Semana',
        plot_bgcolor='lightgrey',
        paper_bgcolor='lightgrey',
        font=dict(color='black'),
        title_font=dict(color='black'),
        xaxis=dict(
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        legend=dict(font=dict(color='black')),
        margin=dict(l=100, r=20, t=50, b=50)
    )

    return fig


def calcular_calorias_mensais(df):
    return df.groupby(df['data'].dt.to_period('M'))['calorias'].sum()

def calcular_km_mensais(df):
    return df.groupby(df['data'].dt.to_period('M'))['quilometragem'].sum()


def criar_grafico(df, media_calorias_com_zeros, media_calorias_sem_zeros):
    fig = go.Figure()

    # Definir as cores dos pontos com base nas condições fornecidas
    cores_pontos = ['green' if calorias > media_calorias_sem_zeros else '#212b2c' if calorias > 0 else 'red' for calorias in df['calorias']]

    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df['calorias'],
        mode='lines+markers',
        line=dict(color='black'),
        marker=dict(
            color=cores_pontos,
            size=10
        ),
        text=df.apply(lambda row: f"Calorias: {row['calorias']}<br>Quilometragem: {row['quilometragem']}", axis=1),
        hoverinfo='text',
        name='Calorias'
    ))

    fig.add_trace(go.Scatter(
        x=[df['data'].min(), df['data'].max()],
        y=[media_calorias_sem_zeros, media_calorias_sem_zeros],
        mode='lines',
        line=dict(color='green', dash='dash'),
        name=f'Média de Calorias (sem zeros: {media_calorias_sem_zeros:.2f})'
    ))

    fig.add_trace(go.Scatter(
        x=[df['data'].min(), df['data'].max()],
        y=[media_calorias_com_zeros, media_calorias_com_zeros],
        mode='lines',
        line=dict(color='blue', dash='dash'),
        name=f'Média de Calorias (com zeros: {media_calorias_com_zeros:.2f})'
    ))

    fig.update_xaxes(
        tickmode='array',
        tickvals=df['data'],
        ticktext=df['data'].dt.strftime('%d-%b-%a'),
        tickangle=-90,
        tickfont=dict(size=10, color='black')
    )

    fig.update_layout(
        title='Evolução Diária de Calorias',
        xaxis_title='Data',
        yaxis_title='Calorias',
        plot_bgcolor='lightgrey',
        paper_bgcolor='lightgrey',
        font=dict(color='black'),
        title_font=dict(color='black'),
        xaxis=dict(
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        legend=dict(font=dict(color='black')),
        autosize=True,
        margin=dict(l=100, r=20, t=50, b=150)
    )

    return fig
