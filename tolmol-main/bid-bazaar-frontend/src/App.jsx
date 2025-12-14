import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { AuctionProvider } from './contexts/AuctionContext';
import Layout from './components/layout/Layout';
import HomePage from './pages/HomePage';
import LoginForm from './components/auth/LoginForm';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <AuctionProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginForm />} />
              <Route path="/register" element={<div className="container mx-auto px-4 py-8"><h1>Register Page - Coming Soon</h1></div>} />
              <Route path="/dashboard" element={<div className="container mx-auto px-4 py-8"><h1>Dashboard - Coming Soon</h1></div>} />
              <Route path="/auction/:id" element={<div className="container mx-auto px-4 py-8"><h1>Auction Detail - Coming Soon</h1></div>} />
              <Route path="/create-auction" element={<div className="container mx-auto px-4 py-8"><h1>Create Auction - Coming Soon</h1></div>} />
              <Route path="/how-it-works" element={<div className="container mx-auto px-4 py-8"><h1>How It Works - Coming Soon</h1></div>} />
              <Route path="/categories" element={<div className="container mx-auto px-4 py-8"><h1>Categories - Coming Soon</h1></div>} />
              <Route path="*" element={<div className="container mx-auto px-4 py-8"><h1>404 - Page Not Found</h1></div>} />
            </Routes>
          </Layout>
        </Router>
      </AuctionProvider>
    </AuthProvider>
  );
}

export default App;

