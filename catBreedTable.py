import csv
from bs4 import BeautifulSoup


html = file("""C:\Users\Joseph\Documents\Kaggle\Shelter Animals\CatLifeSpansTable.html""")
soup = BeautifulSoup(html, 'html5lib')

output_cols = ['breed', 'life_span_low',
            'life_span_high']
with open('cat_breed_info.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(output_cols)
    rows = soup.table.find_all('tr')[1:]
    for row in rows:
        cat = {'breed': row.find_all('td')[0].text.replace('\n', '')}
        age_field = row.find_all('td')[1].text.replace('\n', '')
        if '-' in age_field:
            cat['life_span_low'], cat['life_span_high'] = age_field.split('-')
        elif '~' in age_field:
            cat['life_span_low'] = cat['life_span_high'] = age_field.replace('~', '')
        elif '+' in age_field:
            cat['life_span_low'], cat['life_span_high'] = age_field.replace('+', ''), '25'
            # 25 is chosen arbitrarily, oldest cat in data is 20, oldest cat ever was 38
        csvwriter.writerow([cat[col] for col in output_cols])

