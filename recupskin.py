import requests
from PIL import Image

def recupskin(pseudo):
    try:
        uuid=requests.get(f"https://playerdb.co/api/player/minecraft/{pseudo}").json()['data']['player']['id']
        open('skin/skin.png', 'wb').write(requests.get(f"https://visage.surgeplay.com/frontfull/{uuid}").content)
        skin=Image.open('skin/skin.png')
        coords={
            'tete':(46,0,46+66,66),
            'bg':(22,66,22+24,66+95),
            'buste':(46,66,46+66,66+95),
            'bd':(46+66,66,46+66+24,66+95),
            'jg':(46,66+95,46+33,66+95+95),
            'jd':(46+33,66+95,46+66,66+95+95)
        }
        i=0
        for k in coords.keys():
            cropped=skin.crop(coords[k])
            cropped.save(f"skin/part{i}.png")
            i+=1
        return True
    except Exception as err:
        return False#,str(err)