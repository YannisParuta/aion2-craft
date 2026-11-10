# Génère data.json à partir des données relevées sur guidemmo.com (calculateur craft AION 2)
import json

TYPES = {
    "sword": ["blacksmithing", "Épée", "Sword"],
    "greatsword": ["blacksmithing", "Espadon", "Greatsword"],
    "dagger": ["blacksmithing", "Dague", "Dagger"],
    "mace": ["blacksmithing", "Masse", "Mace"],
    "guarder": ["blacksmithing", "Garde", "Guard"],
    "orb": ["alchemy", "Orbe", "Orb"],
    "magicbook": ["alchemy", "Grimoire", "Spellbook"],
    "bow": ["jewelcrafting", "Arc", "Bow"],
    "staff": ["jewelcrafting", "Bâton", "Staff"],
    "necklace": ["jewelcrafting", "Collier", "Necklace"],
    "earring": ["jewelcrafting", "Boucles d'oreilles", "Earrings"],
    "ring": ["jewelcrafting", "Anneau", "Ring"],
    "helmet": ["tailoring", "Casque", "Helm"],
    "shoulder": ["tailoring", "Épaulières", "Pauldrons"],
    "torso": ["tailoring", "Torse", "Breastplate"],
    "pants": ["tailoring", "Jambières", "Greaves"],
    "gloves": ["tailoring", "Gants", "Gloves"],
    "boots": ["tailoring", "Bottes", "Boots"],
    "cape": ["tailoring", "Cape", "Cloak"],
}

# Pièces Balaur raffinées : 2 Essence de Balaur + réactif du marchand (vérifié en jeu et sur le wiki, nov. 2026)
INTER = {
    "Orichalcum Ingot": "Orichalcum Ore*2|Orichalcum Solvent (Bound)*1",
    "Fine Thick Balaur Horn": "Balaur's Essence*2|Zircon Hammer (Bound)*1",
    "Fine Hard Balaur Horn": "Balaur's Essence*2|Lazuli Hammer (Bound)*1",
    "Fine Durable Balaur Horn": "Balaur's Essence*2|Moonstone Hammer (Bound)*1",
    "Sapphire Decoration": "Sapphire Gemstone*2|Abrasive (Bound)*1",
    "Diamond Decoration": "Diamond Gemstone*2|Abrasive (Bound)*1",
    "Ruby Decoration": "Ruby Gemstone*2|Abrasive (Bound)*1",
    "Yggdrasil Wood": "Yggdrasil Log*2|Sandpaper (Bound)*1",
    "Magic Crystal": "Spiritstone*2|Catalyst (Bound)*1",
    "Enhanced Thick Balaur Scale": "Balaur's Essence*2|Lesser Dragon Scale Hardener (Bound)*1",
    "Enhanced Hard Balaur Scale": "Balaur's Essence*2|Intermediate Dragon Scale Hardener (Bound)*1",
    "Enhanced Durable Balaur Scale": "Balaur's Essence*2|Superior Dragon Scale Hardener (Bound)*1",
    "Asvata Wood": "Asvata Log*2|Sandpaper (Bound)*1",
    "Strong Leather": "Raw Leather*2",
    "Tanned Thick Balaur Leather": "Balaur's Essence*2|Lesser Dragon Leather Softener (Bound)*1",
    "Tanned Hard Balaur Leather": "Balaur's Essence*2|Intermediate Dragon Leather Softener (Bound)*1",
    "Tanned Durable Balaur Leather": "Balaur's Essence*2|Superior Dragon Leather Softener (Bound)*1",
}


def bs_weapon(base, lv):
    """Armes de forge (épée, espadon, dague, masse, garde) : recettes identiques."""
    w, e, a, s = lv
    B = f"Orichalcum {base}"
    D = f"Dragon Lord {base}"
    return [
        [B, w, "Orichalcum Ingot*3|Refining Stone*5|Odyle*2", f"Splendent {B}", "w"],
        [f"Expert's {B}", e, f"Splendent {B}*1|Expert's Refining Stone*5|Fine Orichalcum Ore*6|Fine Odyle*3", f"Expert's Splendent {B}", "e"],
        [f"Artisan's {B}", a, f"Expert's Splendent {B}*1|Artisan's Refining Stone*5|Pure Orichalcum Ore*8|Pure Odyle*4", f"Artisan's Splendent {B}", "a"],
        [f"Star {D}", s, f"Artisan's Splendent {B}*1|Artisan's Ultimate Refining Stone*4|Fine Thick Balaur Horn*22|Wrathful Mind*10|Radiant Orichalcum Ore*9|Radiant Odyle*5", f"Splendent Star {D}", "s1"],
        [f"Splendent Star {D}", None, "Fine Thick Balaur Horn*11|Wrathful Mind*4", "", "s1s"],
        [f"Dark {D}", None, f"Artisan's Splendent {B}*1|Artisan's Ultimate Refining Stone*5|Fine Hard Balaur Horn*29|Wrathful Mind*3|Wrathful Will*15|Radiant Orichalcum Ore*12|Radiant Odyle*7", f"Splendent Dark {D}", "s2"],
        [f"Splendent Dark {D}", None, "Fine Hard Balaur Horn*15|Wrathful Will*5|Radiant Orichalcum Ore*1|Radiant Odyle*2", "", "s2s"],
        [f"Ebony {D}", None, f"Artisan's Splendent {B}*1|Artisan's Ultimate Refining Stone*6|Fine Durable Balaur Horn*41|Wrathful Mind*3|Wrathful Will*3|Wrathful Ego*20|Radiant Orichalcum Ore*15|Radiant Odyle*9", f"Splendent Ebony {D}", "s3"],
        [f"Splendent Ebony {D}", None, "Artisan's Ultimate Refining Stone*2|Fine Durable Balaur Horn*21|Wrathful Ego*7|Radiant Orichalcum Ore*2|Radiant Odyle*3", "", "s3s"],
    ]


def asv_weapon(base):
    B = f"Asvata {base}"
    D = f"Dragon Lord {base}"
    return [
        [B, 3, "Asvata Wood*3|Refining Stone*5|Odyle*2", f"Splendent {B}", "w"],
        [f"Expert's {B}", 15, f"Splendent {B}*1|Expert's Refining Stone*5|Fine Asvata Log*6|Fine Odyle*3", f"Expert's Splendent {B}", "e"],
        [f"Artisan's {B}", 30, f"Expert's Splendent {B}*1|Artisan's Refining Stone*5|Pure Asvata Log*8|Pure Odyle*4", f"Artisan's Splendent {B}", "a"],
        [f"Star {D}", 55, f"Artisan's Splendent {B}*1|Artisan's Ultimate Refining Stone*4|Enhanced Thick Balaur Scale*22|Wrathful Mind*10|Radiant Asvata Log*9|Radiant Odyle*5", f"Splendent Star {D}", "s1"],
        [f"Splendent Star {D}", None, "Enhanced Thick Balaur Scale*11|Wrathful Mind*4", "", "s1s"],
        [f"Dark {D}", None, f"Artisan's Splendent {B}*1|Artisan's Ultimate Refining Stone*5|Enhanced Hard Balaur Scale*29|Wrathful Mind*3|Wrathful Will*15|Radiant Asvata Log*12|Radiant Odyle*7", f"Splendent Dark {D}", "s2"],
        [f"Splendent Dark {D}", None, "Enhanced Hard Balaur Scale*15|Wrathful Will*5|Radiant Asvata Log*1|Radiant Odyle*2", "", "s2s"],
        [f"Ebony {D}", None, f"Artisan's Splendent {B}*1|Artisan's Ultimate Refining Stone*6|Enhanced Durable Balaur Scale*41|Wrathful Mind*3|Wrathful Will*3|Wrathful Ego*20|Radiant Asvata Log*15|Radiant Odyle*9", f"Splendent Ebony {D}", "s3"],
        [f"Splendent Ebony {D}", None, "Artisan's Ultimate Refining Stone*2|Enhanced Durable Balaur Scale*21|Wrathful Ego*7|Radiant Asvata Log*2|Radiant Odyle*3", "", "s3s"],
    ]


def magic(base, gem):
    B = f"Truth {base}"
    D = f"Dragon Lord {base}"
    return [
        [B, 3, "Magic Crystal*3|Refining Stone*5|Odyle*2", f"Splendent {B}", "w"],
        [f"Expert's {B}", 15, f"Splendent {B}*1|Expert's Refining Stone*5|Fine {gem} Gemstone*6|Fine Odyle*3", f"Expert's Splendent {B}", "e"],
        [f"Artisan's {B}", 30, f"Expert's Splendent {B}*1|Artisan's Refining Stone*5|Pure {gem} Gemstone*8|Pure Odyle*4", f"Artisan's Splendent {B}", "a"],
        [f"Star {D}", 55, f"Artisan's Splendent {B}*1|Artisan's Ultimate Refining Stone*4|Enhanced Thick Balaur Scale*22|Wrathful Mind*10|Radiant {gem} Gemstone*9|Radiant Odyle*5", f"Splendent Star {D}", "s1"],
        [f"Splendent Star {D}", None, "Enhanced Thick Balaur Scale*11|Wrathful Mind*4", "", "s1s"],
        [f"Dark {D}", None, f"Artisan's Splendent {B}*1|Artisan's Ultimate Refining Stone*5|Enhanced Hard Balaur Scale*29|Wrathful Mind*3|Wrathful Will*15|Radiant {gem} Gemstone*12|Radiant Odyle*7", f"Splendent Dark {D}", "s2"],
        [f"Splendent Dark {D}", None, f"Enhanced Hard Balaur Scale*15|Wrathful Will*5|Radiant {gem} Gemstone*1|Radiant Odyle*2", "", "s2s"],
        [f"Ebony {D}", None, f"Artisan's Splendent {B}*1|Artisan's Ultimate Refining Stone*6|Enhanced Durable Balaur Scale*41|Wrathful Mind*3|Wrathful Will*3|Wrathful Ego*20|Radiant {gem} Gemstone*15|Radiant Odyle*9", f"Splendent Ebony {D}", "s3"],
        [f"Splendent Ebony {D}", None, f"Artisan's Ultimate Refining Stone*2|Enhanced Durable Balaur Scale*21|Wrathful Ego*7|Radiant {gem} Gemstone*2|Radiant Odyle*3", "", "s3s"],
    ]


def S(rows):
    """Lignes explicites : [nom, niveau, ingrédients, combo, palier]."""
    return rows


CHAINS = {
    "sword": bs_weapon("Longsword", (3, 15, 30, 55)),
    "greatsword": bs_weapon("Greatsword", (3, 15, 30, 55)),
    "dagger": bs_weapon("Dagger", (3, 15, 30, 55)),
    "mace": bs_weapon("Mace", (3, 15, 30, 55)),
    "guarder": bs_weapon("Guard", (5, 20, 35, 60)),
    "bow": asv_weapon("Bow"),
    "staff": asv_weapon("Staff"),
    "magicbook": magic("Spellbook", "Ruby"),
    "orb": magic("Orb", "Sapphire"),
    "necklace": [
        ["Ruby Necklace", 10, "Ruby Decoration*1|Refining Stone*4|Odyle*1", "Splendent Ruby Necklace", "w"],
        ["Expert's Ruby Necklace", 25, "Splendent Ruby Necklace*1|Expert's Refining Stone*4|Fine Ruby Gemstone*4|Fine Odyle*2", "Expert's Splendent Ruby Necklace", "e"],
        ["Artisan's Ruby Necklace", 40, "Expert's Splendent Ruby Necklace*1|Artisan's Refining Stone*4|Pure Ruby Gemstone*5|Pure Odyle*2", "Artisan's Splendent Ruby Necklace", "a"],
        ["Star Dragon Lord Necklace", 60, "Artisan's Splendent Ruby Necklace*1|Artisan's Ultimate Refining Stone*3|Enhanced Thick Balaur Scale*14|Wrathful Mind*6|Radiant Ruby Gemstone*6|Radiant Odyle*2", "Splendent Star Dragon Lord Necklace", "s1"],
        ["Splendent Star Dragon Lord Necklace", None, "Enhanced Thick Balaur Scale*7|Wrathful Mind*2", "", "s1s"],
        ["Dark Dragon Lord Necklace", None, "Artisan's Splendent Ruby Necklace*1|Artisan's Ultimate Refining Stone*3|Enhanced Hard Balaur Scale*19|Wrathful Mind*2|Wrathful Will*9|Radiant Ruby Gemstone*8|Radiant Odyle*5", "Splendent Dark Dragon Lord Necklace", "s2"],
        ["Splendent Dark Dragon Lord Necklace", None, "Enhanced Hard Balaur Scale*10|Wrathful Will*3|Radiant Ruby Gemstone*1|Radiant Odyle*1", "", "s2s"],
        ["Ebony Dragon Lord Necklace", None, "Artisan's Splendent Ruby Necklace*1|Artisan's Ultimate Refining Stone*4|Enhanced Durable Balaur Scale*26|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*12|Radiant Ruby Gemstone*8|Radiant Odyle*7", "Splendent Ebony Dragon Lord Necklace", "s3"],
        ["Splendent Ebony Dragon Lord Necklace", None, "Artisan's Ultimate Refining Stone*1|Enhanced Durable Balaur Scale*13|Wrathful Ego*4|Radiant Ruby Gemstone*2|Radiant Odyle*2", "", "s3s"],
    ],
    "earring": [
        ["Diamond Earrings", 5, "Diamond Decoration*1|Refining Stone*3|Odyle*1", "Splendent Diamond Earrings", "w"],
        ["Expert's Diamond Earrings", 20, "Splendent Diamond Earrings*1|Expert's Refining Stone*3|Fine Diamond Gemstone*3|Fine Odyle*2", "Expert's Splendent Diamond Earrings", "e"],
        ["Artisan's Diamond Earrings", 35, "Expert's Splendent Diamond Earrings*1|Artisan's Refining Stone*3|Pure Diamond Gemstone*4|Pure Odyle*2", "Artisan's Splendent Diamond Earrings", "a"],
        ["Star Dragon Lord Earrings", 60, "Artisan's Splendent Diamond Earrings*1|Artisan's Ultimate Refining Stone*2|Enhanced Thick Balaur Scale*11|Wrathful Mind*5|Radiant Diamond Gemstone*5|Radiant Odyle*2", "Splendent Star Dragon Lord Earrings", "s1"],
        ["Splendent Star Dragon Lord Earrings", None, "Enhanced Thick Balaur Scale*6|Wrathful Mind*2", "", "s1s"],
        ["Dark Dragon Lord Earrings", None, "Artisan's Splendent Diamond Earrings*1|Artisan's Ultimate Refining Stone*3|Enhanced Hard Balaur Scale*15|Wrathful Mind*2|Wrathful Will*8|Radiant Diamond Gemstone*6|Radiant Odyle*4", "Splendent Dark Dragon Lord Earrings", "s2"],
        ["Splendent Dark Dragon Lord Earrings", None, "Enhanced Hard Balaur Scale*8|Wrathful Will*3|Radiant Diamond Gemstone*1|Radiant Odyle*1", "", "s2s"],
        ["Ebony Dragon Lord Earrings", None, "Artisan's Splendent Diamond Earrings*1|Artisan's Ultimate Refining Stone*3|Enhanced Durable Balaur Scale*21|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*11|Radiant Diamond Gemstone*7|Radiant Odyle*5", "Splendent Ebony Dragon Lord Earrings", "s3"],
        ["Splendent Ebony Dragon Lord Earrings", None, "Artisan's Ultimate Refining Stone*1|Enhanced Durable Balaur Scale*11|Wrathful Ego*4|Radiant Diamond Gemstone*2|Radiant Odyle*2", "", "s3s"],
    ],
    "ring": [
        ["Sapphire Ring", 3, "Sapphire Decoration*1|Refining Stone*2|Odyle*1", "Splendent Sapphire Ring", "w"],
        ["Expert's Sapphire Ring", 15, "Splendent Sapphire Ring*1|Expert's Refining Stone*2|Fine Sapphire Gemstone*2|Fine Odyle*1", "Expert's Splendent Sapphire Ring", "e"],
        ["Artisan's Sapphire Ring", 30, "Expert's Splendent Sapphire Ring*1|Artisan's Refining Stone*2|Pure Sapphire Gemstone*3|Pure Odyle*1", "Artisan's Splendent Sapphire Ring", "a"],
        ["Star Dragon Lord Ring", 55, "Artisan's Splendent Sapphire Ring*1|Artisan's Ultimate Refining Stone*2|Enhanced Thick Balaur Scale*8|Wrathful Mind*4|Radiant Sapphire Gemstone*3|Radiant Odyle*2", "Splendent Star Dragon Lord Ring", "s1"],
        ["Splendent Star Dragon Lord Ring", None, "Enhanced Thick Balaur Scale*4|Wrathful Mind*2", "", "s1s"],
        ["Dark Dragon Lord Ring", None, "Artisan's Splendent Sapphire Ring*1|Artisan's Ultimate Refining Stone*2|Enhanced Hard Balaur Scale*11|Wrathful Mind*2|Wrathful Will*6|Radiant Sapphire Gemstone*5|Radiant Odyle*3", "Splendent Dark Dragon Lord Ring", "s2"],
        ["Splendent Dark Dragon Lord Ring", None, "Enhanced Hard Balaur Scale*6|Wrathful Will*2|Radiant Sapphire Gemstone*1|Radiant Odyle*1", "", "s2s"],
        ["Ebony Dragon Lord Ring", None, "Artisan's Splendent Sapphire Ring*1|Artisan's Ultimate Refining Stone*2|Enhanced Durable Balaur Scale*16|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*8|Radiant Sapphire Gemstone*5|Radiant Odyle*3", "Splendent Ebony Dragon Lord Ring", "s3"],
        ["Splendent Ebony Dragon Lord Ring", None, "Artisan's Ultimate Refining Stone*1|Enhanced Durable Balaur Scale*8|Wrathful Ego*3|Radiant Sapphire Gemstone*2|Radiant Odyle*2", "", "s3s"],
    ],
    "torso": [
        ["Orichalcum Breastplate", 3, "Orichalcum Ingot*2|Strong Leather*4|Refining Stone*3|Odyle*1", "Splendent Orichalcum Breastplate", "w"],
        ["Expert's Orichalcum Breastplate", 15, "Splendent Orichalcum Breastplate*1|Expert's Refining Stone*3|Fine Orichalcum Ore*4|Fine Odyle*2", "Expert's Splendent Orichalcum Breastplate", "e"],
        ["Artisan's Orichalcum Breastplate", 30, "Expert's Splendent Orichalcum Breastplate*1|Artisan's Refining Stone*3|Pure Orichalcum Ore*5|Pure Odyle*3", "Artisan's Splendent Orichalcum Breastplate", "a"],
        ["Star Dragon Lord Breastplate", 55, "Artisan's Splendent Orichalcum Breastplate*1|Artisan's Ultimate Refining Stone*3|Tanned Thick Balaur Leather*15|Wrathful Mind*7|Radiant Orichalcum Ore*6|Radiant Odyle*3", "Splendent Star Dragon Lord Breastplate", "s1"],
        ["Splendent Star Dragon Lord Breastplate", None, "Tanned Thick Balaur Leather*8|Wrathful Mind*3", "", "s1s"],
        ["Dark Dragon Lord Breastplate", None, "Artisan's Splendent Orichalcum Breastplate*1|Artisan's Ultimate Refining Stone*3|Tanned Hard Balaur Leather*19|Wrathful Mind*2|Wrathful Will*10|Radiant Orichalcum Ore*8|Radiant Odyle*5", "Splendent Dark Dragon Lord Breastplate", "s2"],
        ["Splendent Dark Dragon Lord Breastplate", None, "Tanned Hard Balaur Leather*10|Wrathful Will*4|Radiant Orichalcum Ore*1|Radiant Odyle*1", "", "s2s"],
        ["Ebony Dragon Lord Breastplate", None, "Artisan's Splendent Orichalcum Breastplate*1|Artisan's Ultimate Refining Stone*4|Tanned Durable Balaur Leather*27|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*13|Radiant Orichalcum Ore*10|Radiant Odyle*6", "Splendent Ebony Dragon Lord Breastplate", "s3"],
        ["Splendent Ebony Dragon Lord Breastplate", None, "Artisan's Ultimate Refining Stone*1|Tanned Durable Balaur Leather*14|Wrathful Ego*5|Radiant Orichalcum Ore*2|Radiant Odyle*2", "", "s3s"],
    ],
    "pants": [
        ["Orichalcum Greaves", 3, "Orichalcum Ingot*2|Strong Leather*3|Refining Stone*2|Odyle*1", "Splendent Orichalcum Greaves", "w"],
        ["Expert's Orichalcum Greaves", 15, "Splendent Orichalcum Greaves*1|Expert's Refining Stone*2|Fine Orichalcum Ore*3|Fine Odyle*2", "Expert's Splendent Orichalcum Greaves", "e"],
        ["Artisan's Orichalcum Greaves", 30, "Expert's Splendent Orichalcum Greaves*1|Artisan's Refining Stone*2|Pure Orichalcum Ore*4|Pure Odyle*2", "Artisan's Splendent Orichalcum Greaves", "a"],
        ["Star Dragon Lord Greaves", 55, "Artisan's Splendent Orichalcum Greaves*1|Artisan's Ultimate Refining Stone*2|Tanned Thick Balaur Leather*11|Wrathful Mind*5|Radiant Orichalcum Ore*4|Radiant Odyle*2", "Splendent Star Dragon Lord Greaves", "s1"],
        ["Splendent Star Dragon Lord Greaves", None, "Tanned Thick Balaur Leather*6|Wrathful Mind*2", "", "s1s"],
        ["Dark Dragon Lord Greaves", None, "Artisan's Splendent Orichalcum Greaves*1|Artisan's Ultimate Refining Stone*2|Tanned Hard Balaur Leather*14|Wrathful Mind*2|Wrathful Will*8|Radiant Orichalcum Ore*6|Radiant Odyle*4", "Splendent Dark Dragon Lord Greaves", "s2"],
        ["Splendent Dark Dragon Lord Greaves", None, "Tanned Hard Balaur Leather*7|Wrathful Will*3|Radiant Orichalcum Ore*1|Radiant Odyle*1", "", "s2s"],
        ["Ebony Dragon Lord Greaves", None, "Artisan's Splendent Orichalcum Greaves*1|Artisan's Ultimate Refining Stone*4|Tanned Durable Balaur Leather*20|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*11|Radiant Orichalcum Ore*8|Radiant Odyle*5", "Splendent Ebony Dragon Lord Greaves", "s3"],
        ["Splendent Ebony Dragon Lord Greaves", None, "Artisan's Ultimate Refining Stone*1|Tanned Durable Balaur Leather*10|Wrathful Ego*4|Radiant Orichalcum Ore*2|Radiant Odyle*2", "", "s3s"],
    ],
}


def armor(base, lv, w_in, e_in, a_in, s1_in, s1s_in, s2_in, s2s_in, s3_in, s3s_in):
    """Pièces d'armure à recettes courtes (casque, épaulières, gants, bottes, cape)."""
    B = f"Orichalcum {base}"
    D = f"Dragon Lord {base}"
    lw, le, la, ls = lv
    return [
        [B, lw, w_in, f"Splendent {B}", "w"],
        [f"Expert's {B}", le, f"Splendent {B}*1|" + e_in, f"Expert's Splendent {B}", "e"],
        [f"Artisan's {B}", la, f"Expert's Splendent {B}*1|" + a_in, f"Artisan's Splendent {B}", "a"],
        [f"Star {D}", ls, f"Artisan's Splendent {B}*1|" + s1_in, f"Splendent Star {D}", "s1"],
        [f"Splendent Star {D}", None, s1s_in, "", "s1s"],
        [f"Dark {D}", None, f"Artisan's Splendent {B}*1|" + s2_in, f"Splendent Dark {D}", "s2"],
        [f"Splendent Dark {D}", None, s2s_in, "", "s2s"],
        [f"Ebony {D}", None, f"Artisan's Splendent {B}*1|" + s3_in, f"Splendent Ebony {D}", "s3"],
        [f"Splendent Ebony {D}", None, s3s_in, "", "s3s"],
    ]


CHAINS["helmet"] = armor("Helm", (3, 15, 30, 55),
    "Orichalcum Ingot*1|Strong Leather*3|Refining Stone*2|Odyle*1",
    "Expert's Refining Stone*2|Fine Orichalcum Ore*3|Fine Odyle*1",
    "Artisan's Refining Stone*2|Pure Orichalcum Ore*3|Pure Odyle*2",
    "Artisan's Ultimate Refining Stone*2|Tanned Thick Balaur Leather*9|Wrathful Mind*4|Radiant Orichalcum Ore*3|Radiant Odyle*2",
    "Tanned Thick Balaur Leather*5|Wrathful Mind*2",
    "Artisan's Ultimate Refining Stone*2|Tanned Hard Balaur Leather*12|Wrathful Mind*2|Wrathful Will*6|Radiant Orichalcum Ore*5|Radiant Odyle*3",
    "Tanned Hard Balaur Leather*6|Wrathful Will*2|Radiant Orichalcum Ore*1|Radiant Odyle*1",
    "Artisan's Ultimate Refining Stone*4|Tanned Durable Balaur Leather*17|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*8|Radiant Orichalcum Ore*7|Radiant Odyle*4",
    "Artisan's Ultimate Refining Stone*1|Tanned Durable Balaur Leather*9|Wrathful Ego*3|Radiant Orichalcum Ore*2|Radiant Odyle*2")

CHAINS["shoulder"] = armor("Pauldrons", (5, 20, 35, 55),
    "Orichalcum Ingot*1|Strong Leather*3|Refining Stone*2|Odyle*1",
    "Expert's Refining Stone*2|Fine Orichalcum Ore*3|Fine Odyle*1",
    "Artisan's Refining Stone*2|Pure Orichalcum Ore*3|Pure Odyle*2",
    "Artisan's Ultimate Refining Stone*2|Tanned Thick Balaur Leather*9|Wrathful Mind*4|Radiant Orichalcum Ore*3|Radiant Odyle*2",
    "Tanned Thick Balaur Leather*5|Wrathful Mind*2",
    "Artisan's Ultimate Refining Stone*2|Tanned Hard Balaur Leather*12|Wrathful Mind*2|Wrathful Will*6|Radiant Orichalcum Ore*5|Radiant Odyle*3",
    "Tanned Hard Balaur Leather*6|Wrathful Will*2|Radiant Orichalcum Ore*1|Radiant Odyle*1",
    "Artisan's Ultimate Refining Stone*4|Tanned Durable Balaur Leather*17|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*8|Radiant Orichalcum Ore*7|Radiant Odyle*4",
    "Artisan's Ultimate Refining Stone*1|Tanned Durable Balaur Leather*9|Wrathful Ego*3|Radiant Orichalcum Ore*2|Radiant Odyle*2")

CHAINS["gloves"] = armor("Gloves", (5, 20, 35, 60),
    "Orichalcum Ingot*1|Strong Leather*2|Refining Stone*2|Odyle*1",
    "Expert's Refining Stone*2|Fine Orichalcum Ore*2|Fine Odyle*1",
    "Artisan's Refining Stone*2|Pure Orichalcum Ore*3|Pure Odyle*2",
    "Artisan's Ultimate Refining Stone*2|Tanned Thick Balaur Leather*7|Wrathful Mind*3|Radiant Orichalcum Ore*2|Radiant Odyle*2",
    "Tanned Thick Balaur Leather*4|Wrathful Mind*1",
    "Artisan's Ultimate Refining Stone*2|Tanned Hard Balaur Leather*10|Wrathful Mind*2|Wrathful Will*5|Radiant Orichalcum Ore*4|Radiant Odyle*2",
    "Tanned Hard Balaur Leather*5|Wrathful Will*2|Radiant Orichalcum Ore*1|Radiant Odyle*1",
    "Artisan's Ultimate Refining Stone*2|Tanned Durable Balaur Leather*14|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*7|Radiant Orichalcum Ore*6|Radiant Odyle*3",
    "Artisan's Ultimate Refining Stone*1|Tanned Durable Balaur Leather*7|Wrathful Ego*3|Radiant Orichalcum Ore*2|Radiant Odyle*2")

CHAINS["boots"] = armor("Boots", (10, 25, 40, 60),
    "Orichalcum Ingot*1|Strong Leather*3|Refining Stone*2|Odyle*1",
    "Expert's Refining Stone*2|Fine Orichalcum Ore*3|Fine Odyle*1",
    "Artisan's Refining Stone*2|Pure Orichalcum Ore*3|Pure Odyle*2",
    "Artisan's Ultimate Refining Stone*2|Tanned Thick Balaur Leather*9|Wrathful Mind*5|Radiant Orichalcum Ore*2|Radiant Odyle*2",
    "Tanned Thick Balaur Leather*5|Wrathful Mind*2",
    "Artisan's Ultimate Refining Stone*3|Tanned Hard Balaur Leather*12|Wrathful Mind*2|Wrathful Will*8|Radiant Orichalcum Ore*5|Radiant Odyle*3",
    "Tanned Hard Balaur Leather*6|Wrathful Will*3|Radiant Orichalcum Ore*1|Radiant Odyle*1",
    "Artisan's Ultimate Refining Stone*3|Tanned Durable Balaur Leather*17|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*11|Radiant Orichalcum Ore*8|Radiant Odyle*4",
    "Artisan's Ultimate Refining Stone*1|Tanned Durable Balaur Leather*9|Wrathful Ego*4|Radiant Orichalcum Ore*2|Radiant Odyle*2")

CHAINS["cape"] = armor("Cloak", (10, 25, 40, 60),
    "Orichalcum Ingot*1|Strong Leather*2|Refining Stone*2|Odyle*1",
    "Expert's Refining Stone*2|Fine Orichalcum Ore*2|Fine Odyle*1",
    "Artisan's Refining Stone*2|Pure Orichalcum Ore*3|Pure Odyle*2",
    "Artisan's Ultimate Refining Stone*2|Tanned Thick Balaur Leather*7|Wrathful Mind*3|Radiant Orichalcum Ore*2|Radiant Odyle*2",
    "Tanned Thick Balaur Leather*4|Wrathful Mind*1",
    "Artisan's Ultimate Refining Stone*2|Tanned Hard Balaur Leather*10|Wrathful Mind*2|Wrathful Will*5|Radiant Orichalcum Ore*4|Radiant Odyle*2",
    "Tanned Hard Balaur Leather*5|Wrathful Will*2|Radiant Orichalcum Ore*1|Radiant Odyle*1",
    "Artisan's Ultimate Refining Stone*2|Tanned Durable Balaur Leather*14|Wrathful Mind*2|Wrathful Will*2|Wrathful Ego*7|Radiant Orichalcum Ore*6|Radiant Odyle*3",
    "Artisan's Ultimate Refining Stone*1|Tanned Durable Balaur Leather*7|Wrathful Ego*3|Radiant Orichalcum Ore*2|Radiant Odyle*2")

# Taux de réussite max (%) selon (niveau métier - niveau recette), relevés en jeu par guidemmo.
TABS = {
    "w": [74.011698,74.718902,75.631177,77.467106,77.669025,78.187021,79.129959,80.157193,80.991798,81.227508,81.43995,82.755613,83.462816,84.356316,84.662035,84.662035,84.662035,85.511803,86.547794,86.547794,87.390018,87.761514,87.761514,87.761514,87.761514,88.157714,88.157714,89.432365,89.432365,90.252757,90.252757,90.676961,90.676961,90.676961,90.676961,90.676961,90.676961,90.676961,91.865563,91.865563,91.865563,92.71533,92.71533,92.71533,93.121326],
    "e": [77.981229,78.681229,79.381229,80.081229,80.781229,81.481229,82.181229,82.881229,83.645249,84.508476,85.061212,85.207336,85.600142,86.372065,87.164426,87.773575,88.05,88.33,88.6,88.87595,89.631358,90.258876,90.467432,90.467432,90.467432,90.467432,91.0588,91.84441,91.84441,92.428919,92.428919,92.671025,92.671025,92.671025,92.671025,92.921018,92.921018,93.808071,93.808071,94.371089,94.371089,94.371089,94.633946],
    "a": [79.571081,80.124386,80.926125,82.284634,82.883323,83.573495,84.114718,85.476782,85.793152,86.556753,87.198972,87.923635,88.210967,88.356177,88.887385,90.030461,90.05525,90.526988,90.526988,90.804885,91.392014,91.969241,92.390526,92.50524,92.50524,92.60178,93.157574,93.157574,93.703275,94.12331,94.12331,94.258973,94.258973,94.258973,94.645133,94.645133,95.200927,95.200927,95.587774,95.587774,95.724539,95.739046,95.739046,95.739046,95.739046,95.888298,95.888298,96.467538,96.467538,96.467538,96.837241],
    "s1": [67.506212,68.198244,69.824562,71.774814,72.773479,74.093554,75.222343,76.203609,77.541261,78.466072,79.033485,80.772127,81.148839,81.583644,82.889213,83.38122,83.713424,84.62849,85.309191,85.836292,86.168055,86.922289,87.551611,88.112297,88.383568,88.600967,89.048631,89.610372,89.9,90.19,90.474499,90.594902,90.971587,91.491841,91.491841,92.029715,92.360459,92.443413,92.443413,92.673487,92.673487,93.175734,93.662103,93.662103,94.008885,94.008885,94.102514,94.179641,94.179641,94.639789],
}

# Prix HdV de secours relevés par guidemmo le 2026-10-05 (modifiables dans l'appli)
PRICES = {"Wrathful Mind":479000,"Wrathful Will":3000000,"Wrathful Ego":209000,"Odyle":6400,"Fine Odyle":5494,"Pure Odyle":120000,"Radiant Odyle":300000,"Refining Stone":6700,"Expert's Refining Stone":94500,"Artisan's Refining Stone":300000,"Artisan's Ultimate Refining Stone":259000,"Thick Balaur Horn":1700,"Hard Balaur Horn":1150,"Durable Balaur Horn":1000,"Thick Balaur Scale":5700,"Hard Balaur Scale":2400,"Durable Balaur Scale":1888,"Thick Balaur Leather":1219,"Hard Balaur Leather":900,"Durable Balaur Leather":1260,"Spiritstone":9480,"Orichalcum Ore":150,"Fine Orichalcum Ore":200,"Pure Orichalcum Ore":4307,"Radiant Orichalcum Ore":230000,"Asvata Log":5580,"Fine Asvata Log":400,"Pure Asvata Log":2000,"Radiant Asvata Log":420000,"Sapphire Gemstone":5000,"Fine Sapphire Gemstone":3500,"Pure Sapphire Gemstone":84000,"Radiant Sapphire Gemstone":100000,"Diamond Gemstone":170,"Fine Diamond Gemstone":200,"Pure Diamond Gemstone":6800,"Radiant Diamond Gemstone":220000,"Ruby Gemstone":190,"Fine Ruby Gemstone":290,"Pure Ruby Gemstone":7500,"Radiant Ruby Gemstone":225000,"Raw Leather":5776,"Orichalcum Solvent (Bound)":400,"Abrasive (Bound)":400,"Catalyst (Bound)":400,"Sandpaper (Bound)":400,"Zircon Hammer (Bound)":4650,"Lazuli Hammer (Bound)":5600,"Moonstone Hammer (Bound)":6550,"Lesser Dragon Scale Hardener (Bound)":4650,"Intermediate Dragon Scale Hardener (Bound)":5600,"Superior Dragon Scale Hardener (Bound)":6550,"Lesser Dragon Leather Softener (Bound)":4650,"Intermediate Dragon Leather Softener (Bound)":5600,"Superior Dragon Leather Softener (Bound)":6550}


# Provenance des matériaux de base, relevée sur le wiki AION 2 (aion2.wiki.fextralife.com, fiches objet, nov. 2026).
# Noms de zones/donjons laissés en anglais (comme sur le wiki).
GROUPS = [
    ["pnj", "Marchand PNJ (lié)", "Prix fixe chez le marchand de métier, Verteron ou Altgard"],
    ["essence", "Extraction d'essence", "Récolte sur les nœuds de minerai, de gemmes et de bois"],
    ["od", "Extraction d'Od", "Récolte en vol sur les nœuds d'Od"],
    ["butin", "Butin de monstres", "Lâché par les monstres des zones ouvertes"],
    ["raffinage", "Pierres de raffinage", "Monstres, donjons, coffres et boutique de saison"],
    ["balaur", "Essence de Balaur", "Base des cornes, écailles et cuirs Balaur raffinés"],
    ["rage", "Donjons Conquête et raid : matériaux de rage", "Donjons en mode Conquête, raid Ludra, boutique de saison"],
]
_SHOP = {"Blacksmith": "marchand de forge d'armes", "Armorsmith": "marchand de forge d'armures",
         "Handicraft": "marchand d'artisanat", "Alchemy": "marchand d'alchimie"}
_PNJ = {  # nom : marchands
    "Orichalcum Solvent (Bound)": "Blacksmith Armorsmith", "Abrasive (Bound)": "Handicraft", "Sandpaper (Bound)": "Handicraft",
    "Catalyst (Bound)": "Handicraft Alchemy", "Zircon Hammer (Bound)": "Blacksmith", "Lazuli Hammer (Bound)": "Blacksmith",
    "Moonstone Hammer (Bound)": "Blacksmith",
    "Lesser Dragon Scale Hardener (Bound)": "Handicraft Alchemy", "Intermediate Dragon Scale Hardener (Bound)": "Handicraft Alchemy",
    "Superior Dragon Scale Hardener (Bound)": "Handicraft Alchemy",
    "Lesser Dragon Leather Softener (Bound)": "Armorsmith", "Intermediate Dragon Leather Softener (Bound)": "Armorsmith",
    "Superior Dragon Leather Softener (Bound)": "Armorsmith",
}
_SEASON = {"Refining Stone": 40, "Expert's Refining Stone": 400, "Artisan's Refining Stone": 4000,
           "Artisan's Ultimate Refining Stone": 4800, "Wrathful Mind": 6250, "Wrathful Will": 7500, "Wrathful Ego": 8750}
_RAGE = {"Wrathful Mind": "les 6 donjons (Conquête)", "Wrathful Will": "Urugugu Canyon, Fire Temple, Vakron Sky Island, Ferocious Horn Den (Conquête)",
         "Wrathful Ego": "Fire Temple, Ferocious Horn Den (Conquête)"}


def _k(x):
    return f"{x:,}".replace(",", "\u202f")


def source(n):
    """-> [groupe, détail] pour un matériau de base"""
    if n in _PNJ:
        who = " / ".join(_SHOP[k] for k in _PNJ[n].split())
        return ["pnj", f"{who} · {_k(PRICES[n])} kinah"]
    if n.endswith("Odyle"):
        return ["od", "Verteron, Altgard, Chaotic Lower Reshanta" + (" · boutique de saison 6 000 pièces" if n == "Radiant Odyle" else "")]
    if n.endswith(("Ore", "Gemstone")):
        return ["essence", ("Minerai" if n.endswith("Ore") else "Gemmes") + " · Verteron, Altgard"]
    if n.endswith("Log"):
        return ["essence", "Bois · " + ("Verteron" if "Yggdrasil" in n else "Altgard")]
    if n in ("Raw Leather", "Spiritstone"):
        return ["butin", "Monstres d'Altgard, Verteron, Chaotic Lower Reshanta · Shulak Loot Bundle"]
    if n.endswith("Refining Stone"):
        return ["raffinage", f"Monstres, donjons, Refining Stone Chest · boutique de saison {_k(_SEASON[n])} pièces de serment"]
    if n == "Balaur's Essence":
        return ["balaur", "Boss élites de Verteron, Altgard, Chaotic Lower Reshanta · les 6 donjons (Conquête) · raid Ludra · non vendable au marchand"]
    if n in _RAGE:
        return ["rage", f"{_RAGE[n]}, raid Ludra · boutique de saison {_k(_SEASON[n])} pièces de serment"]
    raise KeyError("provenance inconnue : " + n)


def parse(s):
    return [[p.rsplit("*", 1)[0], int(p.rsplit("*", 1)[1])] for p in s.split("|")]


if __name__ == "__main__":
    fr = json.load(open("fr.json", encoding="utf-8"))
    chains = {}
    for t, rows in CHAINS.items():
        chains[t] = [{"n": n, "lv": lv, "in": parse(i), "combo": c, "k": k} for n, lv, i, c, k in rows]
    inter = {k: parse(v) for k, v in INTER.items()}
    data = {"types": TYPES, "chains": chains, "inter": inter, "tabs": TABS, "prices": PRICES,
            "pricesDate": "2026-10-05", "fr": fr, "groups": GROUPS}
    made = {r["n"] for t in chains for r in chains[t]} | {r["combo"] for t in chains for r in chains[t]} | set(inter)
    raw = sorted({x for t in chains for r in chains[t] for x, _ in r["in"]} | {x for v in inter.values() for x, _ in v})
    data["sources"] = {n: source(n) for n in raw if n not in made}
    json.dump(data, open("data.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    # empreinte pour vérifier contre la source
    sig = {t: sum(q for r in chains[t] for _, q in r["in"]) for t in chains}
    print(json.dumps(sig, sort_keys=True))
    names = sorted({x for t in chains for r in chains[t] for x, _ in r["in"]} | {r["n"] for t in chains for r in chains[t]} | {r["combo"] for t in chains for r in chains[t] if r["combo"]} | set(inter) | {x for v in inter.values() for x, _ in v})
    print("noms:", len(names), "sans FR:", [n for n in names if n not in fr])
