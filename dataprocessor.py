import pandas as pd

# Дикт для замены сгенерирован на основе provinces.csv при помощи скрипта generate_dict_prid.py
prIdToNewId = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 0, 13: 10, 14: 11, 15: 12,
               16: 13, 17: 14, 18: 15, 19: 16, 20: 26, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5}


# Зчитати завантажені текстові файли у фрейм
# У нас datamerger уже склеил все данные в один файл, который и загружаем
def read_data(path):
    return pd.read_csv(path, index_col=False, header=0)


# Реалізувати процедуру, яка змінить індекси областей, які використані на порталі NOAA
# Выполняет замену в датафреймах при помощи выше описаного дикта в колонке provinceID
def replace_indices(dataframe):
    dataframe['provinceID'] = dataframe['provinceID'].map(prIdToNewId)


# Ряд VHI для області за рік
def province_vhi_year(dataframe, province_id, year):
    return dataframe[(dataframe['year'] == year) & (dataframe['provinceID'] == province_id)][['week', 'VHI']]


# пошук екстремумів (min та max)
# возвращает номер недели где произошел соответствующий экстремум
def pvy_min_week(pvy_data):
    return pvy_data.loc[pvy_data['VHI'].idxmin()]['week']


def pvy_max_week(pvy_data):
    return pvy_data.loc[pvy_data['VHI'].idxmax()]['week']


# Ряд VHI за всі роки для області
def province_vhi_allyears(dataframe, province_id):
    return dataframe[(dataframe['provinceID'] == province_id)]


# Внутренняя функция группировки найденых результатов по годам
def pfd_grouper(found):
    return found['year'].value_counts().sort_index().to_dict()


# виявити роки з екстремальними посухами, які торкнулися більше вказаного відсотка області
def province_find_droughts_extreme(pvay_data, pct_threshold):  # < 15
    found = pvay_data[(pvay_data['0'] + pvay_data['5'] + pvay_data['10'] >= pct_threshold)]
    return pfd_grouper(found)


# Аналогічно для помірних посух
def province_find_droughts_moderate(pvay_data, pct_threshold):  # < 35
    found = pvay_data[(pvay_data['0'] + pvay_data['5'] + pvay_data['10'] + pvay_data['15'] + pvay_data['20'] +
                       pvay_data['25'] + pvay_data['30'] >= pct_threshold)]
    return pfd_grouper(found)


# provinceID,year,week,SMN,SMT,VCI,TCI,VHI,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100
df = read_data('data_massive.csv')
replace_indices(df)  # Заменяем индексы с NOAA на те которые хотят в лабке

print('Provice VHI data for year:')
pvy = province_vhi_year(df, 9, 2010)
print(pvy)
print('Min VHI observed at week:', pvy_min_week(pvy))
print('Max VHI observed at week:', pvy_max_week(pvy))

pvay = province_vhi_allyears(df, 9)
print('Province VHI data for all years:')
print(pvay)
years_extreme = province_find_droughts_extreme(pvay, 30)
years_moderate = province_find_droughts_moderate(pvay, 50)
print('Years with weeks with extreme  droughts >= 30%:', years_extreme)
print('Years with weeks with modarate droughts >= 50%:', years_moderate)
