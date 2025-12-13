# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 14:21:57 2020

@author: 118939
"""

from sklearn.cluster import KMeans


def kmeans(df, cluster=0):
    if df.shape[0] <= cluster: cluster = df.shape[0]
    kmeans = KMeans(n_clusters=cluster)
    kmeans.fit(df)
    # y_kmeans = kmeans.predict(data_kmeans)
    return kmeans


if __name__ == '__main__':
    print("HELLO")

