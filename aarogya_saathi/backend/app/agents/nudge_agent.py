import numpy as np


class NudgeAgent:
    def __init__(self):
        self.strategies = [
            {"name": "Direct", "prompt": "Be firm, authoritative, and direct."},
            {
                "name": "Emotional",
                "prompt": "Be warm, like a family member. Mention family well-being.",
            },
            {
                "name": "Fear",
                "prompt": "Highlight the medical risks if they don't act.",
            },
        ]
        self.n_arms = len(self.strategies)

        self.alpha = np.ones(self.n_arms)
        self.beta = np.ones(self.n_arms)

    def select_action(self):
        """
        Uses Thompson Sampling to pick the best strategy.
        Returns: { "index": int, "name": str, "confidence": float, "strategy": dict }
        """
        samples = [np.random.beta(a, b) for a, b in zip(self.alpha, self.beta)]

        chosen_index = np.argmax(samples)

        return {
            "index": int(chosen_index),
            "name": self.strategies[chosen_index]["name"],
            "confidence": samples[chosen_index],
            "strategy": self.strategies[chosen_index],
        }

    def update(self, action_index, reward):
        """
        Update the model based on outcome.
        Reward: 1 (User complied), 0 (User ignored)
        """
        if reward == 1:
            self.alpha[action_index] += 1
        else:
            self.beta[action_index] += 1
