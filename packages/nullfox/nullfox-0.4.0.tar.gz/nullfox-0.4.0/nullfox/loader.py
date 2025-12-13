import os
import importlib
from .encrypt import decrypt_file

class Loader:
    def __init__(self, key: str):
        self.key = key

    def load(self, path: str):
        """Loads, decrypts, and executes an encrypted NullFox script."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        # 1. Decrypt the file to memory
        decrypted = decrypt_file(path, self.key)

        # 2. Convert bytes to string
        try:
            code_str = decrypted.decode("utf-8")
        except Exception:
            raise ValueError("Decrypted file is not valid UTF‑8 code")

        # 3. Create isolated sandbox
        namespace = {
            "__name__": "__nullfox_script__",
            "__builtins__": __builtins__
        }

        # 4. Execute the script safely
        exec(code_str, namespace)

        return namespace