import streamlit as st
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time

st.set_page_config(page_title="Buscador de Grupos Premium", page_icon="🎯", layout="centered")
st.title("🎯 Extrator de Grupos Segmentados")
st.markdown("Busca inteligente focada em nichos específicos (ex: Religião, Negócios, etc).")

nicho = st.text_input("Qual o nicho exato?", placeholder="Ex: Grupo de Jovens da Igreja")
num_links = st.slider("Profundidade da busca (links)", 10, 50, 20)
botao = st.button("GERAR LISTA SEGMENTADA")

def validar_link(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code == 200 and "chat.whatsapp.com" in url:
            soup = BeautifulSoup(response.text, 'html.parser')
            nome_elemento = soup.find('h3')
            if nome_elemento and "WhatsApp Group Invite" not in nome_elemento.text:
                return nome_elemento.text.strip()
        return None
    except:
        return None

if botao and nicho:
    with st.spinner(f'Filtrando resultados para: {nicho}...'):
        # BUSCA INTELIGENTE: Inclui o nicho e exclui termos comerciais ou irrelevantes
        # Exemplo: busca por igreja mas ignora OLX, Mercado Livre e notícias genéricas
        query = f'site:facebook.com "chat.whatsapp.com" "{nicho}" -venda -comprar -notícia -olx -loja'
        
        resultados_finais = []
        try:
            for url in search(query, num_results=num_links):
                if "chat.whatsapp.com" in url:
                    nome = validar_link(url)
                    # Validação extra: O nome do grupo deve conter palavras do nicho para ser exibido
                    if nome and any(word.lower() in nome.lower() for word in nicho.split()):
                        resultados_finais.append({"Grupo": nome, "Link": url})
                    time.sleep(1.8)
            
            if resultados_finais:
                st.success(f"Encontrei {len(resultados_finais)} grupos altamente segmentados!")
                for item in resultados_finais:
                    with st.container():
                        st.markdown(f"### ⛪ {item['Grupo']}")
                        st.link_button("ENTRAR AGORA", item['Link'])
                        st.divider()
            else:
                st.warning("Nenhum grupo específico encontrado. Tente um termo mais direto.")
        except Exception:
            st.error("O Google detectou muitas requisições. Tente novamente em alguns minutos.")
