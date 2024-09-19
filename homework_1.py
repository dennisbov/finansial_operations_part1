import numpy
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

risk_and_return = pd.DataFrame({
    'Sheet': expected_returns.keys(),
    'E': expected_returns.values(),
    'σ': risks.values()
})


#  Построение "карты" (σ, E)

# plt.figure(figsize=(9, 7))
# plt.scatter(risk_and_return['σ'], risk_and_return['E'])
# plt.title('«Карта» активов в системе координат (σ, E)')
# plt.xlabel('Риск (σ)')
# plt.ylabel('Ожидаемая доходность (E)')
# plt.grid()
# plt.show()

optimal_assets = []

for i, point_1 in risk_and_return.iterrows():
    flag = False
    for j, point_2 in risk_and_return.iterrows():
        if (point_2['E'] >= point_1['E'] and point_2['σ'] < point_1['σ']) or (
            point_2['E'] > point_1['E'] and point_2['σ'] <= point_1['σ']):
            flag = True
            break
    if not flag:
        optimal_assets.append(point_1)

optimal_assets = pd.DataFrame(optimal_assets)

#  Построение "карты" (σ, E) с Парето оптимальными активами

# plt.figure(figsize=(9, 7))
# plt.scatter(risk_and_return['σ'], risk_and_return['E'])
# plt.scatter(optimal_assets['σ'], optimal_assets['E'], color='red')
# plt.title('Парето оптимальные активы')
# plt.xlabel('Риск (σ)')
# plt.ylabel('Ожидаемая доходность (E)')
# plt.grid()
# plt.show()
