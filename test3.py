import CoolProp.CoolProp as CP
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl

environmentT = 273.15+20
# wasteHeat = np.linspace(373.15, 413.15, 10,endpoint=True)
wasteHeat = [373.15]
condenseT = 303.15
evaporatorLoss_per_list =[]
turbineLoss_per_list = []
regenerator1Loss_per_list = []
condenserLoss_per_list = []
regenerator2Loss_per_list = []

for wasteHeatT in wasteHeat:
#选择冷凝温度30°C，蒸发温度140°C，计算冷凝蒸发压力
    P3 = CP.PropsSI('P', 'T', condenseT, 'Q', 0, 'R245fa')
    P1 = P5 = CP.PropsSI('P', 'T', 273.15+80, 'Q', 1, 'R245fa')
    s3 = CP.PropsSI('S', 'T', condenseT, 'Q', 0, 'R245fa')
    h3 = CP.PropsSI('H', 'P', P3, 'Q', 0, 'R245fa')
    s1 = s2s = CP.PropsSI('S', 'P', P5, 'T', 273.15+90, 'R245fa')
    eta = 0.9
    h1 = CP.PropsSI('H', 'P', P5, 'T', 273.15+90, 'R245fa')
    h2s = CP.PropsSI('H', 'S', s2s, 'P', P3, 'R245fa')
    h2 = h1 - eta*(h1-h2s)
    s2 = CP.PropsSI('S', 'P', P3, 'H', h2, 'R245fa')
    #选择抽气压力
    per1 = 0.44678815
    per2 = 0.77561217


    P6 = P1 - per1*(P1-P3)
    P7 = P1 - per2*(P1-P3)
    h6s = CP.PropsSI('H', 'S', s2s, 'P', P6, 'R245fa')
    h7s = CP.PropsSI('H', 'S', s2s, 'P', P7, 'R245fa')
    h6 = h1 - eta*(h1-h6s)
    h7 = h1 - eta*(h1-h7s)
    s6 = CP.PropsSI('S', 'P', P6, 'H', h6, 'R245fa')
    s7 = CP.PropsSI('S', 'P', P7, 'H', h7, 'R245fa')
    h9 = CP.PropsSI('H', 'P', P7, 'Q', 0, 'R245fa')
    h8 = CP.PropsSI('H', 'P', P6, 'Q', 0, 'R245fa')
    s8 = CP.PropsSI('S', 'P', P6, 'Q', 0, 'R245fa')
    s9 = CP.PropsSI('S', 'P', P7, 'Q', 0, 'R245fa')
    s0 = CP.PropsSI('S', 'P', 101325, 'T', environmentT, 'R245fa')
    h0 = CP.PropsSI('H', 'P', 101325, 'T', environmentT, 'R245fa')
    alpha1 = (h8-h9)/(h6-h9)
    alpha2 = (1-alpha1)*(h9-h3)/(h7-h3)
    work = h1-h6 + (1-alpha1)*(h6-h7) + (1-alpha2-alpha1)*(h7-h2)
    evaporator = h1 - h8
    condenser = (1-alpha1-alpha2)*(h3 - h2)
    efficiency = work/evaporator
    eff_condenser = -condenser/evaporator
    turbineLoss_s = alpha1*s6 + alpha2*s7 + (1-alpha1-alpha2)*s2 - s1
    turbineLoss_I = turbineLoss_s*environmentT

    condenserLoss_s = (1-alpha1-alpha2)*(s3-s2) - condenser/environmentT
    condenserLoss_I = condenserLoss_s*environmentT

    regenerator1Loss_s = s8 - alpha1*s6 - (1-alpha1)*s9
    regenerator2Loss_s = (1-alpha1)*s9 - alpha2*s7 - (1-alpha1-alpha2)*s3
    regenerator1Loss_I = regenerator1Loss_s*environmentT
    regenerator2Loss_I = regenerator2Loss_s*environmentT

    evaporatorLoss_s = s1- s8 - evaporator/wasteHeatT
    evaporatorLoss_I = evaporatorLoss_s*environmentT
    total_i = evaporatorLoss_I + regenerator2Loss_I + regenerator1Loss_I + condenserLoss_I + turbineLoss_I
    total_i2 = (-evaporator/wasteHeatT-condenser/environmentT)*environmentT

    aveT = (h1-h8)/(s1-s8)
    exQh = (1-environmentT/wasteHeatT)*(h1-h8)  # 热源㶲
    aveT_condense = (h2-h3)/(s2-s3)
    exQc = (1-environmentT/aveT_condense)*(h2-h3)*(1-alpha1-alpha2)  # 冷源为环境温度，㶲全部损失
    exQh0 = (1-environmentT/aveT)*(h1-h8)   #  热工质㶲
    exh1 = (h1-h0) - environmentT*(s1-s0)
    exh8 = (h8-h0) - environmentT*(s8-s0)
    exh2 = ((h2-h0) - environmentT*(s2-s0))*(1-alpha1-alpha2)
    exh6 = ((h6-h0) - environmentT*(s6-s0))*alpha1
    exh7 = ((h7-h0) - environmentT*(s7-s0))*alpha2
    exh3 = ((h3-h0) - environmentT*(s3-s0))*(1-alpha1-alpha2)
    exh9 = ((h9-h0) - environmentT*(s9-s0))*(1-alpha1)

    evaporatorLoss_per = evaporatorLoss_I/exQh
    eta_evaporater = exh1/(exh8+exQh)
    evaporatorLoss_per_list.append(evaporatorLoss_per)
    # print(exQc - condenserLoss_I)
    print(exQh-(exh1-exh8)-evaporatorLoss_I)

    turbineLoss_per = turbineLoss_I/exQh
    eta_turbine = work/(exh1-exh2-exh6-exh7)
    turbineLoss_per_list.append(turbineLoss_per)

    condenserLoss_per = condenserLoss_I/exQh
    eta_condenser = exh3/exh2
    condenserLoss_per_list.append(condenserLoss_per)

    regenerator1Loss_per = regenerator1Loss_I/exQh
    eta_regenerator1 = exh8/(exh9+exh6)
    regenerator1Loss_per_list.append(regenerator1Loss_per)

    regenerator2Loss_per = regenerator2Loss_I/exQh
    eta_regenerator2 = exh9/(exh3+exh7)
    regenerator2Loss_per_list.append(regenerator2Loss_per)

    work_per = work/exQh
    print(work_per)
    print(P6, P7)
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False
# plt.plot(wasteHeat,evaporatorLoss_per_list )
# plt.show()

