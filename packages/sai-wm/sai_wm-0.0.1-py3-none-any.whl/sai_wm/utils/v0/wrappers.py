import cv2
import numpy as np
import gymnasium as gym
from typing import Tuple, Optional

class ChannelFirstWrapper(gym.ObservationWrapper):

    def __init__(self, env: gym.Env):
        super().__init__(env)

        obs_space = env.observation_space

        # Leave vector observations unchanged
        old_shape = obs_space.shape
        new_shape = (old_shape[-1],) + old_shape[:-1]

        self.observation_space = gym.spaces.Box(
            low=np.transpose(obs_space.low, self._new_order(obs_space.low)),
            high=np.transpose(obs_space.high, self._new_order(obs_space.high)),
            shape=new_shape,
            dtype=obs_space.dtype
        )

    def _new_order(self, arr: np.ndarray):
        """Create permutation order that moves last dim to front."""
        dims = arr.ndim
        return (dims - 1,) + tuple(range(dims - 1))

    def _permute(self, obs: np.ndarray):
        """Move last dimension to first, supporting N-dim arrays."""

        order = self._new_order(obs)
        return np.transpose(obs, order)

    def observation(self, observation):
        return self._permute(observation)

class ImageResizeWrapper(gym.ObservationWrapper):
    """
    Resize observation to match the input shape of the World Model network.
    Leaves vector observations unchanged.
    """

    def __init__(self, env: gym.Env, new_size: Tuple):
        super().__init__(env)

        self.new_size = new_size

        obs_space = env.observation_space

        self.is_image = True
        C = obs_space.shape[-1]

        low_resized  = self._resize_bounds(obs_space.low).astype(obs_space.dtype)
        high_resized = self._resize_bounds(obs_space.high).astype(obs_space.dtype)

        self.observation_space = gym.spaces.Box(
            low=low_resized,
            high=high_resized,
            shape=(*new_size, C),
            dtype=obs_space.dtype
        )

    def _resize_bounds(self, arr):
        resized = cv2.resize(arr, np.transpose(self.new_size), interpolation=cv2.INTER_NEAREST)
        return resized

    def observation(self, obs):
        return self._resize_bounds(obs)
    
class PixelNormalization(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)

    def _pixel_normalization(self, obs):
        return obs / 255.0

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        return self._pixel_normalization(obs), reward, terminated, truncated, info

    def reset(self, *, seed: Optional[int] = None, **kwargs):        
        obs, info = self.env.reset(seed = seed)
        return self._pixel_normalization(obs), info