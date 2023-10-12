import csv
import sys
import datetime

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
    evidence = list()
    labels = list()
    i = 0
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            ev = list()
            if i == 0:
                i = 1
                continue
            for index, value in enumerate(row):
                if index in (0,2,4,11,12,13,14):
                    ev.append(int(value))
                elif index == 10:
                    ev.append(datetime.datetime.strptime(value[:3], '%b').month -1)
                elif index == 15:
                    ev.append(1 if value == 'Returning_Visitor' else 0)
                elif index == 16:
                    ev.append(1 if value == 'TRUE' else 0)
                elif index == 17:
                    labels.append(1 if value == 'TRUE' else 0)
                else:
                    ev.append(float(value))
            evidence.append(ev)

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    classifier = KNeighborsClassifier(1)
    classifier.fit(evidence, labels)
    return classifier

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
    correct_positives = 0
    positives = 0
    correct_negatives = 0
    negatives = 0
    for i in range(len(labels)):
        if labels[i]:
            positives += 1
            if labels[i] == predictions[i]:
                correct_positives += 1
        else:
            negatives += 1
            if labels[i] == predictions[i]:
                correct_negatives += 1

    return correct_positives / positives, correct_negatives / negatives


if __name__ == "__main__":
    main()
