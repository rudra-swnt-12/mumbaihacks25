import React from 'react';
import Button from '../ui/Button';
import './Hero.css';

const Hero = () => {
    return (
        <section className="hero">
            <div className="container hero-container">
                <div className="hero-content">
                    <h1 className="hero-title">
                        Healthcare for the Next Billion. <br />
                        <span className="serif-italic">No Apps. No Internet. Just Voice.</span>
                    </h1>
                    <p className="hero-subtitle">
                        The world's first Autonomous Agentic Swarm that turns a standard phone call into a medical lifeline. Bridging the digital divide with Agentic AI.
                    </p>
                    <div className="hero-actions">
                        <Button variant="primary">Experience the Demo</Button>
                        <Button variant="secondary">View System Architecture</Button>
                    </div>
                </div>
                <div className="hero-image-container">
                    {/* Placeholder for the image from the design */}
                    <div className="hero-image-placeholder">
                        <img src="https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?ixlib=rb-4.0.3&auto=format&fit=crop&w=1287&q=80" alt="Elderly Indian woman using a phone" className="hero-img" />
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Hero;
