import React from 'react';
import Navbar from '../components/landing/Navbar';
import Hero from '../components/landing/Hero';
import ProblemSection from '../components/landing/ProblemSection';

import Reveal from '../components/ui/Reveal';
import SolutionSection from '../components/landing/SolutionSection';
import SwarmSection from '../components/landing/SwarmSection';
import DoctorView from '../components/landing/DoctorView';
import AudioDemo from '../components/landing/AudioDemo';
import Footer from '../components/landing/Footer';

const LandingPage = () => {
    return (
        <div className="min-h-screen bg-white font-sans text-slate-900">
            <Navbar />
            <Reveal width="100%">
                <Hero />
            </Reveal>

            {/* The Digital Divide Section */}
            <Reveal width="100%">
                <ProblemSection />
            </Reveal>



            {/* Meet Aarogya Section */}
            <Reveal width="100%">
                <SolutionSection />
            </Reveal>

            <SwarmSection />

            <Reveal width="100%">
                <DoctorView />
            </Reveal>

            <AudioDemo />
            <Footer />
        </div>
    );
};

export default LandingPage;
