import unittest
from core.agent import TradingAgent

class TestTradingAgent(unittest.TestCase):
    def setUp(self):
        self.agent = TradingAgent()

    def test_analyze_sentiment(self):
        positive_text = "The company is amazing and excellent."
        negative_text = "The company is terrible and awful."

        pos_score = self.agent.analyze_sentiment(positive_text)
        neg_score = self.agent.analyze_sentiment(negative_text)

        # Le sentiment positif doit être supérieur au sentiment négatif
        self.assertTrue(pos_score > neg_score)

    def test_generate_signal_structure(self):
        # Tester que la fonction renvoie bien un dictionnaire avec les clés attendues
        signal = self.agent.generate_signal("AAPL")

        self.assertIsInstance(signal, dict)
        self.assertIn("ticker", signal)
        self.assertIn("action", signal)
        self.assertIn("reason", signal)

    def test_mock_market_data(self):
        # Vérifier que le mock data renvoie bien un DataFrame
        df = self.agent._generate_mock_market_data()
        self.assertFalse(df.empty)
        self.assertIn("Close", df.columns)
        self.assertEqual(len(df), 90)

if __name__ == '__main__':
    unittest.main()
