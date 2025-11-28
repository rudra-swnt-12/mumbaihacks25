import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Button from '../ui/Button';
import './Navbar.css';

const Navbar = () => {
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            if (window.scrollY > 50) {
                setScrolled(true);
            } else {
                setScrolled(false);
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
            <div className="container navbar-container">
                <Link to="/" className="navbar-logo">
                    Aarogya
                </Link>
                <div className="navbar-links">
                    <a href="#features">Features</a>
                    <a href="#how-it-works">How it Works</a>
                    <a href="#demo">Demo</a>
                    <Link to="/login">
                        <Button variant="secondary" className="navbar-btn">Login</Button>
                    </Link>
                    <Link to="/dashboard">
                        <Button variant="primary" className="navbar-btn">Launch Dashboard</Button>
                    </Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;