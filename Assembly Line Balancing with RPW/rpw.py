# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.read_excel("/content/sawyer_30.xlsx")
oncelik_df = pd.read_excel("/content/oncelikler.xlsx")

new_df = oncelik_df["Oncelik"].str.split(",", n = 1, expand = True)
new_df[0] = pd.to_numeric(new_df[0])
new_df[1] = pd.to_numeric(new_df[1])
arr = new_df.to_numpy()

liste = df['İş Elemanı'].tolist()

df['İşlem Süresi'] = df['İşlem Süresi'].astype(int)

# Grafı oluşturalım
graph = {}
for node in arr:
  if node[0] not in graph:
    graph[node[0]] = [node[1]]
  else:
    graph[node[0]].append(node[1])

# 1 numaralı noktadan ilerleyen yolları bulalım
def find_paths(graph, start, path=[]):
  path = path + [start]
  if start not in graph:
    return [path]
  paths = []
  for node in graph[start]:
    if node not in path:
      new_paths = find_paths(graph, node, path)
      for p in new_paths:
        paths.append(p)
  return paths

paths = find_paths(graph, 1)
print(paths)

result = []
for l in paths:
    result.extend(l)

result = list(set(result))
result.sort()

print(result) 
print(graph)

nodes = df['İş Elemanı'].tolist()
ardıl_listesi = []
ardıl_listesi_son = []
for node in nodes:
  paths = find_paths(graph, node)
  result = []
  for l in paths:
      result.extend(l)

  result = list(set(result))
  result.sort()
  ardıl_listesi += [f"{node} numaralı noktadan ilerleyen yollar: {result}"]
  ardıl_listesi_son += [result]

ardıl_listesi

j = 0

pw_list = []
while j < len(ardıl_listesi_son):
  pw_sum = 0
  for i in ardıl_listesi_son[j]:
      pw_sum += df.iloc[i-1][1]
  pw_list += [pw_sum]
  j+=1

sozluk = {}
for key in nodes:
    for value in pw_list:
        sozluk[key] = value
        pw_list.remove(value)
        break

sirali_sozluk = sorted(sozluk.items(), key=lambda x:x[1], reverse=True)
sirali_sozluk = dict(sirali_sozluk)

df_dict = df.set_index('İş Elemanı').to_dict()['İşlem Süresi']
shadow_dict = df_dict.copy()

j = 1
C_list = []
while len(df_dict) > 0:
  C = 30
  for i in sirali_sozluk:
    if i in df_dict:
      C-=df_dict[i]
      del df_dict[i]
      if C < 0:
        df_dict[i] = shadow_dict[i]
        break
      print(i,'.İş Elemanı',j,'.istasyona atandı','---->','Kalan Çevrim Süresi:',C)
      C_list += [C]
      istasyonsayisi=j
  print('---------------------')
  C_list += [C]
 
  j+=1

idle_time = []
i = 0
while i < len(C_list):
  if C_list[i] < 0:
    idle_time += [C_list[i-1]]
    
  i+=1
  
idle_time += [C_list[-1:][0]]

print('Toplam Boş Zaman: ',sum(idle_time))

"""DENGE GECİKMESİ

"""

C = 30
denge_gecikmesi = (100*sum(idle_time)) / (C * istasyonsayisi)

print('Denge Gecikmesi: %',denge_gecikmesi)

"""HAT ETKİNLİĞİ"""

C = 30
hat_etkinligi = (100*((C * istasyonsayisi)-sum(idle_time))) / (C * istasyonsayisi)

print('Hat Etkinliği: %',hat_etkinligi)

"""DÜZGÜNLÜK İNDEKSİ"""

C = 30 
squares = 0
import math
for i in idle_time:
  squares += (C-i)*(C-i)

S_I_ = math.sqrt(squares)

print('Düzgünlük İndeksi: ', S_I_)