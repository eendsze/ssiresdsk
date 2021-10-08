import math

#kis hajo
Hajomodell1 = {
    "M": [2.0, 4.4, 0.04],
    "D": [2.7, 13.4, 0.156],
    "Af": [1.7, 1.8, 1.6],
    'kw': 0.2, # ezzel szorozza be a sebessegbol eredo forgato erot. A kormanylapat hatasara 0, kis negativ szam lesz
    "length": 0.4,
    'offset': 0, #ennyivel van hatrabb a forgaspont a hajo kozepetol, csak a megjeleniteshez kell
    "zoom": 1000,
    'orrL': 0.16, #orrkormany tavolsaga a hajo forgaspontjatol
    'orrF': 0.3,
    'farL': 0.16,
    'farF': 0.3,
    'motL': 0.1, # propellerek tavolsaga egymastol
    'motF': 2, #ez 200%-os is lehet egyelore
    'tauT': 0.1, # thrusterek idoallandoja, kb.
    'tauM': 0.1 # motorok idoallandoja
}
Hajomodell1Becs = {
    "M": [2.0, 4.4, 0.04],
    "D": [1, 3, 0.04],
    "length": 0.4,
    'offset': 0, #ennyivel van hatrabb a forgaspont a hajo kozepetol, csak a megjeleniteshez kell
    "zoom": 100,
    'orrL': 0.16, #orrkormany tavolsaga a hajo forgaspontjatol
    'orrF': 0.3,
    'farL': 0.16,
    'farF': 0.3,
    'motL': 0.1, # propellerek tavolsaga egymastol
    'motF': 2, #ez 200%-os is lehet egyelore
    'tauT': 0.1, # thrusterek idoallandoja, kb.
    'tauM': 0.1, # motorok idoallandoja
    'tauFilt': 2, # a modell es a GPS mix idoallandoja
    'tauSzab': 0.3, # ez a PID-ek szabalyzasi frekvenciaja, a szabalyzs sebessege (1/tau)
    # ide jon meg a sebessegek maximuma, amit a szabalyzas megenged.
    'speedX': 0.3,
    'speedY': 0.15,
    'speedZ': 0.5
}

#Nagy hajo modellje
Hajomodell2 = {
    "M": [12.6, 20, 1.7],
    "D": [2, 20, 0.1],
    "Af": [1.7, 1.8, 1.6],
    'kw': 0.2, # ezzel szorozza be a sebessegbol eredo forgato erot. A kormanylapat hatasara 0, kis negativ szam lesz
    "length": 1.4,
    'offset': 0.1, #ennyivel van hatrabb a forgaspont a hajo kozepetol, csak a megjeleniteshez kell
    "zoom": 200,
    'orrL': 0.43, #orrkormany tavolsaga a hajo forgaspontjatol
    'orrF': 0.95,
    'farL': 0.265,
    'farF': 0.95,
    'motL': 0.18, # propellerek tavolsaga egymastol
    'motF': 2, #ez 200%-os is lehet egyelore
    'tauT': 0.1, # thrusterek idoallandoja, kb.
    'tauM': 0.1 # motorok idoallandoja
}
Hajomodell2Becs = {
    "M": [12, 18, 1.7],
    "D": [1, 5, 0.1],
    "length": 1.4,
    'offset': 0.1, #ennyivel van hatrabb a forgaspont a hajo kozepetol, csak a megjeleniteshez kell
    "zoom": 200,
    'orrL': 0.43, #orrkormany tavolsaga a hajo forgaspontjatol
    'orrF': 0.95,
    'farL': 0.265,
    'farF': 0.95,
    'motL': 0.12, # propellerek tavolsaga egymastol
    'motF': 2, #ez 200%-os is lehet egyelore
    'tauT': 0.1, # thrusterek idoallandoja, kb.
    'tauM': 0.1, # motorok idoallandoja
    'tauFilt': 2, # a modell es a GPS mix idoallandoja
    'tauSzab': 0.3, # ez a PID-ek szabalyzasi frekvenciaja, a szabalyzs sebessege (1/tau)
    # ide jon meg a sebessegek maximuma, amit a szabalyzas megenged.
    'speedX': 0.3,
    'speedY': 0.15,
    'speedZ': 0.3
}


Nagyhajo445_modell = {
    #"M": [12600, 28900, 170000],
    "M": [12600, 18000, 170000],
    "D": [200, 2000, 200000],
    "Af": [1.7, 2.0, 1.6],
    #"Af": [1, 1, 1],
    'kw': 0.2, # ezzel szorozza be a sebessegbol eredo forgato erot. A kormanylapat hatasara 0, kis negativ szam lesz
    "length": 13,
    'offset': 1.0, #ennyivel van hatrabb a forgaspont a hajo kozepetol, csak a megjeleniteshez kell
    "zoom": 25,
    'orrL': 5, #orrkormany tavolsaga a hajo forgaspontjatol
    'orrF': 950,
    'farL': 3,
    'farF': 950,
    'motL': 2.2, # propellerek tavolsaga egymastol
    'motF': 1500, #ez 200%-os is lehet, max az ero felet szabad megadni
    'tauT': 0.5, # thrusterek idoallandoja, kb.
    'tauM': 0.5 # motorok idoallandoja
}

Nagyhajo445_becsles = {
    "M": [12000, 20000, 200000],
    "D": [200, 2000, 200000],
    'orrL': 5, #orrkormany tavolsaga a hajo forgaspontjatol
    'orrF': 950,
    'farL': 3,
    'farF': 950,
    'motL': 2.2, # propellerek tavolsaga egymastol
    'motF': 1500, #ez 200%-os is lehet, max az ero felet szabad megadni
    'tauT': 0.8, # thrusterek idoallandoja, kb.
    'tauM': 0.8, # motorok idoallandoja
    'tauFilt': 4, # a modell es a GPS mix idoallandoja
    'tauSzab': 1, # ez a PID-ek szabalyzasi frekvenciaja, a szabalyzs sebessege (1/tau)
    # ide jon meg a sebessegek maximuma, amit a szabalyzas megenged.
    'speedX': 1,
    'speedY': 0.5,
    'speedZ': 0.1
}


Kornyezet1 = {
    'hullamszog': math.pi/2, # az erok ebben az iranyban hatnak
    'Fkornyezet': 1000, # ez az allando ero tag, kb a szel hatasa, ha oldalraol kapja
    'Fhullam': 2000, # ez a hullamzasi ero amplitudoja ha oldalrol kapja
    'Whullam': 1.0, # ez a hullamzas szogfrekvenciaja, radian/sec
    'Khatulrol': 0.25 # hosszaban ekkora aranyu lesz az ero. Marmint ha a hajot hosszaban eri
}
KornyezetCsendes = {
    'hullamszog': math.pi/2, # az erok ebben az iranyban hatnak
    'Fkornyezet': 0.2, # ez az allando ero tag, kb a szel hatasa, ha oldalraol kapja
    'Fhullam': 1, # ez a hullamzasi ero amplitudoja ha oldalrol kapja
    'Whullam': 3.0, # ez a hullamzas szogfrekvenciaja, radian/sec
    'Khatulrol': 0.25 # hosszaban ekkora aranyu lesz az ero. Marmint ha a hajot hosszaban eri
}