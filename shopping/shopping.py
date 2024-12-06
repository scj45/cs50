import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename, "r") as f:
        csvusers = csv.DictReader(f, delimiter=',')

        evidence = []
        labels = []

        for row in csvusers:
            evidence.append([
                int(row["Administrative"]),
                float(row["Administrative_Duration"]),
                int(row["Informational"]),
                float(row["Informational_Duration"]),
                int(row["ProductRelated"]),
                float(row["ProductRelated_Duration"]),
                float(row["BounceRates"]),
                float(row["ExitRates"]),
                float(row["PageValues"]),
                float(row["SpecialDay"]),
                (0 if row["Month"] == "Jan" else 1 if row["Month"] == "Feb" else 2 if row["Month"] == "Mar" else 3 if row["Month"] == "Apr" else 4 if row["Month"] == "May" else 5 if row["Month"]
                 == "June" else 6 if row["Month"] == "Jul" else 7 if row["Month"] == "Aug" else 8 if row["Month"] == "Sep" else 9 if row["Month"] == "Oct" else 10 if row["Month"] == "Nov" else 11),
                int(row["OperatingSystems"]),
                int(row["Browser"]),
                int(row["Region"]),
                int(row["TrafficType"]),
                1 if row["VisitorType"] == "Returning_Visitor" else 0,
                0 if row["Weekend"] == "FALSE" else 1
            ])
            labels.append(1 if row["Revenue"] == "TRUE" else 0)

        return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # Instantiate the model
    model = KNeighborsClassifier(n_neighbors=1)

    # Assuming lists of dictionaries
    evidence = [row for row in evidence]
    labels = [row for row in labels]

    X_training, X_testing, y_training, y_testing = train_test_split(
        evidence, labels, test_size=0.4
    )

    # Fit model
    model.fit(X_training, y_training)

    # Make predictions on the testing set
    predictions = model.predict(X_testing)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    actual = labels
    predicted = predictions
    truepos = 0
    trueneg = 0
    falsepos = 0
    falseneg = 0

    for a, p in zip(actual, predicted):
        if a == p:
            if a == True:
                truepos += 1
            else:
                trueneg += 1
        else:
            if p == True:
                falsepos += 1
            else:
                falseneg += 1

    sensitivity = truepos / (truepos + falseneg)
    specificity = trueneg / (trueneg + falsepos)

    # return a tuple (sensitivity, specificity)
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
