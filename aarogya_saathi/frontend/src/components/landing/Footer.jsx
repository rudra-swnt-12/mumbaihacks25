import React from 'react';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="container footer-container">
                <div className="footer-links">
                    <a href="https://github.com" target="_blank" rel="noopener noreferrer">Github Repo</a>
                    <a href="#team">Team</a>
                    <a href="#whitepaper">Whitepaper</a>
                </div>
                <div className="footer-quote">
                    "Technology is best when it brings people together." - Matt Mullenweg
                </div>
            </div>
        </footer>
    );
};

export default Footer;
