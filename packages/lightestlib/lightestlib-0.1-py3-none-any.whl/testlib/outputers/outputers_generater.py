"""
A abandoned file, waiting for refactor
"""


def _io_outputers(s: str):
    try:
        print(s)
        return True
    except Exception as e:
        print(e)
        return False


def _get_file_outputers(path: str = "./test.log"):
    def _file_outputers(s: str):
        try:
            with open(path, "a") as f:
                f.write(s + "\n")
            return True
        except Exception as e:
            print(e)
            return False

    return _file_outputers


def _get_io_file_outputers(path: str = "./test.log"):
    _file_outputers = _get_file_outputers(path)

    def _io_file_outputers(s: str):
        r1 = _io_outputers(s)
        r2 = _file_outputers(s)
        return r1 and r2

    return _io_file_outputers


def get_outputers(style: str = "io", path: str = "./test.log"):
    match style:
        case "io":
            return _io_outputers
        case "file":
            return _get_file_outputers(path)
        case "io_file":
            return _get_io_file_outputers(path)
        case _:
            raise ValueError("style must be io, file or io_file")
