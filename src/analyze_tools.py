import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings


from sklearn import preprocessing
from sklearn.decomposition import PCA


def raw_boxplot(data, nrows, ncols, figsize=(20, 15)):
    if len(data.columns) > nrows * ncols:
        warnings.warn('the number of data is more than the case of plot, some information will be lost')
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)

    i = 0
    j = 0
    for cols in data.columns:
        if j != 0 and j % ncols == 0:
            i += 1
            j = 0
        sns.boxplot(y=data.iloc[:, i], ax=axes[i, j])
        axes[i, j].set_title(cols)
        j += 1

    plt.show()


def raw_violinplot(data, nrows, ncols, figsize=(20, 15)):
    if len(data.columns) > nrows * ncols:
        warnings.warn('the number of data is more than the case of plot, some information will be lost')
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)

    i = 0
    j = 0
    count = 0
    for cols in data.columns:
        if j != 0 and j % ncols == 0:
            i += 1
            j = 0
        sns.violinplot(y=data.iloc[:, count], ax=axes[i, j])
        axes[i, j].set_title(cols)
        axes[i, j].set_ylabel('')  # Clear the default y-label
        j += 1
        count += 1

    plt.show()


def corr_heatmap(data, cmap='coolwarm'):
    scaler = preprocessing.StandardScaler()
    norm_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

    corr = norm_data.corr()
    sns.heatmap(corr, cmap=cmap)


def pca_analyze(data):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    pca = PCA()
    scaler = preprocessing.StandardScaler()
    norm_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    pca.fit(norm_data)

    eigenvalue = pca.explained_variance_
    sns.lineplot(eigenvalue, ax=axes[0])
    axes[0].set_title('eigenvalue')

    ratio = pca.explained_variance_ratio_
    cumulated_ratio = np.cumsum(ratio)

    sns.lineplot(cumulated_ratio * 100, markers=True, marker="o", ax=axes[1])
    for i, j in enumerate(cumulated_ratio * 100):
        if j < 93:
            axes[1].annotate("{0: .1f}".format(j), (i, j + 1), textcoords="offset points", xytext=(0, 10), ha='center')

    axes[1].set_title("cumulated_ratio")
    plt.show()


def pca_components(data, n_components=3, dimension=0):
    pca3 = PCA(n_components=n_components)
    scaler = preprocessing.StandardScaler()
    norm_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    pca_array = pca3.fit_transform(norm_data)

    indexs = ['I' * (i+1) + f' component {ratio: .2f}%' for i, ratio in enumerate(pca3.explained_variance_ratio_)]

    pca_data = {}
    for i, index in enumerate(indexs):
        pca_data[index] = pca_array[:, i]

    df_pca = pd.DataFrame(pca_data)

    plt.subplots(figsize=(15, 15))
    sns.scatterplot(data=df_pca, x=indexs[dimension], y=indexs[(dimension + 1) % n_components])
    for i in range(pca3.components_.shape[1]):
        plt.arrow(0, 0, pca3.components_[dimension, i] * 10, pca3.components_[(dimension + 1) % n_components, i] * 10, alpha=0.5, color='black')
        plt.text(pca3.components_[dimension, i] * 10, pca3.components_[(dimension + 1) % n_components, i] * 10, norm_data.columns[i])

    plt.show()

def pca_components3d(data):
    pca = PCA(n_components=3)
    scaler = preprocessing.StandardScaler()
    norm_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    pca_array = pca.fit_transform(norm_data)

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pca_array[:, 0], pca_array[:, 1], pca_array[:, 2])

    for i in range(pca.components_.shape[1]):
        ax.text(pca.components_[0, i], pca.components_[1, i], pca.components_[2, i], norm_data.columns[i])

    plt.show()

def inter_class_variance(df, target):
    inter_class_var = []

    for col in df.columns:
        inter_class_var.append(df.groupby(target)[col].mean().var())

    return inter_class_var



