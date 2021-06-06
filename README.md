# Seismic Design Values Generator Tool

A python program that queries the seismic design values for a particular address, site class and risk category, using the USGS Design Maps database and produces an output CSV file.

The following instructions list all of the requirements to run the program. This assumes that the user has a basic understanding of how to run a python script. [Click here](https://www.python.org/downloads/) to see the python website, where you can download the latest version of python.

# Generating Mapquest API key

The program uses Mapquest [Mapquest API](https://developer.mapquest.com/) to convert the input address into GPS coordinates. The Mapquest API requires an API key in order to use it, which can be generated for free. In order to generate an API key, follow instructions on their website. The first time you run the script, it will prompt you for this API key. For subsequent runs, the script will use the stored value and will not prompt you again.

# Creating virtual environment

With python installed, enter the following command into the terminal. This only needs to be done the first time you run the script. After that, you can just skip to the active the virtual environment step.
```
python3 -m venv venv
```

# Activating virtual environment

Run the following command to activate your virtual environment.

```
source venv/bin/activate
```

# Installing requirements in virtual environment

This only needs to be done the first time using the program. After that, you can just skip to the active the virtual environment step.

```
pip install --upgrade pip
pip install -r requirements.txt
python setup.py install
```

# Running the script

Now that you have the virtual environment set up, you can run the script. Enter the following on the command line:

```
python seismic_values_generator.py
```

The script will prompt you for input values right in the terminal upon running it. If at any point you want to exit, just type `Control + C` into the command line.

# License

Copyright (c) 2021 Jesse Bluestein

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
