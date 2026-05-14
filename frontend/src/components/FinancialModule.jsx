import React, { useState, useEffect } from 'react';
import axios from 'axios';

function FinancialModule() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/transactions')
      .then(res => {
        setTransactions(res.data.transactions);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Chargement du module financier...</p>;

  return (
    <div>
      <h2>🏦 Module Financier - Historique des Transactions</h2>
      <p>Retrouvez ici toutes vos opérations (Actions, Crypto, Obligations, etc.) pour un suivi parfait de votre portefeuille Trade Republic.</p>

      {transactions.length === 0 ? (
        <p>Aucune transaction pour le moment.</p>
      ) : (
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse', marginTop: '20px' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #ddd', backgroundColor: '#f1f1f1' }}>
              <th style={{ padding: '10px' }}>Date</th>
              <th style={{ padding: '10px' }}>Type</th>
              <th style={{ padding: '10px' }}>Actif</th>
              <th style={{ padding: '10px' }}>Quantité</th>
              <th style={{ padding: '10px' }}>Prix Unitaire</th>
              <th style={{ padding: '10px' }}>Total</th>
            </tr>
          </thead>
          <tbody>
            {transactions.slice().reverse().map((t, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '10px' }}>{new Date(t.date).toLocaleString()}</td>
                <td style={{ padding: '10px', color: t.type === 'BUY' ? 'green' : 'red', fontWeight: 'bold' }}>{t.type}</td>
                <td style={{ padding: '10px', fontWeight: 'bold' }}>{t.ticker}</td>
                <td style={{ padding: '10px' }}>{t.quantity}</td>
                <td style={{ padding: '10px' }}>${t.price.toFixed(2)}</td>
                <td style={{ padding: '10px' }}>${t.total.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default FinancialModule;
