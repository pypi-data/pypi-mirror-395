import tomllib
import inspect
import pathlib
from datetime import datetime as dt
from importlib.metadata import Distribution, distributions, version
from typing import Tuple, Union

from loguru import logger as LOGGER


class ProjectHelper:
    """
    Helper class for retrieving project info such as version and installed packages.

    """
    _max_depth = 4

    @staticmethod
    def _search_down_tree(filename: str, start_path: str, depth: int = _max_depth) -> Union[pathlib.Path, None]:
        """
        Search directory tree towards root for filename starting at start path.

        Limit seach to depth number of directories.

        Args:
            filename (str): target_filename.
            start_path (str): path to begin search.
            depth (int, optional): Number of directories to travers (towards root). Defaults to _max_depth.

        Returns:
            str: Full filename/path or None.
        """
        LOGGER.trace(f'  Search for {filename} starting at {start_path}')
        result_file: pathlib.Path = None
        cur_depth = 0
        traverse_path = pathlib.Path(start_path)
        pattern = f"**/{filename}"
        while result_file is None and cur_depth < depth:
            cur_depth += 1
            file_list = list(traverse_path.glob(pattern))
            LOGGER.trace(f'  - directory: {str(traverse_path)}')
            # LOGGER.trace(f'    file_list: {file_list}')
            if len(file_list) == 1:
                result_file = file_list[0]
                LOGGER.trace(f'  FOUND: {result_file}')
            else:
                traverse_path = traverse_path.parent
        return result_file

    @staticmethod
    def _check_metadata(target_name: str) -> Tuple[str,str]:
        ver = None
        determined_from = None
        try:
            LOGGER.trace('Try import.metadata')
            ver = version(target_name)
            determined_from = "importlib.metadata"
        except:  # noqa: E722
            LOGGER.trace('- Not found in metadata')


        return ver, determined_from

    @staticmethod
    def _check_toml(project_name: str, calling_module: str) -> Tuple[str,str]:
        LOGGER.trace(f'_check_toml() project: {project_name}  calling_module: {calling_module}')
        ver = None
        determined_from = None
        target_file = ProjectHelper._search_down_tree("pyproject.toml", pathlib.Path(calling_module).parent)
        # LOGGER.warning(target_file)
        if target_file is None:
            LOGGER.trace('- unable to locate pyproject.toml')
        else:
            buff = target_file.read_text(encoding='utf-8').splitlines()
            proj_name = ""
            name_list = [x for x in buff if x.startswith('name')]
            # LOGGER.warning(name_list)
            if len(name_list) >= 1:
                token = name_list[0].split('=')[1].strip()
                proj_name = token.replace('"',"").replace("'","")
                # LOGGER.warning(f'token: {token}  proj_name: {proj_name}')
            if project_name != proj_name:
                LOGGER.trace(f'- Requested project name {project_name} does not match pyproject.toml project name {proj_name}')
            else:
                ver_line = [x for x in buff if x.startswith('version')]
                LOGGER.trace(f'ver_line: {ver_line}')
                if len(ver_line) == 1:
                    ver = ver_line[0].split('=')[1].replace('"','').replace("'",'').strip()
                    determined_from = "pyproject.toml"
                LOGGER.trace('- Identified via pyproject.toml')
        return ver, determined_from
    
    @staticmethod
    def _check_call_stack(root_path: str, python_file: str) -> Tuple[str, str]:
        LOGGER.trace('Try python file')
        ver = None
        determined_from = None
        if not python_file.endswith('.py'):
            LOGGER.trace(f'  Passed file: {python_file} does not appear to be python file.')
            return ver, determined_from
        
        LOGGER.trace(f'- python file: {python_file}  root_path: {root_path}')
        file_list = list(pathlib.Path(root_path).glob(f"**/{python_file}"))
        if len(file_list) == 0:
            LOGGER.trace(f'  Unable to locate python file: {python_file}')
            return ver, determined_from
        LOGGER.trace(f'  Python file abs: {file_list[0]}')
        file_list = list(pathlib.Path(root_path).glob('**/*.py'))
        ver_date = dt(2000,1,1,0,0,0,0)
        LOGGER.trace(f'  File list: {file_list}')
        for file_nm in file_list:
            if dt.fromtimestamp(file_nm.stat().st_mtime) > ver_date:
                ver_date = dt.fromtimestamp(file_nm.stat().st_mtime)
                ver_file = file_nm
            ver_date = max(ver_date, dt.fromtimestamp(file_nm.stat().st_mtime))
        ver = f'{ver_date.year}.{ver_date.month}.{ver_date.day}'    
        determined_from = f'File date: {str(ver_date)} {ver_file}'
    
        return ver, determined_from
    
    @staticmethod
    def _get_caller(from_caller: str) -> Tuple[pathlib.Path, int]:
        callstack_len = len(inspect.stack())
        LOGGER.trace(f'Who called [{from_caller}()]')
        LOGGER.trace(f'Call Stack ({callstack_len}):')
        from_caller_idx = -1
        for idx in range(callstack_len):
            element = inspect.stack()[idx]
            LOGGER.trace(f'- {idx:2} func: {element.function}()') 
            LOGGER.trace(f'     file: {inspect.stack()[idx].filename}:{element.lineno}')
            if element.function == from_caller:
                from_caller_idx = idx

        caller: pathlib.Path = None        
        lineno: int = None
        # Get caller before from_caller
        if from_caller_idx >= 0:
            element = inspect.stack()[from_caller_idx+1]
            caller = pathlib.Path(element.filename)
            lineno = element.lineno

        return caller, lineno 

    @staticmethod
    def determine_version(target_name: str, identify_src: bool = False) -> Union[str, Tuple[str, str]]:
        """
        Retrieve project version for distribution (or running codebase)

        Version is determined by:  
        - look for pyproject.toml  
        - check importlib metadata
        - scanning calling stack root file newest python module  

        Args:
            distrib_name (str): Package distribution name.
              If distrib_name not found, version will be determined from pyproject.toml (if found) or
              from the newest .py file in the stack path starting at the calling program.
            identify_src (bool, otional): Return a string indicating how the version was determined. Defaults to False

        Returns:
            Union[str,Tuple[str,str]: version or version, source.
            - version is in format major.minor.patch or YYYY.MM.DD.
            - source is one of 'importlib.metadata', 'pyproject.toml' or source filename.

        Raises:
            ValueError: if target_name is not str
            
        """
        if not isinstance(target_name, str):
            raise ValueError(f'Invalid target name (must be str) in determine_version: {target_name}')
        
        LOGGER.trace(f'determine_version for {target_name}')
        ver = None
        # root_idx = len(inspect.stack()) - 1
        # caller = pathlib.Path(inspect.stack()[root_idx].filename)
        caller, lineno = ProjectHelper._get_caller('determine_version') # who called this routine
        LOGGER.trace(f'- calling from {caller}:{lineno}')
        ver = None
        determined_from = None
        if caller is not None:
            ver, determined_from = ProjectHelper._check_toml(target_name, caller)
        if ver is None:
            ver, determined_from = ProjectHelper._check_metadata(target_name)

        if ver is None:
            python_file = f'{target_name}.py'
            ver, determined_from = ProjectHelper._check_call_stack(root_path=caller.parent, python_file=python_file)
            if ver is None:
                root_idx = 0 # len(inspect.stack()) - 2
                caller = pathlib.Path(inspect.stack()[root_idx].filename)
                ver, determined_from = ProjectHelper._check_call_stack(root_path=caller.parent, python_file=python_file)

        if identify_src:
            return (ver, determined_from)
        return ver

    @staticmethod
    def _pyproject_toml_location(from_caller: str) -> pathlib.Path:
        caller, lineno = ProjectHelper._get_caller(from_caller)
        LOGGER.trace(f'_pyproject_toml_location() called from {caller}:{lineno}')
        target_file = ProjectHelper._search_down_tree("pyproject.toml", pathlib.Path(caller).parent)
        if target_file is None:
            LOGGER.trace(f'Unable to locate pyproject.toml for {caller}')
        return target_file
    
    @staticmethod
    def installed_pyproject_toml_packages() -> dict:
        """
        Return a dictionary describing pyproject.toml installed packages.

        Returns:
            dict: in format {"pkg_name1": "pkg_version", "pkg_name2": "pkg_version", ...}
        """
        toml_packages = {}
        toml_file = ProjectHelper._pyproject_toml_location('installed_pyproject_toml_packages')
        if toml_file is not None:
            config = tomllib.loads(toml_file.read_text())
            toml_deps = config.get('tool',{}).get('poetry', None)
            if toml_deps is not None:
                dist_deps = ProjectHelper.installed_distribution_packages()
                for toml_pkg, val in toml_deps['dependencies'].items():
                    dep_version = dist_deps.get(toml_pkg, None)
                    if dep_version is not None:
                        toml_packages[toml_pkg] = dep_version
        return toml_packages
    

    @staticmethod
    def installed_distribution_packages() -> dict:
        """
        Return a dictionary describing installed packages.

        Returns:
            dict: in format {"pkg_name1": "pkg_version", "pkg_name2": "pkg_version", ...}
        """
        package: Distribution = None
        package_dict: dict = {}
        for package in distributions():
            package_dict[package.name] = package.version
        
        return package_dict
    

if __name__ == '__main__':
    import dt_tools.logger.logging_helper as lh
    lh.configure_logger(log_level="TRACE", log_format=lh.DEFAULT_DEBUG_LOGFMT2)
    LOGGER.info(ProjectHelper.determine_version('dt-foundation'))
    LOGGER.info(ProjectHelper.installed_pyproject_toml_packages())
    # print(ProjectHelper.installed_distribution_packages())