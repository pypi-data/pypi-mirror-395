import subprocess
from typing import Any

import execjs
import orjson
import py_mini_racer


def _get_js_code(
        js_code: str | None = None,
        js_file_path: str | None = None
) -> str:
    if js_code is None and js_file_path is None:
        raise ValueError(
            f"Either js_code: {js_code!r} or js_file_path: {js_file_path!r} must be provided"
        )
    if js_code is not None:
        return js_code
    if js_file_path is not None:
        with open(js_file_path, "r", encoding="utf-8") as f:
            js_code = f.read()
    return js_code


def execute_javascript_by_execjs(
        js_code: str | None = None,
        js_file_path: str | None = None,
        func_name: str | None = None,
        func_args: tuple[Any, ...] | None = None
) -> Any:
    """
    import execute


    # language=javascript
    js_code = '''
              function sdk () {
                let sum = 0;
                for (const n of arguments) {
                  if (typeof n === "number") sum += n;
                }
                return sum;
              } \
              '''
    result = execute.js.execute_javascript_by_execjs(js_code, func_name="sdk", func_args=(1, 2, "3"))
    print(result)

    Args:
        js_code:
        js_file_path:
        func_name:
        func_args:

    Returns:

    """
    js_code = _get_js_code(js_code, js_file_path)

    ctx = execjs.compile(js_code)
    if func_name is None:
        result = ctx.eval(js_code)
        return result
    if func_args is None:
        func_args = tuple()
    result = ctx.call(func_name, *func_args)
    return result


def execute_javascript_by_py_mini_racer(
        js_code: str | None = None,
        js_file_path: str | None = None,
        func_name: str | None = None,
        func_args: tuple[Any, ...] | None = None
) -> Any:
    """
    import execute


    # language=javascript
    js_code = '''
              function sdk () {
                let sum = 0;
                for (const n of arguments) {
                  if (typeof n === "number") sum += n;
                }
                return sum;
              } \
              '''
    result = execute.js.execute_javascript_by_py_mini_racer(js_code, func_name="sdk", func_args=(1, 2, "3"))
    print(result)

    Args:
        js_code:
        js_file_path:
        func_name:
        func_args:

    Returns:

    """
    js_code = _get_js_code(js_code, js_file_path)

    ctx = py_mini_racer.MiniRacer()
    result = ctx.eval(js_code)
    if func_name is None:
        return result
    if func_args is None:
        func_args = tuple()
    result = ctx.call(func_name, *func_args)
    return result


def execute_javascript_by_subprocess(
        js_code: str | None = None,
        js_file_path: str | None = None,
        arguments: tuple[Any, ...] | None = None,
) -> Any:
    """
    import execute


    # language=javascript
    js_code = '''(function () {
      arguments = process.argv.slice(1).map(JSON.parse);
      let sum = 0;
      for (const n of arguments) {
        if (typeof n === "number") sum += n;
      }
      console.log(JSON.stringify({ "sum": sum }));
    })();'''

    result = execute.js.execute_javascript_by_subprocess(js_code, arguments=(1, 2, "3",))
    print(result["sum"])

    Args:
        js_code:
        js_file_path:
        arguments:

    Returns:

    """
    js_code = _get_js_code(js_code, js_file_path)

    args = ["node", "-e", js_code] + list(map(lambda x: orjson.dumps(x).decode(), arguments))
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    result = stdout.decode()
    result = orjson.loads(result)
    return result
