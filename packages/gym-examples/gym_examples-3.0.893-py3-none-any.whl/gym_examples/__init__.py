from gym.envs.registration import register

register(
     id="WSNRouting-v0",
     entry_point="gym_examples.envs:WSNRoutingEnv",
)

__version__ = "3.0.893"
