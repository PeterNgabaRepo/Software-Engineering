"""app.py: main application file"""

import requests             # used for downloading files from websites
import pandas as pd         # used for csv
from flask import *         # used for website

# global constants
URL_INFECT = 'https://opendata.maryland.gov/api/views/tm86-dujs/rows.csv?accessType=DOWNLOAD'
URL_VACCINE = 'https://opendata.maryland.gov/api/views/4ibg-xizv/rows.csv?accessType=DOWNLOAD'
CSV_INFECT = 'MD_COVID-19_-_Cases_by_County.csv'
CSV_VACCINE = 'MD_COVID-19_-_Vaccinations_by_County.csv'

# global variables
data_infect = None
data_vaccine = None

header_infect = None
header_vaccine = None

headings = ('Category', 'Value')
data = []

app = Flask(__name__)


def request():
    """
    Downloads files from online database to populate dataframe
    :return:
    """
    # make sure to use global variables instead of initializing new local ones
    global data_infect, data_vaccine, header_infect, header_vaccine

    # open and convert csv into a dataframe
    data_infect = pd.read_csv(CSV_INFECT)
    data_vaccine = pd.read_csv(CSV_VACCINE)

    # drop the OBJECTID column in CSV_INFECT
    data_infect = data_infect.drop('OBJECTID', axis=1)

    # store header names
    header_infect = data_infect.columns
    header_vaccine = data_vaccine.columns


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/get/county')
def county():
    search_county_infected('Baltimore')
    return render_template('county.html', headings=headings, data=data)


def calc_county_infected(county, dataframe):
    """
    Displays dataframe for chosen county
    (currently as a table in alphabetical order)
    :param county: string of the chosen county
    :param dataframe: the given infected dataframe
    :return:
    """
    # infection rate per capita = (infected / total population) * 100
    # test positivity rate = (positive result / total tested) * 100
    # test per capita = (total tests / total population) * 100
    # case fatality rate = (deaths / infected) * 100
    global data

    cumulative = dataframe[county].sum()
    last_7 = dataframe[county].tail(7).sum()
    data = [
        ('Cumulative cases', str(cumulative)),
        ('Last 7 days', str(last_7))
    ]


def search_county_infected(county):
    """
    Finds the given county in the infected dataframe
    Returns error if not found
    :param county: string of the chosen county
    :return:
    """
    # attempt to find chosen county
    if county in header_infect:
        # if county is found, create new dataframe for just that county
        data_county = data_infect[['DATE', county]]

        # remove NA entries of that county
        data_county = data_county.dropna()

        # print dataframe of chosen county
        calc_county_infected(county, data_county)
    else:
        print("Error: County not valid")


if __name__ == '__main__':
    request()
    app.run()
