# SPDX-FileCopyrightText: openSTB contributors
# SPDX-License-Identifier: BSD-2-Clause-Patent

from click.core import ParameterSource
from click_option_group import OptionGroup, optgroup


class LogOptionGroup(OptionGroup):
    def handle_parse_result(self, option, ctx, opts):
        option_names = set(self.get_options(ctx))
        given = option_names.intersection(opts)
        ctx.meta["openstb.log.use_default_configuration"] = len(given) == 0


def log_options():
    def _log_options(f):
        f = optgroup.option("--log-server", type=str, default=None, expose_value=False)(
            f
        )
        f = optgroup.option(
            "--log-stderr",
            type=str,
            default=None,
            callback=log_stderr_callback,
            expose_value=False,
        )(f)
        f = optgroup.group("Logging options", cls=LogOptionGroup)(f)
        return f

    return _log_options


def log_stderr_callback(ctx, param, value):
    if ctx.get_parameter_source(param.name) == ParameterSource.DEFAULT:
        if not ctx.meta["openstb.log.use_default_configuration"]:
            return
