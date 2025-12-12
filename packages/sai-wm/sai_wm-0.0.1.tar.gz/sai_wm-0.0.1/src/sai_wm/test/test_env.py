import gymnasium as gym
import sai_wm

env = gym.make("PwmAnt-v0", render_mode="human")

observation, info = env.reset()

try:
    while True:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        
        if terminated or truncated:
            observation, info = env.reset()

finally:
    env.close()
