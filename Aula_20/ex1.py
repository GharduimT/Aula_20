# from utils import limpar_nome_municipio
# Importa a biblioteca Matplotlib para criar os gráficos
# pip install matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


try:
    print("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

    # Buscar a base de dados CSV online do site ISP (Instituto de Segurança Pública)
    # encoding='iso-8859-1' - Codificação dos caracteres com acentuação
    # outras opções: utf-8, iso-8859-1, latin1, cp1252
    # encodings principais: https://docs.python.org/3/library/codecs.html#standard-encodings
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # Demilitando somente as variáveis do Exemplo01: munic e roubo_veiculo
    df_ocorrencias = df_ocorrencias[['munic', 'roubo_veiculo']]

    # Totalizar roubo de veiculo por municipio (agrupar e somar)
    # reset_index(), traz de volta os índices que numera as colunas, pois se
    # perdem nesta operação
    df_roubo_veiculo = df_ocorrencias.groupby('munic').sum(['roubo_veiculo']).reset_index()

    # Printando as linhas iniciais com o método head() apenas para ver se os dados
    # foram obtidos corretamente
    print(df_roubo_veiculo.head())

except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()


# Inicando a obtenção das medidas fundamentadas em estatística descritiva
try:
    print('Obtendo informações sobre padrão de roubo de veículos...')


    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    # Obtendo média de roubo_veiculo
    media_roubo_veiculo = np.mean(array_roubo_veiculo)


    mediana_roubo_veiculo = np.median(array_roubo_veiculo)


    distancia = abs((media_roubo_veiculo-mediana_roubo_veiculo) / mediana_roubo_veiculo)


    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull') # Q1 é 25% 
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull') # Q2 é 50% (mediana)
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull') # Q3 é 75%
    

    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude_total = maximo - minimo

    # OBTENDO OS MUNÍCIPIOS COM MAIORES E MONORES NÚMEROS DE ROUBOS DE VEÍCULOS
    # Filtramos os registros do DataFrame df_roubo_veiculo para achar os municípios
    # com menores e maiores números de roubos de veículos.
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print('\nMunicípios com Menores números de Roubos: ')
    print(70*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    print('\nMunicípios com Maiores números de Roubos:')
    print(45*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    # ##### DESCOBRIR OUTLIERS #########
    # IQR (Intervalo interquartil)
    # q3 - q1
    # É a amplitude do intervalo dos 50% dos dados centrais
    # Ela ignora os valores extremos.
    # Não sofre a interferência dos valores extremos.
    # Quanto mais próximo de zero, mais homogêneo são os dados.
    # Quanto mais próximo do q3, mais heterogêneo são os dados.
    iqr = q3 - q1

    # Limite superior
    # Vai identificar os outliers acima de q3
    limite_superior = q3 + (1.5 * iqr)

    # Limite inferior
    # Vai identificar os outliers abaixo de q1
    limite_inferior = q1 - (1.5 * iqr)

   
    # PRINTANDO AS MEDIDAS
    print('\nPRINTANDO AS MEDIDAS: ')
    print(30*'-')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Mínimo: {minimo}')
    print(f'1º Quartil: {q1}')
    print(f'2º Quartil: {q2}')  # Mediana
    print(f'3º Quartil: {q3}')
    print(f'IQR: {iqr}')
    print(f'Máximo: {maximo}')
    print(f'Limite Superior: {limite_superior}')
    
    print('\nOUTRAS AS MEDIDAS: ')
    print(30*'-')
    print(f'Amplitude Total: {amplitude_total}')
    print(f'Média: {media_roubo_veiculo:.3f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média e Mediana: {distancia:.4f}')
    
    #  Medias de DISPERSÃO
    #  Indica a variabilidade de um conjunto de dados em relação a média
    #  VARIANCIA é a média dps quadrados das disferenças entre cada valor e a média
    variancia = np.var(array_roubo_veiculo)

    #  DISTANCIA entre média e variância
    distancia_var_media = variancia / (media_roubo_veiculo ** 2)

    #Desvio Padrão
    #O quanto os dados podem estar se distanciando da media
    desvio_padrão = np.std(array_roubo_veiculo)

    #Coeficiente de variação é a magnitude do desvio padrão
    coef_variacao = desvio_padrão / media_roubo_veiculo

    print('\nMEDIDAS DE DISPERSÃO')
    print(30*'-')
    print(f"Variancia: {variancia}")
    print(f"Distancia da Medida (variancia): {distancia_var_media}")
    print(f"Desvio Parão: {desvio_padrão}")
    print(f"Coeficiente de Variação: {coef_variacao}")


    # #### OUTLIERS
    # Obtendo os ouliers inferiores
    # Filtrar o dataframe df_roubo_veiculo para o munics com roubo de veículo
    # abaixo limite inferior (OUTLIERS INFERIORES)
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    
    # Obtendo os ouliers superiores
    # Filtrar o dataframe df_roubo_veiculo para o munics com roubo de veículo
    # acima de limite superior (OUTLIERS SUPERIORES)
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]

    print('\nMunicípios com outliers inferiores: ')
    print(45*'-')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))

    print('\nMunicípios com outliers superiores: ')
    print(45*'-')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers superiores!')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()


# PLOTANDO GRÁFICO
# Matplotlib
try:
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    
    plt.subplots(2, 2, figsize=(16, 10))
    plt.suptitle('Análise de roubo de veículos no RJ') 

    # POSIÇÃO 01
    # BOXPLOT
    plt.subplot(2, 2, 1)  
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title("Boxplot dos Dados")

    # POSIÇÃO 02
    # MEDIDAS
    # Exibição de informações estatísticas
    plt.subplot(2, 2, 2)
    plt.title('Medidas Estatísticas')
    plt.text(0.1, 0.9, f'Limite inferior: {limite_inferior}', fontsize=10)
    plt.text(0.1, 0.8, f'Menor valor: {minimo}', fontsize=10) 
    plt.text(0.1, 0.7, f'Q1: {q1}', fontsize=10)
    plt.text(0.1, 0.6, f'Mediana: {mediana_roubo_veiculo}', fontsize=10)
    plt.text(0.1, 0.5, f'Q3: {q3}', fontsize=10)
    plt.text(0.1, 0.4, f'Média: {media_roubo_veiculo:.3f}', fontsize=10)
    plt.text(0.1, 0.3, f'Maior valor: {maximo}', fontsize=10)
    plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=10)

    plt.text(0.5, 0.9, f'Distância Média e Mediana: {distancia:.4f}', fontsize=10)
    plt.text(0.5, 0.8, f'IQR: {iqr}', fontsize=10)
    plt.text(0.5, 0.7, f'Amplitude Total: {amplitude_total}', fontsize=10)
    
    # POSIÇÃO 03
    # OUTLIERS INFERIORES
    plt.subplot(2, 2, 3)
    plt.title('Outliers Inferiores')
    # Se o DataFrame do outliers não estiver vazio
    if not df_roubo_veiculo_outliers_inferiores.empty:
        dados_inferiores = df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True) #crescente
        # Gráfico de Barras
        plt.barh(dados_inferiores['munic'], dados_inferiores['roubo_veiculo'])
    else:
        # Se não houver outliers
        plt.text(0.5, 0.5, 'Sem Outliers Inferiores', ha='center', va='center', fontsize=12)
        plt.title('Outilers Inferiores')
        plt.xticks([])
        plt.yticks([])
    
    # POSIÇÃO 04
    # OUTLIERS SUPERIORES
    plt.subplot(2, 2, 4)
    plt.title('Outliers Superiores')
    if not df_roubo_veiculo_outliers_superiores.empty:
        dados_superiores = df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=True)

        # Cria o gráfico e guarda as barras
        barras = plt.barh(dados_superiores['munic'], dados_superiores['roubo_veiculo'], color='black')
        # Adiciona rótulos nas barras
        plt.bar_label(barras, fmt='%.0f', label_type='edge', fontsize=8, padding=2)

        # Diminui o tamanho da fonte dos eixos
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)

        plt.title('Outliers Superiores')
        plt.xlabel('Total Roubos de Veículos')    
    else:
        # Se não houver outliers superiores, exibe uma mensagem no lugar.
        plt.text(0.5, 0.5, 'Sem outliers superiores', ha='center', va='center', fontsize=12)
        plt.title('Outliers Superiores')
        plt.xticks([])
        plt.yticks([])

    # Ajusta os espaços do layout para que os gráficos não fiquem espremidos
    plt.tight_layout()
    # Mostra a figura com os dois gráficos
    plt.show()
    
except Exception as e:
    print(f'Erro ao plotar {e}')
    exit()
