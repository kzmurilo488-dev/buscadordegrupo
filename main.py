import streamlit as st
from googlesearch import search
import time
import random
import re

# Configuração visual da página
st.set_page_config(page_title="Minerador de Grupos Pro", page_icon="🚀", layout="centered")

st.title("🚀 Extrator Inteligente de Grupos")
st.write("Filtros avançados, limpeza de links e exportação para CRM.")

# 1. Filtro de Redes Sociais
fonte = st.selectbox(
    "Onde você quer procurar os grupos?",
    ("Facebook", "Instagram", "YouTube", "Twitter")
)

nicho = st.text_input("Qual o tema do grupo? (Ex: Igreja, Vendas, Florianópolis)", "")

# 2. Camuflagem: Lista de aparelhos para enganar o Google
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
]

if st.button("Iniciar Mineração"):
    if nicho:
        # Configurando o filtro do site selecionado
        site_query = f"site:{fonte.lower()}.com"
        query = f'{site_query} "chat.whatsapp.com" "{nicho}"'
        
        # 3. Expressão Regular (Regex) para recortar SÓ o link do WhatsApp
        regex_whatsapp = r"chat\.whatsapp\.com/[A-Za-z0-9]+"

        # Usamos 'set' em vez de lista para ignorar links duplicados
        links_limpos = set() 

        with st.spinner(f'Buscando em {fonte}... Camuflando identidade... Isso pode levar 1 minuto.'):
            try:
                # Escolhe um aparelho aleatório para a busca
                ua_escolhido = random.choice(user_agents)
                
                # Executa a busca
                resultados = search(query, num_results=20, lang="pt", user_agent=ua_escolhido)
                
                for url in resultados:
                    # Aplica o bisturi (Regex) no resultado do Google
                    match = re.search(regex_whatsapp, url)
                    if match:
                        links_limpos.add("https://" + match.group(0))
                    
                    # Pausa humana (essencial para evitar o bloqueio de IP)
                    time.sleep(random.uniform(2.5, 5.5))
                
                if links_limpos:
                    st.success(f"🎯 Captura concluída! {len(links_limpos)} grupos únicos encontrados.")
                    
                    # 4. Prepara o arquivo .txt para exportação
                    texto_exportacao = "\n".join(links_limpos)
                    
                    st.download_button(
                        label="📥 Baixar Lista Limpa (.txt)",
                        data=texto_exportacao,
                        file_name=f"grupos_{fonte.lower()}_{nicho.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                    
                    st.markdown("### Links Encontrados:")
                    for link in links_limpos:
                        # Exibe em formato de código para facilitar a cópia
                        st.code(link, language="text")
                else:
                    st.warning("Nenhum link foi encontrado. Tente trocar a rede social ou o termo.")
                    
            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ O Google percebeu a automação. Aguarde 15 minutos ou troque de rede Wi-Fi/4G.")
                else:
                    st.error(f"Erro inesperado: {e}")
    else:
        st.error("Digite o nicho para começar.")
