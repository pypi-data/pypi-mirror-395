import cv2
import numpy as np
import gymnasium as gym
import sai_wm.utils.v0.wrappers as wrappers

def normalize_pixel_obs(observation):
    return observation / 255.0

def reshape_pixels(image, shape=(64, 64)):
    image = cv2.resize(image, shape).astype(np.float32)
    return image

def make_gym_env(env_name: str, normalize: bool = True, input_shape: np.ndarray = None):

    env = gym.make(env_name, render_mode="rgb_array")

    is_vectorized = len(env.observation_space.shape) < 3

    if input_shape is not None and not is_vectorized:
        env = wrappers.ImageResizeWrapper(env, input_shape)
    
    if normalize:
        env = wrappers.PixelNormalization(env)

    if not is_vectorized:
        env = wrappers.ChannelFirstWrapper(env)

    return env, is_vectorized
