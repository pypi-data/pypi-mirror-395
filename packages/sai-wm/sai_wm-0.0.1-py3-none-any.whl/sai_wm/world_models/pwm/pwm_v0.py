import numpy as np
import gymnasium as gym
from sai_wm.world_models.base.base_v0 import  BaseWM_v0

class PWM_v0(BaseWM_v0):
    """
    PWM wrapper
    """

    def __init__(self, 
                 world_config: dict, 
                 np_random: np.random.Generator,
                 device="cpu"):
        
        super().__init__(world_config, np_random=np_random, device=device)
        self.hidden = None

        self.latent_dim = self.config.get("latent_dim", None)
        self.input_shape = self.config.get("input_shape", (64, 64))

        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(self.latent_dim,), dtype=np.float32)

        assert self.latent_dim is not None, (
            "World Model needs a latent dimension and hidden state dimension of the world model in the config file"
        )

        self.z = None

        self.reset()

    def reset(self):
        pass

    def forward(self, obs):
        
        self.z = self.encode(obs)
        return {
            "latent_state": self.encode(obs)
        }
    
    def encode(self, obs):

        if obs.ndim == 3 or obs.ndim == 1:
            obs = np.expand_dims(obs, 0)  # (1,C,H,W)

        z = self.handler.forward(obs, "encoder")
        return z
    
    def next(self, z, action):

        x = np.concatenate([z, action], axis=-1)
        return self.handler.forward(x, "dynamics")
    
    def reward(self, z, action):

        x = np.concatenate([z, action], axis=-1)
        return self.handler.forward(x, "reward").squeeze(0)[0]

    def predict(self, action):

        if action.ndim == 1: 
            action = np.expand_dims(action, 0)

        z = self.z

        x = np.concatenate([z, action], axis=1)
        x = np.expand_dims(x, 1)

        self.z = self.next(z, action)
        reward = self.reward(z, action)

        return {
            "latent_state": self.z,
            "reward": reward
        }