import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Settings() {
  const [token, setToken] = useState('');
  const [chatId, setChatId] = useState('');
  const [status, setStatus] = useState('');

  useEffect(() => {
    axios.get('/api/settings')
      .then(response => {
        setToken(response.data.token || '');
        setChatId(response.data.chat_id || '');
      })
      .catch(err => console.error("Erreur chargement settings", err));
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setStatus('Sauvegarde en cours...');
    try {
      await axios.post('/api/settings', { token, chat_id: chatId });
      setStatus('Configuration sauvegardée avec succès !');
      setTimeout(() => setStatus(''), 3000);
    } catch (err) {
      console.error(err);
      setStatus('Erreur lors de la sauvegarde.');
    }
  };

  return (
    <div>
      <h2>⚙️ Configuration Telegram</h2>
      <p>Configurez ici votre bot Telegram pour recevoir les alertes d'opportunités d'achat/vente en temps réel.</p>

      <form onSubmit={handleSave} style={{ maxWidth: '500px', display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Bot Token:</label>
          <input
            type="text"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            placeholder="123456789:ABCdefGHIjklMNO..."
          />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Chat ID:</label>
          <input
            type="text"
            value={chatId}
            onChange={(e) => setChatId(e.target.value)}
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            placeholder="Votre identifiant de discussion (ex: 987654321)"
          />
        </div>
        <button type="submit" style={{ padding: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Sauvegarder
        </button>
      </form>

      {status && <p style={{ marginTop: '15px', color: status.includes('succès') ? 'green' : 'red' }}>{status}</p>}

      <div style={{ marginTop: '30px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px', fontSize: '0.9em' }}>
        <strong>Comment obtenir ces informations ?</strong>
        <ol>
          <li>Cherchez <code>@BotFather</code> sur Telegram et envoyez <code>/newbot</code> pour créer un bot et obtenir le <strong>Token</strong>.</li>
          <li>Cherchez <code>@userinfobot</code> sur Telegram et envoyez-lui un message pour obtenir votre <strong>Chat ID</strong>.</li>
          <li>Assurez-vous d'envoyer au moins un premier message à votre nouveau bot pour qu'il puisse vous contacter !</li>
        </ol>
      </div>
    </div>
  );
}

export default Settings;
