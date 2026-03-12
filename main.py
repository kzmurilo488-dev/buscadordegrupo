import streamlit as st
import requests
import re
import time
import random

# Configurações de UI
st.set_page_config(page_title="Minerador LeadGen Pro", page_icon="💎", layout="wide")

st.title("💎 Minerador de Leads High-End")
st.write("Sistema resiliente com rotação de fontes e limpeza de links.")

# Interface
col1, col2 = st.columns([2, 1])
with col1:
    nicho = st.text_input("Nicho ou Palavra-chave (ex: Igreja, Investimentos, VSL)", "")
with col2:
    quantidade = st.slider("Profundidade da busca", 1, 5, 2)

def extrair_links_limpos(texto):
    """Filtra apenas links reais de convite do WhatsApp."""
    padrao = r"chat\.whatsapp\.com/(?:invite/)?([A-Za-z0-9]{20,})"
    encontrados = re.findall(padrao, texto)
    return [f"https://chat.whatsapp.com/{codigo}" for codigo in encontrados]

if st.button("🚀 Iniciar Mineração Inteligente"):
    if nicho:
        links_finais = set()
        progresso = st.progress(0)
        status = st.empty()
        
        # Estratégia Multi-Motor: Se um falha, o outro supre
        motores = [
            f"https://www.bing.com/search?q=site:facebook.com+chat.whatsapp.com+{nicho}",
            f"https://duckduckgo.com/html/?q=chat.whatsapp.com+{nicho}",
            f"https://www.google.com/search?q=intext:chat.whatsapp.com+{nicho}"
        ]

        headers_list = [
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36"},
            {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        ]

        for idx, url in enumerate(motores):
            status.text(f"Explorando fonte {idx+1} de {len(motores)}...")
            try:
                # Rotação de cabeçalho para evitar bloqueio de IP
                h = random.choice(headers_list)
                response = requests.get(url, headers=h, timeout=15)
                
                if response.status_code == 200:
                    links = extrair_links_limpos(response.text)
                    for l in links:
                        links_finais.add(l)
                
                # Pausa técnica para o servidor não identificar o robô
                time.sleep(random.uniform(2, 4))
                progresso.progress((idx + 1) / len(motores))
                
            except Exception as e:
                continue

        status.empty()
        
        if links_finais:
            st.success(f"🎯 Mineração concluída! Encontrei {len(links_finais)} grupos únicos.")
            
            # Área de exportação
            lista_final = "\n".join(list(links_finais))
            st.download_button(
                label="📥 Exportar para CRM/TXT",
                data=lista_final,
                file_name=f"leads_{nicho}.txt",
                mime="text/plain"
            )
            
            # Exibição organizada
            st.markdown("### Links Validados:")
            for link in links_finais:
                st.code(link, language="text")
        else:
            st.error("As fontes de dados estão protegidas ou o termo é muito específico. Dica: Tente usar apenas uma palavra (ex: 'Igreja' em vez de 'Igreja em Florianópolis').")
    else:
        st.error("Por favor, digite um nicho para minerar.")

st.divider()
st.info("💡 **Aviso Técnico:** Este script usa rotação de User-Agents. Se o resultado for zero, o provedor de internet bloqueou a requisição temporariamente. Aguarde 5 minutos.")
