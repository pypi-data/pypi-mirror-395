import logging, logging.config
import os
from sys import stderr
import yaml

# TODO: support the rich library components, to get coloured output
# see https://chatgpt.com/share/68de70b6-2904-800d-a57a-54ede673f531
# 

def logger_config ( 
	logger_name: str = None,
	cfg_path: str = None, 
	disable_existing_loggers: bool = False,
	use_unsafe_loader: bool = False
) -> logging.Logger | None:
	"""
	Configures the Python logging module with a YAML configuration file.
	
	The file name is picked, in order: from cfg_path if provided, from the environment variable 
	PYES_LOG_CONF, from <current directory>/logging-test.yml or <current directory>/logging.yml.
	If none of these files exists, a [default configuration file](logging-default.yml) 
	included in this package is used.

	This should be called at the begin of an application and BEFORE any use of the logging module.
	Multiple calls of this method are idempotent, ie, the Python logging module configures itself
	once only (and only before sending in logging messages).
	
	An example of logging config file is included in the package test files.
	
	If logger_name is provided, the function returns logging.getLogger ( logger_name ) as a facility
	to avoid the need to import logging too, when you already import this. Beware that you load a configuration
	one only in your application (so, don't use this method in modules just to get a logger). 
	
	:param disable_existing_loggers: is false by default, this is the best way to not interfere with modules instantiating
	their own module logger, usually before you call this function on top of your application (but usually after 
	all the imports). By default, the Python logging library has this option set to true and that typically causes
	all the module loggers to be disabled after the configuration loading. See https://docs.python.org/3/library/logging.config.html

	:param use_unsafe_loader: if true, uses yaml.UnsafeLoader to load the configuration file. 
	This is useful when you want to do things like calling functions in the configuration file 
	(see logging-explicitly-loaded.yml in the tests). However, it's False by default, since this behaviour is
	unsafe (see Python documentation).
	"""

	if not cfg_path:
		for probed_path in ( os.getenv ( "PYES_LOG_CONF_PATH", "logging-test.yml" ), "logging.yml" ):
			cfg_path = probed_path
			if os.path.isfile ( probed_path ): break

	if not os.path.isfile ( cfg_path ):
		print ( f"*** Logger config file '{cfg_path}' not found, use the OS variable PYES_LOG_CONF_PATH to point to a logging configuration.", file = stderr )
		print ( "The logger will use a default configuration ", file = stderr )
		cfg_path = os.path.join ( os.path.dirname ( __file__ ), "logging-default.yml" )

	loader = yaml.UnsafeLoader if use_unsafe_loader else yaml.FullLoader

	with open ( cfg_path ) as flog:		
		cfg = yaml.load ( flog, Loader = loader )
		# As per documentation, if not reset, this disables loggers in the modules, which usually are 
		# loaded during 'import', before calling this function
		cfg [ "disable_existing_loggers" ] = disable_existing_loggers
		logging.config.dictConfig ( cfg )
	log = logging.getLogger ( __name__ )
	log.info ( "Logger configuration loaded from '%s'" % cfg_path )

	if logger_name: return logging.getLogger ( logger_name )
	