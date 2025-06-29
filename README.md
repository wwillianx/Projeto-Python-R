Para configurar o ambiente rode o arquivo: setup_project.py
 
 
 
 1. Introdução
Nome do Projeto: Sistema de Análise e Previsão de Vendas de Video Games
Versão do Documento: 1.3
Data: 10 de abril de 2025
Autores: Giordano Cassini, Lucas Pereira, Mikael Sousa, Tiago Marcelo Dalbosco e Willian Scheuermann. - Disciplina DLPD II
Objetivo: Descrever os requisitos funcionais e não funcionais do sistema de previsão e análise de vendas utilizando integração entre R e Python com base no dataset de vendas de video games do Kaggle.
2. Visão Geral
Descrição do Sistema:
O sistema tem como objetivo realizar análise exploratória, previsão de vendas futuras e segmentação de produtos do mercado de videogames. Utilizará integração entre R e Python para processar dados, treinar modelos simples de machine learning e apresentar os resultados em forma de relatórios e gráficos.
Stakeholders:
● Professor da disciplina DLPD II
● Alunos do grupo de projeto
● Futuramente, profissionais interessados em análise de dados em vendas
3. Requisitos Funcionais

        ID
Descrição
Prioridade
Dependências
Critério de Aceitação
RF-01
Importar e exibir o dataset de vendas em uma tabela.
Alta
-
O sistema exibe corretamente o dataset carregado.
RF-02
Gerar gráficos simples de vendas por ano e por plataforma.
Alta
RF-01
O sistema gera pelo menos dois gráficos de barras ou linhas com base nos dados.
RF-03
O sistema deve permitir a comparação entre jogos.
Média
RF-01
O usuário deve poder selecionar dois ou mais jogos e visualizar suas diferenças.
RF-04
Permitir a visualização e filtragem dos dados
Média
RF-01
O sistema deve exibir os dados conforme os filtros aplicados pelo usuário.
RF-05
Permitir salvar os gráficos em PNG.
Baixa
RF-02, RF-04
O sistema gera arquivos PNG a partir dos gráficos exibidos.
      4. Requisitos Não Funcionais
       ID
Descrição
Prioridade
Dependência s
Critério de Aceitação
RNF-01
O sistema deve ser executado localmente em VsCode
Alta
-
Todos os recursos funcionam em execução local.
  
        RNF-02
A previsão deve ser feita em no máximo 5 segundos.
Média
RF-03
Tempo de
execução testado em ambiente real.
RNF-03
O sistema deve ter código comentado e modular.
Alta
Todos
Comentários explicam as funções e blocos principais.
RNF-04
Não depender de bibliotecas complexas ou servidores externos.
Alta
RF-01 a RF-05
Apenas bibliotecas padrão e acessíveis estão sendo utilizadas.
   5. Casos de Uso
Caso de Uso 1: Analisar Dados Estatísticos
Descrição: O usuário pode visualizar estatísticas geradas a partir dos dados disponíveis. Ator(es): Usuário do sistema.
Pré-condição: O usuário deve estar com os dados importados
Fluxo Principal:
1. O usuário acessa a tela de análise estatística.
2. O sistema processa os dados e exibe estatísticas relevantes (médias, totais,
tendências).
Fluxo Alternativo:
1. Se não houver dados disponíveis, o sistema alerta o usuário.
Caso de Uso 2: Gerar Gráficos e Visualizar e Filtrar Dados
Descrição: O sistema gera gráficos para melhor visualização, e permite a refinação dos dados.
Ator(es): Usuário do sistema.
Pré-condição: O usuário deve estar com o dataset importado. Fluxo Principal:
1. O usuário acessa a opção de geração de gráficos.
2. O usuário seleciona os critérios desejados (por exemplo, vendas por ano).
3. O sistema gera e exibe o gráfico correspondente.
Fluxo Alternativo:

 1. Se não houver dados suficientes para gerar o gráfico, o sistema alerta o usuário.
Caso de Uso 3: Comparar Jogos e Calcular Estatísticas de Vendas Descrição: O usuário pode comparar estatísticas entre diferentes jogos.
Ator(es): Usuário do sistema.
Pré-condição: O usuário deve estar autenticado no sistema. Fluxo Principal:
1. O usuário acessa a opção de comparação de jogos.
2. O usuário seleciona dois ou mais jogos para comparar.
3. O sistema exibe um relatório comparativo.
Fluxo Alternativo:
● Se não houver dados para algum dos jogos selecionados, o sistema alerta o usuário.
6. Restrições
● O sistema deve funcionar em notebooks ou scripts simples.
● Não é obrigatória a criação de interface gráfica (pode ser via script).
● Não é obrigatório o uso de banco de dados.
● O arquivo de dados deve estar no formato CSV
7. Tecnologias Utilizadas
● Linguagens:
- R: Utilizado para análise estatística, geração de gráficos e visualizações.
- Python: Aplicado para pré-processamento de dados e modelos de machine learning simples.
● Ferramenta de Desenvolvimento:
- VSCode: Ambiente usado para programar em R e Python, com suporte a execução de notebooks e scripts integrados.
● Bibliotecas:
- Em R: `ggplot2`, `dplyr`, `reticulate` (integração com Python) - Em Python**: `pandas`, `matplotlib`, `scikit-learn`
● Dataset:
- Video Game Sales – Kaggle
- Fonte pública com dados de vendas de jogos por plataforma, gênero e região
- Estruturado, confiável e ideal para aplicações de análise e aprendizado de máquina.

 
