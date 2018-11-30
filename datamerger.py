import pandas as pd
import os


# Зчитати завантажені текстові файли у фрейм
# Ця задача має бути реалізована у вигляді окремої процедури, яка на вхід приймає шлях до директорії,
#   в якій зберігаються файли
def read_frames(dir_name):
    dataframes = []
    for file in os.listdir(dir_name):
        # index: (provinceID,year,week)
        # data (Mean)  : SMN,SMT,VCI,TCI,VHI
        # data (VHI-P) : 0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100
        df = pd.read_csv(dir_name + '/' + file, index_col=(0, 1, 2), header=0)
        dataframes.append(df)
    return dataframes


# Обьединение фреймов с разными данными и одним индексом (горизонтальная)
# Обьединяет Mean + VHI-Parea по конкретным областям (одной области)
# number - количество областей, offset - сдвиг в папке между данными разных типов, key - колонки, по которым склейка
def combine_frames(dataframes, number, offset, key):
    combined_dataframes = []
    for i in range(0, number):
        combined_dataframes.append(pd.merge(dataframes[i], dataframes[offset+i], on=key))
    return combined_dataframes


# Склейка обьединенных фреймов (конкатенация, вертикальная)
# Склеивает фреймы по разным областям в один большой набор данных
def merge_frames(combined_dataframes):
    merged_dataframes = pd.concat(combined_dataframes)
    merged_dataframes.sort_index(inplace=True)
    return merged_dataframes


# Загрузка данных с папки data
dfs = read_frames('data')

# Обьединение фреймов данных по 27 областям (с KievCity и Sevastopol) по ключу
cdfs = combine_frames(dfs, 27, 27, ['provinceID', 'year', 'week'])

# Склейка обьединенных фреймов в большой набор данных
merged = merge_frames(cdfs)

# Запись результирующего набора данных в файл data_massive.csv
merged.to_csv('data_massive.csv')
