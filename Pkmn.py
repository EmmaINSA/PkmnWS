"""
Script for gathering Pokemon data from the complete Pokedex of www.pokepedia.fr

Data gathered for each Pokemon of the Pokedex:
    - Pokedex number
    - French name
    - French type(s)

Output format (text file):
<number> : <name> | <type1>[, <type2>]
"""

import requests
import sys
from bs4 import BeautifulSoup


# returns True if the given tag is a relevant <table>
def isPkmnTable(tag):
    return tag.name == "table" and tag.has_attr('class') and (tag['class'] == tableClass or tag['class'] == tableClass2)


output_path = "Pkmn.txt"
encoding = "UTF-8"

# values of 'class' attributes of <table> tags that are relevant
tableClass = ['tableaustandard', 'sortable']
tableClass2 = ['tableaustandard', 'centre', 'sortable']
# main page from which data is gathered
source = "https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_dans_l%27ordre_du_Pok%C3%A9dex_National"

# ---- EXECUTION ----

# output file
out = open(output_path, mode="w", encoding=encoding)

response = requests.get(source)

if (response.status_code == 200):
    print("Connection successful, initiating parsing...\n", file=sys.stderr)

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all(isPkmnTable)

    for table in tables:
        tbody = table.tbody
        trs = tbody.find_all('tr')

        for tr in trs[1:]:  # do not parse headers
            tds = tr.find_all('td')
            try:
                line = tds[0].string.strip() + " : " + tds[2].a.string.strip() + ' | '
                aes = tds[6].find_all('a')

                for a in aes[:-1]:
                    line += a['title'][:-7] + ", "

                line += aes[-1]['title'][:-7] + "\n"

                # output
                print(line, end="")
                out.write(line)

            except AttributeError as e:
                pass

else:
    raise Exception("Could not access distant file.")

out.close()
print("Successfully gathered and parsed data into " + output_path, file=sys.stderr)
