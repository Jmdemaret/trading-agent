import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from 'react-apexcharts';

function AssetChart({ ticker }) {
  const [series, setSeries] = useState([]);
  const [period, setPeriod] = useState('1mo');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!ticker) return;
    setLoading(true);
    axios.get(`/api/chart/${ticker}?period=${period}`)
      .then(response => {
        if (response.data.data) {
          setSeries([{
            name: 'Prix',
            data: response.data.data
          }]);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Erreur chart", err);
        setLoading(false);
      });
  }, [ticker, period]);

  const options = {
    chart: {
      type: 'candlestick',
      height: 350
    },
    title: {
      text: `${ticker} - Évolution du cours`,
      align: 'left'
    },
    xaxis: {
      type: 'datetime'
    },
    yaxis: {
      tooltip: {
        enabled: true
      }
    }
  };

  return (
    <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#fff', borderRadius: '5px', border: '1px solid #ddd' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3>Graphique interactif</h3>
        <div>
          {['5d', '1mo', '3mo', '6mo', '1y', '5y'].map(p => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              style={{
                marginLeft: '5px',
                padding: '5px 10px',
                backgroundColor: period === p ? '#007bff' : '#f8f9fa',
                color: period === p ? 'white' : 'black',
                border: '1px solid #ddd',
                borderRadius: '3px',
                cursor: 'pointer'
              }}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <p>Chargement du graphique...</p>
      ) : (
        <div style={{ marginTop: '15px' }}>
          <Chart options={options} series={series} type="candlestick" height={350} />
        </div>
      )}
    </div>
  );
}

export default AssetChart;
