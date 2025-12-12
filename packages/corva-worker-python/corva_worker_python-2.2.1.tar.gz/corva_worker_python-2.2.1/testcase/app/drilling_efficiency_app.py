from testcase.app.disable_module import DisableModule
from testcase.app.surface_mse_module import SurfaceMSE
from worker.app import App


class DrillingEfficiency(App):
    # override
    def get_modules(self):
        return [SurfaceMSE, DisableModule]
