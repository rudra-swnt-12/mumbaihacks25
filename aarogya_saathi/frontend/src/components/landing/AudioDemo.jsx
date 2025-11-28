import React, { useState, useRef, useEffect } from 'react';
import { Play, Pause, Volume2, VolumeX, Volume1 } from 'lucide-react';
import Card from '../ui/Card';
import './AudioDemo.css';

const AudioDemo = () => {
    const audioRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [volume, setVolume] = useState(0.7);
    const [isMuted, setIsMuted] = useState(false);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        const audio = audioRef.current;
        if (!audio) return;

        const updateTime = () => setCurrentTime(audio.currentTime);
        const updateDuration = () => {
            if (audio.duration && !isNaN(audio.duration)) {
                setDuration(audio.duration);
                setIsLoaded(true);
            }
        };
        const handleEnded = () => setIsPlaying(false);
        const handleCanPlay = () => {
            if (audio.duration && !isNaN(audio.duration)) {
                setDuration(audio.duration);
                setIsLoaded(true);
            }
        };
        const handleError = (e) => {
            console.error('Audio error:', e);
        };

        audio.addEventListener('timeupdate', updateTime);
        audio.addEventListener('loadedmetadata', updateDuration);
        audio.addEventListener('durationchange', updateDuration);
        audio.addEventListener('canplay', handleCanPlay);
        audio.addEventListener('ended', handleEnded);
        audio.addEventListener('error', handleError);

        // Try to load duration on mount
        if (audio.readyState >= 1) {
            updateDuration();
        }

        return () => {
            audio.removeEventListener('timeupdate', updateTime);
            audio.removeEventListener('loadedmetadata', updateDuration);
            audio.removeEventListener('durationchange', updateDuration);
            audio.removeEventListener('canplay', handleCanPlay);
            audio.removeEventListener('ended', handleEnded);
            audio.removeEventListener('error', handleError);
        };
    }, []);

    const togglePlay = () => {
        const audio = audioRef.current;
        if (isPlaying) {
            audio.pause();
        } else {
            audio.play().catch(err => console.error('Play error:', err));
        }
        setIsPlaying(!isPlaying);
    };

    const handleProgressClick = (e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        const newTime = percent * duration;
        audioRef.current.currentTime = newTime;
        setCurrentTime(newTime);
    };

    const handleVolumeChange = (e) => {
        const newVolume = parseFloat(e.target.value);
        setVolume(newVolume);
        audioRef.current.volume = newVolume;
        if (newVolume === 0) {
            setIsMuted(true);
        } else {
            setIsMuted(false);
        }
    };

    const toggleMute = () => {
        if (isMuted) {
            audioRef.current.volume = volume || 0.7;
            setIsMuted(false);
        } else {
            audioRef.current.volume = 0;
            setIsMuted(true);
        }
    };

    const formatTime = (time) => {
        if (isNaN(time)) return '0:00';
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60).toString().padStart(2, '0');
        return `${minutes}:${seconds}`;
    };

    const progressPercent = duration ? (currentTime / duration) * 100 : 0;

    const VolumeIcon = isMuted || volume === 0 ? VolumeX : volume < 0.5 ? Volume1 : Volume2;

    return (
        <section className="audio-demo-section" id="demo">
            <div className="container">
                <Card className="audio-demo-card">
                    <div className="audio-demo-content">
                        <h2 className="section-title">See Aarogya in Action</h2>
                        <p className="audio-demo-desc">
                            Listen to our Hybrid Script TTS—Native Hindi pronunciation powered by ElevenLabs. This is what empathy sounds like.
                        </p>

                        <audio 
                            ref={audioRef} 
                            src="/response_output.mp3" 
                            preload="auto"
                        />

                        <div className="audio-player">
                            <button className="play-button" onClick={togglePlay} disabled={!isLoaded}>
                                {isPlaying ? <Pause size={24} fill="white" color="white" /> : <Play size={24} fill="white" color="white" />}
                            </button>
                            
                            <div className="progress-bar-container" onClick={handleProgressClick}>
                                <div className="progress-bar" style={{ width: `${progressPercent}%` }}></div>
                            </div>
                            
                            <span className="time-display">{formatTime(currentTime)} / {formatTime(duration)}</span>

                            <div className="volume-controls">
                                <button className="volume-button" onClick={toggleMute}>
                                    <VolumeIcon size={20} />
                                </button>
                                <input
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.01"
                                    value={isMuted ? 0 : volume}
                                    onChange={handleVolumeChange}
                                    className="volume-slider"
                                />
                            </div>
                        </div>
                    </div>
                </Card>
            </div>
        </section>
    );
};

export default AudioDemo;
