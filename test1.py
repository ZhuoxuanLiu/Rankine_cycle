import CoolProp.CoolProp as CP
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
environmentT = 273.15+20
wasteHeatT = 273.15+150
#选择冷凝温度30°C，蒸发温度140°C，计算冷凝蒸发压力
P3 = CP.PropsSI('P', 'T', 303.15, 'Q', 0, 'R245ca')
P1 = P5 = CP.PropsSI('P', 'T', 273.15+120, 'Q', 1, 'R245ca')
s3 = CP.PropsSI('S', 'T', 303.15, 'Q', 0, 'R245ca')
h3 = CP.PropsSI('H', 'P', P3, 'Q', 0, 'R245ca')
s1 = s2s = CP.PropsSI('S', 'P', P5, 'T', 273.15+140, 'R245ca')
eta = 0.9
h1 = CP.PropsSI('H', 'P', P5, 'T', 273.15+140, 'R245ca')
h2s = CP.PropsSI('H', 'S', s2s, 'P', P3, 'R245ca')
h2 = h1 - eta*(h1-h2s)
s2 = CP.PropsSI('S', 'P', P3, 'H', h2, 'R245ca')
#选择抽气压力
percentage1 = np.linspace(0.4, 0.8, 30, endpoint=True)
percentage2 = np.linspace(0.82, 0.96, 30, endpoint=True)
efficiencyList = pd.DataFrame()
turbineLossList = pd.DataFrame()
condenserLossList = pd.DataFrame()
regenerator1LossList = pd.DataFrame()
regenerator2LossList = pd.DataFrame()
evaporatorLossList = pd.DataFrame()
for per1 in percentage1:
    for per2 in percentage2:
        P6 = P1 - per1*(P1-P3)
        P7 = P1 - per2*(P1-P3)
        h6s = CP.PropsSI('H', 'S', s2s, 'P', P6, 'R245ca')
        h7s = CP.PropsSI('H', 'S', s2s, 'P', P7, 'R245ca')
        h6 = h1 - eta*(h1-h6s)
        h7 = h1 - eta*(h1-h7s)
        s6 = CP.PropsSI('S', 'P', P6, 'H', h6, 'R245ca')
        s7 = CP.PropsSI('S', 'P', P7, 'H', h7, 'R245ca')
        h9 = CP.PropsSI('H', 'P', P7, 'Q', 0, 'R245ca')
        h8 = CP.PropsSI('H', 'P', P6, 'Q', 0, 'R245ca')
        s8 = CP.PropsSI('S', 'P', P6, 'Q', 0, 'R245ca')
        s9 = CP.PropsSI('S', 'P', P7, 'Q', 0, 'R245ca')
        alpha1 = (h8-h9)/(h6-h9)
        alpha2 = (1-alpha1)*(h9-h3)/(h7-h3)
        work = h1-h6 + (1-alpha1)*(h6-h7) + (1-alpha2-alpha1)*(h7-h2)
        evaporator = h1 - h8
        condenser = (1-alpha1-alpha2)*(h3 - h2)
        efficiency = work/evaporator
        efficiencyData = {'P6':[P6],'P7':[P7],'efficiency':[efficiency]}
        efficiencyList = efficiencyList.append(efficiencyData,ignore_index=True)

        turbineLoss_s = alpha1*s6 + alpha2*s7 + (1-alpha1-alpha2)*s2 - s1
        turbineLoss_I = turbineLoss_s*environmentT
        turbineData = {'P6': [P6], 'P7': [P7], 'turbineLoss_I': [turbineLoss_I]}
        turbineLossList = turbineLossList.append(turbineData, ignore_index=True)

        condenserLoss_s = (1-alpha1-alpha2)*(s3-s2) - condenser/environmentT
        condenserLoss_I = condenserLoss_s*environmentT
        condenserData = {'P6': [P6], 'P7': [P7], 'condenserLoss_I': [condenserLoss_I]}
        condenserLossList = condenserLossList.append(condenserData, ignore_index=True)

        regenerator1Loss_s = s8 - alpha1*s6 - (1-alpha1)*s9
        regenerator2Loss_s = (1-alpha1)*s9 - alpha2*s7 - (1-alpha1-alpha2)*s3
        regenerator1Loss_I = regenerator1Loss_s*environmentT
        regenerator2Loss_I = regenerator2Loss_s*environmentT
        regenerator1Data = {'P6': [P6], 'P7': [P7], 'regenerator1Loss_I': [regenerator1Loss_I]}
        regenerator1LossList = regenerator1LossList.append(regenerator1Data, ignore_index=True)
        regenerator2Data = {'P6': [P6], 'P7': [P7], 'regenerator2Loss_I': [regenerator2Loss_I]}
        regenerator2LossList = regenerator2LossList.append(regenerator2Data, ignore_index=True)

        evaporatorLoss_s = s1- s8 - evaporator/wasteHeatT
        evaporatorLoss_I = evaporatorLoss_s*environmentT
        evaporatorData = {'P6': [P6], 'P7': [P7], 'evaporatorLoss_I': [evaporatorLoss_I]}
        evaporatorLossList = evaporatorLossList.append(evaporatorData, ignore_index=True)


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False
P6Array = np.array(efficiencyList['P6'].values.tolist())/1000000
P7Array = np.array(efficiencyList['P7'].values.tolist())/1000000

efficiencyArray = np.array(efficiencyList['efficiency'].values.tolist())
ax = plt.axes(projection='3d')
efficiencyList = efficiencyList[efficiencyList['efficiency'] == efficiencyArray.max()]
efficiencyMaxP6 = np.array(efficiencyList['P6'].values.tolist()[0])/1000000
efficiencyMaxP7 = np.array(efficiencyList['P7'].values.tolist()[0])/1000000
ax.set_xlabel('P6 (MPa)')
ax.set_ylabel('P7 (MPa)')
ax.set_zlabel(chr(951))
ax.set_title('循环热效率')
ax.scatter3D(P6Array, P7Array,efficiencyArray,c=efficiencyArray,cmap=plt.get_cmap('rainbow'))
plt.savefig('循环热效率')
plt.show()
print(efficiencyMaxP6,efficiencyMaxP7,efficiencyArray.max())

turbineLossArray = np.array(turbineLossList['turbineLoss_I'].values.tolist())/1000
ax = plt.axes(projection='3d')
turbineLossList = turbineLossList[turbineLossList['turbineLoss_I'] == turbineLossArray.min()*1000]
turbineLossMinP6 = np.array(turbineLossList['P6'].values.tolist()[0])/1000000
turbineLossMinP7 = np.array(turbineLossList['P7'].values.tolist()[0])/1000000
ax.set_xlabel('P6 (MPa)')
ax.set_ylabel('P7 (MPa)')
ax.set_zlabel('i (kJ/kg)')
ax.set_title('膨胀机损失')
ax.scatter3D(P6Array, P7Array,turbineLossArray,c=turbineLossArray,cmap=plt.get_cmap('rainbow'))
plt.savefig('膨胀机损失')
plt.show()
print(turbineLossMinP6,turbineLossMinP7,turbineLossArray.min())

condenserLossArray = np.array(condenserLossList['condenserLoss_I'].values.tolist())/1000
ax = plt.axes(projection='3d')
condenserLossList = condenserLossList[condenserLossList['condenserLoss_I'] == condenserLossArray.min()*1000]
condenserLossMinP6 = np.array(condenserLossList['P6'].values.tolist()[0])/1000000
condenserLossMinP7 = np.array(condenserLossList['P7'].values.tolist()[0])/1000000
ax.set_xlabel('P6 (MPa)')
ax.set_ylabel('P7 (MPa)')
ax.set_zlabel('i (kJ/kg)')
ax.set_title('冷凝器损失')
ax.scatter3D(P6Array, P7Array,condenserLossArray,c=condenserLossArray,cmap=plt.get_cmap('rainbow'))
ax.view_init(elev=30, azim=60)
plt.savefig('冷凝器损失')
plt.show()
print(condenserLossMinP6,condenserLossMinP7,condenserLossArray.min())

regenerator1LossArray = np.array(regenerator1LossList['regenerator1Loss_I'].values.tolist())/1000
ax = plt.axes(projection='3d')
regenerator1LossList = regenerator1LossList[regenerator1LossList['regenerator1Loss_I'] == regenerator1LossArray.min()*1000]
regenerator1LossMinP6 = np.array(regenerator1LossList['P6'].values.tolist()[0])/1000000
regenerator1LossMinP7 = np.array(regenerator1LossList['P7'].values.tolist()[0])/1000000
ax.set_xlabel('P6 (MPa)')
ax.set_ylabel('P7 (MPa)')
ax.set_zlabel('i (kJ/kg)')
ax.set_title('回热器1损失')
ax.scatter3D(P6Array, P7Array,regenerator1LossArray,c=regenerator1LossArray,cmap=plt.get_cmap('rainbow'))
ax.view_init(elev=30, azim=120)
plt.savefig('回热器1损失')
plt.show()
print(regenerator1LossMinP6,regenerator1LossMinP7,regenerator1LossArray.min())

regenerator2LossArray = np.array(regenerator2LossList['regenerator2Loss_I'].values.tolist())/1000
ax = plt.axes(projection='3d')
regenerator2LossList = regenerator2LossList[regenerator2LossList['regenerator2Loss_I'] == regenerator2LossArray.min()*1000]
regenerator2LossMinP6 = np.array(regenerator2LossList['P6'].values.tolist()[0])/1000000
regenerator2LossMinP7 = np.array(regenerator2LossList['P7'].values.tolist()[0])/1000000
ax.set_xlabel('P6 (MPa)')
ax.set_ylabel('P7 (MPa)')
ax.set_zlabel('i (kJ/kg)')
ax.set_title('回热器2损失')
ax.scatter3D(P6Array, P7Array,regenerator2LossArray,c=regenerator2LossArray,cmap=plt.get_cmap('rainbow'))
plt.savefig('回热器2损失')
plt.show()
print(regenerator2LossMinP6,regenerator2LossMinP7,regenerator2LossArray.min())

evaporatorLossArray = np.array(evaporatorLossList['evaporatorLoss_I'].values.tolist())/1000
ax = plt.axes(projection='3d')
evaporatorLossList = evaporatorLossList[evaporatorLossList['evaporatorLoss_I'] == evaporatorLossArray.min()*1000]
evaporatorLossMinP6 = np.array(evaporatorLossList['P6'].values.tolist()[0])/1000000
evaporatorLossMinP7 = np.array(evaporatorLossList['P7'].values.tolist()[0])/1000000
ax.set_xlabel('P6 (MPa)')
ax.set_ylabel('P7 (MPa)')
ax.set_zlabel('i (kJ/kg)')
ax.set_title('蒸发器损失')
ax.scatter3D(P6Array, P7Array,evaporatorLossArray,c=evaporatorLossArray,cmap=plt.get_cmap('rainbow'))
plt.savefig('蒸发器损失')
plt.show()
print(evaporatorLossMinP6,evaporatorLossMinP7,evaporatorLossArray.min())
