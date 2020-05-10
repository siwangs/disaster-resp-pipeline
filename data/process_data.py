import argparse
from os import path
import pandas as pd 
from sqlalchemy import create_engine

AP = argparse.ArgumentParser()
AP.add_argument("--msgcsv", action="store", required=True, help="message CSV")
AP.add_argument("--catcsv", action="store", required=True, help="category CSV")
AP.add_argument("--dbfilename", action="store", required=True, help="db storage file name")
dataPath = 'data/'


def directoryCheck(pathFile):
    if path.exists(pathFile):
        return pd.read_csv(pathFile)
    else:
        raise ValueError("The {} is not existing, please check the file name".format(pathFile))


def load_data(msgCsv, catCsv):
    # Check if the file available
    msgDf = directoryCheck(dataPath+msgCsv)
    catDf = directoryCheck(dataPath+catCsv)
    
    return msgDf.merge(catDf,on = 'id')


def clean_data(df):
    cateDF = df['categories'].str.split(";", expand=True)
    category_colnames = [c.split('-')[0] for c in cateDF.iloc[0,:].tolist()] 
    cateDF.columns = category_colnames

    for column in cateDF.columns:
        # Extract Value of Category Type
        cateDF[column] = cateDF[column].str[-1]
        cateDF[column] = cateDF[column].astype(int)
    # Clean abnormal data of Category Type (values other than 0 or 1)
    for c in category_colnames:
        if len(cateDF[c].unique()) == 3:
            cateDF[c] = cateDF[c].map(lambda x: 1 if x >= 1 else 0)
    # Drop duplicated value of Categories
    df.drop("categories", axis=1, inplace=True)
    df = pd.concat([df, cateDF], axis=1)
   
    return df.drop_duplicates()


def save_data(df, database_filename):
    engine = create_engine('sqlite:///{}{}'.format(dataPath, database_filename))
    df.to_sql('DisasterResponse', engine, index=False, if_exists='replace')


def main(args):
    print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(args.msgcsv, args.catcsv))
    loaddf = load_data(msgCsv=args.msgcsv, catCsv=args.catcsv)

    print('Cleaning data...')
    cleandf = clean_data(loaddf)

    print('Saving data...\n    DATABASE: {}'.format(args.dbfilename))
    save_data(cleandf, args.dbfilename)
    

if __name__ == "__main__":
    main(AP.parse_args())
