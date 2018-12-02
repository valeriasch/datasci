from spyre import server
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


class VisualizerApp(server.App):
    title = "Data Visualizer"

    provinces = pd.read_csv("provinces.csv", header=0)
    provinces.sort_values('newProvinceID', inplace=True)
    province_options = [{'label': "(" + str(row['newProvinceID']) + ") " + row['province_name'],
                         'value': row['newProvinceID']} for index, row in provinces.iterrows()]

    inputs = [{
        "type": 'dropdown',
        "label": 'Series',
        "options": [
            {"label": "Vegetation Condition Index", "value": "VCI"},
            {"label": "Thermal Condition Index", "value": "TCI"},
            {"label": "Vegetation Health Index", "value": "VHI"}
        ],
        "value": 'VHI',
        "key": 'series',
        "action_id": "update_data"
    }, {
        "type": 'dropdown',
        "label": 'Province',
        "options": province_options,
        "value": '9',
        "key": 'province',
        "action_id": "update_data"
    }, {
        "type": 'slider',
        "label": 'Week from',
        "value": 1,
        "min": 1,
        "max": 52,
        "key": 'week_from',
        "action_id": "update_data"
    }, {
        "type": 'slider',
        "label": 'Week to',
        "value": 52,
        "min": 1,
        "max": 52,
        "key": 'week_to',
        "action_id": "update_data"
    }, {
        "type": 'slider',
        "label": 'Year from',
        "value": 2000,
        "min": 2000,
        "max": 2018,
        "key": 'year_from',
        "action_id": "update_data"
    }, {
        "type": 'slider',
        "label": 'Year to',
        "value": 2018,
        "min": 2000,
        "max": 2018,
        "key": 'year_to',
        "action_id": "update_data"
    }]

    controls = [{
        "type": "hidden",
        "id": "update_data"
    }]

    tabs = ["Plot", "Table"]

    outputs = [{
        "type": "plot",
        "id": "plot",
        "control_id": "update_data",
        "tab": "Plot"
    }, {
        "type": "table",
        "id": "table_id",
        "control_id": "update_data",
        "tab": "Table",
        "on_page_load": True
    }]

    def getData(self, params):
        series = params['series']
        province = int(params['province'])
        week_from = int(params['week_from'])
        week_to = int(params['week_to'])
        year_from = int(params['year_from'])
        year_to = int(params['year_to'])

        data_frame = read_data('data_massive.csv')
        replace_indices(data_frame)
        result_frame = data_frame.loc[(data_frame['provinceID'] == province)
                                      & (data_frame['week'] >= week_from)
                                      & (data_frame['week'] <= week_to)
                                      & (data_frame['year'] >= year_from)
                                      & (data_frame['year'] <= year_to),
                                      ['year', 'week', series]]
        return result_frame

    def getPlot(self, params):
        series = params['series']
        province = int(params['province'])
        week_from = int(params['week_from'])
        week_to = int(params['week_to'])
        year_from = int(params['year_from'])
        year_to = int(params['year_to'])

        # Define province_name by province id:
        province_name = self.provinces.loc[(self.provinces['newProvinceID'] == province)].iat[0, 2]

        df = self.getData(params)
        plt_obj = df.set_index(['year', 'week']).plot(figsize=(20, 10), grid=True)
        plt_obj.set_ylabel(series)
        plt_obj.set_xlabel('Year')
        plt_obj.set_title(province_name)
        plt_obj.set_yticks(range(0, 101, 10))
        plt_obj.set_yticks(range(0, 101, 5), minor=True)
        plt_obj.set_xticks(range(0, (year_to - year_from + 1) * (week_to - week_from + 1), (week_to - week_from + 1)))
        # plt_obj.set_xticks(range(0, (year_to - year_from + 1) * (week_to - week_from + 1), 1), minor=True)
        plt_obj.set_xticklabels(range(year_from, year_to + 1))
        fig = plt_obj.get_figure()
        return fig


app = VisualizerApp()
app.launch(port=8042)  # http://127.0.0.1:8042
