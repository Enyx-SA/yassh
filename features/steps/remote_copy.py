from os import path
from behave import *
import sys

from yassh import RemoteCopy, remote_copy, RemoteConfiguration


@step(u'a remote copy from "{source}" file to "{destination}" file'
      u' is created as "{name}"')
def step_impl(context, source, destination, name):
    source = path.join(context.temp_directory, source)
    destination = path.join(context.temp_directory, destination)

    c = RemoteCopy(context.reactor,
                   RemoteConfiguration(host=u'localhost'),
                   source, destination,
                   sys.stdout)

    def _on_exit(run):
        context.results[name] = c.result
    c.register_exit_monitor(_on_exit)

    context.executions[name] = c


@step(u'"{source}" is remotely copied to "{destination}" as "{name}"')
def step_impl(context, source, destination, name):
    source = path.join(context.temp_directory, source)
    destination = path.join(context.temp_directory, destination)

    context.results[name] = remote_copy(RemoteConfiguration(host=u'localhost'),
                                        source, destination,
                                        sys.stdout)
