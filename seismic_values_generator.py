import requests, json, csv, sys, pandas as pd

# try to import config module. if error, prompt user for mapquest api key
try:
    import config as cfg
except ImportError:
    key = input('Please paste in your Mapquest API key (you only need to do this the first time): ')
    with open(f'config.py', 'w') as f:
        f.write(f'MAPQUEST_API_KEY = "{key}"')
    import config as cfg

class SeismicValues:

    def __init__(self):

        self.address = self.getAddressInput()
        self.coordinates = self.getprojectCoordinates(self.address)
        self.riskCategory = self.getRiskCategoryInput()
        self.siteClass = self.getSiteClassInput()
        self.seismicValues = self.getSeismicValues()
        self.writeSeismicValues()

    def getprojectCoordinates(self, address):
        """With project address, get the GPS coordinates using Mapquest API."""

        payload = {"key": cfg.MAPQUEST_API_KEY, "location": address}

        response = requests.get('http://www.mapquestapi.com/geocoding/v1/address',
        params = payload)

        lat = json.loads(response.text)['results'][0]['locations'][0]['latLng']['lat']
        long = json.loads(response.text)['results'][0]['locations'][0]['latLng']['lng']

        return {'lat': lat, 'long': long}

    def getAddressInput(self):
        """Get address input from user. Validate that input produces successful query."""

        address = input('Please enter the project address: ')
        errorMessage = 'Input address is invalid or does not produce unique result. Please try again.'

        try:
            self.getprojectCoordinates(address)
        except:
            print(errorMessage)
            self.getAddressInput()

        return address

    def getSiteClassInput(self):
        """Get site class input from user and validate."""

        site_classes = ['A', 'B', 'C', 'D', 'D-default']
        site_class = input(f'Please enter the project site class ({site_classes}): ')

        if site_class not in site_classes:
            print(f'Input site class is invalid. Please input one of the following: {site_classes} and try again.')
            self.getSiteClassInput()

        return site_class

    def getRiskCategoryInput(self):
        """Get risk category input from user and validate."""

        risk_categories = ['I', 'II', 'III', 'IV']
        risk_category = input(f'Please enter the project risk category ({risk_categories}): ')

        if risk_category not in risk_categories:
            print(f'Input risk category is invalid. Please input one of the following: {risk_categories} and try again.')
            self.getRiskCategoryInput()

        return risk_category

    def getSeismicValues(self):
        """With lat, long, risk category and site class, get seismic values using USGS API."""

        payload = {'latitude': self.coordinates['lat'], 'longitude': self.coordinates['long'],
        'riskCategory': self.riskCategory, 'siteClass': self.siteClass, 'title': 'none'}

        response = requests.get('https://earthquake.usgs.gov/ws/designmaps/asce7-16.json',
        params = payload)
        print(f"SDS... {json.loads(response.text)['response']['data']['sds']}g")
        print(f"SS... {json.loads(response.text)['response']['data']['ss']}g")
        print(f"TL... {json.loads(response.text)['response']['data']['tl']}sec")
        return json.loads(response.text)['response']

    def writeSeismicValues(self):
        """Write seismic values to JSON and CSV formats."""

        # write output JSON file
        cleanAddress = self.address.replace(' ','_')
        cleanAddress = cleanAddress.replace(',', '')
        outputFileName = f"{cleanAddress}_outputData"
        with open(f'{outputFileName}.json', 'w') as outfile:
            json.dump(self.seismicValues, outfile, indent = 4)

        # write output CSV file
        df = pd.read_json(f'./{outputFileName}.json')
        export_csv = df.to_csv(f'./{outputFileName}.csv')

if __name__ == '__main__':

    SeismicValues()
