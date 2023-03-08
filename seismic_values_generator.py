import xlsxwriter, json, requests, pandas as pd

# try to import config module. if error, prompt user for mapquest api key
try:
    import config as cfg
except ImportError:
    key = input(
        "Please paste in your Mapquest API key (you only need to do this the first time): "
    )
    with open(f"config.py", "w") as f:
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

        response = requests.get(
            "http://www.mapquestapi.com/geocoding/v1/address", params=payload
        )

        lat = json.loads(response.text)["results"][0]["locations"][0]["latLng"]["lat"]
        long = json.loads(response.text)["results"][0]["locations"][0]["latLng"]["lng"]

        return {"lat": lat, "long": long}

    def getAddressInput(self):
        """Get address input from user. Validate that input produces successful query."""

        print("########## INPUT PARAMETERS ##########")

        address = input("Please enter the project address: ")
        errorMessage = "Input address is invalid or does not produce unique result. Please try again."

        try:
            self.getprojectCoordinates(address)
        except:
            print(errorMessage)
            address = self.getAddressInput()

        return address

    def getSiteClassInput(self):
        """Get site class input from user and validate."""

        site_classes = ["A", "B", "C", "D", "D-default"]
        site_class = input(f"Please enter the project site class ({site_classes}): ")

        if site_class not in site_classes:
            print(
                f"Input site class is invalid. Please input one of the following: {site_classes} and try again."
            )
            site_class = self.getSiteClassInput()

        return site_class

    def getRiskCategoryInput(self):
        """Get risk category input from user and validate."""

        risk_categories = ["I", "II", "III", "IV"]
        risk_category = input(
            f"Please enter the project risk category ({risk_categories}): "
        )

        if risk_category not in risk_categories:
            print(
                f"Input risk category is invalid. Please input one of the following: {risk_categories} and try again."
            )
            risk_category = self.getRiskCategoryInput()

        return risk_category

    def getSeismicValues(self):
        """With lat, long, risk category and site class, get seismic values using USGS API."""

        payload = {
            "latitude": self.coordinates["lat"],
            "longitude": self.coordinates["long"],
            "riskCategory": self.riskCategory,
            "siteClass": self.siteClass,
            "title": "none",
        }

        response = requests.get(
            "https://earthquake.usgs.gov/ws/designmaps/asce7-16.json", params=payload
        )
        return response.text

    def writeSeismicValues(self):
        """Write seismic values to output spreadsheet."""

        # convert json response to base df
        df_base = pd.DataFrame(data=json.loads(self.seismicValues)["response"])

        # remove metadata column from base df
        df_base = df_base.drop(columns="metadata")

        # remove rows with NaN value from base df
        df_base = df_base.dropna()

        # put response spectra data on separate sheets in workbook
        response_spectra_dfs = []
        for idx in range(4):
            response_spectra_dfs.append(df_base.tail(1))  # pull out last row
            df_base.drop(df_base.tail(1).index, inplace=True)  # drop last row

        print("########## RESPONSE DATA ##########")

        print(df_base.to_string(header=False))
        print("See output spreadsheet for response spectra data and plots.")

        # write dfs to excel spreadsheet
        cleanAddress = self.address.replace(" ", "_")
        cleanAddress = cleanAddress.replace(",", "")
        outputFileName = f"{cleanAddress}_outputData"

        with pd.ExcelWriter(f"./{outputFileName}.xlsx") as writer:
            df_base.to_excel(writer, sheet_name="seismic_vals", header=False)
            for df in response_spectra_dfs:
                sheet = df.index[0]
                vals_only_df = pd.DataFrame(df["data"].iloc[-1])
                vals_only_df.columns = ["Period [s]", "Spectral Acceleration [g]"]
                vals_only_df.to_excel(writer, sheet_name=sheet, index=False)

                # make plots
                workbook = writer.book
                chart = workbook.add_chart({"type": "scatter", "subtype": "smooth"})
                chart.add_series(
                    {
                        "name": f"={sheet}",
                        "categories": f"={sheet}!$A$2:$A$1000",
                        "values": f"={sheet}!$B$2:$B$1000",
                    }
                )
                chart.set_title({"name": sheet})
                chart.set_x_axis({"name": "Period [s]"})
                chart.set_y_axis({"name": "Spectral Acceleration [g]"})
                chart.set_style(15)
                chart.set_legend({"position": "none"})
                worksheet = workbook.get_worksheet_by_name(sheet)
                worksheet.insert_chart("C1", chart)


if __name__ == "__main__":
    SeismicValues()
