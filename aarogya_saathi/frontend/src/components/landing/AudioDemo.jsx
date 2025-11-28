import React from 'react';
import { Play } from 'lucide-react';
import Card from '../ui/Card';
import './AudioDemo.css';

const AudioDemo = () => {
    return (
        <section className="audio-demo-section" id="demo">
            <div className="container">
                <Card className="audio-demo-card">
                    <div className="audio-demo-content">
                        <h2 className="section-title">See Aarogya in Action</h2>
                        <p className="audio-demo-desc">
                            Listen to our Hybrid Script TTS—Native Hindi pronunciation powered by ElevenLabs. This is what empathy sounds like.
                        </p>

                        <div className="audio-player">
                            <button className="play-button">
                                <Play size={24} fill="white" color="white" />
                            </button>
                            <div className="progress-bar-container">
                                <div className="progress-bar"></div>
                            </div>
                            <span className="time-remaining">0:42</span>
                        </div>
                    </div>
                </Card>
            </div>
        </section>
    );
};

export default AudioDemo;
