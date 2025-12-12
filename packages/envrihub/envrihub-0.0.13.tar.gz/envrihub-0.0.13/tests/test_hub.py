'''Testing the Hub class'''

from envrihub import Hub

def test_geo_search():
    geography = 'POLYGON((10.703125000000004 48.345191092562935,28.984375000000004 48.345191092562935,28.984375000000004 36.17766212248528,10.703125000000004 36.17766212248528,10.703125000000004 48.345191092562935))'
    hub = Hub()
    assert len(list(hub.search_catalogue(geography = geography)))>0, 'Geographic search from the Hub does not work'

def test_search_all():
    hub = Hub()
    assert len(list(hub.search_catalogue()))>0, 'Generic search from the Hub does not work'

def test_vermullen_exception():
    hub = Hub()
    file_list = []
    for res in hub.search_catalogue():
        if res.is_downloadable():
            file_list.append(res)
            print(res.title)
    assert len(file_list)>0, 'No downloadable assets...'