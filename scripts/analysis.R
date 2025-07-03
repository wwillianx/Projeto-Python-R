# Carrega os pacotes necessários
library(ggplot2)  # Para criar gráficos
library(dplyr)    # Para manipulação e transformação de dados

# Configuração global para evitar notação científica nos números
options(scipen=999)

# Carrega o dataset limpo com os dados de vendas
df <- read.csv("dados/clean_vgsales.csv")


# GRÁFICO 1: Vendas globais por ano
# Agrupa os dados por ano e soma as vendas globais de cada ano
sales_by_year <- df %>%
  group_by(Year) %>%
  summarise(Global_Sales = sum(Global_Sales))

# Cria um gráfico de linha mostrando a evolução das vendas globais ao longo dos anos
ggplot(sales_by_year, aes(x=Year, y=Global_Sales)) +
  geom_line(color="blue") +
  ggtitle("Vendas Globais por Ano") +
  theme_minimal()

# Salva o gráfico como imagem PNG
ggsave("sales_by_year.png")


# GRÁFICO 2: Top 10 plataformas com mais vendas
# Agrupa por plataforma, soma as vendas e seleciona as 10 maiores
sales_by_platform <- df %>%
  group_by(Platform) %>%
  summarise(Global_Sales = sum(Global_Sales)) %>%
  top_n(10, Global_Sales)  # Seleciona as 10 plataformas com maiores vendas

# Cria um gráfico de barras com as plataformas ordenadas
ggplot(sales_by_platform, aes(x=reorder(Platform, -Global_Sales), y=Global_Sales)) +
  geom_col(fill="darkgreen") +
  ggtitle("Top 10 Plataformas por Vendas") +
  xlab("Plataforma") +
  ylab("Vendas Globais (milhões)") +
  theme_minimal()

# Salva o gráfico
ggsave("sales_by_platform.png")


# GRÁFICO 3: Top 10 jogos mais vendidos (todas as plataformas unificadas)
# Agrupa por nome do jogo, soma vendas globais e pega os 10 mais vendidos
top10_global <- df %>%
  group_by(Name) %>%
  summarise(Global_Sales = sum(Global_Sales)) %>%
  arrange(desc(Global_Sales)) %>%
  head(10)  # Seleciona os 10 primeiros

# Cria gráfico de barras horizontal
ggplot(top10_global, aes(x=reorder(Name, Global_Sales), y=Global_Sales)) +
  geom_col(fill="steelblue") +
  coord_flip() +
  ggtitle("Top 10 Jogos Mais Vendidos (Todas as Plataformas)") +
  xlab("Jogo") +
  ylab("Vendas Globais (milhões)") +
  theme_minimal()

# Salva o gráfico
ggsave("top10_global_unificado.png")


# GRÁFICO 4: Top 10 jogos do último ano presente no dataset
# Identifica o último ano no dataset
ultimo_ano <- max(df$Year)

# Filtra apenas os jogos lançados no último ano e seleciona os 10 mais vendidos
top10_ultimo_ano <- df %>%
  filter(Year == ultimo_ano) %>%
  group_by(Name) %>%
  summarise(Global_Sales = sum(Global_Sales)) %>%
  arrange(desc(Global_Sales)) %>%
  head(10)

# Cria gráfico de barras horizontal com os 10 mais vendidos desse ano
ggplot(top10_ultimo_ano, aes(x=reorder(Name, Global_Sales), y=Global_Sales)) +
  geom_col(fill="orange") +
  coord_flip() +
  ggtitle(paste("Top 10 Jogos em", ultimo_ano)) +
  xlab("Jogo") +
  ylab("Vendas Globais (milhões)") +
  theme_minimal()

# Salva o gráfico
ggsave("top10_ultimo_ano.png")


# GRÁFICO 5: Comparação de vendas anuais entre dois jogos específicos
# Defina os dois jogos a serem comparados aqui
jogo1 <- "Minecraft"
jogo2 <- "Grand Theft Auto V"

# Filtra os dados apenas para os dois jogos e calcula as vendas por ano
df_comparacao <- df %>%
  filter(Name %in% c(jogo1, jogo2)) %>%  # Mantém linhas apenas dos dois jogos
  group_by(Name, Year) %>%  # Agrupa por nome do jogo e ano
  summarise(Vendas_Anuais = sum(Global_Sales), .groups = "drop")  # Soma as vendas por ano

# Cria gráfico de linhas comparando a evolução anual de vendas entre os dois jogos
ggplot(df_comparacao, aes(x = Year, y = Vendas_Anuais, color = Name)) +
  geom_line(size=1.2) +  # Linhas mais grossas
  geom_point(size=2) +   # Pontos marcando cada ano
  ggtitle(paste("Comparação de Vendas Anuais:", jogo1, "vs", jogo2)) +
  xlab("Ano") +
  ylab("Vendas Anuais (milhões)") +
  theme_minimal() +
  theme(legend.title = element_blank())

# Salva o gráfico
ggsave("comparacao_dois_jogos.png")
