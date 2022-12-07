import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from datetime import datetime

class GovBonds():
    '''This class retrieve and dop things with data coming from the webpage:
    http://www.worldgovernmentbonds.com/'''
    
    def __init__(self) -> None:
        
        all_tables = pd.read_html("http://www.worldgovernmentbonds.com/")

        '''In the tables above the first one is sorted by 10 year yield means and teh second one by 
        country name, so I will use just the first one'''
        self.world_principal_bond_info = all_tables[0]
    #--------------------- Main Functions --------------------#
    #To get data.
    def get_country_tables(self, country):
        '''Returns the interest table from the selected country'''
        
        country_tables = pd.read_html(f'http://www.worldgovernmentbonds.com/country/{country}/')
        print(f'\n{country.capitalize()} Government Bonds - Yields\n')
        return country_tables[0]

    def get_yields(self, data):
        '''returns the yield pd for a country data.'''
        first = data.iloc[:, (data.columns.get_level_values(0)=='Yield') | (data.columns.get_level_values(1)=='ResidualMaturity')]
        first.columns = first.columns.droplevel(0)
        return first 
    
    
    def get_yield_curve(self, country, show=True, save=False):
        
        data = self.get_yields(self.get_country_tables(country))
        date = datetime.today()
        data["ResidualMaturity"] =pd.Categorical(data['ResidualMaturity'],
                                             categories=['1 month', '3 months', '6 months','9 months',
                                                         '1 year', '2 years', '3 years',
                                                         '4 years', '5 years', '6 years', 
                                                         '7 years', '8 years', '9 years',
                                                         '10 years', '15 years', 
                                                         '20 years', '30 years', '40 years'],
                                                ordered=True)
        data['Last'] = data['Last'].str.rstrip("%").astype(float)
        data['1M'] = data['Last']+data['Chg 1M'].str.rstrip(" bp").astype(float)/100
        data['6M'] = data['Last']+data['Chg 6M'].str.rstrip(' bp').astype(float)/100
        data.drop(columns=['Chg 1M', 'Chg 6M'], inplace=True, axis=1)  
        sns.set_style('white')
        sns.set_context('notebook')
        plot = sns.lineplot(data=data, x='ResidualMaturity', y='Last',sort=False, marker='h',
                    linewidth=1.5, linestyle='-', label= f'{country.capitalize()} ({date.strftime("%d %b %Y")})')
        plot = sns.lineplot(data=data, x='ResidualMaturity', y='1M',sort=False, marker = 'v', 
                    linewidth=1, linestyle='--', label = '1M ago')
        plot = sns.lineplot(data=data, x='ResidualMaturity', y='6M',sort=False, marker = 'd',
                    linewidth=0.5, linestyle='-.', label = '6M ago')
        sns.color_palette("icefire", as_cmap=True)    
        plot.set(xlabel='', ylabel='', title=f'{country.capitalize()} Yield Curve - {date.strftime("%d %b %Y")}')
        plot.yaxis.set_major_formatter(mtick.PercentFormatter())
        plt.xticks(rotation=45)
        if show:
            plt.show()
        if save:
            pass 
    
    
    #--------------------- Support functions -----------------#
    def get_countries(self): 
        '''This function returns a pandas DF containing all the countries in data set'''
        return self.world_principal_bond_info.iloc[:,self.world_principal_bond_info.columns.get_level_values(1)=='Country']
    
    def get_country_list(self):
        '''This function returns a list containing the countries in DF'''
        return self.Extract([country for country in self.get_countries().values.tolist()])
    
    def get_clean_country_list(self):
        '''Same as get_clean_country_list but getting rid of the "(*)" symbol'''
        first = [country.split()[0] if "(*)" in country else country for country in self.get_country_list()] 
        second = [country.replace(" ", "-") if " " in country else country for country in first]  
        return [country.replace("ù", "u") if "ù" in country else country for country in second] 
    def show_available_countries(self):
        '''This function shows countries that can be called'''
        data = self.get_country_list()
        print(f'\n{len(data)} countries available:\n')
        print(data)        
    #--------------- Utils functions ------------------#
    
    def Extract(self, lst):
        return list(list(zip(*lst))[0])