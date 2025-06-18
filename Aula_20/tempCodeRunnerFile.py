#import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np

#  Obtendo dados
try:
    print("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    
    #  Demilitando somente as variáveis do estlionato
    df_ocorrencias = df_ocorrencias[['munic', 'estelionato']]

    #  Totalizar as ocorrencias de ESTELIONATO por município(agrupar e somar)
    df_estelionato = df_ocorrencias.groupby('munic').sum(['estelionato']).reset_index()

    # O head() vai printar as primeiras linhas pra saber se oobtee os dados corretamente
    
except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()