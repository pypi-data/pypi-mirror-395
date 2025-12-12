import cv2
import numpy as np
import gymnasium as gym
from typing import Optional

from sai_wm.envs.base.base_v0 import BaseEnv_v0
from sai_wm.utils.v0.tools import make_gym_env

class GymEnv_v0(BaseEnv_v0):

    def __init__(self, env_config: dict, world_config: dict, world_model_entry_points: dict, **kwargs):
        super().__init__(env_config, world_config, world_model_entry_points, **kwargs)

        base_env_id = env_config.get("base_env_name", None)
        assert base_env_id is not None, (
            f"Base gymnasium environment should be provided for the world model"
        )
        self.base_env, self.is_vectorized = make_gym_env(base_env_id, normalize= True, input_shape= self.wm.input_shape)

        self.observation_space = gym.spaces.Dict({
            "observation": self.wm.observation_space,
            "decoded": self.base_env.observation_space,
            "original": self.base_env.observation_space
        })

        self.action_space = self.base_env.action_space

        self.latent = None
        self.decoded = None
        self.original = None

    def reset(self, *, seed: Optional[int] = None, **kwargs):
        super().reset(seed=seed)

        self.wm.reset()
        original, _ = self.base_env.reset()

        wm_output = self.wm.forward(original)

        self.latent = wm_output.get("latent_state")
        self.decoded = wm_output.get("recon", original)
        self.original = original

        info = self._get_info()

        return self._get_obs(), info

    def step(self, action: np.ndarray):

        action = np.asarray(action, dtype=np.float32)

        original, reward, terminated, truncated, _ = self.base_env.step(action)
        wm_output = self.wm.predict(action)

        self.latent = wm_output.get("latent_state")
        self.decoded = wm_output.get("recon", original)
        self.original = original

        reward = wm_output.get("reward", reward)

        info = self._get_info()

        if self.render_mode == "human":
            self.render()

        return self._get_obs(), reward, terminated, truncated, info

    def _get_obs(self):

        return {
            "observation": self.latent.astype(np.float32),
            "decoded": self.decoded,
            "original": self.original
        }
    
    def compute_terminated(self):
        return False