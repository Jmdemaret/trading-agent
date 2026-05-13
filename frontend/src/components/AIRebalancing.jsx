import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function AIRebalancing() {
  const [data, setData] = useState([]);
  const [reasoning, setReasoning] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/api/rebalance')
      .then(response => {
        const current = response.data.current;
        const recommended = response.data.recommended;
        setReasoning(response.data.reasoning);

        // Formater les données pour Recharts
        const chartData = current.map(item => {
          const recItem = recommended.find(r => r.name === item.name);
          return {
            name: item.name,
            'Allocation Actuelle (%)': item.value,
            'Recommandation IA (%)': recItem ? recItem.value : 0
          };
        });

        setData(chartData);
        setLoading(false);
      })
      .catch(err => {
        console.error("Erreur rééquilibrage", err);
        setError("Erreur lors de la récupération des recommandations.");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Calcul des projections IA en cours...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>🤖 Rééquilibrage Prédictif IA</h2>
      <p>
        <em>Feature Révolutionnaire</em> : Notre agent n'analyse pas seulement le passé, il projette
        l'allocation optimale pour maximiser le rendement selon les conditions de marché actuelles.
      </p>

      <div style={{ height: 400, marginTop: '30px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Allocation Actuelle (%)" fill="#8884d8" />
            <Bar dataKey="Recommandation IA (%)" fill="#82ca9d" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#e9ecef', borderRadius: '5px' }}>
        <strong>Raisonnement de l'IA : </strong> {reasoning}
      </div>
    </div>
  );
}

export default AIRebalancing;
