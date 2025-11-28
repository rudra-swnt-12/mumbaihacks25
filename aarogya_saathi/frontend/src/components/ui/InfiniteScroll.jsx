import React from 'react';
import { motion } from 'framer-motion';

const InfiniteScroll = () => {
    const items = [
        "⚡ Reflex Cache",
        "🎙️ Acoustic Biomarkers",
        "🧠 Behavioural Dead Reckoning",
        "🗣️ Hybrid Scripting",
        "🛡️ Agentic Swarm",
        "💊 MedPrompt Architecture"
    ];

    // Duplicate items to create seamless loop
    const duplicatedItems = [...items, ...items];

    return (
        <div className="relative w-full overflow-hidden bg-slate-950 py-10">
            {/* Gradient Masks */}
            <div className="absolute left-0 top-0 z-10 h-full w-20 bg-gradient-to-r from-slate-950 to-transparent pointer-events-none"></div>
            <div className="absolute right-0 top-0 z-10 h-full w-20 bg-gradient-to-l from-slate-950 to-transparent pointer-events-none"></div>

            <div className="flex">
                <motion.div
                    className="flex flex-shrink-0 gap-16 pr-16"
                    animate={{ x: "-50%" }}
                    transition={{
                        duration: 20,
                        repeat: Infinity,
                        ease: "linear",
                    }}
                >
                    {duplicatedItems.map((item, index) => (
                        <div
                            key={index}
                            className="whitespace-nowrap text-2xl font-bold uppercase text-slate-400"
                        >
                            {item}
                        </div>
                    ))}
                </motion.div>
            </div>
        </div>
    );
};

export default InfiniteScroll;