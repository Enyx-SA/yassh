from behave import *
import sys

from yassh import RemoteRun, remote_run


def _table_to_options(table):
    return dict([(a['option'], a['value']) for a in table or []])

def _get_logfile(context):
    options = _table_to_options(context.table)

    output = options.get('output', None)
    if output:
        return context.out_buffers.get(output)

    return sys.stdout


@step(u'a remote run "{command}" is created as "{name}"')
def step_impl(context, command, name):
    logfile = _get_logfile(context)

    c = RemoteRun(context.reactor,
                 'localhost', 'login', command,
                 logfile=logfile)

    def on_exit(): context.results[name] = c.result
    c.register_exit_monitor(on_exit)

    context.executions[name] = c


@step(u'"{execution}" is remotely run as "{name}"')
def step_impl(context, execution, name):
    context.results[name] = remote_run('localhost', 'login', execution, sys.stdout)
