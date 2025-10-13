"""
Pokemon Data Module
===================

Contiene información estática de Pokemon necesaria para feature engineering:
- Tipos de Pokemon
- Base Stats Totals (BST)
- Efectividad de tipos
- Tiers competitivos

Fuente: Pokemon Showdown / Smogon University
"""

# Efectividad de tipos (multiplicadores de daño)
# Formato: (tipo_atacante, tipo_defensor): multiplicador
TYPE_EFFECTIVENESS = {
    # Normal
    ('Normal', 'Rock'): 0.5,
    ('Normal', 'Ghost'): 0.0,
    ('Normal', 'Steel'): 0.5,
    
    # Fire
    ('Fire', 'Fire'): 0.5,
    ('Fire', 'Water'): 0.5,
    ('Fire', 'Grass'): 2.0,
    ('Fire', 'Ice'): 2.0,
    ('Fire', 'Bug'): 2.0,
    ('Fire', 'Rock'): 0.5,
    ('Fire', 'Dragon'): 0.5,
    ('Fire', 'Steel'): 2.0,
    
    # Water
    ('Water', 'Fire'): 2.0,
    ('Water', 'Water'): 0.5,
    ('Water', 'Grass'): 0.5,
    ('Water', 'Ground'): 2.0,
    ('Water', 'Rock'): 2.0,
    ('Water', 'Dragon'): 0.5,
    
    # Electric
    ('Electric', 'Water'): 2.0,
    ('Electric', 'Electric'): 0.5,
    ('Electric', 'Grass'): 0.5,
    ('Electric', 'Ground'): 0.0,
    ('Electric', 'Flying'): 2.0,
    ('Electric', 'Dragon'): 0.5,
    
    # Grass
    ('Grass', 'Fire'): 0.5,
    ('Grass', 'Water'): 2.0,
    ('Grass', 'Grass'): 0.5,
    ('Grass', 'Poison'): 0.5,
    ('Grass', 'Ground'): 2.0,
    ('Grass', 'Flying'): 0.5,
    ('Grass', 'Bug'): 0.5,
    ('Grass', 'Rock'): 2.0,
    ('Grass', 'Dragon'): 0.5,
    ('Grass', 'Steel'): 0.5,
    
    # Ice
    ('Ice', 'Fire'): 0.5,
    ('Ice', 'Water'): 0.5,
    ('Ice', 'Grass'): 2.0,
    ('Ice', 'Ice'): 0.5,
    ('Ice', 'Ground'): 2.0,
    ('Ice', 'Flying'): 2.0,
    ('Ice', 'Dragon'): 2.0,
    ('Ice', 'Steel'): 0.5,
    
    # Fighting
    ('Fighting', 'Normal'): 2.0,
    ('Fighting', 'Ice'): 2.0,
    ('Fighting', 'Poison'): 0.5,
    ('Fighting', 'Flying'): 0.5,
    ('Fighting', 'Psychic'): 0.5,
    ('Fighting', 'Bug'): 0.5,
    ('Fighting', 'Rock'): 2.0,
    ('Fighting', 'Ghost'): 0.0,
    ('Fighting', 'Dark'): 2.0,
    ('Fighting', 'Steel'): 2.0,
    ('Fighting', 'Fairy'): 0.5,
    
    # Poison
    ('Poison', 'Grass'): 2.0,
    ('Poison', 'Poison'): 0.5,
    ('Poison', 'Ground'): 0.5,
    ('Poison', 'Rock'): 0.5,
    ('Poison', 'Ghost'): 0.5,
    ('Poison', 'Steel'): 0.0,
    ('Poison', 'Fairy'): 2.0,
    
    # Ground
    ('Ground', 'Fire'): 2.0,
    ('Ground', 'Electric'): 2.0,
    ('Ground', 'Grass'): 0.5,
    ('Ground', 'Poison'): 2.0,
    ('Ground', 'Flying'): 0.0,
    ('Ground', 'Bug'): 0.5,
    ('Ground', 'Rock'): 2.0,
    ('Ground', 'Steel'): 2.0,
    
    # Flying
    ('Flying', 'Electric'): 0.5,
    ('Flying', 'Grass'): 2.0,
    ('Flying', 'Fighting'): 2.0,
    ('Flying', 'Bug'): 2.0,
    ('Flying', 'Rock'): 0.5,
    ('Flying', 'Steel'): 0.5,
    
    # Psychic
    ('Psychic', 'Fighting'): 2.0,
    ('Psychic', 'Poison'): 2.0,
    ('Psychic', 'Psychic'): 0.5,
    ('Psychic', 'Dark'): 0.0,
    ('Psychic', 'Steel'): 0.5,
    
    # Bug
    ('Bug', 'Fire'): 0.5,
    ('Bug', 'Grass'): 2.0,
    ('Bug', 'Fighting'): 0.5,
    ('Bug', 'Poison'): 0.5,
    ('Bug', 'Flying'): 0.5,
    ('Bug', 'Psychic'): 2.0,
    ('Bug', 'Ghost'): 0.5,
    ('Bug', 'Dark'): 2.0,
    ('Bug', 'Steel'): 0.5,
    ('Bug', 'Fairy'): 0.5,
    
    # Rock
    ('Rock', 'Fire'): 2.0,
    ('Rock', 'Ice'): 2.0,
    ('Rock', 'Fighting'): 0.5,
    ('Rock', 'Ground'): 0.5,
    ('Rock', 'Flying'): 2.0,
    ('Rock', 'Bug'): 2.0,
    ('Rock', 'Steel'): 0.5,
    
    # Ghost
    ('Ghost', 'Normal'): 0.0,
    ('Ghost', 'Psychic'): 2.0,
    ('Ghost', 'Ghost'): 2.0,
    ('Ghost', 'Dark'): 0.5,
    
    # Dragon
    ('Dragon', 'Dragon'): 2.0,
    ('Dragon', 'Steel'): 0.5,
    ('Dragon', 'Fairy'): 0.0,
    
    # Dark
    ('Dark', 'Fighting'): 0.5,
    ('Dark', 'Psychic'): 2.0,
    ('Dark', 'Ghost'): 2.0,
    ('Dark', 'Dark'): 0.5,
    ('Dark', 'Fairy'): 0.5,
    
    # Steel
    ('Steel', 'Fire'): 0.5,
    ('Steel', 'Water'): 0.5,
    ('Steel', 'Electric'): 0.5,
    ('Steel', 'Ice'): 2.0,
    ('Steel', 'Rock'): 2.0,
    ('Steel', 'Steel'): 0.5,
    ('Steel', 'Fairy'): 2.0,
    
    # Fairy
    ('Fairy', 'Fire'): 0.5,
    ('Fairy', 'Fighting'): 2.0,
    ('Fairy', 'Poison'): 0.5,
    ('Fairy', 'Dragon'): 2.0,
    ('Fairy', 'Dark'): 2.0,
    ('Fairy', 'Steel'): 0.5,
}

# Tipos de Pokemon (Gen 9)
# Formato: 'Species': ['Type1', 'Type2'] o ['Type1'] para mono-tipo
POKEMON_TYPES = {
    # Starters Gen 1
    'Venusaur': ['Grass', 'Poison'],
    'Charizard': ['Fire', 'Flying'],
    'Blastoise': ['Water'],
    
    # Legendarios populares
    'Mewtwo': ['Psychic'],
    'Mew': ['Psychic'],
    'Lugia': ['Psychic', 'Flying'],
    'Ho-Oh': ['Fire', 'Flying'],
    'Kyogre': ['Water'],
    'Groudon': ['Ground'],
    'Rayquaza': ['Dragon', 'Flying'],
    'Dialga': ['Steel', 'Dragon'],
    'Palkia': ['Water', 'Dragon'],
    'Giratina': ['Ghost', 'Dragon'],
    'Arceus': ['Normal'],
    'Reshiram': ['Dragon', 'Fire'],
    'Zekrom': ['Dragon', 'Electric'],
    'Kyurem': ['Dragon', 'Ice'],
    'Xerneas': ['Fairy'],
    'Yveltal': ['Dark', 'Flying'],
    'Zygarde': ['Dragon', 'Ground'],
    'Solgaleo': ['Psychic', 'Steel'],
    'Lunala': ['Psychic', 'Ghost'],
    'Necrozma': ['Psychic'],
    'Zacian': ['Fairy', 'Steel'],
    'Zamazenta': ['Fighting', 'Steel'],
    'Eternatus': ['Poison', 'Dragon'],
    'Calyrex': ['Psychic', 'Grass'],
    'Koraidon': ['Fighting', 'Dragon'],
    'Miraidon': ['Electric', 'Dragon'],
    
    # Pseudo-Legendarios
    'Dragonite': ['Dragon', 'Flying'],
    'Tyranitar': ['Rock', 'Dark'],
    'Salamence': ['Dragon', 'Flying'],
    'Metagross': ['Steel', 'Psychic'],
    'Garchomp': ['Dragon', 'Ground'],
    'Hydreigon': ['Dark', 'Dragon'],
    'Goodra': ['Dragon'],
    'Kommo-o': ['Dragon', 'Fighting'],
    'Dragapult': ['Dragon', 'Ghost'],
    'Baxcalibur': ['Dragon', 'Ice'],
    
    # Pokemon populares competitivos
    'Pikachu': ['Electric'],
    'Raichu': ['Electric'],
    'Gengar': ['Ghost', 'Poison'],
    'Alakazam': ['Psychic'],
    'Machamp': ['Fighting'],
    'Golem': ['Rock', 'Ground'],
    'Slowbro': ['Water', 'Psychic'],
    'Magnezone': ['Electric', 'Steel'],
    'Lucario': ['Fighting', 'Steel'],
    'Garchomp': ['Dragon', 'Ground'],
    'Togekiss': ['Fairy', 'Flying'],
    'Rotom': ['Electric', 'Ghost'],
    'Excadrill': ['Ground', 'Steel'],
    'Conkeldurr': ['Fighting'],
    'Ferrothorn': ['Grass', 'Steel'],
    'Chandelure': ['Ghost', 'Fire'],
    'Haxorus': ['Dragon'],
    'Volcarona': ['Bug', 'Fire'],
    'Greninja': ['Water', 'Dark'],
    'Talonflame': ['Fire', 'Flying'],
    'Aegislash': ['Steel', 'Ghost'],
    'Sylveon': ['Fairy'],
    'Mimikyu': ['Ghost', 'Fairy'],
    'Toxapex': ['Poison', 'Water'],
    'Tapu Koko': ['Electric', 'Fairy'],
    'Tapu Lele': ['Psychic', 'Fairy'],
    'Tapu Bulu': ['Grass', 'Fairy'],
    'Tapu Fini': ['Water', 'Fairy'],
    'Landorus': ['Ground', 'Flying'],
    'Thundurus': ['Electric', 'Flying'],
    'Tornadus': ['Flying'],
    'Heatran': ['Fire', 'Steel'],
    'Latios': ['Dragon', 'Psychic'],
    'Latias': ['Dragon', 'Psychic'],
    'Cresselia': ['Psychic'],
    'Manaphy': ['Water'],
    'Darkrai': ['Dark'],
    'Shaymin': ['Grass'],
    'Victini': ['Psychic', 'Fire'],
    'Keldeo': ['Water', 'Fighting'],
    'Genesect': ['Bug', 'Steel'],
    'Diancie': ['Rock', 'Fairy'],
    'Hoopa': ['Psychic', 'Ghost'],
    'Volcanion': ['Fire', 'Water'],
    'Magearna': ['Steel', 'Fairy'],
    'Marshadow': ['Fighting', 'Ghost'],
    'Zeraora': ['Electric'],
    'Meltan': ['Steel'],
    'Melmetal': ['Steel'],
    
    # Gen 9 destacados
    'Meowscarada': ['Grass', 'Dark'],
    'Skeledirge': ['Fire', 'Ghost'],
    'Quaquaval': ['Water', 'Fighting'],
    'Lechonk': ['Normal'],
    'Oinkologne': ['Normal'],
    'Pawmi': ['Electric'],
    'Pawmo': ['Electric', 'Fighting'],
    'Pawmot': ['Electric', 'Fighting'],
    'Tandemaus': ['Normal'],
    'Maushold': ['Normal'],
    'Fidough': ['Fairy'],
    'Dachsbun': ['Fairy'],
    'Smoliv': ['Grass', 'Normal'],
    'Dolliv': ['Grass', 'Normal'],
    'Arboliva': ['Grass', 'Normal'],
    'Squawkabilly': ['Normal', 'Flying'],
    'Nacli': ['Rock'],
    'Naclstack': ['Rock'],
    'Garganacl': ['Rock'],
    'Charcadet': ['Fire'],
    'Armarouge': ['Fire', 'Psychic'],
    'Ceruledge': ['Fire', 'Ghost'],
    'Tadbulb': ['Electric'],
    'Bellibolt': ['Electric'],
    'Wattrel': ['Electric', 'Flying'],
    'Kilowattrel': ['Electric', 'Flying'],
    'Maschiff': ['Dark'],
    'Mabosstiff': ['Dark'],
    'Shroodle': ['Poison', 'Normal'],
    'Grafaiai': ['Poison', 'Normal'],
    'Bramblin': ['Grass', 'Ghost'],
    'Brambleghast': ['Grass', 'Ghost'],
    'Toedscool': ['Ground', 'Grass'],
    'Toedscruel': ['Ground', 'Grass'],
    'Klawf': ['Rock'],
    'Capsakid': ['Grass'],
    'Scovillain': ['Grass', 'Fire'],
    'Rellor': ['Bug'],
    'Rabsca': ['Bug', 'Psychic'],
    'Flittle': ['Psychic'],
    'Espathra': ['Psychic'],
    'Tinkatink': ['Fairy', 'Steel'],
    'Tinkatuff': ['Fairy', 'Steel'],
    'Tinkaton': ['Fairy', 'Steel'],
    'Wiglett': ['Water'],
    'Wugtrio': ['Water'],
    'Bombirdier': ['Flying', 'Dark'],
    'Finizen': ['Water'],
    'Palafin': ['Water'],
    'Varoom': ['Steel', 'Poison'],
    'Revavroom': ['Steel', 'Poison'],
    'Cyclizar': ['Dragon', 'Normal'],
    'Orthworm': ['Steel'],
    'Glimmet': ['Rock', 'Poison'],
    'Glimmora': ['Rock', 'Poison'],
    'Greavard': ['Ghost'],
    'Houndstone': ['Ghost'],
    'Flamigo': ['Flying', 'Fighting'],
    'Cetoddle': ['Ice'],
    'Cetitan': ['Ice'],
    'Veluza': ['Water', 'Psychic'],
    'Dondozo': ['Water'],
    'Tatsugiri': ['Dragon', 'Water'],
    'Annihilape': ['Fighting', 'Ghost'],
    'Clodsire': ['Poison', 'Ground'],
    'Farigiraf': ['Normal', 'Psychic'],
    'Dudunsparce': ['Normal'],
    'Kingambit': ['Dark', 'Steel'],
    'Great Tusk': ['Ground', 'Fighting'],
    'Scream Tail': ['Fairy', 'Psychic'],
    'Brute Bonnet': ['Grass', 'Dark'],
    'Flutter Mane': ['Ghost', 'Fairy'],
    'Slither Wing': ['Bug', 'Fighting'],
    'Sandy Shocks': ['Electric', 'Ground'],
    'Iron Treads': ['Ground', 'Steel'],
    'Iron Bundle': ['Ice', 'Water'],
    'Iron Hands': ['Fighting', 'Electric'],
    'Iron Jugulis': ['Dark', 'Flying'],
    'Iron Moth': ['Fire', 'Poison'],
    'Iron Thorns': ['Rock', 'Electric'],
    'Frigibax': ['Dragon', 'Ice'],
    'Arctibax': ['Dragon', 'Ice'],
    'Gholdengo': ['Steel', 'Ghost'],
    'Wo-Chien': ['Dark', 'Grass'],
    'Chien-Pao': ['Dark', 'Ice'],
    'Ting-Lu': ['Dark', 'Ground'],
    'Chi-Yu': ['Dark', 'Fire'],
    'Roaring Moon': ['Dragon', 'Dark'],
    'Iron Valiant': ['Fairy', 'Fighting'],
    'Walking Wake': ['Water', 'Dragon'],
    'Iron Leaves': ['Grass', 'Psychic'],
    'Poltchageist': ['Grass', 'Ghost'],
    'Sinistcha': ['Grass', 'Ghost'],
    'Okidogi': ['Poison', 'Fighting'],
    'Munkidori': ['Poison', 'Psychic'],
    'Fezandipiti': ['Poison', 'Fairy'],
    'Ogerpon': ['Grass'],
    'Archaludon': ['Steel', 'Dragon'],
    'Hydrapple': ['Grass', 'Dragon'],
    'Gouging Fire': ['Fire', 'Dragon'],
    'Raging Bolt': ['Electric', 'Dragon'],
    'Iron Boulder': ['Rock', 'Psychic'],
    'Iron Crown': ['Steel', 'Psychic'],
    'Terapagos': ['Normal'],
    'Pecharunt': ['Poison', 'Ghost'],
    
    # === Pokemon completados automáticamente ===
    # Generado: 2025-10-08 13:04:15
    # Total: 50 Pokemon
    'Deoxys': ['Psychic'],  # 674 apariciones
    'Tauros': ['Normal'],  # 654 apariciones
    'Oricorio': ['Fire', 'Flying'],  # 651 apariciones
    'Illumise': ['Bug'],  # 408 apariciones
    'Sableye': ['Dark', 'Ghost'],  # 405 apariciones
    'Dunsparce': ['Normal'],  # 397 apariciones
    'Galvantula': ['Bug', 'Electric'],  # 394 apariciones
    'Grimmsnarl': ['Dark', 'Fairy'],  # 393 apariciones
    'Uxie': ['Psychic'],  # 391 apariciones
    'Phione': ['Water'],  # 390 apariciones
    'Alomomola': ['Water'],  # 389 apariciones
    'Volbeat': ['Bug'],  # 388 apariciones
    'Granbull': ['Fairy'],  # 387 apariciones
    'Lanturn': ['Water', 'Electric'],  # 386 apariciones
    'Gastrodon': ['Water', 'Ground'],  # 385 apariciones
    'Ariados': ['Bug', 'Poison'],  # 382 apariciones
    'Mudsdale': ['Ground'],  # 381 apariciones
    'Alcremie': ['Fairy'],  # 380 apariciones
    'Chansey': ['Normal'],  # 380 apariciones
    'Vaporeon': ['Water'],  # 380 apariciones
    'Amoonguss': ['Grass', 'Poison'],  # 380 apariciones
    'Hitmontop': ['Fighting'],  # 379 apariciones
    'Milotic': ['Water'],  # 376 apariciones
    'Persian': ['Normal'],  # 375 apariciones
    'Blissey': ['Normal'],  # 374 apariciones
    'Smeargle': ['Normal'],  # 373 apariciones
    'Mienshao': ['Fighting'],  # 372 apariciones
    'Zapdos': ['Electric', 'Flying'],  # 371 apariciones
    'Porygon2': ['Normal'],  # 369 apariciones
    'Scizor': ['Bug', 'Steel'],  # 369 apariciones
    'Gurdurr': ['Fighting'],  # 368 apariciones
    'Wyrdeer': ['Normal', 'Psychic'],  # 368 apariciones
    'Spidops': ['Bug'],  # 367 apariciones
    'Spectrier': ['Ghost'],  # 367 apariciones
    'Palossand': ['Ghost', 'Ground'],  # 366 apariciones
    'Dusknoir': ['Ghost'],  # 366 apariciones
    'Spiritomb': ['Ghost', 'Dark'],  # 365 apariciones
    'Suicune': ['Water'],  # 365 apariciones
    'Vikavolt': ['Bug', 'Electric'],  # 365 apariciones
    'Eelektross': ['Electric'],  # 365 apariciones
    'Swalot': ['Poison'],  # 365 apariciones
    'Mismagius': ['Ghost'],  # 364 apariciones
    'Mesprit': ['Psychic'],  # 364 apariciones
    'Slaking': ['Normal'],  # 364 apariciones
    'Umbreon': ['Dark'],  # 363 apariciones
    'Mandibuzz': ['Dark', 'Flying'],  # 363 apariciones
    'Azumarill': ['Water', 'Fairy'],  # 363 apariciones
    'Vileplume': ['Grass', 'Poison'],  # 362 apariciones
    'Dedenne': ['Electric', 'Fairy'],  # 362 apariciones
    'Electivire': ['Electric'],  # 362 apariciones
    
    # === Pokemon completados automáticamente (PokeAPI) ===
    # Generado: 2025-10-13 10:13:49
    # Total: 229 Pokemon (223 automáticos + 6 manuales)
    'Polteageist': ['Ghost'],  # 362 apariciones
    'Pelipper': ['Water', 'Flying'],  # 361 apariciones
    'Gogoat': ['Grass'],  # 361 apariciones
    'Hypno': ['Psychic'],  # 360 apariciones
    'Kleavor': ['Bug', 'Rock'],  # 360 apariciones
    'Pincurchin': ['Electric'],  # 359 apariciones
    'Clefable': ['Fairy'],  # 359 apariciones
    'Kricketune': ['Bug'],  # 358 apariciones
    'Klefki': ['Steel', 'Fairy'],  # 357 apariciones
    'Whimsicott': ['Grass', 'Fairy'],  # 356 apariciones
    'Gyarados': ['Water', 'Flying'],  # 356 apariciones
    'Arbok': ['Poison'],  # 355 apariciones
    'Bellossom': ['Grass'],  # 355 apariciones
    'Lumineon': ['Water'],  # 354 apariciones
    'Golduck': ['Water'],  # 354 apariciones
    'Araquanid': ['Water', 'Bug'],  # 354 apariciones
    'Cryogonal': ['Ice'],  # 353 apariciones
    'Pachirisu': ['Electric'],  # 353 apariciones
    'Luxray': ['Electric'],  # 353 apariciones
    'Minun': ['Electric'],  # 353 apariciones
    'Ampharos': ['Electric'],  # 352 apariciones
    'Wigglytuff': ['Normal', 'Fairy'],  # 352 apariciones
    'Zebstrika': ['Electric'],  # 352 apariciones
    'Regice': ['Ice'],  # 352 apariciones
    'Piloswine': ['Ice', 'Ground'],  # 351 apariciones
    'Politoed': ['Water'],  # 351 apariciones
    'Overqwil': ['Dark', 'Poison'],  # 351 apariciones
    'Slowking': ['Water', 'Psychic'],  # 351 apariciones
    'Ribombee': ['Bug', 'Fairy'],  # 350 apariciones
    'Honchkrow': ['Dark', 'Flying'],  # 350 apariciones
    'Regigigas': ['Normal'],  # 349 apariciones
    'Espeon': ['Psychic'],  # 349 apariciones
    'Skarmory': ['Steel', 'Flying'],  # 349 apariciones
    'Arcanine': ['Fire'],  # 349 apariciones
    'Clawitzer': ['Water'],  # 349 apariciones
    'Banette': ['Ghost'],  # 349 apariciones
    'Magmortar': ['Fire'],  # 349 apariciones
    'Snorlax': ['Normal'],  # 349 apariciones
    'Florges': ['Fairy'],  # 348 apariciones
    'Misdreavus': ['Ghost'],  # 348 apariciones
    'Chimecho': ['Psychic'],  # 348 apariciones
    'Gumshoos': ['Normal'],  # 347 apariciones
    'Reuniclus': ['Psychic'],  # 346 apariciones
    'Sandaconda': ['Ground'],  # 346 apariciones
    'Empoleon': ['Water', 'Steel'],  # 346 apariciones
    'Quagsire': ['Water', 'Ground'],  # 346 apariciones
    'Carbink': ['Rock', 'Fairy'],  # 345 apariciones
    'Ninetales': ['Fire'],  # 345 apariciones
    'Hitmonchan': ['Fighting'],  # 345 apariciones
    'Luvdisc': ['Water'],  # 344 apariciones
    'Cinccino': ['Normal'],  # 344 apariciones
    'Forretress': ['Bug', 'Steel'],  # 344 apariciones
    'Raikou': ['Electric'],  # 343 apariciones
    'Trevenant': ['Ghost', 'Grass'],  # 343 apariciones
    'Abomasnow': ['Grass', 'Ice'],  # 343 apariciones
    'Eiscue': ['Ice'],  # 342 apariciones
    'Comfey': ['Fairy'],  # 342 apariciones
    'Meganium': ['Grass'],  # 342 apariciones
    'Toxtricity': ['Electric', 'Poison'],  # 342 apariciones
    'Morpeko': ['Electric', 'Dark'],  # 342 apariciones
    'Jumpluff': ['Grass', 'Flying'],  # 342 apariciones
    'Articuno': ['Ice', 'Flying'],  # 341 apariciones
    'Hippowdon': ['Ground'],  # 341 apariciones
    'Entei': ['Fire'],  # 340 apariciones
    'Gliscor': ['Ground', 'Flying'],  # 340 apariciones
    'Ursaring': ['Normal'],  # 340 apariciones
    'Gardevoir': ['Psychic', 'Fairy'],  # 339 apariciones
    'Azelf': ['Psychic'],  # 339 apariciones
    'Weezing': ['Poison'],  # 339 apariciones
    'Jirachi': ['Steel', 'Psychic'],  # 338 apariciones
    'Lilligant': ['Grass'],  # 338 apariciones
    'Donphan': ['Ground'],  # 337 apariciones
    'Primarina': ['Water', 'Fairy'],  # 337 apariciones
    'Ho-Oh': ['Fire', 'Flying'],  # 337 apariciones (Ho + Ting)
    'Greedent': ['Normal'],  # 336 apariciones
    'Barraskewda': ['Water'],  # 336 apariciones
    'Froslass': ['Ice', 'Ghost'],  # 335 apariciones
    'Hatterene': ['Psychic', 'Fairy'],  # 335 apariciones
    'Regieleki': ['Electric'],  # 334 apariciones
    'Probopass': ['Rock', 'Steel'],  # 334 apariciones
    'Gothitelle': ['Psychic'],  # 334 apariciones
    'Sandslash': ['Ground'],  # 334 apariciones
    'Lokix': ['Bug', 'Dark'],  # 334 apariciones
    'Tsareena': ['Grass'],  # 334 apariciones
    'Plusle': ['Electric'],  # 333 apariciones
    'Tentacruel': ['Water', 'Poison'],  # 333 apariciones
    'Inteleon': ['Water'],  # 333 apariciones
    'Moltres': ['Fire', 'Flying'],  # 332 apariciones
    'Heracross': ['Bug', 'Fighting'],  # 332 apariciones
    'Ditto': ['Normal'],  # 332 apariciones
    'Vigoroth': ['Normal'],  # 332 apariciones
    'Muk': ['Poison'],  # 331 apariciones
    'Glalie': ['Ice'],  # 331 apariciones
    'Jolteon': ['Electric'],  # 331 apariciones
    'Drifblim': ['Ghost', 'Flying'],  # 331 apariciones
    'Komala': ['Normal'],  # 331 apariciones
    'Swampert': ['Water', 'Ground'],  # 330 apariciones
    'Falinks': ['Fighting'],  # 330 apariciones
    'Kingdra': ['Water', 'Dragon'],  # 329 apariciones
    'Seviper': ['Poison'],  # 329 apariciones
    'Qwilfish': ['Water', 'Poison'],  # 329 apariciones
    'Golurk': ['Ground', 'Ghost'],  # 329 apariciones
    'Grumpig': ['Psychic'],  # 328 apariciones
    'Registeel': ['Steel'],  # 328 apariciones
    'Ambipom': ['Normal'],  # 328 apariciones
    'Basculegion': ['Water', 'Ghost'],  # 328 apariciones
    'Furret': ['Normal'],  # 327 apariciones
    'Hitmonlee': ['Fighting'],  # 327 apariciones
    'Bronzong': ['Steel', 'Psychic'],  # 327 apariciones
    'Zangoose': ['Normal'],  # 326 apariciones
    'Salazzle': ['Poison', 'Fire'],  # 326 apariciones
    'Pyroar': ['Fire', 'Normal'],  # 326 apariciones
    'Torkoal': ['Fire'],  # 325 apariciones
    'Decidueye': ['Grass', 'Ghost'],  # 325 apariciones
    'Corviknight': ['Flying', 'Steel'],  # 325 apariciones
    'Dragalge': ['Poison', 'Dragon'],  # 325 apariciones
    'Meowstic': ['Psychic'],  # 325 apariciones
    'Toxicroak': ['Poison', 'Fighting'],  # 324 apariciones
    'Mightyena': ['Dark'],  # 324 apariciones
    'Hawlucha': ['Fighting', 'Flying'],  # 323 apariciones
    'Mamoswine': ['Ice', 'Ground'],  # 323 apariciones
    'Sunflora': ['Grass'],  # 323 apariciones
    'Poliwrath': ['Water', 'Fighting'],  # 323 apariciones
    'Masquerain': ['Bug', 'Flying'],  # 322 apariciones
    'Incineroar': ['Fire', 'Dark'],  # 322 apariciones
    'Glastrier': ['Ice'],  # 322 apariciones
    'Beartic': ['Ice'],  # 322 apariciones
    'Flygon': ['Ground', 'Dragon'],  # 321 apariciones
    'Delibird': ['Ice', 'Flying'],  # 321 apariciones
    'Duraludon': ['Steel', 'Dragon'],  # 321 apariciones
    'Krookodile': ['Ground', 'Dark'],  # 321 apariciones
    'Cacturne': ['Grass', 'Dark'],  # 321 apariciones
    'Hariyama': ['Fighting'],  # 321 apariciones
    'Staraptor': ['Normal', 'Flying'],  # 321 apariciones
    'Malamar': ['Dark', 'Psychic'],  # 320 apariciones
    'Ursaluna': ['Ground', 'Normal'],  # 320 apariciones
    'Chesnaught': ['Grass', 'Fighting'],  # 320 apariciones
    'Whiscash': ['Water', 'Ground'],  # 320 apariciones
    'Feraligatr': ['Water'],  # 319 apariciones
    'Skuntank': ['Poison', 'Dark'],  # 319 apariciones
    'Delphox': ['Fire', 'Psychic'],  # 318 apariciones
    'Lycanroc': ['Rock'],  # 318 apariciones
    'Scrafty': ['Dark', 'Fighting'],  # 318 apariciones
    'Girafarig': ['Normal', 'Psychic'],  # 318 apariciones
    'Braviary': ['Normal', 'Flying'],  # 317 apariciones
    'Lapras': ['Water', 'Ice'],  # 317 apariciones
    'Yanmega': ['Bug', 'Flying'],  # 316 apariciones
    'Sawsbuck': ['Normal', 'Grass'],  # 316 apariciones
    'Glaceon': ['Ice'],  # 315 apariciones
    'Dewgong': ['Water', 'Ice'],  # 315 apariciones
    'Chi-Yu': ['Dark', 'Fire'],  # 315 apariciones (Chi)
    'Emboar': ['Fire', 'Fighting'],  # 315 apariciones
    'Dugtrio': ['Ground'],  # 314 apariciones
    'Swanna': ['Water', 'Flying'],  # 314 apariciones
    'Torterra': ['Grass', 'Ground'],  # 314 apariciones
    'Typhlosion': ['Fire'],  # 313 apariciones
    'Copperajah': ['Steel'],  # 313 apariciones
    'Rillaboom': ['Grass'],  # 313 apariciones
    'Sneasler': ['Fighting', 'Poison'],  # 312 apariciones
    'Camerupt': ['Fire', 'Ground'],  # 312 apariciones
    'Rampardos': ['Rock'],  # 312 apariciones
    'Cramorant': ['Flying', 'Water'],  # 311 apariciones
    'Electrode': ['Electric'],  # 311 apariciones
    'Regirock': ['Rock'],  # 310 apariciones
    'Victreebel': ['Grass', 'Poison'],  # 309 apariciones
    'Sceptile': ['Grass'],  # 308 apariciones
    'Flareon': ['Fire'],  # 308 apariciones
    'Porygon': ['Normal'],  # 308 apariciones
    'Terrakion': ['Rock', 'Fighting'],  # 308 apariciones
    'Toucannon': ['Normal', 'Flying'],  # 307 apariciones
    'Floatzel': ['Water'],  # 307 apariciones
    'Frosmoth': ['Ice', 'Bug'],  # 307 apariciones
    'Rhyperior': ['Ground', 'Rock'],  # 306 apariciones
    'Crawdaunt': ['Water', 'Dark'],  # 306 apariciones
    'Oranguru': ['Normal', 'Psychic'],  # 306 apariciones
    'Houndoom': ['Dark', 'Fire'],  # 306 apariciones
    'Meloetta': ['Normal', 'Psychic'],  # 305 apariciones
    'Wo-Chien': ['Dark', 'Grass'],  # 305 apariciones (Wo)
    'Cobalion': ['Steel', 'Fighting'],  # 304 apariciones
    'Perrserker': ['Steel'],  # 304 apariciones
    'Bruxish': ['Water', 'Psychic'],  # 303 apariciones
    'Sudowoodo': ['Rock'],  # 303 apariciones
    'Regidrago': ['Dragon'],  # 302 apariciones
    'Chien-Pao': ['Dark', 'Ice'],  # 302 apariciones (Chien)
    'Cinderace': ['Fire'],  # 302 apariciones
    'Samurott': ['Water'],  # 302 apariciones
    'Scyther': ['Bug', 'Flying'],  # 301 apariciones
    'Coalossal': ['Rock', 'Fire'],  # 300 apariciones
    'Gallade': ['Psychic', 'Fighting'],  # 299 apariciones
    'Exeggutor': ['Grass', 'Psychic'],  # 299 apariciones
    'Leafeon': ['Grass'],  # 299 apariciones
    'Weavile': ['Dark', 'Ice'],  # 299 apariciones
    'Lurantis': ['Grass'],  # 299 apariciones
    'Cloyster': ['Water', 'Ice'],  # 298 apariciones
    'Indeedee': ['Psychic', 'Normal'],  # 298 apariciones
    'Serperior': ['Grass'],  # 297 apariciones
    'Magcargo': ['Fire', 'Rock'],  # 297 apariciones
    'Flapple': ['Grass', 'Dragon'],  # 297 apariciones
    'Venomoth': ['Bug', 'Poison'],  # 296 apariciones
    'Passimian': ['Fighting'],  # 295 apariciones
    'Infernape': ['Fire', 'Fighting'],  # 294 apariciones
    'Vespiquen': ['Bug', 'Flying'],  # 294 apariciones
    'Noctowl': ['Normal', 'Flying'],  # 293 apariciones
    'Drednaw': ['Water', 'Rock'],  # 293 apariciones
    'Crabominable': ['Fighting', 'Ice'],  # 293 apariciones
    'Ludicolo': ['Water', 'Grass'],  # 292 apariciones
    'Leavanny': ['Bug', 'Grass'],  # 292 apariciones
    'Medicham': ['Fighting', 'Psychic'],  # 292 apariciones
    'Dipplin': ['Grass', 'Dragon'],  # 290 apariciones
    'Zarude': ['Dark', 'Grass'],  # 290 apariciones
    'Basculin': ['Water'],  # 290 apariciones
    'Rhydon': ['Ground', 'Rock'],  # 289 apariciones
    'Avalugg': ['Ice'],  # 287 apariciones
    'Blaziken': ['Fire', 'Fighting'],  # 287 apariciones
    'Breloom': ['Grass', 'Fighting'],  # 287 apariciones
    'Shiftry': ['Grass', 'Dark'],  # 286 apariciones
    'Dodrio': ['Normal', 'Flying'],  # 283 apariciones
    'Appletun': ['Grass', 'Dragon'],  # 282 apariciones
    'Bastiodon': ['Rock', 'Steel'],  # 281 apariciones
    'Kommo-o': ['Dragon', 'Fighting'],  # 280 apariciones (Kommo)
    'Stonjourner': ['Rock'],  # 279 apariciones
    'Noivern': ['Flying', 'Dragon'],  # 278 apariciones
    'Virizion': ['Grass', 'Fighting'],  # 277 apariciones
    'Minior': ['Rock', 'Flying'],  # 273 apariciones
    'Vivillon': ['Bug', 'Flying'],  # 269 apariciones
    'Tropius': ['Grass', 'Flying'],  # 264 apariciones
    'Altaria': ['Dragon', 'Flying'],  # 260 apariciones
    'Zoroark': ['Dark'],  # 17 apariciones
    
    # Formas alternativas importantes
    'Rotom-Wash': ['Electric', 'Water'],
    'Rotom-Heat': ['Electric', 'Fire'],
    'Rotom-Frost': ['Electric', 'Ice'],
    'Rotom-Fan': ['Electric', 'Flying'],
    'Rotom-Mow': ['Electric', 'Grass'],
    'Landorus-Therian': ['Ground', 'Flying'],
    'Thundurus-Therian': ['Electric', 'Flying'],
    'Tornadus-Therian': ['Flying'],
    'Urshifu': ['Fighting', 'Dark'],
    'Urshifu-Rapid-Strike': ['Fighting', 'Water'],
    'Enamorus': ['Fairy', 'Flying'],
    'Enamorus-Therian': ['Fairy', 'Flying'],
    'Ogerpon-Wellspring': ['Grass', 'Water'],
    'Ogerpon-Hearthflame': ['Grass', 'Fire'],
    'Ogerpon-Cornerstone': ['Grass', 'Rock'],
    
    # Aliases para nombres truncados en dataset
    'Ho': ['Fire', 'Flying'],  # Ho-Oh truncado
    'Ting': ['Fire', 'Flying'],  # Parte de "Ho-Oh" (Ho + Ting)
    'Chi': ['Dark', 'Fire'],  # Chi-Yu truncado
    'Wo': ['Dark', 'Grass'],  # Wo-Chien truncado
    'Chien': ['Dark', 'Ice'],  # Chien-Pao truncado
    'Kommo': ['Dragon', 'Fighting'],  # Kommo-o truncado
}

# Base Stat Totals (BST) - Suma de HP + Atk + Def + SpA + SpD + Spe
POKEMON_BST = {
    # Legendarios (680+)
    'Arceus': 720,
    'Mewtwo': 680,
    'Lugia': 680,
    'Ho-Oh': 680,
    'Rayquaza': 680,
    'Dialga': 680,
    'Palkia': 680,
    'Giratina': 680,
    'Reshiram': 680,
    'Zekrom': 680,
    'Kyurem': 660,
    'Xerneas': 680,
    'Yveltal': 680,
    'Zygarde': 708,
    'Solgaleo': 680,
    'Lunala': 680,
    'Necrozma': 600,
    'Zacian': 670,
    'Zamazenta': 670,
    'Eternatus': 690,
    'Calyrex': 500,
    'Koraidon': 670,
    'Miraidon': 670,
    'Kyogre': 670,
    'Groudon': 670,
    
    # Pseudo-Legendarios (600)
    'Dragonite': 600,
    'Tyranitar': 600,
    'Salamence': 600,
    'Metagross': 600,
    'Garchomp': 600,
    'Hydreigon': 600,
    'Goodra': 600,
    'Kommo-o': 600,
    'Dragapult': 600,
    'Baxcalibur': 600,
    
    # Starters finales (530-540)
    'Venusaur': 525,
    'Charizard': 534,
    'Blastoise': 530,
    'Meowscarada': 530,
    'Skeledirge': 534,
    'Quaquaval': 530,
    
    # Pokemon competitivos fuertes (500-580)
    'Gengar': 500,
    'Alakazam': 500,
    'Machamp': 505,
    'Golem': 495,
    'Slowbro': 490,
    'Magnezone': 535,
    'Lucario': 525,
    'Togekiss': 545,
    'Rotom': 520,
    'Excadrill': 508,
    'Conkeldurr': 505,
    'Ferrothorn': 489,
    'Chandelure': 520,
    'Haxorus': 540,
    'Volcarona': 550,
    'Greninja': 530,
    'Talonflame': 499,
    'Aegislash': 520,
    'Sylveon': 525,
    'Mimikyu': 476,
    'Toxapex': 495,
    'Landorus': 600,
    'Thundurus': 580,
    'Tornadus': 580,
    'Heatran': 600,
    'Latios': 600,
    'Latias': 600,
    'Cresselia': 600,
    'Manaphy': 600,
    'Darkrai': 600,
    'Shaymin': 600,
    'Victini': 600,
    'Keldeo': 580,
    'Genesect': 600,
    'Diancie': 600,
    'Hoopa': 600,
    'Volcanion': 600,
    'Magearna': 600,
    'Marshadow': 600,
    'Zeraora': 600,
    'Melmetal': 600,
    
    # Tapus (570)
    'Tapu Koko': 570,
    'Tapu Lele': 570,
    'Tapu Bulu': 570,
    'Tapu Fini': 570,
    
    # Gen 9 destacados
    'Gholdengo': 550,
    'Kingambit': 550,
    'Iron Valiant': 570,
    'Flutter Mane': 570,
    'Roaring Moon': 590,
    'Great Tusk': 570,
    'Iron Treads': 570,
    'Palafin': 457,  # Forma Hero: 650
    'Tinkaton': 506,
    'Annihilape': 535,
    'Clodsire': 430,
    'Farigiraf': 520,
    'Dudunsparce': 520,
    'Armarouge': 525,
    'Ceruledge': 525,
    'Bellibolt': 495,
    'Kilowattrel': 490,
    'Mabosstiff': 505,
    'Grafaiai': 485,
    'Brambleghast': 480,
    'Toedscruel': 515,
    'Scovillain': 486,
    'Rabsca': 470,
    'Espathra': 481,
    'Wugtrio': 425,
    'Bombirdier': 485,
    'Revavroom': 500,
    'Cyclizar': 501,
    'Orthworm': 480,
    'Glimmora': 525,
    'Houndstone': 488,
    'Flamigo': 500,
    'Cetitan': 521,
    'Veluza': 478,
    'Dondozo': 530,
    'Tatsugiri': 475,
    'Wo-Chien': 570,
    'Chien-Pao': 570,
    'Ting-Lu': 570,
    'Chi-Yu': 570,
    'Walking Wake': 590,
    'Iron Leaves': 570,
    'Sinistcha': 508,
    'Okidogi': 555,
    'Munkidori': 555,
    'Fezandipiti': 555,
    'Ogerpon': 550,
    'Archaludon': 600,
    'Hydrapple': 540,
    'Gouging Fire': 590,
    'Raging Bolt': 590,
    'Iron Boulder': 570,
    'Iron Crown': 570,
    'Terapagos': 600,
    'Pecharunt': 600,
    
    # === BST de Pokemon completados ===
    # Generado: 2025-10-08 13:04:15
    'Deoxys': 600,
    'Tauros': 490,
    'Oricorio': 476,
    'Illumise': 430,
    'Sableye': 380,
    'Dunsparce': 415,
    'Galvantula': 472,
    'Grimmsnarl': 510,
    'Uxie': 580,
    'Phione': 480,
    'Alomomola': 470,
    'Volbeat': 430,
    'Granbull': 450,
    'Lanturn': 460,
    'Gastrodon': 475,
    'Ariados': 400,
    'Mudsdale': 500,
    'Alcremie': 495,
    'Chansey': 450,
    'Vaporeon': 525,
    'Amoonguss': 464,
    'Hitmontop': 455,
    'Milotic': 540,
    'Persian': 440,
    'Blissey': 540,
    'Smeargle': 250,
    'Mienshao': 510,
    'Zapdos': 580,
    'Porygon2': 515,
    'Scizor': 500,
    'Gurdurr': 405,
    'Wyrdeer': 525,
    'Spidops': 404,
    'Spectrier': 580,
    'Palossand': 480,
    'Dusknoir': 525,
    'Spiritomb': 485,
    'Suicune': 580,
    'Vikavolt': 500,
    'Eelektross': 515,
    'Swalot': 467,
    'Mismagius': 495,
    'Mesprit': 580,
    'Slaking': 670,
    'Umbreon': 525,
    'Mandibuzz': 510,
    'Azumarill': 420,
    'Vileplume': 490,
    'Dedenne': 431,
    'Electivire': 540,
    
    # Pokemon comunes (300-450)
    'Pikachu': 320,
    'Raichu': 485,
    'Lechonk': 254,
    'Oinkologne': 489,
    'Pawmi': 240,
    'Pawmo': 350,
    'Pawmot': 490,
    'Tandemaus': 305,
    'Maushold': 470,
    'Fidough': 312,
    'Dachsbun': 477,
    'Smoliv': 260,
    'Dolliv': 354,
    'Arboliva': 510,
    'Squawkabilly': 417,
    'Nacli': 280,
    'Naclstack': 355,
    'Garganacl': 500,
    'Charcadet': 288,
    'Tadbulb': 272,
    'Wattrel': 280,
    'Maschiff': 340,
    'Shroodle': 290,
    'Bramblin': 275,
    'Toedscool': 335,
    'Klawf': 450,
    'Capsakid': 304,
    'Rellor': 270,
    'Flittle': 280,
    'Tinkatink': 297,
    'Tinkatuff': 380,
    'Wiglett': 245,
    'Finizen': 315,
    'Varoom': 300,
    'Greavard': 290,
    'Cetoddle': 334,
    'Frigibax': 320,
    'Arctibax': 423,
    'Poltchageist': 308,
    
    # === BST de Pokemon completados (PokeAPI) ===
    # Generado: 2025-10-13 10:13:49
    'Polteageist': 508,
    'Pelipper': 440,
    'Gogoat': 531,
    'Hypno': 483,
    'Kleavor': 500,
    'Pincurchin': 435,
    'Clefable': 483,
    'Kricketune': 384,
    'Klefki': 470,
    'Whimsicott': 480,
    'Gyarados': 540,
    'Arbok': 448,
    'Bellossom': 490,
    'Lumineon': 460,
    'Golduck': 500,
    'Araquanid': 454,
    'Cryogonal': 515,
    'Pachirisu': 405,
    'Luxray': 523,
    'Minun': 405,
    'Ampharos': 510,
    'Wigglytuff': 435,
    'Zebstrika': 497,
    'Regice': 580,
    'Piloswine': 450,
    'Politoed': 500,
    'Overqwil': 510,
    'Slowking': 490,
    'Ribombee': 464,
    'Honchkrow': 505,
    'Regigigas': 670,
    'Espeon': 525,
    'Skarmory': 465,
    'Arcanine': 555,
    'Clawitzer': 500,
    'Banette': 455,
    'Magmortar': 540,
    'Snorlax': 540,
    'Florges': 552,
    'Misdreavus': 435,
    'Chimecho': 455,
    'Gumshoos': 418,
    'Reuniclus': 490,
    'Sandaconda': 510,
    'Empoleon': 530,
    'Quagsire': 430,
    'Carbink': 500,
    'Ninetales': 505,
    'Hitmonchan': 455,
    'Luvdisc': 330,
    'Cinccino': 470,
    'Forretress': 465,
    'Raikou': 580,
    'Trevenant': 474,
    'Abomasnow': 494,
    'Eiscue': 470,
    'Comfey': 485,
    'Meganium': 525,
    'Toxtricity': 502,
    'Morpeko': 436,
    'Jumpluff': 460,
    'Articuno': 580,
    'Hippowdon': 525,
    'Entei': 580,
    'Gliscor': 510,
    'Ursaring': 500,
    'Gardevoir': 518,
    'Azelf': 580,
    'Weezing': 490,
    'Jirachi': 600,
    'Lilligant': 480,
    'Donphan': 500,
    'Primarina': 530,
    'Ho-Oh': 680,
    'Greedent': 460,
    'Barraskewda': 490,
    'Froslass': 480,
    'Hatterene': 510,
    'Regieleki': 580,
    'Probopass': 525,
    'Gothitelle': 490,
    'Sandslash': 450,
    'Lokix': 450,
    'Tsareena': 510,
    'Plusle': 405,
    'Tentacruel': 515,
    'Inteleon': 530,
    'Moltres': 580,
    'Heracross': 500,
    'Ditto': 288,
    'Vigoroth': 440,
    'Muk': 500,
    'Glalie': 480,
    'Jolteon': 525,
    'Drifblim': 498,
    'Komala': 480,
    'Swampert': 535,
    'Falinks': 470,
    'Kingdra': 540,
    'Seviper': 458,
    'Qwilfish': 440,
    'Golurk': 483,
    'Grumpig': 470,
    'Registeel': 580,
    'Ambipom': 482,
    'Basculegion': 530,
    'Furret': 415,
    'Hitmonlee': 455,
    'Bronzong': 500,
    'Zangoose': 458,
    'Salazzle': 480,
    'Pyroar': 507,
    'Torkoal': 470,
    'Decidueye': 530,
    'Corviknight': 495,
    'Dragalge': 494,
    'Meowstic': 466,
    'Toxicroak': 490,
    'Mightyena': 420,
    'Hawlucha': 500,
    'Mamoswine': 530,
    'Sunflora': 425,
    'Poliwrath': 510,
    'Masquerain': 454,
    'Incineroar': 530,
    'Glastrier': 580,
    'Beartic': 505,
    'Flygon': 520,
    'Delibird': 330,
    'Duraludon': 535,
    'Krookodile': 519,
    'Cacturne': 475,
    'Hariyama': 474,
    'Staraptor': 485,
    'Malamar': 482,
    'Ursaluna': 550,
    'Chesnaught': 530,
    'Whiscash': 468,
    'Feraligatr': 530,
    'Skuntank': 479,
    'Delphox': 534,
    'Lycanroc': 487,
    'Scrafty': 488,
    'Girafarig': 455,
    'Braviary': 510,
    'Lapras': 535,
    'Yanmega': 515,
    'Sawsbuck': 475,
    'Glaceon': 525,
    'Dewgong': 475,
    'Chi-Yu': 570,
    'Emboar': 528,
    'Dugtrio': 425,
    'Swanna': 473,
    'Torterra': 525,
    'Typhlosion': 534,
    'Copperajah': 500,
    'Rillaboom': 530,
    'Sneasler': 510,
    'Camerupt': 460,
    'Rampardos': 495,
    'Cramorant': 475,
    'Electrode': 490,
    'Regirock': 580,
    'Victreebel': 490,
    'Sceptile': 530,
    'Flareon': 525,
    'Porygon': 395,
    'Terrakion': 580,
    'Toucannon': 485,
    'Floatzel': 495,
    'Frosmoth': 475,
    'Rhyperior': 535,
    'Crawdaunt': 468,
    'Oranguru': 490,
    'Houndoom': 500,
    'Meloetta': 600,
    'Wo-Chien': 570,
    'Cobalion': 580,
    'Perrserker': 440,
    'Bruxish': 475,
    'Sudowoodo': 410,
    'Regidrago': 580,
    'Chien-Pao': 570,
    'Cinderace': 530,
    'Samurott': 528,
    'Scyther': 500,
    'Coalossal': 510,
    'Gallade': 518,
    'Exeggutor': 530,
    'Leafeon': 525,
    'Weavile': 510,
    'Lurantis': 480,
    'Cloyster': 525,
    'Indeedee': 475,
    'Serperior': 528,
    'Magcargo': 430,
    'Flapple': 485,
    'Venomoth': 450,
    'Passimian': 490,
    'Infernape': 534,
    'Vespiquen': 474,
    'Noctowl': 452,
    'Drednaw': 485,
    'Crabominable': 478,
    'Ludicolo': 480,
    'Leavanny': 500,
    'Medicham': 410,
    'Dipplin': 485,
    'Zarude': 600,
    'Basculin': 460,
    'Rhydon': 485,
    'Avalugg': 514,
    'Blaziken': 530,
    'Breloom': 460,
    'Shiftry': 480,
    'Dodrio': 470,
    'Appletun': 485,
    'Bastiodon': 495,
    'Kommo-o': 600,
    'Stonjourner': 470,
    'Noivern': 535,
    'Virizion': 580,
    'Minior': 440,
    'Vivillon': 411,
    'Tropius': 460,
    'Altaria': 490,
    'Zoroark': 510,
    
    # Formas alternativas
    'Rotom-Wash': 520,
    'Rotom-Heat': 520,
    'Rotom-Frost': 520,
    'Rotom-Fan': 520,
    'Rotom-Mow': 520,
    'Landorus-Therian': 600,
    'Thundurus-Therian': 580,
    'Tornadus-Therian': 580,
    'Urshifu': 550,
    'Urshifu-Rapid-Strike': 550,
    'Enamorus': 580,
    'Enamorus-Therian': 580,
    'Ogerpon-Wellspring': 550,
    'Ogerpon-Hearthflame': 550,
    'Ogerpon-Cornerstone': 550,
    
    # Aliases para nombres truncados en dataset
    'Ho': 680,  # Ho-Oh truncado
    'Ting': 680,  # Parte de "Ho-Oh"
    'Chi': 570,  # Chi-Yu truncado
    'Wo': 570,  # Wo-Chien truncado
    'Chien': 570,  # Chien-Pao truncado
    'Kommo': 600,  # Kommo-o truncado
}

# Tiers competitivos (Smogon)
POKEMON_TIERS = {
    'Uber': [
        'Arceus', 'Mewtwo', 'Lugia', 'Ho-Oh', 'Rayquaza', 'Dialga', 'Palkia', 'Giratina',
        'Reshiram', 'Zekrom', 'Kyurem', 'Xerneas', 'Yveltal', 'Zygarde', 'Solgaleo', 'Lunala',
        'Necrozma', 'Zacian', 'Zamazenta', 'Eternatus', 'Calyrex', 'Koraidon', 'Miraidon',
        'Kyogre', 'Groudon', 'Flutter Mane', 'Chi-Yu'
    ],
    'OU': [  # OverUsed
        'Dragonite', 'Tyranitar', 'Salamence', 'Metagross', 'Garchomp', 'Hydreigon',
        'Goodra', 'Kommo-o', 'Dragapult', 'Baxcalibur', 'Landorus', 'Heatran',
        'Gholdengo', 'Kingambit', 'Iron Valiant', 'Great Tusk', 'Roaring Moon',
        'Volcarona', 'Greninja', 'Toxapex', 'Ferrothorn', 'Rotom-Wash'
    ],
    'UU': [  # UnderUsed
        'Gengar', 'Alakazam', 'Machamp', 'Magnezone', 'Lucario', 'Togekiss',
        'Excadrill', 'Conkeldurr', 'Chandelure', 'Haxorus', 'Talonflame', 'Aegislash',
        'Sylveon', 'Mimikyu', 'Annihilape', 'Tinkaton', 'Armarouge', 'Ceruledge'
    ]
}

def get_pokemon_types(species: str) -> list:
    """Obtiene los tipos de un Pokemon."""
    return POKEMON_TYPES.get(species, ['Normal'])

def get_pokemon_bst(species: str) -> int:
    """Obtiene el Base Stat Total de un Pokemon."""
    return POKEMON_BST.get(species, 400)  # Default 400 para desconocidos

def get_type_effectiveness(attacking_type: str, defending_type: str) -> float:
    """Obtiene la efectividad de un tipo atacando a otro."""
    return TYPE_EFFECTIVENESS.get((attacking_type, defending_type), 1.0)

def calculate_matchup_score(attacker_types: list, defender_types: list) -> float:
    """
    Calcula el score de matchup entre dos Pokemon.
    Retorna un valor donde:
    - 2.0+ = ventaja fuerte
    - 1.0 = neutral
    - 0.5- = desventaja
    """
    max_effectiveness = 1.0
    for att_type in attacker_types:
        for def_type in defender_types:
            effectiveness = get_type_effectiveness(att_type, def_type)
            max_effectiveness = max(max_effectiveness, effectiveness)
    return max_effectiveness

def is_legendary(species: str) -> bool:
    """Determina si un Pokemon es legendario (BST >= 580)."""
    bst = get_pokemon_bst(species)
    return bst >= 580

def is_pseudo_legendary(species: str) -> bool:
    """Determina si un Pokemon es pseudo-legendario (BST == 600)."""
    bst = get_pokemon_bst(species)
    return bst == 600

def get_pokemon_tier(species: str) -> str:
    """Obtiene el tier competitivo de un Pokemon."""
    for tier, pokemon_list in POKEMON_TIERS.items():
        if species in pokemon_list:
            return tier
    return 'RU'  # RarelyUsed por defecto
