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
        - Administrative, int
        - Administrative_Duration, float
        - Informational, int
        - Informational_Duration, float
        - ProductRelated, int
        - ProductRelated_Duration, float
        - BounceRates, float
        - ExitRates, float
        - PageValues, float
        - SpecialDay, float
        - Month, an index from 0 (January) to 11 (December) 
        - OperatingSystems, int
        - Browser, int
        - Region, int
        - TrafficType, int
        - VisitorType, int 0 (not returning) or 1 (returning) 
        - Weekend, int 0 (if false) or 1 (if true) 

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    months = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}
    int_ranges = [0, 2, 4, 11, 12, 13, 14]
    float_ranges = [1, 3, 5, 6, 7, 8, 9]

    with open(filename) as f:

        reader = csv.DictReader(f)

        # add data from all the csv columns to evidence, add revenue to labels
        for row in reader: 
            evidence.append(list(row.values()))
            labels.append(row['Revenue'])
        
        for i in range(len(evidence)): 
            
            # converting visitor type from string to int
            if evidence[i][15] == 'Returning_Visitor':
                evidence[i][15] = 1
            else:
                evidence[i][15] = 0
            
            # converting weekend from string to int
            if evidence[i][16] == 'TRUE':
                evidence[i][16] = 1
            else:
                evidence[i][16] = 0

            # converting months to index (10)
            for month in months:
                if evidence[i][10] == month:
                    evidence[i][10] = months[month]
                
            # remove revenue from evidence 
            del evidence[i][-1]

            # final cleanup: converting remaining columns to int or float
            for index in int_ranges:
                evidence[i][index] = int(evidence[i][index])
            for index in float_ranges:
                evidence[i][index] = float(evidence[i][index])

        # converting labels from string to int
        for i in range(len(labels)):
            if labels[i] == 'TRUE':
                labels[i] = 1
            else:
                labels[i] = 0

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence, labels)

    return neigh

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    false_positives = 0
    false_negatives = 0
    
    for i in range(len(predictions)):
        if (predictions[i] != labels[i]) and labels[i] == 1:
            false_negatives += 1
        elif (predictions[i] != labels[i]) and labels[i] == 0:
            false_positives += 1
    
    sensitivity = 1 - (false_negatives / labels.count(1)) # true positive (1) rate
    specificity = 1 - (false_positives / labels.count(0)) # true negative (0) rate 

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()