import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import SingleAnalysis from './pages/SingleAnalysis';
import Comparison from './pages/Comparison';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analyze" element={<SingleAnalysis />} />
            <Route path="/compare" element={<Comparison />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
