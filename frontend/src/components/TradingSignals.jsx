import React, { useState } from 'react';
import axios from 'axios';

function TradingSignals() {
  const [tickers, setTickers] = useState(['AAPL', 'MSFT', 'TSLA', 'GOOGL']);
  const [signals, setSignals] = useState({});
  const [loading, setLoading] = useState(false);

  const analyzeAll = async () => {
    setLoading(true);
    const newSignals = {};
    for (const ticker of tickers) {
      try {
        const response = await axios.get(`/api/analyze/${ticker}`);
        newSignals[ticker] = response.data.signal;
      } catch (err) {
        newSignals[ticker] = { action: 'ERROR', reason: 'Erreur réseau ou API' };
      }
    }
    setSignals(newSignals);
    setLoading(false);
  };

  const getActionColor = (action) => {
    if (action.includes('BUY')) return 'green';
    if (action.includes('SELL')) return 'red';
    return 'orange';
  };

  return (
    <div>
      <h2>Analyse en Temps Réel de vos Actifs</h2>
      <button
        onClick={analyzeAll}
        disabled={loading}
        style={{ padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
      >
        {loading ? 'L\'IA analyse...' : 'Lancer l\'Analyse Expert'}
      </button>

      <div style={{ marginTop: '20px' }}>
        {Object.keys(signals).map(ticker => {
          const signal = signals[ticker];
          return (
            <div key={ticker} style={{ border: '1px solid #ddd', padding: '15px', marginBottom: '10px', borderRadius: '5px' }}>
              <h3>{ticker} <span style={{ float: 'right' }}>Prix: ${signal.current_price?.toFixed(2) || 'N/A'}</span></h3>
              <p>
                <strong>Signal: </strong>
                <span style={{ color: getActionColor(signal.action), fontWeight: 'bold' }}>
                  {signal.action}
                </span>
                {signal.confidence && ` (Confiance: ${signal.confidence})`}
              </p>
              <p style={{ fontStyle: 'italic', color: '#555' }}>{signal.reason}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default TradingSignals;
