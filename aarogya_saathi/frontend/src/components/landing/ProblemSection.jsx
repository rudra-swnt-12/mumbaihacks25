import React from 'react';
import { SignalHigh, Languages, UserX } from 'lucide-react';
import Card from '../ui/Card';
import './ProblemSection.css';

const ProblemSection = () => {
    const problems = [
        {
            icon: <SignalHigh size={32} color="#D97706" />,
            title: "The Digital Gap",
            description: "500 Million users in India have feature phones, not smartphones. They are invisible to modern HealthTech apps."
        },
        {
            icon: <Languages size={32} color="#D97706" />,
            title: "The Literacy Barrier",
            description: "Text-based chatbots fail when users cannot read. Medical adherence drops by 40% due to confusion."
        },
        {
            icon: <UserX size={32} color="#D97706" />,
            title: "The Caregiver Crisis",
            description: "Doctors are overworked. Families are distant. Who watches over the elderly in-between visits?"
        }
    ];

    return (
        <section className="problem-section">
            <div className="container">
                <div className="section-header">
                    <h2 className="section-title">The Digital Divide is a Human Divide</h2>
                    <p className="section-subtitle">Modern HealthTech is failing the very people who need it most. We're changing that.</p>
                </div>
                <div className="problem-grid">
                    {problems.map((problem, index) => (
                        <Card key={index} className="problem-card">
                            <div className="problem-icon-wrapper">
                                {problem.icon}
                            </div>
                            <h3 className="problem-card-title">{problem.title}</h3>
                            <p className="problem-card-desc">{problem.description}</p>
                        </Card>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default ProblemSection;
