import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import DashboardPage from './pages/DashboardPage';
import DoctorDashboardPage from './pages/DoctorDashboardPage';
import DoctorPortal from './pages/DoctorPortal';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import OTPVerificationPage from './pages/OTPVerificationPage';
import SystemArchitecture from './pages/SystemArchitecture';
import GetCallPage from './pages/GetCallPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />

        {/* --- NEW ROUTE --- */}
        <Route path="/doctor-dashboard" element={<DoctorDashboardPage />} />
        <Route path="/doctor" element={<DoctorPortal />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/otp-verify" element={<OTPVerificationPage />} />
        <Route path="/architecture" element={<SystemArchitecture />} />
  <Route path="/call" element={<GetCallPage />} />

      </Routes>
    </Router>
  );
}

export default App;
