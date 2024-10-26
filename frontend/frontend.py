from make_back_request import make_request
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Live Chess Player Ratings",
    page_icon="♟️",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #2e7d32;
        font-size: 2.8em;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subheader {
        text-align: center;
        color: #2e7d32;
        font-size: 1.5em;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #e0f7fa; /* Change to a light teal color */
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem;
        position: relative; /* For animated outline */
        overflow: hidden; /* To contain the outline */
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border: 2px solid #2e7d32; /* Dark green outline */
        border-radius: 0.5rem;
        opacity: 0;
        transition: opacity 0.5s ease;
        z-index: 0; /* Behind the content */
    }
    .metric-card:hover::before {
        opacity: 1; /* Show outline on hover */
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #2e7d32;
    }
    .metric-label {
        font-size: 1.2em;
        color: #424242;
        margin-bottom: 0.5rem;
    }
    .stDataFrame {
        margin: 2rem auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<h1 class='title' style='color: #2e7d32;'>Live Chess Player Ratings</h1>", unsafe_allow_html=True)
st.markdown(
    '<h2 class="subheader" style="color: #2e7d32;">♟️ Acompanhe em tempo real os ratings dos melhores enxadristas do mundo! ♟️</h2>',
    unsafe_allow_html=True
)

# Sidebar configuration
with st.sidebar:
    st.title("Configurações")
    
    # Time control selection
    st.subheader("Controle de Tempo")
    rating_types = {
        "FIDE Ratings": "fide",
        "Chess.com Blitz": "blitz",
        "Chess.com Bullet": "bullet"
    }
    selected_rating = st.selectbox(
        "Escolha o controle de tempo:",
        rating_types.keys()
    )
    
    # Additional filters
    st.subheader("Filtros")
    min_rating = st.slider(
        "Rating Mínimo:",
        min_value=2000,
        max_value=3000,
        value=2500,
        step=50
    )
    
    # Update frequency

def process_ratings_data(data, rating_type, min_rating):
    """Process and filter the ratings data."""
    if not data:
        st.error("Não foi possível obter os dados. Tente novamente mais tarde.")
        return None
    
    df = pd.DataFrame(data[rating_types[selected_rating]])
    
    # Convert rating column to numeric, handling any non-numeric values
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    
    # Filter out any NaN values that resulted from the conversion
    df = df.dropna(subset=['Rating'])
    
    # Now filter by minimum rating
    df = df[df['Rating'] >= min_rating].reset_index(drop=True)
    
    # Reorder columns to make 'Rank', 'Nome', 'Nacionalidade', 'Rating' the first columns
    cols = ['Rank', 'Nome', 'Nacionalidade', 'Rating'] + [col for col in df.columns if col not in ['Rank', 'Nome', 'Nacionalidade', 'Rating']]
    df = df[cols]
    
    return df

def display_metrics(df):
    """Display key metrics about the ratings data."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_rating = int(df['Rating'].mean())
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Rating Médio</div>
                <div class="metric-value">{avg_rating}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        max_rating = int(df['Rating'].max())
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Rating Máximo</div>
                <div class="metric-value">{max_rating}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        total_players = len(df)
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total de Jogadores</div>
                <div class="metric-value">{total_players}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def create_rating_chart(df):
    """Create a bar chart of player ratings."""
    fig = px.bar(
        df,
        x='Nome',
        y='Rating',
        labels={'Nome': 'Jogador', 'Rating': 'Rating'},
        color='Rating',
        color_continuous_scale='viridis'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=500
    )
    return fig

def main():
    # Get data
    data = make_request()
    df = process_ratings_data(data, rating_types[selected_rating], min_rating)
    
    if df is not None and not df.empty:
        # Display metrics
        st.subheader("Ratings Atualizados")
        st.markdown("<h3 style='text-align: center; color: #2e7d32;'>Informações Gerais</h3>", unsafe_allow_html=True)
        st.text("")
        display_metrics(df)
        st.markdown("<h3 style='text-align: center; color: #2e7d32;'>Tabela de Ratings</h3>", unsafe_allow_html=True)
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )
        st.markdown(
            f"<h3 style='text-align: center; color: #2e7d32;'>Gráfico de Ratings por Jogador</h3>",
            unsafe_allow_html=True
        )
        st.plotly_chart(create_rating_chart(df), use_container_width=True)
        # Last update information
        
        st.markdown(
            f"<div style='text-align: center; color: #666;'>"
            f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

if __name__ == "__main__":
    main()
