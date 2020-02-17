"""
Script for gathering Pokemon sprite images from 1st to 4th Pokemon generation from www.pokebip.com
"""

import urllib.request
import time
import sys

sprite_root = "https://www.pokebip.com/pokedex/images/gen4_general/"
last_sprite = 493  # number of pokemon from 1st to 4th generation

output_dir = "Sprites/"
delay = 1   # waiting time before each http request

for i in range(1, last_sprite + 1):
    url = sprite_root + str(i) + ".png"

    print(str(i) + " / " + str(last_sprite), file=sys.stderr)
    (filename, headers) = urllib.request.urlretrieve(url, filename=output_dir + str(i) + ".png")

    # don't spam the server !
    time.sleep(delay)

print("Done !")
