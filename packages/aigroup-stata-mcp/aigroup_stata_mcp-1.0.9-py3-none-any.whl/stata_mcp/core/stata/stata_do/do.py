#!/usr/bin/python3
# -*- coding: utf-8 -*-


import logging
import os
import subprocess

from ....utils import get_nowtime


class StataDo:
   
    """Stata do文件执行器，用于执行Stata脚本并管理日志"""
    def __init__(self,
                 stata_cli: str,
                 log_file_path: str,
                 dofile_base_path: str,
                 sys_os: str = None):
        """
        Initialize Stata executor

        Args:
            stata_cli: Path to Stata command line tool
            log_file_path: Path for storing log files
            dofile_base_path: Base path for do files
            sys_os: Operating system type
        """
        self.stata_cli = stata_cli
        self.log_file_path = log_file_path
        self.dofile_base_path = dofile_base_path
        if sys_os:
            self.sys_os = sys_os
        else:
            from ....utils import get_os
            self.sys_os = get_os()

    def set_cli(self, cli_path):
        """设置Stata CLI路径"""
        self.stata_cli = cli_path

    @property
    def STATA_CLI(self):
        """获取Stata CLI路径"""
        return self.stata_cli

    def execute_dofile(self,
                       dofile_path: str,
                       log_file_name: str = None,
                       is_replace: bool = True) -> str:
        """
        Execute Stata do file and return log file path

        Args:
            dofile_path (str): Path to do file
            log_file_name (str, optional): File name of log
            is_replace (bool): Whether replace the log file if exists before. Default is True

        Returns:
            str: Path to generated log file

        Raises:
            ValueError: Unsupported operating system
            RuntimeError: Stata execution error
        """
        nowtime = get_nowtime()
        log_name = log_file_name or nowtime
        log_file = os.path.join(self.log_file_path, f"{log_name}.log")

        if self.sys_os == "Darwin" or self.sys_os == "Linux":
            self._execute_unix_like(dofile_path, log_file, is_replace)
        elif self.sys_os == "Windows":
            self._execute_windows(dofile_path, log_file, nowtime, is_replace)
        else:
            raise ValueError(f"Unsupported operating system: {self.sys_os}")

        return log_file

    def _execute_unix_like(self, dofile_path: str, log_file: str, is_replace: bool = True):
        """
        Execute Stata on macOS/Linux systems

        Args:
            dofile_path: Path to do file
            log_file: Path to log file
            is_replace: Whether replace the log file if exists.

        Raises:
            RuntimeError: Stata execution error
        """
        proc = subprocess.Popen(
            [self.STATA_CLI],  # Launch the Stata CLI
            stdin=subprocess.PIPE,  # Prepare to send commands
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,  # Required when the path contains spaces
        )

        # Execute commands sequentially in Stata
        replace_clause = ", replace" if is_replace else ""

        commands = f"""
        log using "{log_file}"{replace_clause}
        do "{dofile_path}"
        log close
        exit, STATA
        """
        stdout, stderr = proc.communicate(
            input=commands
        )  # Send commands and wait for completion

        if proc.returncode != 0:
            logging.error(f"Stata execution failed: {stderr}")
            raise RuntimeError(f"Something went wrong: {stderr}")
        else:
            logging.info(
                f"Stata execution completed successfully. Log file: {log_file}")

    def _execute_windows(self, dofile_path: str, log_file: str, nowtime: str, is_replace: bool = True):
        """
        Execute Stata on Windows systems

        Args:
            dofile_path: Path to do file
            log_file: Path to log file
            nowtime: Timestamp for generating temporary file names
        """
        # Windows approach - use the /e /q flags for clean batch processing
        # Create a temporary batch file
        batch_file = os.path.join(self.dofile_base_path, f"{nowtime}_batch.do")

        replace_clause = ", replace" if is_replace else ""
        try:
            with open(batch_file, "w", encoding="utf-8") as f:
                f.write(f'log using "{log_file}"{replace_clause}\n')
                f.write(f'do "{dofile_path}"\n')
                f.write("log close\n")
                f.write("exit, STATA\n")

            # Run Stata on Windows using /e /q for clean batch processing
            # /e: batch mode (execute and exit)
            # /q: quiet mode (no startup messages)
            cmd = f'"{self.STATA_CLI}" /e /q do "{batch_file}"'
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True)

            if result.returncode != 0:
                logging.error(
                    f"Stata execution failed on Windows: {result.stderr}")
                raise RuntimeError(
                    f"Windows Stata execution failed: {result.stderr}")
            else:
                logging.info(
                    f"Stata execution completed successfully on Windows. Log file: {log_file}")

        except Exception as e:
            logging.error(f"Error during Windows Stata execution: {str(e)}")
            raise
        finally:
            # Clean up temporary batch file
            if os.path.exists(batch_file):
                try:
                    os.remove(batch_file)
                    logging.debug(
                        f"Temporary batch file removed: {batch_file}")
                except Exception as e:
                    logging.warning(
                        f"Failed to remove temporary batch file "
                        f"{batch_file}: {str(e)}")

    @staticmethod
    def read_log(log_file_path, mode="r", encoding="utf-8") -> str:
        """读取Stata日志文件内容"""
        with open(log_file_path, mode, encoding=encoding) as file:
            log_content = file.read()
        return log_content
