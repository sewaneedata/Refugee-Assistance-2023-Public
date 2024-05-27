### README

Welcome to our Project Github! Follow the instructions below or access this link (https://docs.google.com/document/d/1OHcjyDyuhsk-SzfkMzg-le1S5vk8A222Ilmf-CHBhDw/edit) to use our dashboard.

Prerequisites:

Windows:
1. Install the latest version of Python from this link: https://www.python.org/downloads/ 
  >Download the latest version
  >Run the downloaded package
  >Installation window will open
  >Make sure to check the box ‘Add python.exe to PATH’ before installing
  >Select Install 
2. Open your computer’s Terminal (you can access Terminal by searching for the ‘command prompt’ app on your computer)
3. Make sure your pip version is up to date with the command “pip install --upgrade pip”.
4. Enter the command “pip install dash” to install Dash on your computer.

Mac:
1. Install the latest version of Python from this link: https://www.python.org/downloads/  
  >Download the latest version
  >Run the downloaded package 
  >Installation window will open
  >Make sure to check the box ‘Add python.exe to PATH’ before installing
  >Select Install 
2. Open your computer’s Terminal (you can access Terminal by searching for it on Launchpad).
3. Make sure your pip version is up to date with the command “pip install --upgrade pip”.
4. Enter the command “pip install dash” to install Dash on your computer.


Accessing the Dashboard Code:

Before you can begin to run the dashboard you need the relevant files:
1. Download all the files in the ‘Final Package’ folder.
2. Go to your files explorer and create a folder.
3. Place all the downloaded files in this new folder and recompile the files as they are in GitHub (meaning make sure you keep the files in the ‘assets’ folder in a folder called ‘assets’ within the new folder you just created).

Accessing the Maps:

1. Open Google Collaboratory (preferred) or Jupyter notebook.
2. Within the ‘map’ folder there is a notebook named ‘folium_map_code.ipynb’. Open this notebook in the Google Collaboratory or Jupyter notebook.
3. Now upload all the other files from the ‘map’ folder in the upload section of the Google Collaboratory or Jupyter notebook that you are working on.
Here’s a list of those files:
  countries.geojson
  plotting_a18.csv
  plotting_a19.csv
  plotting_a20.csv
  plotting_a21.csv
  plotting_a22.csv
  plotting_o18.csv
  plotting_o19.csv
  plotting_o20.csv
  plotting_o21.csv
  plotting_o22.csv 
  plotting_under.csv
4. Run the code and this will generate 12 maps (in html file format)
5. Download the 12 files and save them in the ‘assets’ folder.

YOU ARE NOW SET TO RUN THE DASHBOARD!!🎉🎉

Running the Dashboard:
1. Use the “cd” command to navigate to the directory where the dashboard files are located (ex. “cd Desktop”, cd “DisplacementCrisisDashboard”).
2. Run the dashboard with the command “python app.py” (IMPORTANT: make sure the “assets” folder is inside the same folder as the app.py file).
3. Copy and paste the host address of the file into a new tab on your browser.
4. To shut the dashboard down, type control + C into the Terminal.
