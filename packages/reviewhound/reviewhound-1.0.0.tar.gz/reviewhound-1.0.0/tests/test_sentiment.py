import pytest

from reviewhound.analysis.sentiment import analyze_review


class TestSentimentAnalysis:
    def test_positive_review(self):
        text = "Absolutely amazing! Best experience ever. Highly recommend!"
        score, label = analyze_review(text)
        assert label == "positive"
        assert score > 0.1

    def test_negative_review(self):
        text = "Terrible service. Worst experience of my life. Avoid at all costs."
        score, label = analyze_review(text)
        assert label == "negative"
        assert score < -0.1

    def test_neutral_review(self):
        text = "The product arrived. It works as described."
        score, label = analyze_review(text)
        assert label == "neutral"
        assert -0.1 <= score <= 0.1

    def test_empty_text(self):
        score, label = analyze_review("")
        assert label == "neutral"
        assert score == 0.0

    def test_very_short_text(self):
        score, label = analyze_review("OK")
        assert label in ("positive", "negative", "neutral")
        assert -1.0 <= score <= 1.0
