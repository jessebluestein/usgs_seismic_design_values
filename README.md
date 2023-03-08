# Seismic Design Values Generator Tool

This python program queries the seismic design values for a particular address, site class and risk category, using the USGS Design Maps database. It then outputs the results in the form of an Excel Spreadsheet along with plots of the response spectra for the site.

The following instructions list all of the requirements to run the program. This assumes that the user has a basic understanding of how to run a python script. [Click here](https://www.python.org/downloads/) to see the python website, where you can download the latest version of python.

# Generating Mapquest API key

The program uses Mapquest [Mapquest API](https://developer.mapquest.com/) to convert the input address into GPS coordinates. The Mapquest API requires an API key in order to use it, which can be generated for free. In order to generate an API key, follow instructions on their website. The first time you run the script, it will prompt you for this API key. For subsequent runs, the script will use the stored value and will not prompt you again.

# Setup environment to run script

The package includes a handy shell script to run all of the steps to setup your virtual environment that you'll need to run the script. To run the shell script, make sure you are in the project directory and paste the following into your terminal. This only needs to be done the first time after downloading the package.

```
./setup_environment.sh
```

# Run script

To run the main script via a helper shell script, make sure you are in the project directory and paste the following into your terminal. The helper shell script activates the virtual environment for you, runs the main script, and then deactivates the virtual environment automatically.

```
./run_script.sh
```

The script will prompt you for input values right in the terminal upon running it. If at any point you want to exit, just type `Control + C` into the command line. The first time you run the script, it will prompt you for the Mapquest API key. For subsequent runs, the script will use the stored value and will not prompt you again. To generate the Mapquest API key, follow the instructions above.

Alternatively, you can run the python script directly without the helper script. To do that, run the following commands:

```
source venv/bin/activate
python seismic_values_generator.py
deactivate
```

After the script runs, it prints the seismic design values to the terminal. It outputs these same values to an Excel file, along with plots of the response spectra. The output Excel file is stored in the same folder as this code.

# License

Copyright (c) 2022 Jesse Bluestein

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
