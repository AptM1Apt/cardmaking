import numpy as nm
import pandas as pd

from cardmaking.Cards import create_cards_CSV
from cardmaking.Sheets import create_a4_sheets
from cardmaking.PDF import images_to_pdf

def start():
    df = pd.read_csv("test_data\\test.csv", usecols=["name", "condition", "price", "description", "typeofitem", "typeofdamage", "damage", "usage"], keep_default_na=False).applymap(lambda x: None if x == "" else x)

    if not os.path.exists("output"):
        os.makedirs("output")

    create_cards_CSV(df, "output\\cards\\")
    print("Cards has been created!")
    create_a4_sheets("output\\cards", "output\\sheets\\")
    print("Sheets has been created!")
    images_to_pdf("output\\sheets", "TEST")
    print("PDF has been created!")