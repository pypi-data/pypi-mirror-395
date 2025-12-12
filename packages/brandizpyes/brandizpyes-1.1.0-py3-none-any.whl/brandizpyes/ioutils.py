from typing import TextIO
from io import StringIO

from typing import Callable

def dump_output ( writer: Callable [ TextIO, str | None], out_path: str | TextIO | None = None , mode = "w", **open_opts ) -> str | None:
	"""
	Utility to quickly deal with a writer that writes on a file handle.

	Args:
		writer (Callable [ TextIO, str | None]): A function that takes a file-like object as its only argument and writes to it.

		out_path (str | TextIO | None): If this is a string, the function will open a file against the given path and
		will pass the corresponding file handle to the `writer` function. 
		Else, if it's a file-like object, it will be passed as is to the `writer` function.
		If it's null, a :class:`StringIO` buffer will be used and its content returned as a string.

		mode: The mode to open the file if `out_path` is a string, ie, the argument is passed to :fun:`open()`.
		
		open_opts: Additional options passed to :fun:`open()`.

	Returns:
		str | None: If `out_path` is None, the function returns the content written to a StringIO.
		
	"""
	if isinstance ( out_path, str ):
		with open ( out_path, mode, **open_opts ) as fh:
			writer ( fh )
		return None
	
	if out_path is None:
		output = StringIO()
		writer ( output )
		return output.getvalue()
	
	# Else, assume it's a file-like object and pass it down
	writer ( out_path )
	return None
