
import pandas as pd

store=pd.HDFStore("store2.h5")

df1=store['df1']

out_link_df=store['df2']

#print(out_link_df.columns)

def Distance(graph, start, end):
    path=[]
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in set(graph.neighbors(start)) - set(path):
        paths.extend(Distance(graph, node, end))
    return paths

