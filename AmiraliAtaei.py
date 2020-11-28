#!/usr/bin/env python
# coding: utf-8

# In[74]:


import pandas as pd
import numpy as np
import random
import time


# In[75]:


#And 0
#Or 1
#Xor 2
#Nand 3
#Nor 4
#Xnor 5

def And(a, b):
    return a & b

def Or(a, b):
    return a | b

def Xor(a, b):
    return a ^ b

def Nand(a, b):
    return not a & b

def Nor(a, b):
    return not a | b

def Xnor(a, b):
    return not a ^ b

def gate(a, b, char):
    if char == '0':
        return And(a, b)
    if char == '1':
        return Or(a, b)
    if char == '2':
        return Xor(a, b)
    if char == '3':
        return Nand(a, b)
    if char == '4':
        return Nor(a, b)
    if char == '5':
        return Xnor(a, b)

def check(selectedRow, gates):
    out = selectedRow[0]
    output = selectedRow[len(selectedRow) - 1]
    
    for i in range(1, len(selectedRow) - 1):
        out = gate(out, selectedRow[i], gates[i - 1])
    
    return out == output


# ## تعریف کروموزوم:
# هر کروموزوم را برابر گیت‌های جواب قرار دادیم. به هر گیت عدد صفر تا پنج را نسبت دادیم. در این مسئله طول هر کروموزوم برابر ۹ است.
# ## جمعیت اولیه:
# جمعیت اولیه را به صورت رندم تولید می‌کنیم. طول جمعیت اولیه را برابر ۲۰۴ (۱۰۲۴ / ۵) قرار دادیم.
# ## عملیات کراس اور:
# سه نقطه را انتخاب می‌کنیم و یکی در میان در آن بازه‌ها پدرها را قرار می‌دهیم.
# ## عملیات میوتیشن:
# با توجه به احتمال تعیین شده برای هر ژن, ژن جایگزین را به صورت رندم انتخاب می‌کنیم.
# ## جلوگیری از سو گیری:
# با توجه به این که ممکن است در ماکسیمم محلی گیر بیفتیم, یا باید تاثیر وزن را بیشتر کنیم که در اینجا اینکار انتخاب شده است به دلیل سرعت بیشتر و یا بر اساس رنک سلکشن را انجام دهیم تا گوناگونی کروموزوم‌ها بیشتر شود.
# ## هایپر پارامترها:
# جمعیت اولیه, انتخاب معیار فیتنس, احتمال کراس اور و میوتیشن, شیوه سلکشن و تعداد جمعیت سلکت شده همگی هایپر پارامترها هستند که در بخش‌های دیگر توضیح داده شدند که به صورت کلی با امتحان و خطا بدست آمده‌اند. ولی به صورت خاص بعضی از آن‌ها مانند احتمال میوتیشن یا کراس اور باید در یک بازهٔ خاص باشند ولی عدد مورد نظر با امتحان و خطا بدست آمده‌است. 

# In[84]:


def initSpace():
    global spaceSize, gateSize
    chromosomes = []
    for i in range(spaceSize):
        chromosome = ''
        for j in range(gateSize):
            rnd = random.randint(0, 5)
            chromosome += str(rnd)
        chromosomes.append(chromosome)
    return chromosomes

def findFitness(chromosomes):
    global tableSize
    global truthTable
    space = {}
    tests = truthTable
    maxFit = 0
    sumFitness = 0
    for i in range(len(chromosomes)):
        fitness = 0
        for test in tests.values:
            if check(test, chromosomes[i]):
                fitness += 1
        space[chromosomes[i]] = fitness / len(tests)
        if fitness > maxFit:
            maxFit = fitness
        sumFitness += fitness
        if fitness == len(tests):
            return chromosomes[i], True
#     print(maxFit, sumFitness / len(chromosomes))
    return space, False


def goalTest(space):
    if 1.0 in space.values():
        return list(s.keys())[list(s.values()).index(1.0)]
    return False


# In[85]:


def selection(space):
    global spaceSize
    keys = list(space.keys())
    fitness = list(space.values())
    sumFitness = sum(fitness)
    w = [i * 100 for i in fitness]

    selectedList = random.choices(keys, k = spaceSize, weights = w)
    return selectedList


# In[86]:


def crossover(parent1, parent2):
    points = np.random.choice([i for i in range(1, gateSize - 2)], 3, replace=False)
    points = np.sort(points)
    child1 = parent1[:points[0]] + parent2[points[0]:points[1]] + parent1[points[1]:points[2]] + parent2[points[2]:]
    child2 = parent2[:points[0]] + parent1[points[0]:points[1]] + parent2[points[1]:points[2]] + parent1[points[2]:]
    return child1, child2

def mutation(child, prob):
    newChild = ''
    for s in child:
        rnd = random.random()
        if rnd <= prob:
            newChild += str(random.randint(0, 5))
        else:
            newChild += s

    return newChild

def convertToGate(goal):
    out = []
    for s in goal:
        if s == '0':
            out.append('AND')
        if s == '1':
            out.append('OR')
        if s == '2':
            out.append('XOR')
        if s == '3':
            out.append('NAND')
        if s == '4':
            out.append('NOR')
        if s == '5':
            out.append('XNOR')
    return out


# In[83]:


truthTable = pd.read_csv('truth_table.csv')
tableSize = truth_table.shape[0]
spaceSize = int(tableSize / 5)
gateSize = truth_table.shape[1] - 2
# sumT = 0
# for j in range(10):
tStart = time.time()
children = initSpace()
while(True):
#         tIn = time.time()
    space, reachGoal = findFitness(children)
    if reachGoal:
        goal = space
        break
    
    selectedList = selection(space)
    children = []
    for i in range(0, len(selectedList), 2):
        rnd = random.random()
        if rnd <= (space[selectedList[i]] + space[selectedList[i + 1]]) / 2:
            child1, child2 = crossover(selectedList[i], selectedList[i + 1])
            children.append(child1)
            children.append(child2)

    for i in range(len(children)):
        prob = 0.01 #(1 / len(children) + 1 / gateSize) / 2
        children[i] = mutation(children[i], prob)
#     tOut = time.time()
#     print('time: %d' %(tOut - tIn))

tFinish = time.time()
t = tFinish - tStart
# sumT += t
print('\nWhole time: %f' %(t))
print(convertToGate(goal))

# print('\nAverage time %f: ' %(sumT / 10))


# میانگین زمان بدست آمدن جواب برابر ۱۷۹ ثانیه است.
# همینطور جواب بدست آمده برابراست با: 
# And, XOR, Or, XNOR, And, Or, Nand, Xnor, Nor

# # سوالات
# ## سوال ۱:
# برای حساب کردن فیتنس, تمام ورودی‌های جدول حالت را چک می‌کنیم و عدد حاصل را تقسیم بر تعداد کل ورودی‌ها می‌کنیم تا عددی بین صفر و یک بدست بیاید. زیرا هرچه ورودی‌های بیشتری چک شوند فیتنس دقیقتر به دست می‌آید. مگر آنکه تعداد ورودی‌ها خیلی زیاد باشد. در این صورت بخشی از آن‌ها را چک می‌کنیم و برای چک کردن حالت پایانی, اگر کروموزومی با فیتنس یک وجود داشت, تمام حالات را برای آن چک می‌کنیم تا از جواب اطمینان حاصل کنیم. 
# ## سوال ۲:
# جمعیت انتخاب شده بر اساس فیتنس است. به این دلیل که کروموزوم‌هایی که احتمال بیشتری دارند با هم پیوند دهند تا به جواب نزدیک شویم.
# ## سوال ۳:
# با استفاده از کراس اور و میوتیشن می‌توان فرزندان جدید تولید کرد به صورتی که به جواب مسئله نزدیکتر شویم. احتمال کراس اور را برابر میانگین فیتنس دو پدر قرار دادیم و احتمال میوتیشن را برای هر ژن برابر یک صدم. (احتمال میوتیشن باید بین یک به روی تعداد کروموزوم‌ها و یک به روی طول کروموزوم‌ها باشد)
# ## سوال ۴:
# این اتفاق ممکن است به دو دلیل رخ دهد: 
# 1. به دلیل ماکسیمم محلی. که برای حل این مشکل می‌توان در مرحله سلکشن چند کروموزوم را به صورت رندم انتخاب کرد.
# 2. ممکن است به جایی برسیم که فیتنس‌های کروموزوم‌های موجود خیلی نزدیک به هم باشند و تمایز چندانی بین آن‌ها قائل نشود. برای حل این مشکل فیتنس‌ها را در یک ضریب نسبتا بزرگی ضرب می‌کنیم تا فاصله فیتنس‌ها و در نتیجه فاصلهٔ وزن آن‌ها در سلکشن زیاد شود.





