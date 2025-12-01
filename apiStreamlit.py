import requests
import streamlit as st
import pandas as pd
import requests
from pprint import pprint




def pegar_nome_por_decada(nome: str):
    url = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'
    dados_decadas = fazer_request(url=url)
    pprint(dados_decadas)
    dict_decadas = {}

    if not dados_decadas:
        return {}

    for dados in dados_decadas[0]['res']:
        decada = dados['periodo']
        quantidade = dados['frequencia']
        dict_decadas[decada] = quantidade    
    return dict_decadas    
   


def fazer_request(url, params=None):
    """
        Realiza as requests para API do IBGE
    """
    try:
        resposta = requests.get(url, params=params, timeout=10)
        resposta.raise_for_status()  # Levanta exceção para erros HTTP
        return resposta.json()
    
    except requests.exceptions.RequestException as e:
        print(f'Erro ao fazer a request para {url}: {e}')
        return None
    
    except ValueError as e:
        print(f'Erro ao decodificar JSON: {e}')
        return None


def main():
   st.title('Web App API Ibge')
   st.write('Dados do IBGE')

   nome = st.text_input('Consulte um nome')
   if not nome:
       st.stop()
   else:
    dict_decadas = pegar_nome_por_decada(nome=nome)
    if not dict_decadas:
        st.warning(f'Nenhum dado encontrada para o {nome}')
        st.stop()

    df = pd.DataFrame(list(dict_decadas.items()),columns= ['Década','Frequencia'])
    df.set_index('Década',inplace = True)

    col1,col2 = st.columns([0.3,0.7])
    with col1:
        st.write('Frequencia por década')
        st.dataframe(df)
    with col2:        
        st.write('Evolução no tempo')
        st.line_chart(df)


if __name__ == '__main__':
    main()

    