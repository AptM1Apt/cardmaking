from PIL import Image, ImageDraw, ImageFont
import numpy as nm 
import pandas as pd 
import pyphen

import Cards, Sheets, PDF

df = pd.read_csv("test.csv", usecols=["name", "condition", "price", "description", "typeofitem", "typeofdamage", "damage", "usage"], keep_default_na=False).applymap(lambda x: None if x == "" else x)

Cards.create_cards_CSV(df, "cards\\")
Sheets.create_a4_sheets("cards", "sheets\\")
PDF.images_to_pdf("sheets", "TEST")