import { useEffect } from 'react';

export const useArrowConnections = (arrows) => {
    useEffect(() => {
        const updateArrows = () => {
            arrows.forEach((arrow, idx) => {
                const fromEl = document.getElementById(arrow.from);
                const toEl = document.getElementById(arrow.to);
                const pathEl = document.getElementById(`arrow-${idx}`);

                if (fromEl && toEl && pathEl) {
                    const fromRect = fromEl.getBoundingClientRect();
                    const toRect = toEl.getBoundingClientRect();
                    const container = document.querySelector('.arch-container');
                    const containerRect = container?.getBoundingClientRect();

                    if (containerRect) {
                        // Calculate positions relative to container
                        const startX = fromRect.right - containerRect.left;
                        const startY = fromRect.top + fromRect.height / 2 - containerRect.top;
                        const endX = toRect.left - containerRect.left;
                        const endY = toRect.top + toRect.height / 2 - containerRect.top;

                        // Create curved path
                        const midX = (startX + endX) / 2;
                        const path = `M ${startX} ${startY} Q ${midX} ${startY}, ${midX} ${(startY + endY) / 2} T ${endX} ${endY}`;
                        
                        pathEl.setAttribute('d', path);
                    }
                }
            });
        };

        // Initial update
        setTimeout(updateArrows, 100);

        // Update on resize
        window.addEventListener('resize', updateArrows);
        
        return () => {
            window.removeEventListener('resize', updateArrows);
        };
    }, [arrows]);
};
