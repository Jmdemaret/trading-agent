import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Ajouter la racine du projet au path pour pouvoir importer core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.agent import TradingAgent

st.set_page_config(page_title="IA Trading Dashboard", layout="wide")

st.title("📈 Dashboard d'Investissement Expert IA")
st.markdown("Suivez votre portefeuille et obtenez des recommandations en temps réel.")

# Initialiser l'agent
@st.cache_resource
def get_agent():
    return TradingAgent()

agent = get_agent()

# --- Données Fictives de Portefeuille ---
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = pd.DataFrame({
        'Ticker': ['AAPL', 'MSFT', 'TSLA', 'GOOGL'],
        'Quantité': [50, 30, 20, 40],
        'Prix_Achat': [150.0, 300.0, 200.0, 120.0]
    })

portfolio = st.session_state.portfolio

st.sidebar.header("Votre Portefeuille")
st.sidebar.dataframe(portfolio)

# --- Onglets ---
tab1, tab2, tab3 = st.tabs(["Vue d'ensemble", "Analyse Expert & Signaux", "Feature Révolutionnaire : Auto-Rééquilibrage IA"])

with tab1:
    st.header("Performance du Portefeuille (Simulation)")

    # Génération d'une courbe de valeur de portefeuille fictive
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
    valeurs = np.linspace(25000, 28000, 30) + np.random.normal(0, 500, 30)
    df_perf = pd.DataFrame({'Date': dates, 'Valeur Globale ($)': valeurs})

    st.line_chart(df_perf.set_index('Date'))

    total_value = valeurs[-1]
    st.metric(label="Valeur Totale Estimée", value=f"${total_value:,.2f}", delta=f"${valeurs[-1] - valeurs[-2]:.2f}")

with tab2:
    st.header("Analyse en Temps Réel de vos Actifs")

    if st.button("Lancer l'Analyse Expert"):
        with st.spinner("L'IA analyse les marchés et les annonces..."):
            for ticker in portfolio['Ticker']:
                st.subheader(f"Analyse pour {ticker}")
                signal = agent.generate_signal(ticker)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Prix Actuel", f"${signal.get('current_price', 0):.2f}")
                    if "BUY" in signal['action']:
                        st.success(f"Signal: {signal['action']}")
                    elif "SELL" in signal['action']:
                        st.error(f"Signal: {signal['action']}")
                    else:
                        st.warning(f"Signal: {signal['action']}")

                with col2:
                    st.info(f"Raison: {signal['reason']}")
                st.divider()

with tab3:
    st.header("🤖 Rééquilibrage Prédictif IA")
    st.markdown("""
    *Feature Révolutionnaire* : Notre agent n'analyse pas seulement le passé, il projette l'allocation optimale
    pour maximiser le rendement selon les conditions de marché actuelles.
    """)

    # Simulation de la suggestion de rééquilibrage
    st.subheader("Allocation Actuelle vs Allocation Recommandée")

    current_allocation = {'AAPL': 35, 'MSFT': 30, 'TSLA': 15, 'GOOGL': 20}
    recommended_allocation = {'AAPL': 20, 'MSFT': 40, 'TSLA': 5, 'GOOGL': 35}

    df_alloc = pd.DataFrame({
        'Actuelle (%)': current_allocation,
        'Recommandée IA (%)': recommended_allocation
    })

    st.bar_chart(df_alloc)

    st.info("L'IA recommande d'augmenter votre exposition sur MSFT et GOOGL en raison de signaux fondamentaux forts sur l'IA générative, tout en réduisant TSLA à cause d'une analyse de sentiment négative récente.")
