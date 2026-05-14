import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AssetChart from './AssetChart';

function AssetDetails({ ticker, onBack }) {
  const [signal, setSignal] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDetails = () => {
    setLoading(true);
    axios.get(`/api/analyze/${ticker}`)
      .then(res => {
        setSignal(res.data.signal);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchDetails();
    const interval = setInterval(fetchDetails, 60000); // Refresh toutes les minutes
    return () => clearInterval(interval);
  }, [ticker]);

  if (loading && !signal) return <p>Analyse de {ticker} en cours par l'IA...</p>;

  const getActionColor = (action) => {
    if (action.includes('BUY')) return 'green';
    if (action.includes('SELL')) return 'red';
    return 'orange';
  };

  return (
    <div>
      <button onClick={onBack} style={{ marginBottom: '20px', padding: '5px 10px', cursor: 'pointer' }}>
        ← Retour au Portefeuille
      </button>

      <h2>Analyse Détaillée : {ticker}</h2>

      {signal && (
        <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '300px', backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '5px', borderLeft: `5px solid ${getActionColor(signal.action)}` }}>
            <h3 style={{ margin: '0 0 10px 0' }}>Prix Actuel: ${signal.current_price?.toFixed(2)}</h3>
            <p><strong>Recommandation IA :</strong> <span style={{ color: getActionColor(signal.action), fontWeight: 'bold', fontSize: '1.2em' }}>{signal.action}</span></p>

            <h4 style={{ marginTop: '20px' }}>Justification de l'Expert :</h4>
            <ul style={{ paddingLeft: '20px', lineHeight: '1.6' }}>
              {signal.reason.split(' | ').map((line, idx) => {
                 if (line.includes('Prix actuel:')) return null;
                 if (line.includes('Signal Tech')) return null;
                 return <li key={idx}>{line}</li>;
              })}
            </ul>
          </div>
        </div>
      )}

      {/* Graphique de l'évolution */}
      <AssetChart ticker={ticker} />
    </div>
  );
}

export default AssetDetails;
