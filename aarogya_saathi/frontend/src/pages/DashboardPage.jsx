import React from 'react';
import { LayoutDashboard, BarChart3, Settings, HelpCircle, LogOut, Sun, Bell, Calendar, Clock, FileText, User } from 'lucide-react';
import './DashboardPage.css';

const DashboardPage = () => {
  return (
    <div className="patient-dashboard">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="patient-profile">
          <div>
            <p className="profile-name">Dr. Ananya Sharma</p>
            <p className="profile-specialty">Cardiologist</p>
          </div>
        </div>

        <nav className="sidebar-nav">
          <a href="#" className="nav-item active">
            <LayoutDashboard className="material-icon" size={20} />
            <span>Dashboard</span>
          </a>
          <a href="#" className="nav-item">
            <BarChart3 className="material-icon" size={20} />
            <span>Analytics</span>
          </a>
          <a href="#" className="nav-item">
            <Settings className="material-icon" size={20} />
            <span>Settings</span>
          </a>
        </nav>

        <div className="sidebar-footer">
          <a href="#" className="nav-item">
            <HelpCircle className="material-icon" size={20} />
            <span>Help</span>
          </a>
          <a href="#" className="nav-item">
            <LogOut className="material-icon" size={20} />
            <span>Logout</span>
          </a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header className="dashboard-header">
          <h1 className="dashboard-title">Arogya Command Center</h1>
          <div className="header-info">
            <div className="weather-info">
              <Sun className="weather-icon" size={18} />
              <span>Mumbai: 34°C</span>
            </div>
            <div className="notification-icon">
              <Bell size={20} />
              <span className="notification-badge">2</span>
            </div>
          </div>
        </header>

        {/* Content Grid */}
        <div className="content-grid">
          {/* Left Column */}
          <div className="left-column">
            {/* Patient Details Card */}
            <div className="patient-details-card">
              <div className="patient-header">
                <div className="patient-info">
                  <div>
                    <h2 className="patient-name">Shanti Devi</h2>
                    <p className="patient-meta">Female, 68 years</p>
                  </div>
                </div>
                <div className="patient-id-info">
                  <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>ID: <span className="id-code">AYB3-C992-E1F8</span></p>
                  <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8' }}>Kolhapur, Maharashtra</p>
                </div>
              </div>

              <div className="patient-stats">
                <div className="stat">
                  <p className="stat-label">Risk Score</p>
                  <p className="stat-value risk-score">7.2</p>
                </div>
                <div className="stat">
                  <p className="stat-label">Phone Number</p>
                  <p className="stat-value phone-number">+91 98765 43210</p>
                </div>
                <div className="stat">
                  <p className="stat-label">Last Contact</p>
                  <p className="stat-value">12m ago</p>
                </div>
              </div>
            </div>

            {/* Patient Report */}
            <div className="patient-details-card patient-report">
              <h3 className="section-title">Patient Report</h3>

              {/* Medical History */}
              <div className="report-section">
                <div className="report-header">
                  <FileText className="report-icon" size={18} />
                  <h4 className="report-subtitle">Medical History</h4>
                </div>
                <p className="report-content">
                  Type 2 Diabetes (2010), Hypertension (2015), Penicillin Allergy.
                </p>
              </div>

              {/* Medication Schedule */}
              <div className="report-section">
                <div className="report-header">
                  <Calendar className="report-icon" size={18} />
                  <h4 className="report-subtitle">Medication Schedule</h4>
                </div>
                <div className="medication-list">
                  <div className="medication-item">
                    <span className="med-name">Metformin 500mg</span>
                    <span className="med-schedule">Morning, Evening</span>
                  </div>
                  <div className="medication-item">
                    <span className="med-name">Lisinopril 10mg</span>
                    <span className="med-schedule">Morning</span>
                  </div>
                  <div className="medication-item">
                    <span className="med-name">Aspirin 81mg</span>
                    <span className="med-schedule">Morning</span>
                  </div>
                </div>
              </div>

              {/* Vital Signs */}
              <div className="report-section">
                <div className="report-header">
                  <Clock className="report-icon" size={18} />
                  <h4 className="report-subtitle">Vital Signs</h4>
                  <span className="time-label">(12m ago)</span>
                </div>
                <div className="vitals-grid">
                  <div className="vital-item">
                    <span className="vital-label">BP:</span>
                    <span className="vital-value">130/85</span>
                  </div>
                  <div className="vital-item">
                    <span className="vital-label">HR:</span>
                    <span className="vital-value">72 bpm</span>
                  </div>
                  <div className="vital-item">
                    <span className="vital-label">SpO2:</span>
                    <span className="vital-value">98%</span>
                  </div>
                  <div className="vital-item">
                    <span className="vital-label">Temp:</span>
                    <span className="vital-value">98.6°F</span>
                  </div>
                </div>
              </div>

              {/* Lab Results */}
              <div className="report-section">
                <div className="report-header">
                  <FileText className="report-icon" size={18} />
                  <h4 className="report-subtitle">Lab Results</h4>
                  <span className="time-label">(2 weeks ago)</span>
                </div>
                <div className="lab-list">
                  <div className="lab-item">
                    <span className="lab-test">HbA1c</span>
                    <span className="lab-value">7.1%</span>
                  </div>
                  <div className="lab-item">
                    <span className="lab-test">Creatinine</span>
                    <span className="lab-value">1.1 mg/dL</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div className="right-column">
            {/* Upcoming Appointments */}
            <div className="appointments-section">
              <h3 className="section-title">Upcoming Appointments</h3>
              <div className="appointments-list">
                <div className="appointment-card confirmed">
                  <div className="appointment-header">
                    <div className="appointment-info">
                      <h4 className="appointment-doctor">Dr. Ananya Sharma</h4>
                      <p className="appointment-specialty">Cardiologist</p>
                    </div>
                    <div className="appointment-status confirmed">✓</div>
                  </div>
                  <div className="appointment-details">
                    <div className="appointment-detail">
                      <Calendar className="detail-icon" size={16} />
                      <span className="detail-text">Dec 15, 2025</span>
                    </div>
                    <div className="appointment-detail">
                      <Clock className="detail-icon" size={16} />
                      <span className="detail-text">10:30 AM</span>
                    </div>
                    <div className="appointment-detail">
                      <FileText className="detail-icon" size={16} />
                      <span className="detail-text">Follow-up</span>
                    </div>
                  </div>
                </div>

                <div className="appointment-card scheduled">
                  <div className="appointment-header">
                    <div className="appointment-info">
                      <h4 className="appointment-doctor">Dr. Rajesh Kumar</h4>
                      <p className="appointment-specialty">Endocrinologist</p>
                    </div>
                    <div className="appointment-status scheduled">📅</div>
                  </div>
                  <div className="appointment-details">
                    <div className="appointment-detail">
                      <Calendar className="detail-icon" size={16} />
                      <span className="detail-text">Dec 20, 2025</span>
                    </div>
                    <div className="appointment-detail">
                      <Clock className="detail-icon" size={16} />
                      <span className="detail-text">2:00 PM</span>
                    </div>
                    <div className="appointment-detail">
                      <FileText className="detail-icon" size={16} />
                      <span className="detail-text">Consultation</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Secure Message */}
            <div className="secure-message">
              <h3 className="section-title">Secure Message</h3>
              <div className="message-box">
                <div className="message doctor">
                  <div className="message-content">
                    <p>Doctor sahib, I am feeling a little weak today. Should I take the new medicine?</p>
                    <span className="message-time">10:05 AM</span>
                  </div>
                </div>

                <div className="message patient">
                  <div className="message-content">
                    <p>Shanti ji, please take the new medicine after your evening meal. Rest well today.</p>
                    <span className="message-time">10:12 AM</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;
