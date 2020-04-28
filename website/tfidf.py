import sys, os, re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords

def pre_process(text):    
    text=text.lower()                       # lowercase
    text=re.sub("<!--?.*?-->","",text)      # remove tags
    text=re.sub("(\\d|\\W)+"," ",text)      # remove special characters and digits
    return text
 
 
# load a set of stop words
stopwords = stopwords.words('english')

cv = ""
tfidf_transformer = ""
feature_names = ""

def create_vocab_tfidf(dirpath):
    global cv
    global tfidf_transformer
    global feature_names
    filenames = []
    docs = []
    listOfDir = os.listdir(dirpath)
    for dir in listOfDir:
        path = os.path.join(dirpath, dir)
        for file in os.listdir(path):
            filenames.append(file.split(".")[0].replace('-', " "))
            with open(path+"/"+file, "r") as f:
                doc = ' '.join([str(line) for line in f.readlines()]) 
                docs.append(doc)
    
    df_idf = pd.DataFrame()
    df_idf['title'] = filenames
    print(df_idf['title'])
    df_idf['body'] = docs
    df_idf['text'] = df_idf['title'] + df_idf['body']
    df_idf['text'] = df_idf['text'].apply(lambda x:pre_process(x))

    # get the text column 
    docs=df_idf['text'].tolist()

    # create a vocabulary of words, ignore words that appear in 85% of documents, eliminate stop words
    cv=CountVectorizer(max_df=0.85,stop_words=stopwords)
    word_count_vector=cv.fit_transform(docs)
    print(list(cv.vocabulary_.keys())[:50])

    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)

    # this is done only once, this is a mapping of index to words 
    feature_names=cv.get_feature_names()


####################################################################################################


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
def extract_topn_from_vector(feature_names, sorted_items, topn):
    """get the feature names and tf-idf score of top n items"""
    
    sorted_items = sorted_items[:topn]       # use only topn items from vector
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    return results


# extract keywords
def extract_keywords(filename):
    print(filename)
    with open(filename, "r") as f:
        doc = ' '.join([str(line) for line in f.readlines()])
    
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
    
    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    
    #extract only the top n; n is given as the last argument
    keywords=extract_topn_from_vector(feature_names,sorted_items, 5)
    print(keywords)
    return list(keywords.keys())