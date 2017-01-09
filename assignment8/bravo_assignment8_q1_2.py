
# coding: utf-8

import pandas as pd
from bravo_assignment8_q1_1 import calcJaccardSimilarity

store=pd.HDFStore("store2.h5")
#df1=store['df1']
out_link_df=store['df2']
#print(out_link_df.head)
print(out_link_df.columns)


Germany =out_link_df['out_links'][out_link_df['name']=='Germany']
Europe = out_link_df['out_links'][out_link_df['name']=='Europe']

germany_list = Germany.tolist()[0]
europe_list = Europe.tolist()[0]

print('Based on Outlinks : Jaccard coefficent for articles Germany and Europe :',
      calcJaccardSimilarity(germany_list, europe_list))