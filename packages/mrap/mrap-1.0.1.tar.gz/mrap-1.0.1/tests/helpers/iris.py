from sklearn import datasets

iris = datasets.load_iris(as_frame=True).frame
iris['Species'] = iris['target'].replace({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
iris = iris.rename(columns={"petal length (cm)": "Petal.Length",
                            "sepal length (cm)": "Sepal.Length",
                            "petal width (cm)": "Petal.Width",
                            "sepal width (cm)": "Sepal.Width"})
