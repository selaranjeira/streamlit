import plotly.graph_objects as go
import streamlit as st

def criar_grafico(df, media_calorias_com_zeros, media_calorias_sem_zeros):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df['calorias'],
        mode='lines+markers',
        line=dict(color='black'),
        marker=dict(
            color=['green' if calorias > media_calorias_sem_zeros else 'red' for calorias in df['calorias']],
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
        title='Calorias por Dia com Médias',
        xaxis_title='Data',
        yaxis_title='Calorias',
        plot_bgcolor='darkgrey',
        paper_bgcolor='darkgrey',
        font=dict(color='black'),
        autosize=True,
        margin=dict(l=100, r=20, t=50, b=150)
    )

    return fig


def criar_grafico_barra_horizontal(data, title):
    fig = go.Figure(go.Bar(
        x=data.values,
        y=data.index,
        orientation='h',
        marker=dict(
            color='green',  # Cor das barras
            line=dict(color='black', width=0.9)  # Cor e largura da borda das barras
        )
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Média',
        yaxis_title='Dia da Semana',
        plot_bgcolor='darkgray',
        paper_bgcolor='darkgray',
        font=dict(color='black'),
        xaxis=dict(
            title=dict(font=dict(size=14)),  # Tamanho da fonte do título do eixo x
            tickfont=dict(size=10)  # Tamanho da fonte dos rótulos do eixo x
        ),
        yaxis=dict(
            title=dict(font=dict(size=14)),  # Tamanho da fonte do título do eixo y
            tickfont=dict(size=12)  # Tamanho da fonte dos rótulos do eixo y
        ),
        margin=dict(l=100, r=20, t=50, b=50)  # Ajustar as margens
    )

    return fig
