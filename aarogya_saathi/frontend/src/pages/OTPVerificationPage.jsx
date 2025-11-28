import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Phone } from 'lucide-react';
import './OTPVerificationPage.css';

const OTPVerificationPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const phoneNumber = location.state?.phoneNumber || '';
    
    const [otp, setOtp] = useState(['', '', '', '', '', '']);
    const [timer, setTimer] = useState(30);
    const [canResend, setCanResend] = useState(false);
    const [isVerifying, setIsVerifying] = useState(false);
    const inputRefs = useRef([]);

    // Timer countdown
    useEffect(() => {
        if (timer > 0) {
            const interval = setInterval(() => {
                setTimer((prev) => prev - 1);
            }, 1000);
            return () => clearInterval(interval);
        } else {
            setCanResend(true);
        }
    }, [timer]);

    // Handle OTP input change
    const handleChange = (index, value) => {
        // Only allow numbers
        if (value && !/^\d$/.test(value)) return;

        const newOtp = [...otp];
        newOtp[index] = value;
        setOtp(newOtp);

        // Auto-focus next input
        if (value && index < 5) {
            inputRefs.current[index + 1]?.focus();
        }
    };

    // Handle backspace
    const handleKeyDown = (index, e) => {
        if (e.key === 'Backspace' && !otp[index] && index > 0) {
            inputRefs.current[index - 1]?.focus();
        }
    };

    // Handle paste
    const handlePaste = (e) => {
        e.preventDefault();
        const pastedData = e.clipboardData.getData('text').slice(0, 6);
        if (!/^\d+$/.test(pastedData)) return;

        const newOtp = [...otp];
        pastedData.split('').forEach((char, index) => {
            if (index < 6) {
                newOtp[index] = char;
            }
        });
        setOtp(newOtp);

        // Focus last filled input or next empty
        const nextIndex = Math.min(pastedData.length, 5);
        inputRefs.current[nextIndex]?.focus();
    };

    // Verify OTP
    const handleVerifyOTP = async () => {
        const otpValue = otp.join('');
        if (otpValue.length !== 6) return;

        setIsVerifying(true);
        
        // Simulate API call
        setTimeout(() => {
            setIsVerifying(false);
            // Navigate to patient dashboard on success
            navigate('/dashboard');
        }, 1500);
    };

    // Resend OTP
    const handleResendOTP = () => {
        setOtp(['', '', '', '', '', '']);
        setTimer(30);
        setCanResend(false);
        inputRefs.current[0]?.focus();
        
        // Simulate API call to resend OTP
        console.log('Resending OTP to:', phoneNumber);
    };

    // Auto-submit when all 6 digits are entered
    useEffect(() => {
        if (otp.every(digit => digit !== '')) {
            handleVerifyOTP();
        }
    }, [otp]);

    return (
        <div className="otp-container">
            <div className="otp-card">
                {/* Left Branding Section */}
                <div className="otp-branding">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <h1>Aarogya Saathi</h1>
                        <p>Healthcare for the Next Billion</p>
                    </motion.div>
                </div>

                {/* Right OTP Section */}
                <div className="otp-form-section">
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                    >
                        {/* Back Button */}
                        <button 
                            className="back-button"
                            onClick={() => navigate('/login')}
                        >
                            <ArrowLeft size={20} />
                            <span>Back to Login</span>
                        </button>

                        <h2>Verify OTP</h2>
                        <p className="otp-subtitle">
                            We've sent a 6-digit code to
                            <span className="phone-display">
                                <Phone size={14} />
                                {phoneNumber || '+91 XXXXXXXXXX'}
                            </span>
                        </p>

                        {/* OTP Input Boxes */}
                        <div className="otp-inputs">
                            {otp.map((digit, index) => (
                                <input
                                    key={index}
                                    ref={(el) => (inputRefs.current[index] = el)}
                                    type="text"
                                    inputMode="numeric"
                                    maxLength={1}
                                    value={digit}
                                    onChange={(e) => handleChange(index, e.target.value)}
                                    onKeyDown={(e) => handleKeyDown(index, e)}
                                    onPaste={handlePaste}
                                    className={`otp-input ${digit ? 'filled' : ''}`}
                                    autoFocus={index === 0}
                                />
                            ))}
                        </div>

                        {/* Timer and Resend */}
                        <div className="otp-footer">
                            {!canResend ? (
                                <p className="timer-text">
                                    Resend OTP in <span className="timer">{timer}s</span>
                                </p>
                            ) : (
                                <button 
                                    className="resend-button"
                                    onClick={handleResendOTP}
                                >
                                    Resend OTP
                                </button>
                            )}
                        </div>

                        {/* Verify Button */}
                        <button
                            className={`verify-button ${otp.every(d => d !== '') ? 'active' : ''}`}
                            onClick={handleVerifyOTP}
                            disabled={otp.some(d => d === '') || isVerifying}
                        >
                            {isVerifying ? (
                                <span className="loading-spinner"></span>
                            ) : (
                                'Verify & Continue'
                            )}
                        </button>

                        <div className="otp-help">
                            Didn't receive the code?{' '}
                            <a href="#" onClick={(e) => {
                                e.preventDefault();
                                if (canResend) handleResendOTP();
                            }}>
                                Contact Support
                            </a>
                        </div>
                    </motion.div>
                </div>
            </div>
        </div>
    );
};

export default OTPVerificationPage;
