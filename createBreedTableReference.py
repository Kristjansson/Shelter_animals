import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import time

def floats_from_elm(elm):
    return tuple([float(token) for token in elm.text.replace(u'\xa0', ' ').split(' ') if token.replace('.','',1).isdecimal()])

html = requests.get("""http://www.vetstreet.com/dogs/breeds#all-breeds""").text
soup = BeautifulSoup(html, 'html5lib')

breed_to_url = [{'breed': elm.text, 'url': elm.a['href']}
                for list_section in soup.find(id="""breed-links""").find_all('ul')
                for elm in list_section.find_all('li')]

DOMAIN_NAME = """http://www.vetstreet.com"""

# dog_data = []

output_cols = ['breed', 'breed_group', 'height_low', 'height_high', 'weight_low', 'weight_high', 'life_span_low',
               'life_span_high']
with open('dog_breed_info.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(output_cols)

    for dog in breed_to_url:
        soup = BeautifulSoup(requests.get(DOMAIN_NAME + dog['url']).text, 'html5lib')
        physical_info = soup.find(id='breed-detail').ul.find_all('li')

        dog_datum = {'breed': dog['breed']}

        for elm in physical_info:
            field = elm.span.text.split(':')[0]
            if field == 'Breed Group':
                dog_datum['breed_group'] = elm.a.text
            numeric_fields = ['Height', 'Weight', 'Life Span']
            for nf in numeric_fields:
                if field == nf:
                    col_name = nf.lower().replace(' ', '_')
                    try:
                        dog_datum[col_name + '_low'], dog_datum[col_name + '_high'] = floats_from_elm(elm)
                        errors = False
                    except ValueError:
                        dog_datum[col_name + '_low'], dog_datum[col_name + '_high'] = ('', '')
                        errors = True
        # dog_data.append(dog_datum)

        # Write to csv for each completed dog
        csvwriter.writerow([dog_datum[col] for col in output_cols])

        # Update User
        print 'Completed: ' + dog['breed'] + (' with ' if errors else ' without ') + 'errors'

        # Rate Limit to be a nice crawler.
        time.sleep(5)


