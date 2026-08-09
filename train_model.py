import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

from feature_extractor import extract_features


# ============================================================
# LOAD DATASET
# ============================================================

dataset = pd.read_csv("dataset/phishing_email.csv")

print("=" * 60)
print("          PHISHING EMAIL DETECTION MODEL")
print("=" * 60)

X = dataset["text_combined"]
y = dataset["label"]


# ============================================================
# SPLIT DATASET
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"\nTraining Emails : {len(X_train)}")
print(f"Testing Emails  : {len(X_test)}")


# ============================================================
# FEATURE EXTRACTION
# ============================================================

print("\nExtracting TF-IDF features...")

X_train_features, X_test_features, vectorizer = extract_features(
    X_train,
    X_test
)

print("Feature extraction complete.")


# ============================================================
# TRAIN MODEL
# ============================================================

print("\nTraining Machine Learning Model...")

model = MultinomialNB()

model.fit(X_train_features, y_train)

print("Training Complete!")


# ============================================================
# PREDICTIONS
# ============================================================

predictions = model.predict(X_test_features)


# ============================================================
# ACCURACY
# ============================================================

accuracy = accuracy_score(y_test, predictions)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"\nAccuracy : {accuracy * 100:.2f}%")


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=["Safe", "Phishing"]
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(y_test, predictions)

print("Confusion Matrix:")
print(cm)


# ============================================================
# CONFUSION MATRIX VISUALIZATION
# ============================================================

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Safe", "Phishing"]
)

display.plot()

plt.title("Phishing Email Detection - Confusion Matrix")
plt.tight_layout()

plt.savefig("confusion_matrix.png")

plt.show()


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(model, "phishing_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel saved successfully!")
print("Files created:")
print("- phishing_model.pkl")
print("- vectorizer.pkl")
print("- confusion_matrix.png")