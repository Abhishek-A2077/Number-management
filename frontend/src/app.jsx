// src/App.jsx


import React from 'react';
import { NumbersProvider } from './contexts/NumbersContext';
import Dashboard from './pages/Dashboard';  // Correct default import

import './assets/styles/theme.css';
import './assets/styles/global.css';

const App = () => {
  return (
    <NumbersProvider>
      <div className="app-container">
        <main>
          <Dashboard />
        </main>
      </div>
    </NumbersProvider>
  );
};

export default App;
