import importlib.metadata
import os
import sys
import traceback

__author__ = "SINTEF Energy Research"
__copyright__ = "SINTEF Energy Research"
__license__ = "MIT"

# Default path on vlab
PYLTM_DEFAULT_PATH = "/opt/sintef-energy/ltm/lib/"

# Override if ICC_LIBRARY_PATH is set
if "ICC_LIBRARY_PATH" in os.environ:
    PYLTM_DEFAULT_PATH = os.environ["ICC_LIBRARY_PATH"]


class LtmSession(object):

    def __init__(
        self,
        session_name: str,
        pyltm_path: str = PYLTM_DEFAULT_PATH,
        ltm_core_path: str = None,
        overwrite_session = False,
        ltm_license_file_path = None
    ) -> None:

        # Add module to path to system path
        if pyltm_path:
            module_path = os.path.abspath(pyltm_path)
            sys.path.insert(0, module_path)

        # Check if path to the LTM core applications exists
        self.original_path = None
        if ltm_core_path:
            if not os.path.isdir(ltm_core_path):
                raise RuntimeError(
                    f"parameter ltm_core_path='{ltm_core_path}' is not a directory"
                )

            # Preserve old PATH environment variable
            self.original_path = os.environ["PATH"]

            # Prepend LTM core path to PATH
            os.environ["PATH"] = ltm_core_path + os.pathsep + os.environ["PATH"]

        # Import LTM module
        import pyltm as pb

        # Instanciate
        self._pb = pb
        self._apimodule = pb.LtmApiModule(session_name, overwrite_session)
        self.export_target = pb.ExportTarget
        self.model = self._apimodule.model
        self.model.global_settings.ltm_license_file_path = ltm_license_file_path

    # Shortcut to defined methods in pyltm
    def __getattr__(self, action: str):
        try:
            return self._apimodule.__getattribute__(action)
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{action}'"
            )

    def __repr__(self):
        return f"LtmSession {self._apimodule}, {self._pb}"

    def __enter__(self):
        return self._apimodule.__enter__()

    def __exit__(self, exception_type, exception_value, tb):
        # Restore old environment
        if self.original_path is not None:
            os.environ["PATH"] = self.original_path

        self._apimodule.__exit__(exception_type, exception_value, tb)
        if exception_type is not None:
            traceback.print_exception(exception_type, exception_value, tb)
            return False

        return True

    @staticmethod
    def version():
        try:
            return f"PyLTM version: {importlib.metadata.version('pyltm')}"
        except importlib.metadata.PackageNotFoundError:
            return "PyLTM version: unknown"
