# Disaster Response Pipeline Project

### Table of Contents

- [Environment](#environment)
- [Instructions of Running the Programs](#instructions)
- [Project Overview](#overview)
- [Structure of Projects](#structure)
- [Delivery](#delivery)

### Environment <a name="environment"></a>
Beside standard Conda Library, follow library need to installed:

- argparse

Following packages needs to be downloaded from NLTK before first used:

- punkt
- stopwords
- wordnet

### Instructions of Running the Programs: <a name="instructions"></a>
1. Run the following commands in the project's root directory to set up your database and model. `argparse` is introduced instead of python default arg library from python.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py --msgcsv disaster_messages.csv --catcsv disaster_categories.csv --dbfilename DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py --sourcedb DisasterResponse.db --modeloutput classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

### Project Overview <a name="overview"></a>
Data Engineering, NLP and Flask API were applied to build an APP/API which potentially help emergency department to pass related disaster agency faster.

### Structure of Projects:  <a name="structure"></a>
#### app:
    templates(for Web API)
        go.html 
        master.html
#### Data:
    disaster_categories.csv (disaster lable file)
    disaster_messages.csv (disaster message)
    DisasterResponse.db (output db file, NOT include in this git)
    process_data.py (Main Program to clean and transform the source files for model to consume)
#### model:
    classifier.pkl (Model output file, NOT including in the git)
    train_classifier.py ( Main Program to read Source DB, train and save the model) 

### Delivery: <a name="delivery"></a>
A web API was created to show the summary of 36 disaster categories and functionality to categorized new disaster messages to its corresponding categories.
#### Examples and Screenshot
Categorize messages:
![](.README_images/ae062569.png)

Distribution of genres:
![](.README_images/e29b3df3.png)

Top and Bottom 10 Counts of Categories:
![](.README_images/c6eac10c.png)
![](.README_images/500ff0f6.png)


