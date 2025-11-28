import React, { useState } from 'react';
import { PhoneCall, CheckCircle, AlertCircle, ShieldCheck, Globe, Lock } from 'lucide-react';
import './GetCallPage.css';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

const GetCallPage = () => {
  const [phone, setPhone] = useState('');
  const [status, setStatus] = useState(null); // null | 'loading' | 'success' | 'error'
  const [message, setMessage] = useState('');
  const [countryCode, setCountryCode] = useState('+91');

  const onSubmit = async (e) => {
    e.preventDefault();
    const fullNumber = `${countryCode}${phone}`.replace(/\s+/g, '');
    if (!phone || phone.replace(/\D/g, '').length < 10) {
      setStatus('error');
      setMessage('Please enter a valid phone number');
      return;
    }
    try {
      setStatus('loading');
      setMessage('');
      const res = await fetch(`${API_BASE}/call/trigger`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: fullNumber }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.message || 'Failed to trigger call');
      setStatus('success');
      setMessage(data.mode === 'simulated' ? 'Simulation: Call would be placed.' : 'Call initiated! Please keep your phone nearby.')
    } catch (err) {
      setStatus('error');
      setMessage(err.message || 'An error occurred triggering the call');
    }
  };

  return (
    <div className="getcall-page">
      <div className="layout">
        <div className="left">
          <div className="page-title">
            <PhoneCall size={22} />
            <h1>Request a Call</h1>
          </div>
          <p className="page-subtitle">Enter your number to connect with Aarogya Saathi via a secure voice stream. No app required.</p>

          <div className="card">
            <form onSubmit={onSubmit} className="form">
              <label htmlFor="phone">Phone Number</label>
              <div className="input-row">
                <select className="code-select" value={countryCode} onChange={(e) => setCountryCode(e.target.value)}>
                  <option value="+91">+91 (IN)</option>
                  <option value="+1">+1 (US)</option>
                  <option value="+44">+44 (UK)</option>
                </select>
                <input
                  id="phone"
                  type="tel"
                  placeholder="XXXXXXXXXX"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  autoComplete="tel"
                />
                <button type="submit" className="submit-btn" disabled={status === 'loading'}>
                  {status === 'loading' ? 'Calling…' : 'Request Call'}
                </button>
              </div>
              <p className="helper">We’ll call you shortly. Standard voice rates may apply.</p>
            </form>

            {status === 'success' && (
              <div className="status success">
                <CheckCircle size={18} />
                <span>{message}</span>
              </div>
            )}
            {status === 'error' && (
              <div className="status error">
                <AlertCircle size={18} />
                <span>{message}</span>
              </div>
            )}
          </div>

          <div className="trust">
            <div className="trust-item"><ShieldCheck size={18} /> HIPAA-like privacy</div>
            <div className="trust-item"><Lock size={18} /> Secure voice stream</div>
            <div className="trust-item"><Globe size={18} /> Works over phone network</div>
          </div>
        </div>

        <div className="right">
          <div className="illustration" aria-hidden="true">
            <div className="circle big" />
            <div className="circle mid" />
            <div className="circle small" />
          </div>
          <div className="info">
            <h3>How it works</h3>
            <ol>
              <li>Enter your phone number and request a call.</li>
              <li>We’ll connect you to our AI assistant over a secure stream.</li>
              <li>Speak naturally—no app or internet needed.</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GetCallPage;
