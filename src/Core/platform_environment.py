import gym
from typing import Optional
from Core.Models.abstract_server import AbstractServer


class PlatformEnvironment(gym.Env):

    def __init__(self) -> None:
        super(PlatformEnvironment, self).__init__()
        self._env_server: Optional[AbstractServer] = None

    def reset(self):
        raise NotImplementedError("Reset method should be implented specifically for each Gym environment")
    
    def step(self, _):
        raise NotImplementedError("Step method should be implented specifically for each Gym environment")

    @property
    def env_server(self) -> AbstractServer:
        """
        Interface for getting the environment server in Gym environment
        """
        assert self._env_server, "Environment server should be injected in runtime"
        return self._env_server
    
    @env_server.setter
    def env_server(self, server: AbstractServer):
        """
        Interface for setting the environment server in Gym environment at runtime
        """
        self._env_server = server
