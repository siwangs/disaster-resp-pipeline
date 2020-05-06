import argparse
from os import path
import pandas as pd 
from sqlalchemy import create_engine

AP = argparse.ArgumentParser()
AP.add_argument("--msgCSV", action="store", required=True, help="message CSV")
AP.add_argument("--catCSV", action="store", required=True, help="category CSV")
AP.add_argument("--dbFilename", action="store", required=True, help="db storage file name")
dataPath = 'Data/'

def directoryCheck(pathFile):
    if(path.exists(pathFile)) == True:
        return pd.read_csv(pathFile)
    else:
        raise ValueError("The {} is not existing, please check the file name".format(pathFile))
    
def load_data(msgCsv,catCsv):
    msgDf = directoryCheck(dataPath+msgCsv)
    catDf = directoryCheck(dataPath+catCsv)
    
    return msgDf.merge(catDf,on = "id")

def clean_data(df):
    cateDF = df['categories'].str.split(";", expand = True)
    category_colnames = [c.split('-')[0] for c in cateDF.iloc[0,:].tolist()] 
    cateDF.columns = category_colnames

    for column in cateDF.columns:
        # set each value to be the last character of the string
        cateDF[column] = cateDF[column].str[-1]
        
        # convert column from string to numeric
        cateDF[column] = cateDF[column].astype(int)

    
    df.drop("categories",axis=1, inplace = True)
    df = pd.concat([df,cateDF], axis = 1)
   
    return df.drop_duplicates()

def save_data(df, database_filename):
   engine = create_engine('sqlite:///{}{}.db'.format(dataPath,database_filename))
   df.to_sql(dataPath+database_filename, engine, index=False,if_exists = 'replace') 


def main(args):
    print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(args.msgCSV, args.catCSV))
    loadDF = load_data(msgCsv=args.msgCSV, catCsv = args.catCSV)

    print('Cleaning data...')
    cleanDF = clean_data(loadDF)

    print('Saving data...\n    DATABASE: {}'.format(args.dbFilename))
    save_data(cleanDF, args.dbFilename)
    
    

if __name__ == "__main__":
    main(AP.parse_args())