# Configuration loader

A configuration loader plugin is responsible for loading a simulation configuration from
a user-specified source. Its interface is specified by the [`ConfigLoader`][openstb.simulator.plugin.abc.ConfigLoader]
base class.


## Entry point

Implementations of a configuration loader plugin should be registered under the
`openstb.simulator.config_loader` entry point.


## `could_handle`

A configuration loader must provide a `could_handle` method which is given the
user-specified configuration source as a string. It must return a Boolean indicating
whether it thinks it can load this source. It is intended for use in automatically
determining which of the available plugins to use to load the configuration.

Note that this method should be quick to return, for example, guess suitability based on
the file extension of the source rather than actually attempting to load it. Both false
positives (which will result in exceptions when subsequently trying to load the
configuration) and false negatives (which may result in no plugin being found) are
permissible. In these cases, the user will have to explicitly specify the name of the
configuration loader to use. Any code calling this method must be prepared to handle
these false result cases.
