from bond_class import GovBonds
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns



bonds_data = GovBonds()
country = 'chile'
date = datetime.today()


if __name__ == '__main__':
    
    #this is the function to create the graphics 
    bonds_data.get_yield_curve(country)
    # print( bonds_data.get_country_tables(country) )