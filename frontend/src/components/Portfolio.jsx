import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Portfolio() {
  const [portfolio, setPortfolio] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/api/portfolio')
      .then(response => {
        setPortfolio(response.data.portfolio);
        setLoading(false);
      })
      .catch(err => {
        console.error("Erreur lors de la récupération du portefeuille", err);
        setError("Impossible de charger le portefeuille.");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Chargement du portefeuille...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Votre Portefeuille Actuel</h2>
      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #ddd' }}>
            <th>Ticker</th>
            <th>Quantité</th>
            <th>Prix d'Achat ($)</th>
          </tr>
        </thead>
        <tbody>
          {portfolio.map((item, index) => (
            <tr key={index} style={{ borderBottom: '1px solid #eee' }}>
              <td>{item.ticker}</td>
              <td>{item.quantity}</td>
              <td>{item.buyPrice.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Portfolio;
