import streamlit as st
from googlesearch import search
import time
import random
import re

st.set_page_config(page_title="Minerador Pro - AntiBloqueio", page_icon="🛡️")

st.title("🛡️ Minerador Anti-Bloqueio")
st.write("Busca inteligente com pausas humanas para evitar o erro 429.")

fonte = st.selectbox("Onde minerar:", ("Facebook", "Instagram", "YouTube"))
nicho = st.text_input("Tema do grupo:", "")

if st.button("🚀 Iniciar Mineração Segura"):
    if nicho:
        # A query agora usa aspas duplas de forma mais eficiente
        query = f'site:{fonte.lower()}.com "chat.whatsapp.com" "{nicho}"'
        links_unicos = set()
        
        container = st.empty() # Espaço para mensagens de status
        
        try:
            # Aumentamos o intervalo de sono (sleep_interval) para 5 segundos
            # Isso é o que mais protege o seu IP
            with st.spinner('Simulando comportamento humano... Aguarde.'):
                busca = search(query, num_results=12, lang="pt", sleep_interval=5)
                
                for url in busca:
                    # Regex para pegar apenas o link puro
                    match = re.search(r"chat\.whatsapp\.com/[A-Za-z0-9]+", url)
                    if match:
                        links_unicos.add("https://" + match.group(0))
                    
                    # Pausa aleatória extra entre 3 e 7 segundos
                    time.sleep(random.uniform(3, 7))
                
                if links_unicos:
                    st.success(f"🎯 Captura concluída! {len(links_unicos)} grupos encontrados.")
                    st.download_button("📥 Baixar Lista", "\n".join(links_unicos), "grupos.txt")
                    for l in links_unicos:
                        st.code(l)
                else:
                    st.warning("O Google não retornou links. Tente mudar a Rede Social ou aguarde 10 min.")
                    
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ O Google bloqueou este IP do servidor. SOLUÇÃO: Espere 15 min ou mude o termo da busca (ex: em vez de 'Igreja', use 'Católicos').")
            else:
                st.error(f"Erro: {e}")
    else:
        st.error("Digite um tema.")

st.markdown("---")
st.info("💡 **Dica de Especialista:** Se o bloqueio persistir, abra o seu buscador em uma **Aba Anônima** do navegador ou mude a sua conexão (de Wi-Fi para 4G do celular) por 2 minutos. Isso força o servidor a renovar a sessão.")
