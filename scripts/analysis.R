library(ggplot2)
library(dplyr)
options(scipen=999) # evita notação científica

df <- read.csv("dados/clean_vgsales.csv")

# 🔷 Gráfico: Vendas por Ano
sales_by_year <- df %>%
  group_by(Year) %>%
  summarise(Global_Sales = sum(Global_Sales))

ggplot(sales_by_year, aes(x=Year, y=Global_Sales)) +
  geom_line(color="blue") +
  ggtitle("Vendas Globais por Ano") +
  theme_minimal()

ggsave("sales_by_year.png")

# 🔷 Gráfico: Top 10 Plataformas
sales_by_platform <- df %>%
  group_by(Platform) %>%
  summarise(Global_Sales = sum(Global_Sales)) %>%
  top_n(10, Global_Sales)

ggplot(sales_by_platform, aes(x=reorder(Platform, -Global_Sales), y=Global_Sales)) +
  geom_col(fill="darkgreen") +
  ggtitle("Top 10 Plataformas por Vendas") +
  xlab("Plataforma") +
  ylab("Vendas Globais (milhões)") +
  theme_minimal()

ggsave("sales_by_platform.png")

# 🔷 Gráfico: Top 10 Jogos mais vendidos (unificando plataformas)
top10_global <- df %>%
  group_by(Name) %>%
  summarise(Global_Sales = sum(Global_Sales)) %>%
  arrange(desc(Global_Sales)) %>%
  head(10)

ggplot(top10_global, aes(x=reorder(Name, Global_Sales), y=Global_Sales)) +
  geom_col(fill="steelblue") +
  coord_flip() +
  ggtitle("Top 10 Jogos Mais Vendidos (Todas as Plataformas)") +
  xlab("Jogo") +
  ylab("Vendas Globais (milhões)") +
  theme_minimal()

ggsave("top10_global_unificado.png")

# 🔷 Gráfico: Top 10 Jogos do Último Ano (com valores em milhões)
ultimo_ano <- max(df$Year)

top10_ultimo_ano <- df %>%
  filter(Year == ultimo_ano) %>%
  group_by(Name) %>%
  summarise(Global_Sales = sum(Global_Sales)) %>%
  arrange(desc(Global_Sales)) %>%
  head(10)

ggplot(top10_ultimo_ano, aes(x=reorder(Name, Global_Sales), y=Global_Sales)) +
  geom_col(fill="orange") +
  coord_flip() +
  ggtitle(paste("Top 10 Jogos em", ultimo_ano)) +
  xlab("Jogo") +
  ylab("Vendas Globais (milhões)") +
  theme_minimal()

ggsave("top10_ultimo_ano.png")

library(ggplot2)
library(dplyr)
options(scipen=999) # evita notação científica

df <- read.csv("dados/clean_vgsales.csv")

# (seus gráficos atuais aqui...)

# ---- Novo gráfico: Comparação de vendas anuais entre dois jogos ----

# Defina aqui os dois jogos para comparar (pode trocar os nomes)
jogo1 <- "Minecraft"
jogo2 <- "Grand Theft Auto V"

# Filtra os dados só dos dois jogos escolhidos
df_comparacao <- df %>%
  filter(Name %in% c(jogo1, jogo2)) %>%
  group_by(Name, Year) %>%
  summarise(Vendas_Anuais = sum(Global_Sales), .groups = "drop")

# Plot comparativo de vendas por ano
ggplot(df_comparacao, aes(x = Year, y = Vendas_Anuais, color = Name)) +
  geom_line(size=1.2) +
  geom_point(size=2) +
  ggtitle(paste("Comparação de Vendas Anuais:", jogo1, "vs", jogo2)) +
  xlab("Ano") +
  ylab("Vendas Anuais (milhões)") +
  theme_minimal() +
  theme(legend.title = element_blank())

ggsave("comparacao_dois_jogos.png")