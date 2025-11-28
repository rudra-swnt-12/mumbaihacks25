import React, { useState } from 'react';
import { Phone, Lock, Eye, EyeOff, Stethoscope } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './LoginPage.css';

const LoginPage = () => {
    const [userType, setUserType] = useState('patient'); // 'patient' or 'doctor'
    const [showPassword, setShowPassword] = useState(false);

    return (
        <div className="login-container">
            <div className="login-card">
                {/* Left Column (Branding Section) */}
                <div className="login-branding">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <h1>Aarogya Saathi</h1>
                        <p>Healthcare for the Next Billion</p>
                    </motion.div>
                </div>

                {/* Right Column (Form Section) */}
                <div className="login-form-section">
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                    >
                        <h2>Login to your Account</h2>

                        {/* Toggle Switch */}
                        <div className="login-toggle">
                            <button
                                className={userType === 'patient' ? 'active' : ''}
                                onClick={() => setUserType('patient')}
                            >
                                Patient
                            </button>
                            <button
                                className={userType === 'doctor' ? 'active' : ''}
                                onClick={() => setUserType('doctor')}
                            >
                                Doctor
                            </button>
                        </div>

                        {/* Forms with Animation */}
                        <div className="login-form-container">
                            <AnimatePresence mode="wait">
                                {userType === 'patient' ? (
                                    <motion.form
                                        key="patient"
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: 20 }}
                                        transition={{ duration: 0.3 }}
                                        className="login-form"
                                    >
                                        <div className="form-group">
                                            <label>Phone Number</label>
                                            <div className="input-wrapper">
                                                <Phone className="input-icon" size={20} />
                                                <input
                                                    type="tel"
                                                    className="form-input"
                                                    placeholder="Enter your phone number"
                                                />
                                            </div>
                                        </div>

                                        <button type="button" className="login-button">
                                            Get OTP
                                        </button>

                                        <div className="signup-link">
                                            Don't have an account?{' '}
                                            <a href="/signup">Sign up here</a>
                                        </div>
                                    </motion.form>
                                ) : (
                                    <motion.form
                                        key="doctor"
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: -20 }}
                                        transition={{ duration: 0.3 }}
                                        className="login-form"
                                    >
                                        <div className="form-group">
                                            <label>Doctor's ID</label>
                                            <div className="input-wrapper">
                                                <Stethoscope className="input-icon" size={20} />
                                                <input
                                                    type="text"
                                                    className="form-input"
                                                    placeholder="Enter your Doctor's ID"
                                                />
                                            </div>
                                        </div>

                                        <div className="form-group">
                                            <label>Password</label>
                                            <div className="input-wrapper password-wrapper">
                                                <Lock className="input-icon" size={20} />
                                                <input
                                                    type={showPassword ? 'text' : 'password'}
                                                    className="form-input"
                                                    placeholder="••••••••"
                                                />
                                                <button
                                                    type="button"
                                                    className="password-toggle"
                                                    onClick={() => setShowPassword(!showPassword)}
                                                >
                                                    {showPassword ? (
                                                        <EyeOff size={20} />
                                                    ) : (
                                                        <Eye size={20} />
                                                    )}
                                                </button>
                                            </div>
                                            <div className="forgot-password">
                                                <a href="#">Forgot Password?</a>
                                            </div>
                                        </div>

                                        <button type="button" className="login-button">
                                            Login
                                        </button>

                                        <div className="signup-link">
                                            Don't have an account?{' '}
                                            <a href="/signup">Sign up here</a>
                                        </div>
                                    </motion.form>
                                )}
                            </AnimatePresence>
                        </div>
                    </motion.div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;