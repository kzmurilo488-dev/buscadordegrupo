import streamlit as st
from googlesearch import search
import time
import random
import re

# Configuração da Página
st.set_page_config(page_title="Minerador Pro - WhatsApp", page_icon="🚀")

st.title("🚀 Minerador de Grupos Profissional")
st.write("Busca automática com filtros de redes sociais e exportação.")

# Interface de usuário
fonte = st.selectbox("Escolha a rede social para minerar:", ("Facebook", "Instagram", "YouTube"))
nicho = st.text_input("Qual o tema dos grupos? (Ex: Igreja, Marketing, Vendas)", "")

if st.button("Iniciar Mineração"):
    if nicho:
        # Montagem automática da Query "Dork"
        query = f'site:{fonte.lower()}.com "chat.whatsapp.com" "{nicho}"'
        
        # Regex para extrair apenas o link limpo do WhatsApp
        regex_whatsapp = r"chat\.whatsapp\.com/[A-Za-z0-9]+"
        links_unicos = set()

        with st.spinner(f'Garimpando links no {fonte}... Por favor, aguarde.'):
            try:
                # Busca configurada para evitar bloqueios (pausa de 2s entre resultados)
                # Removemos o 'user_agent' que causava erro e usamos o padrão estável
                resultados = search(query, num_results=20, lang="pt", sleep_interval=2)
                
                for url in resultados:
                    # Tenta encontrar o padrão do link do zap dentro da URL do Google
                    match = re.search(regex_whatsapp, url)
                    if match:
                        link_final = "https://" + match.group(0)
                        links_unicos.add(link_final)
                    
                    # Pausa extra aleatória para parecer um humano
                    time.sleep(random.uniform(1, 3))
                
                if links_unicos:
                    st.success(f"🎯 Sucesso! Encontrei {len(links_unicos)} grupos únicos.")
                    
                    # Botão para baixar a lista pronta para o seu computador
                    lista_txt = "\n".join(links_unicos)
                    st.download_button(
                        label="📥 Baixar Lista para CRM (.txt)",
                        data=lista_txt,
                        file_name=f"leads_{nicho}_{fonte}.txt",
                        mime="text/plain"
                    )
                    
                    st.markdown("### Links Extraídos:")
                    for l in links_unicos:
                        st.code(l, language="text")
                else:
                    st.warning("Nenhum link direto encontrado nesta busca. Tente mudar o tema ou a rede social.")
                    
            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ O Google bloqueou o acesso temporariamente. Aguarde 15 minutos ou use outra rede (Wi-Fi/4G).")
                else:
                    st.error(f"Ocorreu um ajuste necessário: {e}")
    else:
        st.error("Por favor, digite um tema antes de começar.")

st.divider()
st.caption("Dica: Não faça mais de 5 buscas por hora para manter o seu IP seguro.")
