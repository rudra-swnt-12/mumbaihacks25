import React from 'react';
import {
    LayoutDashboard, Users, BarChart3, Settings, HelpCircle, LogOut,
    Sun, User, FileText, Calendar, Phone, Ambulance, MessageSquare,
    AlertTriangle, Activity
} from 'lucide-react';
import './DoctorDashboardPage.css';

const DoctorDashboardPage = () => {
    return (
        <div className="doctor-dashboard">
            {/* Sidebar */}
            <aside className="sidebar">
                <div className="doctor-profile">
                    <div className="doctor-avatar-placeholder">
                        AS
                    </div>
                    <div>
                        <p className="profile-name">Dr. Ananya Sharma</p>
                        <p className="profile-specialty">Cardiologist</p>
                    </div>
                </div>

                <nav className="sidebar-nav">
                    <a href="#" className="nav-item active">
                        <LayoutDashboard size={20} />
                        <span>Dashboard</span>
                    </a>
                    <a href="#" className="nav-item">
                        <Users size={20} />
                        <span>Patients</span>
                    </a>
                    <a href="#" className="nav-item">
                        <BarChart3 size={20} />
                        <span>Analytics</span>
                    </a>
                    <a href="#" className="nav-item">
                        <Settings size={20} />
                        <span>Settings</span>
                    </a>
                </nav>

                <div className="sidebar-footer">
                    <a href="#" className="nav-item">
                        <HelpCircle size={20} />
                        <span>Help</span>
                    </a>
                    <a href="#" className="nav-item">
                        <LogOut size={20} />
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
                        <div className="patient-count">
                            Monitoring <strong>1,240 Patients</strong>
                        </div>
                        <div className="user-profile-icon">
                            <User size={20} />
                        </div>
                    </div>
                </header>

                {/* Content Grid */}
                <div className="content-grid">
                    {/* Left Column */}
                    <div className="left-column">
                        {/* Patient Card */}
                        <div className="patient-card">
                            <div className="patient-card-header">
                                <div className="patient-identity">
                                    <div className="patient-avatar-placeholder">
                                        SD
                                        <div className="status-badge">✓</div>
                                    </div>
                                    <div>
                                        <h2 className="patient-name">Shanti Devi</h2>
                                        <p className="patient-demographics">Female, 68 years</p>
                                    </div>
                                </div>
                                <div className="patient-meta-info">
                                    <p>ID: <span className="patient-id">A7B3-C902-E1F8</span></p>
                                    <p>Kolhapur, Maharashtra</p>
                                </div>
                            </div>

                            <div className="patient-stats-row">
                                <div className="stat-box">
                                    <h4>Risk Score</h4>
                                    <span className="stat-value risk-high">7.2</span>
                                </div>
                                <div className="stat-box">
                                    <h4>Onboarding</h4>
                                    <span className="stat-value">Auto-filling...</span>
                                </div>
                                <div className="stat-box">
                                    <h4>Last Contact</h4>
                                    <span className="stat-value">12m ago</span>
                                </div>
                            </div>
                        </div>

                        {/* Consultation Timeline */}
                        <div className="timeline-section">
                            <h3 className="section-title">Consultation Timeline</h3>

                            <div className="timeline-item">
                                <div className="timeline-icon soap">
                                    <FileText size={20} />
                                </div>
                                <div className="timeline-content">
                                    <h4>SOAP Note: Follow-up on medication</h4>
                                    <p>AI call initiated. Patient confirmed taking Metformin. No new symptoms reported. Vital signs estimated stable.</p>
                                    <span className="timeline-time">Today, 09:30 AM</span>
                                </div>
                            </div>

                            <div className="timeline-item">
                                <div className="timeline-icon checkin">
                                    <Calendar size={20} />
                                </div>
                                <div className="timeline-content">
                                    <h4>Weekly Check-in</h4>
                                    <p>Patient reported feeling well. Discussed importance of diet. No changes to medication.</p>
                                    <span className="timeline-time">3 days ago</span>
                                </div>
                            </div>

                            <div className="timeline-item">
                                <div className="timeline-icon call">
                                    <Phone size={20} />
                                </div>
                                <div className="timeline-content">
                                    <h4>Initial Onboarding Call</h4>
                                    <p>Completed initial health assessment. Patient's daughter was present to assist with setup.</p>
                                    <span className="timeline-time">1 week ago</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column */}
                    <div className="right-column">
                        {/* Priority List */}
                        <div className="priority-section">
                            <h3 className="section-title">Priority List</h3>
                            <div className="priority-list">
                                <div className="priority-card critical">
                                    <div className="priority-info">
                                        <div className="status-dot"></div>
                                        <div>
                                            <span className="priority-name">Ramesh K.</span>
                                            <span className="priority-condition">Chest Pain Reported</span>
                                        </div>
                                    </div>
                                    <div className="priority-score">
                                        <span className="score-value">9.8</span>
                                        <span className="score-time">2m ago</span>
                                    </div>
                                </div>

                                <div className="priority-card high">
                                    <div className="priority-info">
                                        <div className="status-dot"></div>
                                        <div>
                                            <span className="priority-name">Sunita P.</span>
                                            <span className="priority-condition">Vitals Unstable</span>
                                        </div>
                                    </div>
                                    <div className="priority-score">
                                        <span className="score-value">8.5</span>
                                        <span className="score-time">5m ago</span>
                                    </div>
                                </div>

                                <div className="priority-card moderate">
                                    <div className="priority-info">
                                        <div className="status-dot"></div>
                                        <div>
                                            <span className="priority-name">Anil G.</span>
                                            <span className="priority-condition">Medication Missed</span>
                                        </div>
                                    </div>
                                    <div className="priority-score">
                                        <span className="score-value">6.1</span>
                                        <span className="score-time">1h ago</span>
                                    </div>
                                </div>

                                <div className="priority-card low">
                                    <div className="priority-info">
                                        <div className="status-dot"></div>
                                        <div>
                                            <span className="priority-name">Priya S.</span>
                                            <span className="priority-condition">Follow-up Due</span>
                                        </div>
                                    </div>
                                    <div className="priority-score">
                                        <span className="score-value">5.5</span>
                                        <span className="score-time">3h ago</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Intervention Suite */}
                        <div className="intervention-section">
                            <h3 className="section-title">Intervention Suite</h3>
                            <div className="intervention-buttons">
                                <button className="action-btn btn-ambulance">
                                    <Ambulance size={18} />
                                    Dispatch Ambulance
                                </button>
                                <button className="action-btn btn-neighbor">
                                    <Phone size={18} />
                                    Call Neighbor (Ramu)
                                </button>
                                <button className="action-btn btn-sms">
                                    <MessageSquare size={18} />
                                    Send SMS Report
                                </button>
                            </div>
                        </div>

                        {/* Live Transcript */}
                        <div className="transcript-section">
                            <h3 className="section-title">Live Transcript</h3>
                            <div className="transcript-box">
                                <div className="chat-message ai-message">
                                    <p>Shanti ji, did you remember to take your morning sugar medicine?</p>
                                </div>
                                <div className="chat-message patient-message">
                                    <p>Oh... I am not sure, beta. I forgot.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default DoctorDashboardPage;
