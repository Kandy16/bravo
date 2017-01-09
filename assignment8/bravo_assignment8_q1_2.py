
# coding: utf-8

import pandas as pd

store=pd.HDFStore("store2.h5")
#df1=store['df1']
out_link_df=store['df2']
#print(out_link_df.head)
print(out_link_df.columns)


def calcJaccardSimilarity(wordset1, wordset2):
    wordset1=set(wordset1)
    wordset2=set(wordset2)
    # we wanted to make the article names case insensitive
    wordset1 = {x.lower() for x in wordset1}
    wordset2 = {x.lower() for x in wordset2}

    inter=wordset1.intersection(wordset2)
    union=wordset1.union(wordset2)
    jc=(len(inter)/len(union))
    return jc

Germany =out_link_df['out_links'][out_link_df['name']=='Germany']
Europe = out_link_df['out_links'][out_link_df['name']=='Europe']

print('Based on Outlinks : Jaccard coefficent for articles Germany and Europe :',
      calcJaccardSimilarity(Germany.tolist()[0],Europe.tolist()[0]))