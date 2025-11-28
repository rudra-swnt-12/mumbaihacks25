import React from 'react';
import { motion } from 'framer-motion';
import './SolutionSection.css';

const SolutionSection = () => {
    const features = [
        {
            title: "Hybrid Scripting",
            description: "Combines structured clinical pathways with dynamic, empathetic conversational AI for natural, effective consultations.",
            color: "text-green-600"
        },
        {
            title: "Reflex Cache",
            description: "Pre-computes and caches common conversational branches for millisecond response times, even on low-bandwidth networks.",
            color: "text-green-600"
        },
        {
            title: "Acoustic Biomarkers",
            description: "Analyzes vocal patterns for signs of respiratory distress, fatigue, or emotional state, adding a critical layer of diagnostic data.",
            color: "text-green-600"
        },
        {
            title: "Behavioral Nudges",
            description: "Continuously adapts to patient responses, allowing for personalized health conversations and resolving ambiguity.",
            color: "text-green-600"
        }
    ];

    // Duplicate features for seamless loop
    const duplicatedFeatures = [...features, ...features, ...features];

    return (
        <section className="solution-section" id="features">
            <div className="container-fluid"> {/* Use fluid container for full width scroll */}
                <div className="section-header">
                    <h2 className="section-title">Meet Aarogya. The AI That Listens.</h2>
                </div>

                <div className="features-scroll-wrapper">
                    <motion.div
                        className="features-track"
                        animate={{ x: "-33.33%" }} // Move by one set of items
                        transition={{
                            duration: 20, // Adjust speed as needed
                            repeat: Infinity,
                            ease: "linear",
                        }}
                    >
                        {duplicatedFeatures.map((feature, index) => (
                            <div key={index} className="feature-card">
                                <h3 className={`feature-card-title ${feature.color}`}>{feature.title}</h3>
                                <p className="feature-card-desc">{feature.description}</p>
                            </div>
                        ))}
                    </motion.div>
                </div>
            </div>
        </section>
    );
};

export default SolutionSection;
