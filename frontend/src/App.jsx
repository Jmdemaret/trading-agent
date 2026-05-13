import React, { useState } from 'react';
import Portfolio from './components/Portfolio';
import TradingSignals from './components/TradingSignals';
import AIRebalancing from './components/AIRebalancing';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('portfolio');

  return (
    <div className="App" style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>📈 Dashboard d'Investissement Expert IA</h1>
      <p>Suivez votre portefeuille et obtenez des recommandations en temps réel.</p>

      <div style={{ marginBottom: '20px' }}>
        <button
          onClick={() => setActiveTab('portfolio')}
          style={{ fontWeight: activeTab === 'portfolio' ? 'bold' : 'normal', marginRight: '10px' }}
        >
          Vue d'ensemble
        </button>
        <button
          onClick={() => setActiveTab('signals')}
          style={{ fontWeight: activeTab === 'signals' ? 'bold' : 'normal', marginRight: '10px' }}
        >
          Analyse Expert & Signaux
        </button>
        <button
          onClick={() => setActiveTab('rebalance')}
          style={{ fontWeight: activeTab === 'rebalance' ? 'bold' : 'normal' }}
        >
          Feature Révolutionnaire : Auto-Rééquilibrage IA
        </button>
      </div>

      <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '5px' }}>
        {activeTab === 'portfolio' && <Portfolio />}
        {activeTab === 'signals' && <TradingSignals />}
        {activeTab === 'rebalance' && <AIRebalancing />}
      </div>
    </div>
  );
}

export default App;
