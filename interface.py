import streamlit as st
from analise_acao import AnalisadorAcoes
from banco_dados import salvar_dados_banco
from previsao import prever_precos
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Analisador de Ações", layout="wide")

# Lista de ações disponíveis
lista_acoes = [
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA",
    "WEGE3.SA", "ABEV3.SA", "MGLU3.SA", "RENT3.SA", "GGBR4.SA",
    "AAPL", "GOOG", "MSFT", "TSLA", "AMZN"
]

# Título do app
st.title("📈 Analisador de Múltiplas Ações")

# Seleção das ações
simbolos_selecionados = st.multiselect("Selecione as ações para analisar:", lista_acoes, default=["PETR4.SA", "AAPL"])

# Botão para iniciar a análise
if st.button("Analisar"):
    st.subheader("🔍 Analisando ações...")

    # Criar DataFrame para armazenar os resultados
    resultados = []

    # Loop sobre cada ação selecionada
    for simbolo in simbolos_selecionados:
        st.write(f"📊 **Analisando {simbolo}...**")

        try:
            # Criando objeto da classe AnalisadorAcoes
            analise = AnalisadorAcoes(simbolo)

            # Obtendo os dados da ação
            dados = analise.obter_dados_acao()

            if not dados.empty:
                # Gerar recomendação
                recomendacao = analise.executar_analise()
                salvar_dados_banco(simbolo, recomendacao)

                # Previsão de preços
                df_previsoes = prever_precos(simbolo)
                preco_previsto = df_previsoes['Previsao'].iloc[-1] if df_previsoes is not None and not df_previsoes.empty else None

                # Adicionar os dados na lista de resultados
                resultados.append({
                    "Símbolo": simbolo,
                    "Último Preço": f"R$ {dados['Close'].iloc[-1]:.2f}",
                    "Recomendação": recomendacao,
                    "Preço Previsto": f"R$ {preco_previsto:.2f}" if preco_previsto else "N/A"
                })

            else:
                st.warning(f"⚠️ Dados não encontrados para {simbolo}")

        except Exception as e:
            st.error(f"❌ Erro ao processar {simbolo}: {e}")

    # Criar DataFrame com os resultados
    if resultados:
        df_resultados = pd.DataFrame(resultados)
        st.write("📌 **Resultados da análise:**")
        st.dataframe(df_resultados)
