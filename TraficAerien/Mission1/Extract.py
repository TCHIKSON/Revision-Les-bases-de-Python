import pandas as pd
import numpy as np
from PyPDF2 import PdfReader
import os

def extract_csv(path): 
    data= "test"
    try:
        data = pd.read_csv(path)
        return data
    except Exception as e:
        print(f"Echec du chargement de {path} : {e}")

def extract_excel(path): 
    data= "test"
    try:
        data = pd.read_excel(path)
        return data
    except Exception as e:
        print(f"Echec du chargement de {path} : {e}")

def extract_json(path): 
    try:
        data = pd.read_json(path)
        return data
    except Exception as e:
        print(f"Echec du chargement de {path} : {e}")

def extract_pdf(path): 
    try:
        data= "test"
        reader = PdfReader(path)
        number_of_pages = len(reader.pages)
        page = reader.pages[0]
        data = page.extract_text()
        with open("temp.txt","x") as temp:
            temp.write(data)
        csv = extract_csv("temp.txt")
        os.remove("temp.txt")
        return csv
    except Exception as e:
            print(f"Echec du chargement du PDF {path} : {e}")
        
def extract_html(path): 
    try:
        data = pd.read_html(path)
        return data
    except Exception as e:
        print(f"Echec du chargement de {path} : {e}")