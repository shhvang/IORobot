import importlib.util
import logging
import os
from pathlib import Path
from typing import List, Optional, Union

class Loader:
    def __init__(self, path: str):
        self.path = path
        self.loaded_modules = []
        self._modules = {}

    def list_all_modules(self) -> List[str]:
        directory_path = Path(self.path)
        all_modules = []

        if not directory_path.exists() or not directory_path.is_dir():
            logging.error(f"Directory {directory_path} does not exist or is not accessible")
            return []

        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith('.py') and file != "__init__.py":
                    module_name = file[:-3]  # Remove the .py extension
                    all_modules.append(module_name)

        return all_modules

    def import_module(
        self,
        include: Optional[Union[str, List[str]]] = None,
        exclude: Optional[Union[str, List[str]]] = None,
        log: bool = False
    ) -> List[str]:
        all_modules = self.list_all_modules()

        if include:
            all_modules = [mod for mod in all_modules if mod in include]

        if exclude:
            all_modules = [mod for mod in all_modules if mod not in exclude]

        loaded_modules = []

        for module_name in all_modules:
            module_path = Path(os.path.join(self.path, f"{module_name}.py"))
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self._initialize_module(module)
                if log:
                    logging.info(f"Loaded \"{module_name}\" from \"{module_path}\"")
                loaded_modules.append(module_name)
            except Exception as e:
                if log:
                    logging.error(f"Error loading \"{module_name}\": {e}")

        if log:
            logging.info(
                f'Successfully loaded {len(loaded_modules)} module{"s" if len(loaded_modules) != 1 else ""}'
            )

        return loaded_modules

    def _initialize_module(self, module):
        if hasattr(module, 'on_load') and callable(module.on_load):
            module.on_load(self)
        self._modules[module.__name__] = module

    def unload_module(self, module_name: str):
        if module_name in self._modules:
            module = self._modules.pop(module_name)
            if hasattr(module, 'on_unload') and callable(module.on_unload):
                module.on_unload(self)
