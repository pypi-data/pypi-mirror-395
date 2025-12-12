import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys

from sklearn import tree, metrics
from sklearn.tree import DecisionTreeClassifier
from IPython.display import display, HTML
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")


class DT():

    def __init__(self): 
        super().__init__()
        pass
    

    RANDOM_STATE = 42
    NUMBER_OF_DASHES = 100

    """
    Decision Tree Classifier related visualizations
    To plot the confusion_matrix with percentages
    """

    @staticmethod
    # defining a function to compute different metrics to check performance of a classification model built using sklearn
    def model_performance_classification(
            model,
            predictors: pd.DataFrame,
            expected: pd.Series,
            printall: bool = False,
            title: str = 'DecisionTreeClassifier') -> pd.DataFrame:
        """
        Function to compute different metrics to check classification model performance
        model: classifier \n
        predictors: independent variables \n
        target: dependent variable \n
        return: dataframe of different performance metrics
        """

        # predicting using the independent variables
        predictions = model.predict(predictors)

        accuracy = metrics.accuracy_score(expected, predictions)  # to compute Accuracy
        recall = metrics.recall_score(expected, predictions)  # to compute Recall
        precision = metrics.precision_score(expected, predictions)  # to compute Precision
        f1 = metrics.f1_score(expected, predictions)  # to compute F1-score

        # creating a dataframe of metrics
        df_perf = pd.DataFrame(
            {
                "Accuracy": accuracy,
                "Recall": recall,
                "Precision": precision,
                "F1": f1,
            },
            index=[0],
        )
        if (printall):
            display(
                HTML(
                    f"<h3>Classification Model Performance Metrics : {title}</h3>"
                ))
            display(df_perf)

        return df_perf

        # END OF MODEL PERFORMANCE CLASSIFICATION FUNCTION
    @staticmethod
    def plot_confusion_matrix(
                              model,
                              predictors: pd.DataFrame,
                              expected: pd.Series,
                              title: str = "DecisionTreeClassifier") -> None:
        """
        To plot the confusion_matrix with percentages \n
        model: classifier \n
        predictors: independent variables  \n
        target: dependent variable \n
        return: None
        """
        # Predict the target values using the provided model and predictors
        predicted = model.predict(predictors)

        # Compute the confusion matrix comparing the true target values with the predicted values
        conf_matrix = metrics.confusion_matrix(expected, predicted)

        # Create labels for each cell in the confusion matrix with both count and percentage
        labels = np.asarray([[
            "{0:0.0f}".format(item) +
            "\n{0:.2%}".format(item / conf_matrix.flatten().sum())
        ] for item in conf_matrix.flatten()
                             ]).reshape(2, 2)  # reshaping to a matrix

        # Set the figure size for the plot
        plt.figure(figsize=(6, 4))
        plt.title("Confusion Matrix for " + title)
        # Plot the confusion matrix as a heatmap with the labels
        sns.heatmap(conf_matrix, annot=labels, fmt="")

        # Add a label to the y-axis
        plt.ylabel("True label")

        # Add a label to the x-axis
        plt.xlabel("Predicted label")
        plt.show()
        sys.stdout.flush()
        # END OF PLOT CONFUSION MATRIX FUNCTION
    @staticmethod
    def tune_decision_tree(
            X_train: pd.DataFrame,
            y_train: pd.Series,
            X_test: pd.DataFrame,
            y_test: pd.Series,
            max_depth_v: tuple[int, int, int] = (2, 11, 2),
            max_leaf_nodes_v: tuple[int, int, int] = (10, 51, 10),
            min_samples_split_v: tuple[int, int, int] = (10, 51, 10),
            printall: bool = True,
            sortresultby: list = ['F1Difference'],
            sortbyAscending: bool = False) -> DecisionTreeClassifier:
        """
        Function to tune hyperparameters of Decision Tree Classifier \n
        X_train: training independent variables \n
        y_train: training dependent variable \n
        X_test: test independent variables \n  
        y_test: test dependent variable
        max_depth_v: tuple containing (start, end, step) values for max_depth parameter \n
        max_leaf_nodes_v: tuple containing (start, end, step) values for max_leaf_nodes parameter \n
        min_samples_split_v: tuple containing (start, end, step) values for min_samples_split parameter \n
        printall: whether to print all results (default is False) \n
        sortresultby: list of columns to sort the results by (default is ['score_diff']) \n
        return: best DecisionTreeClassifier model
        """

        # define the parameters of the tree to iterate over - Define by default
        max_depth_values = np.arange(max_depth_v[0], max_depth_v[1],
                                     max_depth_v[2])
        max_leaf_nodes_values = np.arange(max_leaf_nodes_v[0],
                                          max_leaf_nodes_v[1],
                                          max_leaf_nodes_v[2])
        min_samples_split_values = np.arange(min_samples_split_v[0],
                                             min_samples_split_v[1],
                                             min_samples_split_v[2])

        # initialize variables to store the best model and its performance
        best_estimator = None
        best_scoreF1Difference = float('inf')
        best_scoreRecallDifference = float('inf')
        results = pd.DataFrame(columns=[
            'TreeDepth', 'LeafNodes', 'SampleSplit', 'Accuracy', 'Recall',
            'Precision', 'F1', 'F1Difference', 'RecallDifference'
        ])

        # iterate over all combinations of the specified parameter values
        for max_depth in max_depth_values:
            for max_leaf_nodes in max_leaf_nodes_values:
                for min_samples_split in min_samples_split_values:

                    # initialize the tree with the current set of parameters
                    estimator = DecisionTreeClassifier(
                        max_depth=max_depth,
                        max_leaf_nodes=max_leaf_nodes,
                        min_samples_split=min_samples_split,
                        random_state=DT.RANDOM_STATE) 

                    # fit the model to the training data
                    estimator.fit(X_train, y_train)

                    # make predictions on the training and test sets
                    y_train_pred = estimator.predict(X_train)
                    y_test_pred = estimator.predict(X_test)

                    # calculate F1 scores for training and test sets
                    train_f1_score = f1_score(y_train, y_train_pred)
                    test_f1_score = f1_score(y_test, y_test_pred)
                    # calculate the absolute difference between training and test F1 scores
                    scoreF1Difference = abs(train_f1_score - test_f1_score)

                    # Calculate recall scores for training and test sets
                    train_recall_score = recall_score(y_train, y_train_pred)
                    test_recall_score = recall_score(y_test, y_test_pred)
                    # Calculate the absolute difference between training and test recall scores
                    scoreRecallDifference = abs(train_recall_score -
                                                test_recall_score)

                    test_performance = DT.model_performance_classification(
                        model=estimator,
                        predictors=X_test,
                        expected=y_test,
                        title="DecisionTreeClassifier",
                        printall=False)

                    results = pd.concat([
                        results,
                        pd.DataFrame(
                            {
                                'TreeDepth': [max_depth],
                                'LeafNodes': [max_leaf_nodes],
                                'SampleSplit': [min_samples_split],
                                'Accuracy':test_performance['Accuracy'].values,
                                'Recall': test_performance['Recall'].values,
                                'Precision':test_performance['Precision'].values,
                                'F1': test_performance['F1'].values,
                                'F1Difference': [scoreF1Difference],
                                'RecallDifference': [scoreRecallDifference]
                            })
                    ],
                                        ignore_index=True)

                    # update the best estimator and best score if the current one has a smaller score difference
                    if (scoreF1Difference < best_scoreF1Difference):
                        best_scoreF1Difference = scoreF1Difference
                        best_scoreRecallDifference = scoreRecallDifference
                        best_estimator = estimator

        results.sort_values(by=sortresultby,
                            ascending=sortbyAscending,
                            inplace=True)

        best_results = pd.DataFrame({
            'TreeDepth': [best_estimator.get_params()['max_depth']],
            'LeafNodes': [best_estimator.get_params()['max_leaf_nodes']],
            'SampleSplit': [best_estimator.get_params()['min_samples_split']],
            'F1Difference': [best_scoreF1Difference],
            'RecallDifference': [best_scoreRecallDifference]
        })
        print("-" * DT.NUMBER_OF_DASHES)
        display(best_results)
        print("-" * DT.NUMBER_OF_DASHES)
        # Set display option to show all rows

        if printall:
            pd.set_option('display.max_rows', None)
            display(results)
            pd.reset_option('display.max_rows')
        else:
            display(results)

        return best_estimator

        # END OF TUNE DECISION TREE FUNCTION
    @staticmethod
    def tune_decision_tree_results(
            X_train: pd.DataFrame,
            y_train: pd.Series,
            X_test: pd.DataFrame,
            y_test: pd.Series,
            max_depth_v: tuple[int, int, int] = (2, 11, 2),
            max_leaf_nodes_v: tuple[int, int, int] = (10, 51, 10),
            min_samples_split_v: tuple[int, int, int] = (10, 51, 10),
            printall: bool = False,
            sortresultby: list = ['F1Difference'],
            sortbyAscending: bool = False,
            metrictooptimize: str = 'F1Difference') -> dict:
        """
        Function to tune hyperparameters of Decision Tree Classifier \n
        X_train: training independent variables \n
        y_train: training dependent variable \n
        X_test: test independent variables \n  
        y_test: test dependent variable
        max_depth_v: tuple containing (start, end, step) values for max_depth parameter \n
        max_leaf_nodes_v: tuple containing (start, end, step) values for max_leaf_nodes parameter \n
        min_samples_split_v: tuple containing (start, end, step) values for min_samples_split parameter \n
        printall: whether to print all results (default is False) \n
        sortresultby: list of columns to sort the results by (default is ['score_diff']) \n
        metrictooptimize: metric to optimize (default is 'F1Difference') | possible values: 'Accuracy', 'Recall', 'Precision', F1Difference', 'RecallDifference' \n
        return: dictionary containing the scores dataframe, tuned model scores dataframe, and the best DecisionTreeClassifier model
        """
        # Metric Column Indices
        metric = {
            'Accuracy': 3,
            'Recall': 4,
            'Precision': 5,
            'F1': 6,
            'F1Difference': 7,
            'RecallDifference': 8
        }[metrictooptimize]

        # define the parameters of the tree to iterate over - Define by default
        max_depth_values = np.arange(max_depth_v[0], max_depth_v[1],
                                     max_depth_v[2])
        max_leaf_nodes_values = np.arange(max_leaf_nodes_v[0],
                                          max_leaf_nodes_v[1],
                                          max_leaf_nodes_v[2])
        min_samples_split_values = np.arange(min_samples_split_v[0],
                                             min_samples_split_v[1],
                                             min_samples_split_v[2])

        # initialize variables to store the best model and its performance
        best_estimator = None
        best_scoreF1Difference = float('inf')
        best_scoreRecallDifference = float('inf')
        scores = pd.DataFrame(columns=[
            'TreeDepth', 'LeafNodes', 'SampleSplit', 'Accuracy', 'Recall',
            'Precision', 'F1', 'F1Difference', 'RecallDifference'
        ])

        # iterate over all combinations of the specified parameter values
        for max_depth in max_depth_values:
            for max_leaf_nodes in max_leaf_nodes_values:
                for min_samples_split in min_samples_split_values:

                    # initialize the tree with the current set of parameters
                    estimator = DecisionTreeClassifier(
                        max_depth=max_depth,
                        max_leaf_nodes=max_leaf_nodes,
                        min_samples_split=min_samples_split,
                        random_state=DT.RANDOM_STATE)

                    # fit the model to the training data
                    estimator.fit(X_train, y_train)

                    # make predictions on the training and test sets
                    y_train_pred = estimator.predict(X_train)
                    y_test_pred = estimator.predict(X_test)

                    # calculate F1 scores for training and test sets
                    train_f1_score = metrics.f1_score(y_train, y_train_pred)
                    test_f1_score = metrics.f1_score(y_test, y_test_pred)
                    # calculate the absolute difference between training and test F1 scores
                    scoreF1Difference = abs(train_f1_score - test_f1_score)

                    # Calculate recall scores for training and test sets
                    train_recall_score = metrics.recall_score(y_train, y_train_pred)
                    test_recall_score = metrics.recall_score(y_test, y_test_pred)
                    # Calculate the absolute difference between training and test recall scores
                    scoreRecallDifference = abs(train_recall_score -
                                                test_recall_score)

                    test_performance = DT.model_performance_classification(
                        model=estimator,
                        predictors=X_test,
                        expected=y_test,
                        title="DecisionTreeClassifier",
                        printall=False)
                        
                    score = pd.DataFrame({
                        'TreeDepth': [max_depth],
                        'LeafNodes': [max_leaf_nodes],
                        'SampleSplit': [min_samples_split],
                        'Accuracy': test_performance['Accuracy'].values,
                        'Recall': test_performance['Recall'].values,
                        'Precision':test_performance['Precision'].values,
                        'F1':   test_performance['F1'].values,
                        'F1Difference': [scoreF1Difference],
                        'RecallDifference': [scoreRecallDifference]
                    })

                    scores = pd.concat([scores, score], ignore_index=True)

                    # update the best estimator and best score if the current one has a smaller score difference
                    if (score[metric] < best_score[metric]):
                        best_score = score
                        best_estimator = estimator

        scores.sort_values(by=sortresultby,
                           ascending=sortbyAscending,
                           inplace=True)

        tuned_model_scores = pd.DataFrame({
            'TreeDepth': [best_estimator.get_params()['max_depth']],
            'LeafNodes': [best_estimator.get_params()['max_leaf_nodes']],
            'SampleSplit': [best_estimator.get_params()['min_samples_split']],
            'F1Difference': [best_scoreF1Difference],
            'RecallDifference': [best_scoreRecallDifference]
        })

        if (printall):
            print("-" * DT.NUMBER_OF_DASHES)
            display(tuned_model_scores)
            print("-" * DT.NUMBER_OF_DASHES)
            # Set display option to show all rows
            pd.set_option('display.max_rows', None)
            display(scores)
            pd.reset_option('display.max_rows')

        return {
            'scores': scores,
            'tuned_model_scores': tuned_model_scores,
            'model': best_estimator
        }

        # END OF TUNE DECISION TREE FUNCTION
    @staticmethod
    def plot_feature_importance(model: DecisionTreeClassifier,
                                features: list,
                                figsize: tuple[float, float] = (10, 6),
                                numberoftopfeatures: int = None,
                                title: str = '',
                                ignoreZeroImportance: bool = False,
                                ) -> None:
        """
        Plot feature importance for a given model and feature names

        model: trained model with feature_importances_ attribute \n
        feature_names: list of feature names    \n
        figsize: size of the figure (default (10,6)) \n
        numberoftopfeatures: number of top features to display (default None, i.e., display all features) \n
        return: None
        """

        df_importance = pd.DataFrame({
            'Feature': features,
            'Importance': model.feature_importances_
        }).sort_values(by='Importance', ascending=False)

        if numberoftopfeatures:
            df_importance.head(numberoftopfeatures, inplace=True)

        if ignoreZeroImportance:
            df_importance = df_importance[df_importance['Importance'] > 0]

        display(df_importance)

        plt.figure(figsize=figsize)
        sns.barplot(x='Importance',
                    y='Feature',
                    data=df_importance,
                    palette='viridis')
        plt.title('Feature and their Importance Scores : ' + title)
        plt.xlabel('Importance Score')
        plt.ylabel('Features')
        plt.show()
        sys.stdout.flush()

        # END OF PLOT FEATURE IMPORTANCE FUNCTION
    @staticmethod
    def visualize_decision_tree(model: DecisionTreeClassifier,
                                features: list,
                                classes: list = None,
                                figsize: tuple[float, float] = (20, 10),
                                showtext: bool = False,
                                showimportance: bool = False) -> None:
        """
        Visualize the structure of the decision tree \n

        model: trained DecisionTreeClassifier model \n
        feature_names: list of feature names \n
        class_names: list of class names \n
        figsize: size of the figure (default (20,10)) \n
        showtext: whether to show the text report showing the rules of a decision tree (default False) \n
        shiwImportance: whether to show feature importance (default False) \n
        return: None
        """

        display(HTML("<h2>Visualizing Decision Tree</h2>"))
        # set the figure size for the plot
        plt.figure(figsize=figsize)

        # plotting the decision tree
        out = tree.plot_tree(
            model,  # decision tree classifier model
            feature_names=
            features,  # list of feature names (columns) in the dataset
            filled=True,  # fill the nodes with colors based on class
            fontsize=9,  # font size for the node text
            node_ids=False,  # do not show the ID of each node
            class_names=classes,  # whether or not to display class names
        )

        # add arrows to the decision tree splits if they are missing
        for o in out:
            arrow = o.arrow_patch
            if arrow is not None:
                arrow.set_edgecolor("black")  # set arrow color to black
                arrow.set_linewidth(1)  # set arrow linewidth to 1

        # displaying the plot
        plt.show()
        sys.stdout.flush()

        if (showtext):
            display(HTML("<h3>Text depiction of the Decision Tree</h3>"))
            # printing a text report showing the rules of a decision tree
            print(
                tree.export_text(
                    model,  # specify the model
                    feature_names=features,  # specify the feature names
                    show_weights=
                    True  # specify whether or not to show the weights associated with the model
                ))
            print("*" * DT.NUMBER_OF_DASHES)

        if (showimportance):
            display(HTML("<h3>Feature Importance</h3>"))
            DT.plot_feature_importance(model, features=features)
            print("*" * DT.NUMBER_OF_DASHES)

        return None

        # END OF VISUALIZE DECISION TREE FUNCTION
    @staticmethod
    def prepruning_nodes_samples_split(X_train: pd.DataFrame,
                                       y_train: pd.Series,
                                       X_test: pd.DataFrame,
                                       y_test: pd.Series,
                                       max_depth_v=(2, 9, 2),
                                       max_leaf_nodes_v=(50, 250, 50),
                                       min_samples_split_v=(10, 70, 10),
                                       printall=True,
                                       sortresultby="F1",
                                       sortbyAscending=False) -> dict:
        """
        Function to perform pre-pruning on Decision Tree Classifier \n
        X_train: training independent variables \n
        y_train: training dependent variable \n
        X_test: test independent variables \n  
        y_test: test dependent variable \n  
        max_depth_v: tuple containing (start, end, step) values for max_depth parameter \n
        max_leaf_nodes_v: tuple containing (start, end, step) values for max_leaf_nodes parameter \n
        min_samples_split_v: tuple containing (start, end, step) values for min_samples_split parameter \n
        printall: whether to print all results (default is True) \n
        sortresultby: column to sort the results by (default is 'F1') \n
        return: dictionary containing the pre-pruned model and its performance metrics
        """

        tuning_results = DT.tune_decision_tree_results(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            max_depth_v=max_depth_v,
            max_leaf_nodes_v=max_leaf_nodes_v,
            min_samples_split_v=min_samples_split_v,
            printall=False,
            sortresultby=[sortresultby],
            sortbyAscending=sortbyAscending)

        if (printall):
            display(HTML("<h3>Tuning Results - All Combinations</h3>"))
            # Set display option to show all rows
            pd.set_option('display.max_rows', None)
            display(tuning_results['scores'])
            # Reset display option to default
            pd.reset_option('display.max_rows')
            print("-" * DT.NUMBER_OF_DASHES)

            display(HTML("<h3>Tuning Results - Best Combination</h3>"))
            display(tuning_results['tuned_model_scores'])
            print("-" * DT.NUMBER_OF_DASHES)

        model_prepruning = tuning_results['model'].fit(X=X_train, y=y_train)

        features = list(X_train.columns)

        if (printall):
            DT.visualize_decision_tree(model=model_prepruning,
                                         features=features,
                                         classes=None,
                                         figsize=(20, 20),
                                         showtext=True,
                                         showimportance=True)

        model_prepruning_train_perf = DT.model_performance_classification(
            model=model_prepruning, predictors=X_train, expected=y_train)

        if (printall):
            display(HTML("<h3>Pre-pruning on Training Set</h3>"))
            DT.plot_confusion_matrix(model=model_prepruning,
                                       predictors=X_train,
                                       expected=y_train,
                                       title="Pre-pruning on Test Set")
            display(model_prepruning_train_perf)

        model_prepruning_test_perf = DT.model_performance_classification(
            model=model_prepruning, predictors=X_test, expected=y_test)

        if (printall):
            display(HTML("<h3>Pre-pruning on Train Set</h3>"))
            DT.plot_confusion_matrix(model=model_prepruning,
                                       predictors=X_test,
                                       expected=y_test,
                                       title="Pre-pruning on Train Set")
            display(model_prepruning_test_perf)

        return {
            'model': model_prepruning,
            'prepruning_train_perf': model_prepruning_train_perf,
            'prepruning_test_perf': model_prepruning_test_perf,
            'prepruning_scores_tuned': tuning_results['tuned_model_scores'],
            'prepruning_scores_all': tuning_results['scores']
        }

        # END OF PRE-PRUNING FUNCTION
    @staticmethod
    def postpruning_cost_complexity(
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        printall: bool = True,
        figsize: tuple[float, float] = (10, 6)) -> dict:
        """
        Plot cost complexity pruning path and accuracy vs alpha for training and testing sets \n
        X_train: training independent variables \n
        y_train: training dependent variable \n
        X_test: test independent variables \n  
        y_test: test dependent variable \n
        printall: whether to print all results (default is True) \n
        figsize: size of the figure (default (10,6)) \n
        return: None
        """
        # Create an instance of the decision tree model
        decisionTreeClassifier = DecisionTreeClassifier(
            random_state=DT.RANDOM_STATE)

        # Compute the cost complexity pruning path for the model using the training data
        path = decisionTreeClassifier.cost_complexity_pruning_path(
            X_train, y_train)

        # Extract the array of effective alphas from the pruning path,  Extract the array of total impurities at each alpha along the pruning path
        ccp_alphas, impurities = path.ccp_alphas, path.impurities

        if (printall):
            display(
                HTML(
                    "<h3>Effective alphas and corresponding total impurities</h3>"
                ))
            display(
                pd.DataFrame({
                    'ccp_alphas': ccp_alphas,
                    'impurities': impurities
                }))

            # Create a figure
            fig, ax = plt.subplots(figsize=figsize)

            # Plot the total impurities versus effective alphas, excluding the last value,
            # using markers at each data point and connecting them with steps
            ax.plot(ccp_alphas[:-1],
                    impurities[:-1],
                    marker="o",
                    drawstyle="steps-post")

            # Set the x-axis label
            ax.set_xlabel("Effective Alpha")

            # Set the y-axis label
            ax.set_ylabel("Total impurity of leaves")

            # Set the title of the plot
            ax.set_title("Total Impurity vs Effective Alpha for training set")

        #Initialize an empty list to store the decision tree classifiers
        decisionTreeClassifiers = []

        # Iterate over each ccp_alpha value extracted from cost complexity pruning path
        for ccp_alpha in ccp_alphas:
            # Create an instance of the DecisionTreeClassifier
            decisionTreeClassifier = DecisionTreeClassifier(
                ccp_alpha=ccp_alpha, random_state=DT.RANDOM_STATE)

            # Fit the classifier to the training data
            decisionTreeClassifier.fit(X_train, y_train)

            # Append the trained classifier to the list
            decisionTreeClassifiers.append(decisionTreeClassifier)
        if (printall):
            # Print the number of nodes in the last tree along with its ccp_alpha value
            display(
                HTML(
                    "<b>Number of nodes in the last tree is {} with ccp_alpha {}</b> "
                    .format(decisionTreeClassifiers[-1].tree_.node_count,
                            ccp_alphas[-1])))

        # Remove the last classifier and corresponding ccp_alpha value from the lists
        decisionTreeClassifiers = decisionTreeClassifiers[:-1]
        ccp_alphas = ccp_alphas[:-1]

        # Extract the number of nodes in each tree classifier
        node_counts = [
            decisionTreeClassifier.tree_.node_count
            for decisionTreeClassifier in decisionTreeClassifiers
        ]

        # Extract the maximum depth of each tree classifier
        depth = [
            decisionTreeClassifier.tree_.max_depth
            for decisionTreeClassifier in decisionTreeClassifiers
        ]

        # Create a figure and a set of subplots
        fig, ax = plt.subplots(2, 1, figsize=figsize)

        # Plot the number of nodes versus ccp_alphas on the first subplot
        ax[0].plot(ccp_alphas, node_counts, marker="o", drawstyle="steps-post")
        ax[0].set_xlabel("Alpha")
        ax[0].set_ylabel("Number of nodes")
        ax[0].set_title("Number of nodes vs Alpha")

        # Plot the depth of tree versus ccp_alphas on the second subplot
        ax[1].plot(ccp_alphas, depth, marker="o", drawstyle="steps-post")
        ax[1].set_xlabel("Alpha")
        ax[1].set_ylabel("Depth of tree")
        ax[1].set_title("Depth vs Alpha")

        # Adjust the layout of the subplots to avoid overlap
        fig.tight_layout()
        fig.show()
        sys.stdout.flush()

        # Initialize an empty list to store F1 scores for training set for each decision tree classifier
        train_f1_scores = []

        # Iterate through each decision tree classifier in 'decisionTreeClassifiers'
        for decisionTreeClassifier in decisionTreeClassifiers:
            # Predict labels for the training set using the current decision tree classifier
            pred_train = decisionTreeClassifier.predict(X_train)

            # Calculate the F1 score for the training set predictions compared to true labels
            f1_train = f1_score(y_train, pred_train)

            # Append the calculated F1 score to the train_f1_scores list
            train_f1_scores.append(f1_train)

        # Initialize an empty list to store F1 scores for test set for each decision tree classifier
        test_f1_scores = []

        # Iterate through each decision tree classifier in 'decisionTreeClassifiers'
        for decisionTreeClassifier in decisionTreeClassifiers:
            # Predict labels for the test set using the current decision tree classifier
            pred_test = decisionTreeClassifier.predict(X_test)

            # Calculate the F1 score for the test set predictions compared to true labels
            f1_test = f1_score(y_test, pred_test)

            # Append the calculated F1 score to the test_f1_scores list
            test_f1_scores.append(f1_test)

        if (printall):
            # Create a figure
            fig, ax = plt.subplots(figsize=figsize)
            ax.set_xlabel("Alpha")  # Set the label for the x-axis
            ax.set_ylabel("F1 Score")  # Set the label for the y-axis
            ax.set_title("F1 Score vs Alpha for training and test sets"
                         )  # Set the title of the plot

            # Plot the training F1 scores against alpha, using circles as markers and steps-post style
            ax.plot(ccp_alphas,
                    train_f1_scores,
                    marker="o",
                    label="training",
                    drawstyle="steps-post")

            # Plot the testing F1 scores against alpha, using circles as markers and steps-post style
            ax.plot(ccp_alphas,
                    test_f1_scores,
                    marker="o",
                    label="test",
                    drawstyle="steps-post")

            # Add a legend to the plot
            ax.legend()

        # creating the model where we get highest test F1 Score
        index_best_model = np.argmax(test_f1_scores)

        # selcting the decision tree model corresponding to the highest test score
        model_postpruning = decisionTreeClassifiers[index_best_model]

        if (printall):
            display(model_postpruning)
            DT.plot_confusion_matrix(model=model_postpruning,
                                       predictors=X_train,
                                       expected=y_train,
                                       title="Post-pruning on Training Set")

        model_postpruning_train_perf = DT.model_performance_classification(
            model=model_postpruning,
            predictors=X_train,
            expected=y_train,
            title="Post-pruning on Training Set")
        if (printall):
            display(model_postpruning_train_perf)
            DT.plot_confusion_matrix(model=model_postpruning,
                                       predictors=X_test,
                                       expected=y_test,
                                       title="Post-pruning on Test Set")

        model_postpruning_test_perf = DT.model_performance_classification(
            model=model_postpruning,
            predictors=X_test,
            expected=y_test,
            title="Post-pruning on Test Set")

        if (printall):
            display(model_postpruning_test_perf)
        if (printall):
            DT.visualize_decision_tree(model=model_postpruning,
                                         features=X_train.columns,
                                         classes=None,
                                         figsize=(20, 20),
                                         showtext=True,
                                         showimportance=True)

        return {
            'model': model_postpruning,
            'postpruning_train_perf': model_postpruning_train_perf,
            'postpruning_test_perf': model_postpruning_test_perf,
            'train_f1_scores': train_f1_scores,
            'test_f1_scores': test_f1_scores,
            'ccp_alphas': ccp_alphas,
            'impurities': impurities
        }

        # END OF POST-PRUNING FUNCTION
