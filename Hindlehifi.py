from __future__ import division
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch

dataplm = pd.read_excel('datafile.xlsx',sheet_name='datafile4')
profit = pd.read_excel('datafile.xlsx',sheet_name='profit')
listobj=[]
listcost=[]
listmachineday=[]
machineday = 10
while (machineday<21):
    machineday +=1
    listmachineday.append(machineday)
#model
    model = pyo.ConcreteModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    model.x = pyo.Var(range(3),  bounds=(0,None))
    x = model.x
#obj
    maxprofit = sum([x[i]*profit.p[i] for i in range(3)])
    model.obj=pyo.Objective(expr=maxprofit, sense= maximize)
#constraints
    model.cap = pyo.ConstraintList()
    for i in range(3):
        model.cap.add(expr= x[i] >= profit.order[i])
    A = sum([x[i]*profit.A[i]  for i in range(3)])
    model.A = pyo.Constraint(expr=A<=505)
    B = sum([x[i]*profit.B[i] for i in range(3)])
    model.B =pyo.Constraint(expr=B<=435)
    C = sum([x[i]*profit.C[i] for i in range(3)])
    model.C =pyo.Constraint(expr= C<=435)
    D = sum([x[i]*profit.D[i] for i in range(3)])
    model.D =pyo.Constraint(expr= D<=700)

    timecap= sum([x[i]*profit.time[i] for i in range(3)])



    model.timecap = pyo.Constraint(expr=timecap +2700 <=480*machineday)


    totalcost = sum([x[i]*profit.cost[i] for i in range(3)])

    SolverFactory('gurobi').solve(model).write()
#results = opt.solve(model)
    listobj.append(pyo.value(model.obj))
    listcost.append(pyo.value(totalcost))
    model.pprint()
    model.dual.pprint()
    print ("Duals")
    for c in [model.A,model.B, model.C,model.D]:
        print ("   Constraint",c,model.dual[c])
    #for index in c:
     #   print ("      ", index, model.dual[c[index]])

    print('Maximum Profit',pyo.value(model.obj))

    print('Total Cost:',pyo.value(totalcost))
    lis1=[]
    lis2=[]
    for j in range(45,60):
        x1 = (pyo.value(model.obj)-63.99*pyo.value(x[1])-99.99*pyo.value(x[2]))/j
        lis1.append(int(x1))
        lis2.append(j)
print(lis2,lis1)
plt.plot(lis2,lis1,color='brown', label='X1')
plt.title('X1 Values')
plt.show()
plt.plot(listmachineday,listobj)
plt.title('Obj Values')
plt.show()
plt.plot(listmachineday,listcost)
plt.title('Total Cost Values')
plt.show()
figure, (ax1,ax2,ax3) = plt.subplots(1, 3)
ax1.plot(lis2,lis1)
ax1.set_title('X1')
ax2.plot(listmachineday,listobj)
ax2.set_title('Obj Values')
ax3.plot(listmachineday,listcost)
ax3.set_title('Total Cost Values')
plt.show()
#plt.axhline(2, color='orange', label = 'max profit')

