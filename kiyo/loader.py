import importlib.util
import logging
import os
from pathlib import Path
from typing import List, Optional, Union, Any, Dict

from kiyo.logger import logger

class Loader:
    def __init__(self, path: str):
        self.path = path
        self.loaded_modules = []
        self._modules = {}

    def list_all_modules(self) -> List[str]:
        all_modules = []

        def _get_modules_in_directory(dir_path: Path):
            for item in dir_path.iterdir():
                if item.is_file() and item.suffix == '.py' and item.stem != "__init__":
                    # Append relative path to module (without extension) to all_modules list
                    all_modules.append(str(item.relative_to(Path(self.path)).with_suffix('')))
                elif item.is_dir():
                    _get_modules_in_directory(item)

        directory_path = Path(self.path)
        if not directory_path.exists() or not directory_path.is_dir():
            logger.error(f"Directory {directory_path} does not exist or is not accessible")
            return []

        _get_modules_in_directory(directory_path)
        return all_modules

    def import_module(
        self,
        include: Optional[Union[str, List[str]]] = None,
        exclude: Optional[Union[str, List[str]]] = None,
        log: bool = False,
        **kwargs: Any
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
                self._initialize_module(module, **kwargs)
                if log:
                    logger.info(f"Loaded \"{module_name}\" from \"{module_path}\"")
                loaded_modules.append(module_name)
            except Exception as e:
                if log:
                    logger.error(f"Error loading \"{module_name}\": {e}")

        if log:
            logger.info(
                f'Successfully loaded {len(loaded_modules)} module{"s" if len(loaded_modules) != 1 else ""}'
            )

        return loaded_modules

    def _initialize_module(self, module: Any, **kwargs: Any):
        if hasattr(module, 'on_load') and callable(module.on_load):
            module.on_load(self, **kwargs)
        self._modules[module.__name__] = module

    def reload_module(
        self,
        module_name: str,
        log: bool = False,
        **kwargs: Any
    ) -> Optional[str]:
        if module_name not in self._modules:
            if log:
                logger.error(f"Module \"{module_name}\" is not currently loaded")
            return None

        module = self._modules[module_name]
        module_path = Path(os.path.join(self.path, f"{module_name}.py"))
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            new_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(new_module)

            # Unload existing module
            if hasattr(module, 'on_unload') and callable(module.on_unload):
                module.on_unload(self)

            # Initialize new module
            self._initialize_module(new_module, **kwargs)
            self._modules[module_name] = new_module

            if log:
                logger.info(f"Reloaded \"{module_name}\" from \"{module_path}\"")
            return module_name
        except Exception as e:
            if log:
                logger.error(f"Error reloading \"{module_name}\": {e}")
            return None

    def unload_module(self, module_name: str, log: bool = False):
        if module_name in self._modules:
            module = self._modules.pop(module_name)
            if hasattr(module, 'on_unload') and callable(module.on_unload):
                module.on_unload(self)
            if log:
                logger.info(f"Unloaded module \"{module_name}\"")
        else:
            if log:
                logger.error(f"Module \"{module_name}\" is not currently loaded")

    def get_module(self, module_name: str) -> Optional[Any]:
        return self._modules.get(module_name, None)

    def get_all_modules(self) -> Dict[str, Any]:
        return self._modules
