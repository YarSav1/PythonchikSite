from bs4 import BeautifulSoup
import json

from django.shortcuts import render
import requests
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/87.0.4280.88 Safari/537.36',
           'accept': '*/*'}
all_carts = ['http://95.217.194.41:7777/up/world/world/733',
             'http://145.239.134.46:7788/up/world/world/489',
             'http://145.239.134.46:7777/up/world/world/408',
             'http://148.251.76.169:7788/up/world/world/654',
             'http://217.182.201.195:8888/up/world/world/45',
             'http://217.182.201.195:7777/up/world/world/89',
             'http://95.217.194.41:8877/up/world/world/1639137464772',
             'http://51.75.55.87:8877/up/world/world/404',
             'http://51.75.55.87:8878/up/world/world/735',
             'http://217.182.201.210:8888/up/world/world/1639137730077',
             'http://148.251.76.169:8888/up/world/world/1639137861358',
             'http://95.217.194.41:7777/up/world/world/1610494681403'
             ]

urls_md = [
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=0',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=12',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=7',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=20',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=15',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=18',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=38',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=16',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=26',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=17',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=23',
    'https://minecraftonly.ru/engine/scripts/moderators.php?action=showmoders&serverid=13'
]

all_servers = ['Classic',
          'HiTech',
          'HiTech2',
          'Industrial',
          'Divine',
          'Divine2',
          'RPG',
          'TechnoMagic',
          'TechnoMagic2',
          'Pixelmon',
          'GalaxyCraft',
          'HungerGames']


def index(request):
    context = {'name': 'Профиль'}
    return render(request, 'main/index.html', context=context)


def profile(request):
    try:
        if request.GET['code'] is not None:
            user = login(str(request.GET['code']))
            context = {'name': user['username']}
            return render(request, 'main/Profile.html', context=context)
    except:
        pass

    context = {'name': 'Профиль'}
    return render(request, 'main/Profile.html', context=context)


def login(code):
    API_ENDPOINT = 'https://discord.com/api/v8'
    CLIENT_ID = '769936189808967762'
    CLIENT_SECRET = 'IExW_c6ZDSuGU2Y-vKIwf_emwF0MdcDd'
    REDIRECT_URI = 'http://127.0.0.1:8000/profile'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    r.raise_for_status()
    response = r.json()
    access_token = response['access_token']
    response = requests.get('https://discord.com/api/v8/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = response.json()
    print(user)
    return user


def parsing(request):
    context = {'name': 'Профиль'}
    return render(request, 'main/parsing.html', context=context)


def find_player(request):
    context = {'name': 'Профиль'}
    return render(request, 'main/find_player.html', context=context)


def online_server(request):
    context = {'name': 'Профиль', 'servers': all_servers}
    return render(request, 'main/online_server.html', context=context)


def online_player(request):
    context = {'name': 'Профиль'}
    return render(request, 'main/online_player.html', context=context)


def see_online(request):

    index_server = 0
    for i in all_servers:
        if i in request.GET:
            index_server = all_servers.index(i)

    r = requests.get(all_carts[index_server], headers=HEADERS, params=None).text
    html = requests.get(all_carts[index_server], headers=HEADERS, params=None)
    if html.status_code == 200:
        r = json.loads(r)
    else:
        return
    cikl_online = r["currentcount"]
    online = []
    try:
        for i in range(0, cikl_online):
            online.append(r["players"][i]['name'])
    except:
        pass
    html = requests.get(urls_md[index_server], headers=HEADERS, params=None)
    if html.status_code == 200:
        html = html.text
    else:
        return
    soup = BeautifulSoup(html, 'html.parser')
    spis_md = soup.find_all('tr')
    cikl = len(spis_md)
    helpers = []
    moders = []
    curator = []
    headmoder = []
    for i in range(1, cikl):
        moder = soup.find_all('tr')[i]
        moder_name = moder.find_all('td')[1].text
        moder_rank = moder.find_all('td')[2].text
        if moder_rank == 'helper':
            if moder_name in online:
                helpers.append(moder_name)
                online.remove(moder_name)
        elif moder_rank == 'curator':
            if moder_name in online:
                online.remove(moder_name)
                curator.append(moder_name)
        elif moder_rank == 'headmoder':
            if moder_name in online:
                online.remove(moder_name)
                headmoder.append(moder_name)
        else:
            if moder_name in online:
                moders.append(moder_name)
                online.remove(moder_name)
    print(f'{online} \n- md {moders} \n- hd {headmoder} \n- hp {helpers} \n- cur {curator}')
    context = {'name': "Профиль", 'title': f'Онлайн сервера {all_servers[index_server]}', 'all_online': len(online), 'players': online, 'moders': moders,
               'headmoders': headmoder, 'helpers': helpers, 'curator': curator}
    return render(request, 'main/See_online.html', context=context)
