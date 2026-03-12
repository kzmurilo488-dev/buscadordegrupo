
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import time

st.set_page_config(page_title="Minerador Pro + Filtro Ativo", page_icon="✅")

st.title("✅ Minerador de Grupos Ativos")
st.write("Buscando apenas links verificados em diretórios públicos.")

nicho = st.text_input("Qual nicho buscar? (Ex: Igreja, Marketing, Vendas)", "")

def verificar_link_ativo(url):
    """Verifica se o link do WhatsApp ainda é válido e não expirou."""
    try:
        # Faz uma pequena requisição ao convite para ver se a página existe
        response = requests.get(url, timeout=5)
        if "WhatsApp Group Invite" in response.text and "Invite Link" not in response.text:
            return True
        # Se na página aparecer 'Link de convite revogado' ou similar, ele descarta
        if "Lookup a WhatsApp" in response.text or "revoked" in response.text:
            return False
        return True
    except:
        return False

if st.button("Explorar e Validar Grupos"):
    if nicho:
        links_sujos = []
        # Alvo: Diretório que permite buscas rápidas
        url_busca = f"https://www.gruposwhats.app/br/search?q={nicho}"
        
        headers = {"User-Agent": "Mozilla/5.0"}

        with st.spinner(f'Garimpando e testando links de "{nicho}"...'):
            try:
                res = requests.get(url_busca, headers=headers, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Captura todos os links que apontam para convites
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if "chat.whatsapp.com" in href:
                        links_sujos.append(href)

                links_sujos = list(set(links_sujos)) # Remove duplicatas iniciais
                
                links_validados = []
                progresso = st.progress(0)
                status_text = st.empty()

                # Fase de Validação (O Filtro de Ativos)
                for i, link in enumerate(links_sujos):
                    status_text.text(f"Verificando link {i+1} de {len(links_sujos)}...")
                    if verificar_link_ativo(link):
                        links_validados.append(link)
                    progresso.progress((i + 1) / len(links_sujos))
                    time.sleep(0.5) # Pausa curta para não sobrecarregar

                status_text.empty()

                if links_validados:
                    st.success(f"🎯 Encontrei {len(links_validados)} grupos ATIVOS e verificados!")
                    
                    csv = "\n".join(links_validados)
                    st.download_button("📥 Baixar Lista de Ativos", csv, f"ativos_{nicho}.txt")
                    
                    for l in links_validados:
                        st.code(l)
                else:
                    st.warning("Nenhum grupo ativo encontrado para este termo no momento.")
                    
            except Exception as e:
                st.error(f"Erro na mineração: {e}")
    else:
        st.error("Digite um nicho.")

st.divider()
st.caption("Esta ferramenta filtra links expirados automaticamente para economizar seu tempo.")
