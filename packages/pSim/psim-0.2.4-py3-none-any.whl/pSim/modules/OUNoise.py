import numpy as np


class OrnsteinUhlenbeckNoise:
    """This class implements an Ornstein-Uhlenbeck noise which is used to add
    noise to the actions of the agents."""

    def __init__(self, theta=0.17, dt=0.025, x0=None):
        self.mu = 0
        self.sigma = 0.5
        self.theta = theta
        self.dt = dt
        self.x0 = x0
        self.reset()

    def sample(self):
        x = (
            self.x_prev
            + self.theta * (self.mu - self.x_prev) * self.dt
            + self.sigma * np.sqrt(self.dt) * np.random.normal()
        )
        self.x_prev = x
        return x

    def reset(self):
        self.x_prev = self.x0 if self.x0 is not None else np.zeros_like(self.mu)
