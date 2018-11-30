import urllib.request
import datetime

addressTemplate = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/' \
                  'VH/get_provinceData.php?country=UKR&' \
                  'provinceID=%d&year1=%d&year2=%d&type=%s'


# Mean data for UKR  Province= 1: Cherkasy,  from 1981 to 2018<br>The data below were extracted from weekly files like:
#          ../NPP_VH/4km/ts_L1_v1/ByWeek/VHP_L1_Mean_198201.txt<br><tt><pre>year,week,, provinceID, SMN,SMT,VCI,TCI,VHI
# 1982 01  0.053,260.31, 45.01, 39.46, 42.23                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 1982 02  0.054,262.29, 46.83, 31.75, 39.29                                provinceID,year,week,SMN,SMT,VCI,TCI,VHI <-
# 1982 03  0.055,263.82, 48.13, 27.24, 37.68 -> 1,1982,03,0.055,263.82,48.13,27.24,37.68
# ..........................................
def load_data(province_id, year_from, year_to, data_type):
    print('Load %s of %d from %d to %d' % (data_type, province_id, year_from, year_to))
    address = addressTemplate % (province_id, year_from, year_to, data_type)
    with urllib.request.urlopen(address) as response:
        html = response.read()
    when = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    data_type_file = data_type.replace('_', '-')
    with open('data/%s_%d_%d_%d_%s.txt' % (data_type_file, province_id, year_from, year_to, when), 'w') as fi:
        for b_line in html.splitlines():
            line: str = b_line.decode('ascii')
            if line.find('</pre>') >= 0:
                continue
            if line.find('<pre>') >= 0:
                line = 'provinceID,' + line[line.find('<pre>') + 5:].replace('provinceID, ', '')
            else:
                line = str(province_id) + ',' + line
            line = line.replace(', ', ',').replace('  ', ' ').replace(' ', ',').replace(',,', ',')
            fi.write(line + '\n')


with open('provinces.csv') as f:
    content = f.readlines()

content = [x.strip() for x in content]

for l in content:
    (provinceId, newProvinceId, provinceName) = l.split(',')
    if provinceId == 'provinceID':
        continue
    load_data(int(provinceId), 2000, 2018, 'Mean')
    load_data(int(provinceId), 2000, 2018, 'VHI_Parea')
