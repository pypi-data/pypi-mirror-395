"""Glavne komande prilagođene srpskom jeziku i dodatne funkcije za unos podataka."""

def ispiši(*args, **kwargs):
    """Prilagođena funkcija za ispis koja obavija ugrađenu funkciju print"""
    print(*args, **kwargs)

def input_broj(*args, **kwargs):
    """Prilagođena funkcija za unos broja koja obavija ugrađenu funkciju int(input())"""
    return int(input(*args, **kwargs))

def input_tekst(*args, **kwargs):
    """Prilagođena funkcija za unos teksta koja obavija ugrađenu funkciju input()"""
    return input(*args, **kwargs)

def unos_lista_sa_razmacima(*args, **kwargs):
    """Prilagođena funkcija za unos liste sa razmacima koja obavija ugrađenu funkciju input() i split()"""
    return input(*args, **kwargs).split()

def unos_tuple_sa_razmacima(*args, **kwargs):
    """Prilagođena funkcija za unos tuple sa razmacima koja obavija ugrađenu funkciju input() i split()"""
    return tuple(input(*args, **kwargs).split())

def unos_set_sa_razmacima(*args, **kwargs):
    """Prilagođena funkcija za unos seta sa razmacima koja obavija ugrađenu funkciju input() i split()"""
    return set(input(*args, **kwargs).split())

def unos_dict_sa_razmacima(*args, **kwargs):
    """Prilagođena funkcija za unos dict sa razmacima koja obavija ugrađenu funkciju input() i split()"""
    unos = input(*args, **kwargs).split()
    rezultat = {}
    for par in unos:
        ključ, vrednost = par.split(':')
        rezultat[ključ] = vrednost
    return rezultat

def da_li_je_pyinstaller():
    """Proverava da li je program pokrenut putem PyInstaller-a"""
    import sys
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

"""

More coming soon...

Još dolazi uskoro...

"""