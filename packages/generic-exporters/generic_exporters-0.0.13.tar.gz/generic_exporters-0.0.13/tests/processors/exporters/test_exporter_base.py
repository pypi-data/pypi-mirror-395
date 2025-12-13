
from generic_exporters.processors.exporters._base import _ExporterBase

class DummyExporter(_ExporterBase):
    async def data_exists(self):
        return False
    async def run(self):
        pass

def test_exporter_base():
    exporter = DummyExporter()
    data_exists = exporter.data_exists()
    assert not data_exists
