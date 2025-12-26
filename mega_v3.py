import streamlit as st
import random
from datetime import datetime
from collections import Counter
import pandas as pd

# --- 1. CONFIGURAÇÃO E ESTILO (O visual das bolinhas e cards) ---
st.set_page_config(page_title="Mega Blindada V3", page_icon="🍀", layout="wide")

st.markdown("""
    <style>
    .bolinha {
        display: inline-block;
        width: 42px;
        height: 42px;
        line-height: 42px;
        border-radius: 50%;
        background-color: #209869;
        color: white;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        margin: 4px;
        border: 2px solid #145d41;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    .card-jogo {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 6px solid #d4a017;
        color: #128F55 ;
    }
    .status-excelente { color: #d4a017; font-weight: bold; }
    .status-bom { color: #209869; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HISTÓRICO RECENTE ---
historico_sorteios = [
    {"concurso": 2807, "data": "13/12/2025", "dezenas": [5, 18, 27, 40, 48, 59]},
    {"concurso": 2806, "data": "11/12/2025", "dezenas": [2, 11, 28, 37, 43, 55]}
]
ultimos_5_sorteios = [s["dezenas"] for s in historico_sorteios]

# --- 3. MOTOR DE FILTRAGEM (Lógica do Colab) ---
def possui_aglomeracao(jogo, limite=3):
    linhas = [(n - 1) // 10 for n in jogo]
    colunas = [(n - 1) % 10 for n in jogo]
    return any(q > limite for q in Counter(linhas).values()) or \
           any(q > limite for q in Counter(colunas).values())

def possui_muitos_finais_iguais(jogo, limite=2):
    return any(q > limite for q in Counter([n % 10 for n in jogo]).values())

def possui_sequencia_longa(jogo, limite=2):
    c = 1
    for i in range(len(jogo) - 1):
        if jogo[i+1] == jogo[i] + 1:
            c += 1
            if c > limite: return True
        else: c = 1
    return False

def gerar_jogo_blindado():
    viciados = set([n for s in ultimos_5_sorteios for n in s])
    todos = list(range(1, 61))
    pares = [n for n in todos if n % 2 == 0]; impares = [n for n in todos if n % 2 != 0]
    while True:
        jogo = sorted(random.sample(pares, 3) + random.sample(impares, 3))
        soma = sum(jogo)
        if not (150 <= soma <= 220): continue
        if possui_sequencia_longa(jogo): continue
        if possui_muitos_finais_iguais(jogo): continue
        if possui_aglomeracao(jogo): continue
        if len([n for n in jogo if n not in viciados]) < 3: continue
        status = "⭐ EXCELENTE" if 170 <= soma <= 195 else "✅ BOM"
        dist = f"{len([n for n in jogo if n <= 30])}L / {len([n for n in jogo if n > 30])}H"
        return jogo, soma, dist, status

# --- 4. INTERFACE ---
st.title("💰 Mega Sena Blindada V3")

col_gen, col_hist = st.columns([1.1, 0.9])

with col_gen:
    st.subheader("Gerar Palpites")
    qtd = st.slider("Quantidade de jogos:", 1, 15, 6)
    
    if st.button("🍀 Gerar Jogos Inteligentes"):
        st.balloons() # Balões da sorte!
        for i in range(qtd):
            jogo, soma, dist, status = gerar_jogo_blindado()
            bolinhas_html = "".join([f'<div class="bolinha">{n:02d}</div>' for n in jogo])
            cor_status = "status-excelente" if "EXCELENTE" in status else "status-bom"
            
            st.markdown(f"""
                <div class="card-jogo">
                    <strong>Jogo {i+1} - <span class="{cor_status}">{status}</span></strong><br>
                    {bolinhas_html}<br>
                    <small>Soma: {soma} | Distr: {dist}</small>
                </div>
            """, unsafe_allow_html=True)
        
        st.success(f"💰 Investimento Total: R$ {qtd * 6:.2f}")

with col_hist:
    st.subheader("📊 Histórico Recente")
    st.table(pd.DataFrame(historico_sorteios))
    st.info("Filtros Ativos: Soma (150-220), Equilíbrio P/I, Sem sequências longas e Memória de sorteios.")
