import re

# Definirajte vaš vzorec
vzorec_bloka = re.compile(
    r'<div class="panel panel-default resort-list-item resort-list-item-image--big"'
    r'.*?'
    r'<div class=".*?"><a class=".*?"\s*href=".*?">\s*Details\s*</a>\s*</div>\s*</div>\s*</div>',
    flags=re.DOTALL
)

# Preberite HTML datoteko
with open('smucisca.html', 'r', encoding='utf-8') as f:
    stran = f.read()

# Poiščite vse bloke
bloki = vzorec_bloka.findall(stran)

# Izpišite rezultate
print(f"Število najdenih blokov: {len(bloki)}")

