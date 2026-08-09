import re
import numpy as np

from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer


# Common words/patterns often found in phishing emails
PHISHING_KEYWORDS = [
    "urgent",
    "verify",
    "verification",
    "account suspended",
    "account locked",
    "click here",
    "confirm",
    "password",
    "login",
    "security alert",
    "bank",
    "winner",
    "prize",
    "reward",
    "claim",
    "limited time",
    "expire",
    "immediately",
    "credit card",
    "update your account"
]


def extract_manual_features(text):
    """
    Extract explicit security-related features from an email.
    """

    text_lower = text.lower()

    # Count URLs
    url_count = len(
        re.findall(r"https?://\S+|www\.\S+", text_lower)
    )

    # Count phishing-related keywords
    keyword_count = 0

    for keyword in PHISHING_KEYWORDS:
        if keyword in text_lower:
            keyword_count += 1

    # Count suspicious urgency words
    urgency_words = [
        "urgent",
        "immediately",
        "now",
        "asap",
        "warning",
        "alert",
        "expire"
    ]

    urgency_count = sum(
        1 for word in urgency_words
        if word in text_lower
    )

    # Check whether email contains a URL
    contains_url = 1 if url_count > 0 else 0

    return [
        url_count,
        keyword_count,
        urgency_count,
        contains_url
    ]


def extract_features(train_text, test_text):

    # TF-IDF text features
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    X_train_tfidf = vectorizer.fit_transform(train_text)
    X_test_tfidf = vectorizer.transform(test_text)

    # Explicit security features
    train_manual = np.array([
        extract_manual_features(text)
        for text in train_text
    ])

    test_manual = np.array([
        extract_manual_features(text)
        for text in test_text
    ])

    # Convert manual features to sparse matrices
    train_manual = csr_matrix(train_manual)
    test_manual = csr_matrix(test_manual)

    # Combine TF-IDF + security features
    X_train = hstack([
        X_train_tfidf,
        train_manual
    ])

    X_test = hstack([
        X_test_tfidf,
        test_manual
    ])

    return X_train, X_test, vectorizer