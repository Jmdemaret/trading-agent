import React, { useState } from 'react';
import Portfolio from './components/Portfolio';
import TradingSignals from './components/TradingSignals';
import AIRebalancing from './components/AIRebalancing';
import Settings from './components/Settings';
import FinancialModule from './components/FinancialModule';
import AssetDetails from './components/AssetDetails';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('portfolio');
  const [selectedAsset, setSelectedAsset] = useState(null);

  // Écouter l'événement pour basculer sur la vue détaillée d'un actif
  React.useEffect(() => {
    const handleViewAsset = (e) => {
      setSelectedAsset(e.detail);
      setActiveTab('asset_details');
    };
    window.addEventListener('viewAsset', handleViewAsset);
    return () => window.removeEventListener('viewAsset', handleViewAsset);
  }, []);

  return (
    <div className="App" style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>📈 Dashboard d'Investissement Expert IA</h1>
      <p>Suivez votre portefeuille et obtenez des recommandations en temps réel.</p>

      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <button
          onClick={() => setActiveTab('portfolio')}
          style={{ fontWeight: activeTab === 'portfolio' ? 'bold' : 'normal', padding: '8px 12px' }}
        >
          📊 Vue d'ensemble (Temps Réel)
        </button>
        <button
          onClick={() => setActiveTab('signals')}
          style={{ fontWeight: activeTab === 'signals' ? 'bold' : 'normal', padding: '8px 12px' }}
        >
          🧠 Analyse Expert & Signaux
        </button>
        <button
          onClick={() => setActiveTab('rebalance')}
          style={{ fontWeight: activeTab === 'rebalance' ? 'bold' : 'normal', padding: '8px 12px' }}
        >
          ✨ Feature Révolutionnaire : Auto-Rééquilibrage IA
        </button>
        <button
          onClick={() => setActiveTab('financials')}
          style={{ fontWeight: activeTab === 'financials' ? 'bold' : 'normal', padding: '8px 12px' }}
        >
          🏦 Historique Financier
        </button>
        <button
          onClick={() => setActiveTab('settings')}
          style={{ fontWeight: activeTab === 'settings' ? 'bold' : 'normal', padding: '8px 12px' }}
        >
          ⚙️ Paramètres Telegram
        </button>
      </div>

      <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '5px', backgroundColor: '#fff' }}>
        {activeTab === 'portfolio' && <Portfolio />}
        {activeTab === 'signals' && <TradingSignals />}
        {activeTab === 'rebalance' && <AIRebalancing />}
        {activeTab === 'financials' && <FinancialModule />}
        {activeTab === 'settings' && <Settings />}
        {activeTab === 'asset_details' && selectedAsset && (
          <AssetDetails ticker={selectedAsset} onBack={() => setActiveTab('portfolio')} />
        )}
      </div>
    </div>
  );
}

export default App;
