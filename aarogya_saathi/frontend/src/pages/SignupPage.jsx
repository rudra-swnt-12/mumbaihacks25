import React, { useState, useRef } from 'react';
import { User, Stethoscope, Mic, Info, Eye, EyeOff, Phone, Check } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './SignupPage.css';

const SignupPage = () => {
    const [step, setStep] = useState(1);
    const [userType, setUserType] = useState(''); // 'patient' or 'doctor'

    // Patient state
    const [phoneNumber, setPhoneNumber] = useState('');
    const [otp, setOtp] = useState(['', '', '', '']);
    const [fullName, setFullName] = useState('');
    const [age, setAge] = useState('');

    // Doctor state
    const [doctorId, setDoctorId] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [specialization, setSpecialization] = useState('');
    const [clinicName, setClinicName] = useState('');
    const [contactNumber, setContactNumber] = useState('');

    const otpRefs = [useRef(null), useRef(null), useRef(null), useRef(null)];

    // Handle user type selection
    const handleUserTypeSelect = (type) => {
        setUserType(type);
        setTimeout(() => setStep(2), 300);
    };

    // Handle OTP input
    const handleOtpChange = (index, value) => {
        if (value.length <= 1 && /^\d*$/.test(value)) {
            const newOtp = [...otp];
            newOtp[index] = value;
            setOtp(newOtp);

            if (value && index < 3) {
                otpRefs[index + 1].current?.focus();
            }
        }
    };

    const handleOtpKeyDown = (index, e) => {
        if (e.key === 'Backspace' && !otp[index] && index > 0) {
            otpRefs[index - 1].current?.focus();
        }
    };

    const isOtpComplete = otp.every(digit => digit !== '');

    // Render patient signup flow
    const renderPatientFlow = () => {
        if (step === 2) {
            return (
                <motion.div
                    key="patient-step2"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3 }}
                    className="signup-step"
                >
                    <div className="phone-otp-step">
                        <h2>Please enter your 10-digit mobile number to begin.</h2>
                        <div className="phone-input-group">
                            <div className="country-code">+91</div>
                            <div className="phone-input-wrapper">
                                <input
                                    type="tel"
                                    placeholder="98765 43210"
                                    value={phoneNumber}
                                    onChange={(e) => setPhoneNumber(e.target.value)}
                                    maxLength={10}
                                />
                                <Mic className="voice-input-icon" size={20} />
                            </div>
                        </div>
                        <button className="send-otp-button">Send OTP</button>

                        <div className="otp-section">
                            <p>Enter the 4-digit code sent to your mobile number.</p>
                            <div className="otp-inputs">
                                {otp.map((digit, index) => (
                                    <input
                                        key={index}
                                        ref={otpRefs[index]}
                                        type="text"
                                        className="otp-input"
                                        value={digit}
                                        onChange={(e) => handleOtpChange(index, e.target.value)}
                                        onKeyDown={(e) => handleOtpKeyDown(index, e)}
                                        maxLength={1}
                                    />
                                ))}
                            </div>
                            <button
                                className={`verify-button ${isOtpComplete ? 'active' : ''}`}
                                disabled={!isOtpComplete}
                                onClick={() => isOtpComplete && setStep(3)}
                            >
                                Verify & Login
                            </button>
                            <div className="resend-otp">
                                Didn't receive the code? <a>Resend OTP</a>
                            </div>
                        </div>
                    </div>
                </motion.div>
            );
        } else if (step === 3) {
            return (
                <motion.div
                    key="patient-step3"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3 }}
                    className="signup-step"
                >
                    <div className="profile-step">
                        <div className="profile-header">
                            <div className="profile-icon">
                                <User size={24} />
                            </div>
                            <h2>Create Your Profile</h2>
                        </div>
                        <form className="profile-form">
                            <div className="profile-form-group">
                                <label>Full Name</label>
                                <div className="profile-input-wrapper">
                                    <input
                                        type="text"
                                        placeholder="Enter your full name"
                                        value={fullName}
                                        onChange={(e) => setFullName(e.target.value)}
                                    />
                                    <Mic className="voice-input-icon" size={20} />
                                </div>
                            </div>
                            <div className="profile-form-group">
                                <label>Age (Optional)</label>
                                <div className="profile-input-wrapper">
                                    <input
                                        type="text"
                                        placeholder="Enter your age"
                                        value={age}
                                        onChange={(e) => setAge(e.target.value)}
                                    />
                                    <Mic className="voice-input-icon" size={20} />
                                </div>
                            </div>
                            <button
                                type="button"
                                className="complete-profile-button"
                                onClick={() => {
                                    console.log('Patient profile completed:', { userType, phoneNumber, fullName, age });
                                }}
                            >
                                Complete Profile
                            </button>
                        </form>
                    </div>
                </motion.div>
            );
        }
    };

    // Render doctor signup flow
    const renderDoctorFlow = () => {
        if (step === 2) {
            return (
                <motion.div
                    key="doctor-step2"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="doctor-account-creation"
                >
                    <div className="doctor-left-panel">
                        <div className="doctor-branding">
                            <h1>Aarogya Saathi</h1>
                            <p>Healthcare for the Next Billion</p>
                        </div>
                        <div className="doctor-tagline">
                            <h2>Empowering Doctors with Advanced Digital Tools.</h2>
                            <p>Join a network of forward-thinking medical professionals revolutionizing healthcare access in India.</p>
                        </div>
                    </div>
                    <div className="doctor-right-panel">
                        <div className="doctor-form-container">
                            <h2>Create Your Doctor's Account</h2>
                            <p>Create your professional account to get started.</p>
                            <form>
                                <div className="doctor-form-group">
                                    <label>Doctor's ID</label>
                                    <div className="doctor-input-wrapper">
                                        <input
                                            type="text"
                                            placeholder="Medical Council Registration Number or Email"
                                            value={doctorId}
                                            onChange={(e) => setDoctorId(e.target.value)}
                                        />
                                    </div>
                                </div>
                                <div className="doctor-form-group">
                                    <label>Password</label>
                                    <div className="doctor-input-wrapper">
                                        <input
                                            type={showPassword ? 'text' : 'password'}
                                            placeholder="Enter your password"
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                        />
                                        <button
                                            type="button"
                                            className="password-toggle-icon"
                                            onClick={() => setShowPassword(!showPassword)}
                                        >
                                            {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                                        </button>
                                    </div>
                                </div>
                                <button
                                    type="button"
                                    className="create-account-button"
                                    onClick={() => setStep(3)}
                                >
                                    Create Account
                                </button>
                                <div className="already-account">
                                    Already have an account? <a href="/login">Log In</a>
                                </div>
                            </form>
                        </div>
                    </div>
                </motion.div>
            );
        } else if (step === 3) {
            return (
                <motion.div
                    key="doctor-step3"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3 }}
                    className="signup-step"
                >
                    <div className="professional-profile-step">
                        <div className="progress-indicator">
                            <div className="progress-text">Step 2 of 4</div>
                            <div className="progress-bar-container">
                                <div className="progress-bar" style={{ width: '50%' }}></div>
                            </div>
                        </div>
                        <h2>Set Up Your Professional Profile</h2>
                        <p>This information will be visible to patients and helps them connect with you.</p>
                        <form>
                            <div className="form-group-select">
                                <label>Specialization</label>
                                <select
                                    value={specialization}
                                    onChange={(e) => setSpecialization(e.target.value)}
                                >
                                    <option value="">Select your specialization</option>
                                    <option value="general">General Physician</option>
                                    <option value="cardiology">Cardiology</option>
                                    <option value="dermatology">Dermatology</option>
                                    <option value="pediatrics">Pediatrics</option>
                                    <option value="orthopedics">Orthopedics</option>
                                </select>
                            </div>
                            <div className="doctor-form-group">
                                <label>Clinic Name</label>
                                <div className="doctor-input-wrapper">
                                    <input
                                        type="text"
                                        placeholder="Dr. Sharma's Wellness Clinic"
                                        value={clinicName}
                                        onChange={(e) => setClinicName(e.target.value)}
                                    />
                                </div>
                            </div>
                            <div className="doctor-form-group">
                                <label>Contact Number</label>
                                <div className="professional-input-wrapper">
                                    <Phone className="professional-input-icon" size={20} />
                                    <input
                                        type="tel"
                                        placeholder="+91 98765 43210"
                                        value={contactNumber}
                                        onChange={(e) => setContactNumber(e.target.value)}
                                    />
                                </div>
                            </div>
                            <button
                                type="button"
                                className="save-continue-button"
                                onClick={() => setStep(4)}
                            >
                                Save and Continue
                            </button>
                            <div className="skip-link">
                                <a onClick={() => setStep(4)}>Skip for now</a>
                            </div>
                        </form>
                    </div>
                </motion.div>
            );
        } else if (step === 4) {
            return (
                <div className="signup-container">
                    <motion.div
                        key="doctor-step4"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                        className="signup-step"
                    >
                        <div className="success-confirmation">
                            <div className="success-icon">
                                <Check size={40} />
                            </div>
                            <h2>Account Created Successfully!</h2>
                            <p>Welcome! You are now part of a growing network dedicated to accessible healthcare. Let's get started on your health journey.</p>
                            <button
                                type="button"
                                className="dashboard-button"
                                onClick={() => {
                                    console.log('Navigating to dashboard');
                                    window.location.href = '/doctor';
                                }}
                            >
                                Go to Your Dashboard
                            </button>
                        </div>
                    </motion.div>
                </div>
            );
        }
    };

    return (
        <>
            {step === 1 || (userType === 'patient' && step <= 3) ? (
                <div className="signup-container">
                    {step === 1 && (
                        <div className="signup-header">
                            <motion.h1
                                initial={{ opacity: 0, y: -20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5 }}
                            >
                                Aarogya Saathi
                            </motion.h1>
                            <motion.p
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ duration: 0.5, delay: 0.2 }}
                            >
                                Healthcare for the Next Billion
                            </motion.p>
                        </div>
                    )}

                    <AnimatePresence mode="wait">
                        {step === 1 && (
                            <motion.div
                                key="step1"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20 }}
                                transition={{ duration: 0.3 }}
                                className="signup-step"
                            >
                                <div className="user-type-selection">
                                    <h2>Sign up as a:</h2>
                                    <div className="user-type-cards">
                                        <div
                                            className="user-type-card"
                                            onClick={() => handleUserTypeSelect('patient')}
                                        >
                                            <div className="user-type-icon">
                                                <User size={32} />
                                            </div>
                                            <h3>I am a Patient</h3>
                                            <p>Access records & connect with doctors.</p>
                                        </div>
                                        <div
                                            className="user-type-card"
                                            onClick={() => handleUserTypeSelect('doctor')}
                                        >
                                            <div className="user-type-icon">
                                                <Stethoscope size={32} />
                                            </div>
                                            <h3>I am a Doctor</h3>
                                            <p>Manage your practice & consult patients.</p>
                                        </div>
                                    </div>
                                    <div className="login-link">
                                        Already have an account? <a href="/login">Log In</a>
                                    </div>
                                </div>
                            </motion.div>
                        )}

                        {userType === 'patient' && renderPatientFlow()}
                    </AnimatePresence>
                </div>
            ) : (
                <AnimatePresence mode="wait">
                    {userType === 'doctor' && renderDoctorFlow()}
                </AnimatePresence>
            )}
        </>
    );
};

export default SignupPage;
