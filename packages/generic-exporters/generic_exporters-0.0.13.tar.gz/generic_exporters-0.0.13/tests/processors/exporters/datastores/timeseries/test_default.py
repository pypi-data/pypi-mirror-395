from generic_exporters.processors.exporters.datastores.default import sqlite_settings

def test_default_sqlite_settings():
    assert sqlite_settings['provider'] == "sqlite"
    assert 'filename' in sqlite_settings
    assert sqlite_settings['create_db'] is True