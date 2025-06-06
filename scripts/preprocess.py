import pandas as pd

def load_dataset(path='data/vgsales.csv'):
    df = pd.read_csv(path)
    df = df.dropna(subset=['Year', 'Global_Sales'])  # remove valores ausentes
    df['Year'] = df['Year'].astype(int)
    return df

def save_clean_data(df, path='data/clean_vgsales.csv'):
    df.to_csv(path, index=False)

if __name__ == "__main__":
    df = load_dataset()
    save_clean_data(df)
