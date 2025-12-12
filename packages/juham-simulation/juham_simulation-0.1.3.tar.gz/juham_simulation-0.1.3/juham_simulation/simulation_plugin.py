from typing_extensions import override
from masterpiece import Plugin, Composite
from .watermetersim import WaterMeterSim
from .powermetersim import PowerMeterSim
from .temperaturesim import TemperatureSim


class SimulationPlugin(Plugin):
    """Plugin class for installing and instantiating simulation classes
    into the host application."""

    enable_watermetersim: bool = True
    enable_powermetersim: bool = True
    enable_temperaturesim: bool = True

    def __init__(self, name: str = "simulation_plugin") -> None:
        """Create and install WaterMeterSim."""
        super().__init__(name)

    @override
    def install(self, app: Composite) -> None:
        if self.enable_watermetersim:
            app.add(WaterMeterSim())
        if self.enable_powermetersim:
            app.add(PowerMeterSim())
        if self.enable_temperaturesim:
            app.add(TemperatureSim())
