with open('provinces.csv') as f:
    content = f.readlines()

content = [x.strip() for x in content]

s = 'prIdToNewId = {'
n = 'prIdToName = {'
o = 'newIdToName = {'
r = 'newIdToPrId = {'
for l in content:
    (provinceId, newProvinceId, provinceName) = l.split(',')
    if provinceId == 'provinceID':
        continue
    s += ' ' + str(provinceId) + ': ' + str(newProvinceId) + ','
    n += ' ' + str(provinceId) + ': \'' + provinceName + '\','
    o += ' ' + str(newProvinceId) + ': \'' + provinceName + '\','
    r += ' ' + str(newProvinceId) + ': ' + str(provinceId) + ','

s = s.rstrip(',') + '}'
n = n.rstrip(',') + '}'
o = o.rstrip(',') + '}'
r = r.rstrip(',') + '}'

print(s)
print(n)
print(o)
print(r)

# ----------------------------------------------------------------------------------------------------------------------

prIdToNewId = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 0, 13: 10, 14: 11, 15: 12,
               16: 13, 17: 14, 18: 15, 19: 16, 20: 26, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5}

prIdToName = {1: 'Cherkasy', 2: 'Chernihiv', 3: 'Chernivtsi', 4: 'Crimea', 5: 'Dnipropetrovsk', 6: 'Donetsk',
              7: 'Ivano-Frankivsk', 8: 'Kharkiv', 9: 'Kherson', 10: 'Khmelnytskyy', 11: 'Kiev', 12: 'KievCity',
              13: 'Kirovohrad', 14: 'Luhansk', 15: 'Lviv', 16: 'Mykolayiv', 17: 'Odessa', 18: 'Poltava', 19: 'Rivne',
              20: 'Sevastopol', 21: 'Sumy', 22: 'Ternopil', 23: 'Transcarpathia', 24: 'Vinnytsya', 25: 'Volyn',
              26: 'Zaporizhzhya', 27: 'Zhytomyr'}

newIdToName = {22: 'Cherkasy', 24: 'Chernihiv', 23: 'Chernivtsi', 25: 'Crimea', 3: 'Dnipropetrovsk', 4: 'Donetsk',
               8: 'Ivano-Frankivsk', 19: 'Kharkiv', 20: 'Kherson', 21: 'Khmelnytskyy', 9: 'Kiev', 0: 'KievCity',
               10: 'Kirovohrad', 11: 'Luhansk', 12: 'Lviv', 13: 'Mykolayiv', 14: 'Odessa', 15: 'Poltava', 16: 'Rivne',
               26: 'Sevastopol', 17: 'Sumy', 18: 'Ternopil', 6: 'Transcarpathia', 1: 'Vinnytsya', 2: 'Volyn',
               7: 'Zaporizhzhya', 5: 'Zhytomyr'}

newIdToPrId = {22: 1, 24: 2, 23: 3, 25: 4, 3: 5, 4: 6, 8: 7, 19: 8, 20: 9, 21: 10, 9: 11, 0: 12, 10: 13, 11: 14, 12: 15,
               13: 16, 14: 17, 15: 18, 16: 19, 26: 20, 17: 21, 18: 22, 6: 23, 1: 24, 2: 25, 7: 26, 5: 27}

