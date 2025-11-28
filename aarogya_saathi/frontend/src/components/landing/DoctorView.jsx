import React from 'react';
import { motion } from 'framer-motion';
import './DoctorView.css';

const DoctorView = () => {
    return (
        <section className="doctor-view-section">
            <div className="container doctor-view-container">
                <motion.div
                    className="doctor-view-image"
                    initial={{ x: -100, opacity: 0 }}
                    whileInView={{ x: 0, opacity: 1 }}
                    transition={{ duration: 0.8 }}
                    viewport={{ once: true }}
                >
                    <div className="mock-browser-window">
                        <div className="browser-header">
                            <span className="dot red"></span>
                            <span className="dot yellow"></span>
                            <span className="dot green"></span>
                        </div>
                        <div className="browser-content">
                            <div className="live-log-header">
                                <span className="live-indicator"></span> Live Patient Log
                            </div>
                            <div className="log-entries">
                                <div className="log-entry">{'> Patient (45s): Initiated call...'}</div>
                                <div className="log-entry">{'> Aarogya Triage: Keyword "Dizzy" detected.'}</div>
                                <div className="log-entry">{'> Sentinel: Acoustic biomarkers normal.'}</div>
                                <div className="log-entry">{'> Risk Score: 4.5 (Moderate)'}</div>
                            </div>
                        </div>
                    </div>
                </motion.div>
                <div className="doctor-view-content">
                    <h2 className="section-title">The Doctor's View</h2>
                    <p className="doctor-view-desc">
                        Aarogya provides real-time insights and risk scoring, allowing healthcare professionals to intervene precisely when needed. All from a simple, secure web portal.
                    </p>
                    <div className="feature-highlight">
                        <h4 className="highlight-title">Key Feature: Login-by-Phone</h4>
                        <p className="highlight-desc">
                            No passwords to forget. Secure, OTP-based access for any doctor, anywhere.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default DoctorView;
