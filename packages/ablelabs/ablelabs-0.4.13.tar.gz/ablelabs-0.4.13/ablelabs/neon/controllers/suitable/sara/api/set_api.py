from typing import Any

import sys, os

sys.path.append(os.path.abspath(os.curdir))
from ablelabs.neon.utils.network.messenger import MessengerClient, run_server_func
from ablelabs.neon.utils.network.tcp_client import TcpClient
from ablelabs.neon.controllers.suitable.sara.api.robot_router import RobotRouter
from ablelabs.neon.common.suitable.enums import PipetteCalibrationType


class SetAPI(MessengerClient):
    def __init__(self, tcp_client: TcpClient) -> None:
        super().__init__(tcp_client)

    @run_server_func(RobotRouter.set_pipettes)
    async def pipettes(self, value: dict[int, str | None]):
        pass

    @run_server_func(RobotRouter.set_tips)
    async def tips(self, value: dict[int, str | None]):
        pass

    @run_server_func(RobotRouter.set_labwares)
    async def labwares(self, value: dict[int, str | None]):
        pass

    @run_server_func(RobotRouter.set_update_setup_data)
    async def update_setup_data(self, value: dict, save: bool):
        pass

    @run_server_func(RobotRouter.set_update_pipette_attrs)
    async def update_pipette_attrs(self, value: dict[int, dict]):
        pass

    @run_server_func(RobotRouter.set_pipette_calibrations)
    async def pipette_calibrations(self, value: dict[int, PipetteCalibrationType]):
        pass

    @run_server_func(RobotRouter.set_position)
    async def position(
        self,
        labware_code: str,
        deck: int,
        x: float,
        ys: list[float],
        zs: list[float],
        tip_volume: int = None,
        save: bool = True,
    ) -> dict:
        """position 저장"""
        pass
