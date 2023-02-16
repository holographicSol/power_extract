""" Written by Benjamin Jack Cullen """

import handler_chunk
import asyncio
import handler_strings
import handler_file
import scanfs
import handler_extraction_method
import aiomultiprocess
import multiprocessing
import sys
import variable_paths


async def entry_point_power_extract(chunk: list, **kwargs) -> list:
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _program_root = str(kwargs.get('program_root'))

    return [await power_extract(item, _buffer_max, _target, _program_root) for item in chunk]


async def power_extract(file: str, _buffer_max: int, _target: str, _program_root: str) -> list:
    _result = []
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        _result = await extract_power_extract(_buffer=buffer, _file=file, _buffer_max=_buffer_max, _target=_target,
                                              _program_root=_program_root)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def extract_power_extract(_buffer: bytes, _file: str, _buffer_max: int, _target: str, _program_root: str) -> list:
    _results = []
    m = await asyncio.to_thread(handler_file.get_m_time, _file)
    s = await asyncio.to_thread(handler_file.get_size, _file)
    _results = [[m, _buffer, s, _file]]
    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    result_bool, extraction = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    # await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results


async def main(_chunks: list, _multiproc_dict: dict):
    async with aiomultiprocess.Pool() as pool:
        _results = await pool.map(entry_point_power_extract, _chunks, _multiproc_dict)
    return _results


if __name__ == '__main__':

    # used for compile time
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    # get input
    STDIN = list(sys.argv)

    target = STDIN[1]

    program_root = variable_paths.program_root

    multiproc_dict = {'buffer_max': 2048,
                      'target': target,
                      'program_root': program_root}

    files, x_files, pre_scan_time = scanfs.pre_scan_handler(_target=target, _verbose=False)

    # chunk data ready for async multiprocess
    chunks = handler_chunk.chunk_data(files, 16)

    results = asyncio.run(main(chunks, multiproc_dict))
