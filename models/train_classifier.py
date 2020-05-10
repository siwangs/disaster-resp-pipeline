from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import pandas as pd
import pickle
import re
from sqlalchemy import create_engine
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import random
from sklearn.model_selection import train_test_split
import argparse
from os import path




AP = argparse.ArgumentParser()
AP.add_argument("--sourcedb", action="store", required=True, help="source db path")
AP.add_argument("--modeloutput", action="store", required=True, help="model output file name with path")

def directoryCheck(pathFile):
    if path.exists(pathFile):
       pass
    else:
        raise ValueError("The {} is not existing, please check the file name".format(pathFile))


def load_data(database_filepath):
    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql_table('DisasterResponse', con=engine)

    X = df['message']
    Y = df.iloc[:, 4:]
    category_names = Y.columns

    return X, Y, category_names


def tokenize(text):
    # Normalized Text Keep Only lower case words and numbers
    text = re.sub(r"[^a-z0-9]", " ", text.lower())

    # tokenize text and remove stop words
    tokens = word_tokenize(text)
    stopWords = stopwords.words("english")
    words = [t for t in tokens if t not in stopWords]

    # word lemmatize
    words = [WordNetLemmatizer().lemmatize(word) for word in words]

    return words

def build_model():
    random.seed(42)
    pipeline = Pipeline([('vect', CountVectorizer(tokenizer=tokenize)),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultiOutputClassifier(RandomForestClassifier()))])
    parameters = {
                   'clf__estimator__n_estimators': [50, 100],
                  # 'clf__estimator__min_samples_split': [3, 4],
                  'tfidf__use_idf': [True, False]
                  }
    model = GridSearchCV(estimator=pipeline,
            param_grid=parameters,
            cv=2,
            verbose=1)

    return model




def evaluate_model(model, X_test, Y_test, category_names):
    y_pred = model.predict(X_test)
    for c, i in zip(category_names, range(len(category_names))):
        print(c,'\n',classification_report(Y_test[c], y_pred[:, i]))

    overall_accuracy = (y_pred == Y_test).mean().mean()
    print('Average overall accuracy {0:.2f}% \n'.format(overall_accuracy * 100))


def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath, 'wb'))



def main(args):
    database_filepath = 'data/'+args.sourcedb
    model_filepath = 'models/'+args.modeloutput
    directoryCheck(database_filepath)

    print('Loading data...\n    DATABASE: {}'.format(database_filepath))
    X, Y, category_names = load_data(database_filepath)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    print('Building model...')
    model = build_model()

    print('Training model...')
    model.fit(X_train, Y_train)

    print('Evaluating model...')
    evaluate_model(model, X_test, Y_test, category_names)

    print('Saving model...\n    MODEL: {}'.format(model_filepath))
    save_model(model, model_filepath)

    print('Trained model saved!')




if __name__ == '__main__':
    main(AP.parse_args())