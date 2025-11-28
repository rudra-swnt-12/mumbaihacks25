import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { 
    Phone, Database, Shield, Brain, Activity, 
    Smartphone, X, AlertTriangle, Grid, Fingerprint
} from 'lucide-react';
import { Link } from 'react-router-dom';
import './SystemArchitecture.css';

const SystemArchitecture = () => {
    const svgRef = useRef(null);
    const containerRef = useRef(null);
    const architecture = {
        input: {
            title: "The Physical Bridge",
            subtitle: "(Input)",
            color: "#10b981",
            items: [
                { id: "patient-device", icon: Phone, title: "Patient's Device", desc: "Voice/Text Input via App" },
                { id: "community-kiosk", icon: Smartphone, title: "Community Health Kiosk", desc: "Assisted Data Entry" }
            ]
        },
        processing: {
            title: "Real-Time AI Core",
            subtitle: "(Processing)",
            color: "#3b82f6",
            items: [
                { id: "llm-router", icon: Grid, title: "LLM Router", desc: "Routes queries to agents" },
                { id: "risk-detector", icon: Shield, title: "Risk Detector", desc: "Assesses urgency & raises alerts" },
                { id: "knowledge-agent", icon: Brain, title: "Medical Knowledge Agent", desc: "Provides medical insights" }
            ]
        },
        output: {
            title: "Persistence & Action",
            subtitle: "(Output)",
            color: "#8b5cf6",
            items: [
                { id: "ehr-db", icon: Database, title: "EHR Database", desc: "Secure Patient Records" },
                { id: "vector-db", icon: Fingerprint, title: "Vector DB", desc: "Semantic Search & Context" },
                { id: "doctor-dashboard", icon: Activity, title: "Doctor's Dashboard", desc: "Patient Insights & UI" },
                { id: "l2-escalation", icon: AlertTriangle, title: "L2 Escalation", desc: "Notifies on critical events", highlight: true }
            ]
        }
    };

    // Define arrow connections
    const arrows = [
        // From Input to Processing
        { from: "patient-device", to: "llm-router", color: "#10b981" },
        { from: "community-kiosk", to: "llm-router", color: "#10b981" },
        
        // Within Processing
        { from: "llm-router", to: "risk-detector", color: "#3b82f6" },
        { from: "llm-router", to: "knowledge-agent", color: "#3b82f6" },
        
        // From Processing to Output
        { from: "risk-detector", to: "ehr-db", color: "#8b5cf6" },
        { from: "knowledge-agent", to: "ehr-db", color: "#8b5cf6" },
        { from: "knowledge-agent", to: "vector-db", color: "#8b5cf6" },
        { from: "risk-detector", to: "doctor-dashboard", color: "#8b5cf6" },
        
        // Critical path
        { from: "risk-detector", to: "l2-escalation", color: "#ef4444", dashed: true }
    ];

    useEffect(() => {
        const updateArrows = () => {
            if (!containerRef.current) return;
            
            const containerRect = containerRef.current.getBoundingClientRect();
            
            // Pre-compute grouping to spread arrows that share the same endpoints
            const fromGroups = new Map();
            const toGroups = new Map();
            arrows.forEach((a) => {
                if (!fromGroups.has(a.from)) fromGroups.set(a.from, []);
                if (!toGroups.has(a.to)) toGroups.set(a.to, []);
                fromGroups.get(a.from).push(a);
                toGroups.get(a.to).push(a);
            });
            
            arrows.forEach((arrow, idx) => {
                const fromEl = document.getElementById(arrow.from);
                const toEl = document.getElementById(arrow.to);
                const pathEl = document.getElementById(`arrow-${idx}`);

                if (fromEl && toEl && pathEl) {
                    const fromRect = fromEl.getBoundingClientRect();
                    const toRect = toEl.getBoundingClientRect();

                    // Calculate positions relative to container
                    let startX = fromRect.right - containerRect.left + 6; // small nudge away from the card edge
                    let startY = fromRect.top + fromRect.height / 2 - containerRect.top;
                    let endX = toRect.left - containerRect.left - 6; // small nudge before the target edge
                    let endY = toRect.top + toRect.height / 2 - containerRect.top;

                    // Spread arrows that share same from/to to reduce overlap
                    const spread = 12; // pixels per step
                    const siblingsFrom = fromGroups.get(arrow.from) || [];
                    const siblingsTo = toGroups.get(arrow.to) || [];
                    const fromIndex = siblingsFrom.findIndex(a => a === arrow);
                    const toIndex = siblingsTo.findIndex(a => a === arrow);
                    const fromCenter = (siblingsFrom.length - 1) / 2;
                    const toCenter = (siblingsTo.length - 1) / 2;

                    // Apply vertical staggering near start and end
                    startY += (fromIndex - fromCenter) * spread;
                    endY += (toIndex - toCenter) * spread;

                    // Create smooth curved path
                    const dx = Math.abs(endX - startX);
                    const controlPointOffset = Math.max(40, dx * 0.5);

                    // Also offset control points slightly on Y to keep curves separated
                    const controlYOffset = (fromIndex - fromCenter + toIndex - toCenter) * (spread * 0.6);
                    const c1x = startX + controlPointOffset;
                    const c1y = startY + controlYOffset;
                    const c2x = endX - controlPointOffset;
                    const c2y = endY + controlYOffset;
                    const path = `M ${startX} ${startY} C ${c1x} ${c1y}, ${c2x} ${c2y}, ${endX} ${endY}`;
                    
                    pathEl.setAttribute('d', path);
                }
            });
        };

        // Update arrows after render
        const timer = setTimeout(updateArrows, 500);
        window.addEventListener('resize', updateArrows);
        
        return () => {
            clearTimeout(timer);
            window.removeEventListener('resize', updateArrows);
        };
    }, []);

    return (
        <div className="system-architecture-page">
            {/* Header */}
            <header className="arch-header">
                <Link to="/" className="back-button">
                    <X size={18} />
                </Link>
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="arch-header-content"
                >
                    <h1>Aarogya Saathi: System Architecture Diagram</h1>
                </motion.div>
            </header>

            {/* Three Column Architecture */}
            <section className="architecture-section">
                <div className="arch-container" ref={containerRef}>
                    {/* SVG for Arrows */}
                    <svg className="connection-svg" ref={svgRef} xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                                <polygon points="0 0, 10 3, 0 6" fill="#666" />
                            </marker>
                            <marker id="arrowhead-red" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                                <polygon points="0 0, 10 3, 0 6" fill="#ef4444" />
                            </marker>
                            <marker id="arrowhead-green" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                                <polygon points="0 0, 10 3, 0 6" fill="#10b981" />
                            </marker>
                            <marker id="arrowhead-blue" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                                <polygon points="0 0, 10 3, 0 6" fill="#3b82f6" />
                            </marker>
                            <marker id="arrowhead-purple" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                                <polygon points="0 0, 10 3, 0 6" fill="#8b5cf6" />
                            </marker>
                        </defs>
                        {arrows.map((arrow, idx) => {
                            const markerColor = arrow.dashed ? 'red' : 
                                               arrow.color === '#10b981' ? 'green' :
                                               arrow.color === '#3b82f6' ? 'blue' :
                                               arrow.color === '#8b5cf6' ? 'purple' : '';
                            return (
                                <path
                                    key={idx}
                                    id={`arrow-${idx}`}
                                    className={arrow.dashed ? "arrow-path dashed" : "arrow-path"}
                                    stroke={arrow.color}
                                    strokeWidth="2"
                                    fill="none"
                                    markerEnd={`url(#arrowhead-${markerColor})`}
                                    opacity="0.5"
                                />
                            );
                        })}
                    </svg>

                    {/* Input Column */}
                    <motion.div
                        className="arch-column"
                        initial={{ opacity: 0, x: -30 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1 }}
                    >
                        <div className="column-header" style={{ color: architecture.input.color }}>
                            <h2>{architecture.input.title}</h2>
                            <p>{architecture.input.subtitle}</p>
                        </div>
                        <div className="column-cards">
                            {architecture.input.items.map((item, idx) => {
                                const Icon = item.icon;
                                return (
                                    <motion.div
                                        key={idx}
                                        id={item.id}
                                        className="arch-card"
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.2 + idx * 0.1 }}
                                    >
                                        <div className="card-icon" style={{ color: architecture.input.color }}>
                                            <Icon size={24} />
                                        </div>
                                        <h3>{item.title}</h3>
                                        <p>{item.desc}</p>
                                    </motion.div>
                                );
                            })}
                        </div>
                    </motion.div>

                    {/* Processing Column */}
                    <motion.div
                        className="arch-column processing-column"
                        initial={{ opacity: 0, y: -30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <div className="column-header" style={{ color: architecture.processing.color }}>
                            <h2>{architecture.processing.title}</h2>
                            <p>{architecture.processing.subtitle}</p>
                        </div>
                        <div className="column-cards">
                            {architecture.processing.items.map((item, idx) => {
                                const Icon = item.icon;
                                return (
                                    <motion.div
                                        key={idx}
                                        id={item.id}
                                        className="arch-card"
                                        initial={{ opacity: 0, scale: 0.9 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        transition={{ delay: 0.3 + idx * 0.1 }}
                                    >
                                        <div className="card-icon" style={{ color: architecture.processing.color }}>
                                            <Icon size={24} />
                                        </div>
                                        <h3>{item.title}</h3>
                                        <p>{item.desc}</p>
                                    </motion.div>
                                );
                            })}
                        </div>
                    </motion.div>

                    {/* Output Column */}
                    <motion.div
                        className="arch-column"
                        initial={{ opacity: 0, x: 30 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 }}
                    >
                        <div className="column-header" style={{ color: architecture.output.color }}>
                            <h2>{architecture.output.title}</h2>
                            <p>{architecture.output.subtitle}</p>
                        </div>
                        <div className="column-cards">
                            {architecture.output.items.map((item, idx) => {
                                const Icon = item.icon;
                                return (
                                    <motion.div
                                        key={idx}
                                        id={item.id}
                                        className={`arch-card ${item.highlight ? 'highlight-card' : ''}`}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.4 + idx * 0.1 }}
                                    >
                                        <div className="card-icon" style={{ color: item.highlight ? '#ef4444' : architecture.output.color }}>
                                            <Icon size={24} />
                                        </div>
                                        <h3>{item.title}</h3>
                                        <p>{item.desc}</p>
                                    </motion.div>
                                );
                            })}
                        </div>
                    </motion.div>
                </div>
            </section>
        </div>
    );
};

export default SystemArchitecture;
