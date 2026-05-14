import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Portfolio() {
  const [portfolio, setPortfolio] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Nouveaux états pour le formulaire
  const [newTicker, setNewTicker] = useState('');
  const [newQuantity, setNewQuantity] = useState('');
  const [newPrice, setNewPrice] = useState('');

  const fetchPortfolio = () => {
    setLoading(true);
    axios.get('/api/portfolio/live')
      .then(response => {
        setPortfolio(response.data.live_portfolio);
        setLoading(false);
      })
      .catch(err => {
        console.error("Erreur lors de la récupération du portefeuille", err);
        setError("Impossible de charger le portefeuille.");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchPortfolio();
    // Rafraîchir toutes les minutes
    const interval = setInterval(fetchPortfolio, 60000);
    return () => clearInterval(interval);
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newTicker || !newQuantity || !newPrice) return;

    try {
      // Passer par les transactions pour mettre à jour l'historique ET le portefeuille
      await axios.post('/api/transactions', {
        type: 'BUY',
        ticker: newTicker.toUpperCase(),
        quantity: parseFloat(newQuantity),
        price: parseFloat(newPrice)
      });
      setNewTicker(''); setNewQuantity(''); setNewPrice('');
      fetchPortfolio();
    } catch (err) {
      console.error(err);
      alert("Erreur lors de l'ajout.");
    }
  };

  const handleRemove = async (ticker, currentQuantity, currentPrice) => {
    try {
      // Pour l'instant, on vend la totalité pour simuler la suppression
      await axios.post('/api/transactions', {
        type: 'SELL',
        ticker: ticker,
        quantity: currentQuantity,
        price: currentPrice
      });
      fetchPortfolio();
    } catch (err) {
      console.error(err);
      alert("Erreur lors de la suppression.");
    }
  };

  if (loading && portfolio.length === 0) return <p>Chargement des données du marché en temps réel...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  // Props pour la navigation vers le détail
  const handleViewDetails = (ticker) => {
    // Dispatch un custom event pour que App.jsx le capte (ou passer par props)
    const event = new CustomEvent('viewAsset', { detail: ticker });
    window.dispatchEvent(event);
  };

  return (
    <div>
      <h2>📊 Votre Portefeuille (Temps Réel)</h2>

      <form onSubmit={handleAdd} style={{ marginBottom: '20px', display: 'flex', gap: '10px', alignItems: 'center', backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '5px' }}>
        <input type="text" placeholder="Ticker (ex: AAPL)" value={newTicker} onChange={e => setNewTicker(e.target.value)} required />
        <input type="number" placeholder="Quantité" value={newQuantity} onChange={e => setNewQuantity(e.target.value)} required step="0.01" />
        <input type="number" placeholder="Prix d'achat ($)" value={newPrice} onChange={e => setNewPrice(e.target.value)} required step="0.01" />
        <button type="submit" style={{ padding: '8px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>Ajouter</button>
      </form>

      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #ddd', backgroundColor: '#f1f1f1' }}>
            <th style={{ padding: '10px' }}>Ticker</th>
            <th style={{ padding: '10px' }}>Quantité</th>
            <th style={{ padding: '10px' }}>Prix d'Achat</th>
            <th style={{ padding: '10px' }}>Prix Actuel</th>
            <th style={{ padding: '10px' }}>Variation (24h)</th>
            <th style={{ padding: '10px' }}>Profit/Perte</th>
            <th style={{ padding: '10px' }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {portfolio.map((item, index) => {
             const isPositive = item.changePercent >= 0;
             const isProfit = item.profit >= 0;
             return (
              <tr key={index} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '10px', fontWeight: 'bold' }}>{item.ticker}</td>
                <td style={{ padding: '10px' }}>{item.quantity}</td>
                <td style={{ padding: '10px' }}>${item.buyPrice.toFixed(2)}</td>
                <td style={{ padding: '10px' }}>${item.currentPrice.toFixed(2)}</td>
                <td style={{ padding: '10px', color: isPositive ? 'green' : 'red', fontWeight: 'bold' }}>
                  {isPositive ? '▲' : '▼'} {Math.abs(item.changePercent).toFixed(2)}%
                </td>
                <td style={{ padding: '10px', color: isProfit ? 'green' : 'red' }}>
                   ${item.profit.toFixed(2)}
                </td>
                <td style={{ padding: '10px' }}>
                  <button onClick={() => handleViewDetails(item.ticker)} style={{ backgroundColor: '#17a2b8', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '3px', cursor: 'pointer', marginRight: '5px' }}>
                    Détails & Graph
                  </button>
                  <button onClick={() => handleRemove(item.ticker, item.quantity, item.currentPrice)} style={{ backgroundColor: '#dc3545', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '3px', cursor: 'pointer' }}>
                    Vendre / Supprimer
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default Portfolio;
