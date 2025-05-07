import pandas as pd

def load_dataset(save_path):
    df = pd.read_csv(save_path)
    return df