import React from 'react';
import { Zap, Brain, Activity, ShieldAlert } from 'lucide-react';
import Card from '../ui/Card';
import './SwarmSection.css';

const SwarmSection = () => {
    const agents = [
        {
            icon: <Zap size={24} color="#D97706" />,
            title: "The Triage Agent (The Reflex)",
            description: "Instant reaction to critical keywords like 'Pain' or 'Dizzy'. <200ms latency."
        },
        {
            icon: <Brain size={24} color="#D97706" />,
            title: "The Nudge Agent (The Psychologist)",
            description: "Uses Reinforcement Learning (Contextual Bandits) to adapt its tone. It learns if Shanti listens better to 'Fear' or 'Love'."
        },
        {
            icon: <Activity size={24} color="#D97706" />,
            title: "The Sentinel (Slur Detection)",
            description: "Analyzes acoustic biomarkers. Detects slurred speech (Dysarthria) to predict strokes before words are even spoken."
        },
        {
            icon: <ShieldAlert size={24} color="#D97706" />,
            title: "The Safety Net (Escalation)",
            description: "If Shanti stops responding, Aarogya autonomously dials her neighbor via Twilio and alerts the clinic."
        }
    ];

    return (
        <section className="swarm-section">
            <div className="container">
                <div className="section-header">
                    <h2 className="section-title">Powered by an Autonomous Swarm</h2>
                </div>
                <div className="swarm-grid">
                    {agents.map((agent, index) => (
                        <Card key={index} className="swarm-card">
                            <div className="swarm-icon-wrapper">
                                {agent.icon}
                            </div>
                            <h3 className="swarm-card-title">{agent.title}</h3>
                            <p className="swarm-card-desc">{agent.description}</p>
                        </Card>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default SwarmSection;
