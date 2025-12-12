import subprocess
from dataclasses import dataclass

from charset_normalizer import from_bytes
from logger import Logger


@dataclass(frozen=True)
class SubprocessPopenResult:
    returncode: int  # noqa
    stdout_content: bytes | None
    stdout_text: str
    stderr_content: bytes | None
    stderr_text: str


@dataclass(frozen=True)
class SubprocessRunResult:
    result: subprocess.CompletedProcess
    stdout_content: bytes
    stdout_text: str
    stderr_content: bytes
    stderr_text: str


def _get_text(data: bytes, encoding: str | None = None) -> str:
    if encoding:
        text = data.decode(encoding)
    elif best_match := from_bytes(data).best():
        text = data.decode(best_match.encoding)
    else:
        text = str(data)
    return text


def execute_cmd_code_by_subprocess_popen(
        cmd_code: str,
        encoding: str | None = None,
        logger: Logger | None = None
) -> SubprocessPopenResult:
    """
    import execute
    import logger


    _logger = logger.get_logger(__name__)
    execute.cmd.execute_cmd_code_by_subprocess_popen("ping www.baidu.com", "cp936", _logger)

    Args:
        cmd_code:
        encoding:
        logger:

    Returns:

    """
    if logger:
        logger.debug(f"$ {cmd_code}")

    process = subprocess.Popen(
        cmd_code, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    stdout_content, stdout_text = process.stdout, str()

    for i in process.stdout:
        text = _get_text(i, encoding=encoding)
        stdout_text += text
        if text:
            if logger:
                logger.success(f"[√] {text}")

    stderr_content, stderr_text = process.stderr, str()
    for i in process.stderr:
        text = _get_text(i, encoding=encoding)
        stderr_text += text
        if text:
            if logger:
                logger.error(f"[×] {text}")

    returncode = process.wait()

    return SubprocessPopenResult(
        returncode, stdout_content, stdout_text, stderr_content, stderr_text
    )


def execute_cmd_code_by_subprocess_run(
        cmd_code: str,
        encoding: str | None = None,
        logger: Logger | None = None
) -> SubprocessRunResult:
    """
    import execute
    import logger


    _logger = logger.get_logger(__name__)
    execute.cmd.execute_cmd_code_by_subprocess_run("ping www.baidu.com", "cp936", _logger)

    Args:
        cmd_code:
        encoding:
        logger:

    Returns:

    """
    if logger:
        logger.debug(f"> {cmd_code}")

    result = subprocess.run(cmd_code, shell=True, capture_output=True)

    stdout_content, stdout_text = result.stdout, _get_text(result.stdout, encoding=encoding)
    if stdout_text:
        if logger:
            logger.success(f"[√] {stdout_text}")

    stderr_content, stderr_text = result.stderr, _get_text(result.stderr, encoding=encoding)
    if stderr_text:
        if logger:
            logger.error(f"[×] {stderr_text}")

    return SubprocessRunResult(
        result, stdout_content, stdout_text, stderr_content, stderr_text
    )
