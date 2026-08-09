import joblib

from feature_extractor import extract_manual_features


# Load trained model
model = joblib.load("phishing_model.pkl")

# Load TF-IDF vectorizer
vectorizer = joblib.load("vectorizer.pkl")


print("=" * 50)
print("       PHISHING EMAIL DETECTOR")
print("=" * 50)

print("\nPaste the email below.")
print("When finished, type END on a new line.\n")


# Collect multi-line email
lines = []

while True:

    line = input()

    if line.strip().upper() == "END":
        break

    lines.append(line)


email = "\n".join(lines)


# Convert email into TF-IDF features
email_tfidf = vectorizer.transform([email])


# Extract explicit security features
manual_features = extract_manual_features(email)


# Combine TF-IDF + manual features
from scipy.sparse import csr_matrix, hstack

manual_features = csr_matrix([manual_features])

email_features = hstack([
    email_tfidf,
    manual_features
])


# Predict
prediction = model.predict(email_features)


print("\n" + "=" * 50)
print("             ANALYSIS")
print("=" * 50)

print(f"\nURL Count          : {manual_features.toarray()[0][0]:.0f}")
print(f"Phishing Keywords : {manual_features.toarray()[0][1]:.0f}")
print(f"Urgency Indicators: {manual_features.toarray()[0][2]:.0f}")
print(f"Contains URL      : {'Yes' if manual_features.toarray()[0][3] else 'No'}")


print("\nPrediction")

if prediction[0] == 1:

    print("🚨 PHISHING EMAIL")

else:

    print("✅ SAFE EMAIL")