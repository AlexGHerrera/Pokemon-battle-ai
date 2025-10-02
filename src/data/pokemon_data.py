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
