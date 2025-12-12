import numpy as np
import gymnasium as gym
from torch import P
from sai_wm.world_models.base.base_v0 import  BaseWM_v0

class WorldModel_v0(BaseWM_v0):
    """
    Original World Model paper wrapper
    """

    def __init__(self, 
                 world_config: dict, 
                 np_random: np.random.Generator,
                 device="cpu"):
        
        super().__init__(world_config, np_random=np_random, device=device)
        self.hidden = None

        self.latent_dim = self.config.get("latent_dim", None)
        self.hidden_dim = self.config.get("hidden_state_dim", None)
        self.input_shape = self.config.get("input_shape", (64, 64))

        if self.dream:
            self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(self.latent_dim,), dtype=np.float32)
        else:
            self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(self.latent_dim + 2 * self.hidden_dim,), dtype=np.float32)

        assert self.latent_dim is not None and self.hidden_dim is not None, (
            "World Model needs a latent dimension and hidden state dimension of the world model in the config file"
        )

        self.z = None
        self.reset()

    def reset(self, batch_size=1):

        h = np.zeros((1, batch_size, self.hidden_dim), dtype=np.float32)
        c = np.zeros((1, batch_size, self.hidden_dim), dtype=np.float32)
        self.hidden = (h, c)

    def forward(self, obs):

        self.z = self.encode(obs)
        recon = self.decode(self.z)

        latent_state = self._get_obs(self.z)

        return {
            "latent_state": latent_state,
            "recon": recon
        }

    def encode(self, obs):

        if obs.ndim == 3:
            obs = np.expand_dims(obs, 0)  # (1,C,H,W)

        mu, sigmavar = self.handler.forward(obs, "encoder")
        std = np.exp(sigmavar)
        eps =  self.np_random.random(std.shape)
        z = mu + eps * std
        return z

    def decode(self, z):

        if z.ndim == 1: 
            z = np.expand_dims(z, 0)
        
        recon = self.handler.forward(z, "decoder")
        return recon.squeeze(0)

    def sample_mdn(self, pi, sigma, mu):

        pi = pi[:,0]
        sigma = sigma[:,0]
        mu = mu[:,0]

        B, K, D = pi.shape

        pi_reduced = pi.mean(axis=2)
        mix_idx = self.handler.categorical_sample(pi_reduced)

        batch_indices = np.arange(B)
        chosen_mu = mu[batch_indices, mix_idx, :]        # (B, D)
        chosen_sigma = sigma[batch_indices, mix_idx, :]

        return self.handler.normal_sample(chosen_mu, chosen_sigma)

    def predict(self, action):

        if action.ndim == 1: 
            action = np.expand_dims(action, 0)

        z = self.z

        x = np.concatenate([z, action], axis=1)
        x = np.expand_dims(x, 1)

        if self.hidden is None:
            self.reset(batch_size=x.shape(0))

        self.handler.forward((x, self.hidden), "world_model")
        pi, sigma, mu, hidden_out = self.handler.forward((x, self.hidden), "world_model")
        self.hidden = hidden_out

        self.z = self.sample_mdn(pi, sigma, mu)
        recon = self.decode(self.z)

        latent_state = self._get_obs(self.z)
        return {
            "latent_state": latent_state,
            "recon": recon
        }
    
    def _get_obs(self, z):
        
        hidden = np.concatenate(self.hidden, axis=-1).squeeze(0)
        latent_state = np.concatenate([z, hidden], axis=1)
        
        return latent_state

    def step(self, obs, action):
        z = self.encode(obs)
        return self.predict(z, action)