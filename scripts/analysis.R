library(ggplot2)
library(dplyr)

df <- read.csv("dados/clean_vgsales.csv")

# Vendas por Ano
sales_by_year <- df %>%
  group_by(Year) %>%
  summarise(Global_Sales = sum(Global_Sales))

ggplot(sales_by_year, aes(x=Year, y=Global_Sales)) +
  geom_line(color="blue") +
  ggtitle("Vendas Globais por Ano") +
  theme_minimal()

ggsave("sales_by_year.png")

# Vendas por Plataforma (Top 10)
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
