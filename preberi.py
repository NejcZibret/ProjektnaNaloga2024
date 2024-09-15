import re

# Vzorec za posamezen blok smučišča
vzorec_bloka = re.compile(
    r'<div class="panel panel-default resort-list-item resort-list-item-image--big"'  # Začetek bloka smučišča
    r'.*?'
    r'</div>\s*</div>\s*</div>',  # Konec bloka smučišča
    flags=re.DOTALL
)

with open('html_prva_stran', 'r', encoding='utf-8') as f:
    stran = f.read()
    

def prestej_ponovitve(vsebina):
    # Poiščem vsa ujemanja z uporabo findall
    ujemanja = vzorec_bloka.findall(vsebina) # Preštejem število ujemanj, mi jih da v seznam
    stevec = len(ujemanja)
    return stevec

# Preverim, ali imam prav
stevilo_blokov = prestej_ponovitve(stran)
print(f"Število smučišč: {stevilo_blokov}")
    
        
