import toml
from .global_backend import ConfigBackend

class TomlBackend(ConfigBackend):
    """NOUVEAU: Backend pour les fichiers TOML."""
    def load(self, filename):
        return toml.loads(filename.read_text())

    def load_data(self, rendered):
        return toml.loads(rendered) if rendered.strip() else {}

    def save(self, filename, data):
        filename.write_text(toml.dumps(data))