import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_sheets = pd.read_excel('data.xlsx', sheet_name=None)

def find_risk(data):
    risk = data['log_return'].std()
    return risk

def find_expected_return(data):
    expected_return = data['log_return'].mean()
    return expected_return

expected_returns = {}
risks = {}

for sheet, data in data_sheets.items():
    expected_returns[sheet] = find_expected_return(data)
    risks[sheet] = find_risk(data)

risk_return_df = pd.DataFrame({
    'Sheet': expected_returns.keys(),
    'E': expected_returns.values(),
    'σ': risks.values()
}).dropna()


#  Построение "карты" (σ, E)

# plt.figure(figsize=(9, 7))
# plt.scatter(risk_return_df['σ'], risk_return_df['E'], marker='o')
# plt.title('«Карта» активов в системе координат (σ, E)')
# plt.xlabel('σ')
# plt.ylabel('E')
# plt.grid()

def pareto_optimal(rrisk_return_df):
    optimal_assets = []

    for index, point in risk_return_df.iterrows():
        dominated = False
        for compare_index, compare_point in risk_return_df.iterrows():
            if (compare_point['E'] >= point['E'] and compare_point['σ'] < point['σ']) or (
                compare_point['E'] > point['E'] and compare_point['σ'] <= point['σ']):
                dominated = True
                break
        if not dominated:
            optimal_assets.append(point)

    return pd.DataFrame(optimal_assets)

optimal_assets_df = pareto_optimal(risk_return_df)

def plot_assets(risk_return_df, optimal_assets_df):
    plt.figure(figsize=(9, 7))
    plt.scatter(risk_return_df['σ'], risk_return_df['E'], color='blue', label='Все активы', alpha=0.6)
    plt.scatter(optimal_assets_df['σ'], optimal_assets_df['E'], color='red', label='Парето оптимальные активы', s=100)
    plt.title('Эффективный фронт')
    plt.xlabel('Риск (σ)')
    plt.ylabel('Ожидаемая доходность (E)')
    plt.grid()
    plt.show()

# Вызов функции для построения графика
plot_assets(risk_return_df, optimal_assets_df)