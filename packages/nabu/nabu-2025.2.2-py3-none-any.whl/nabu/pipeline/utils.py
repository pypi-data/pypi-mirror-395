from ..utils import deprecated_class
from .config_validators import str2bool
from dataclasses import dataclass
import os

#
# Decorators and callback mechanism
#


def use_options(step_name, step_attr):
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            if step_name not in self.processing_steps:
                self.__setattr__(step_attr, None)
                return
            self._steps_name2component[step_name] = step_attr
            self._steps_component2name[step_attr] = step_name
            return func(*args, **kwargs)

        return wrapper

    return decorator


def pipeline_step(step_attr, step_desc):
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            if getattr(self, step_attr, None) is None:
                return
            self.logger.info(step_desc)
            res = func(*args, **kwargs)
            step_name = self._steps_component2name[step_attr]
            callbacks = self._callbacks.get(step_name, None)
            if callbacks is not None:
                for callback in callbacks:
                    callback(self)
            if self.datadump_manager is not None and step_name in self.datadump_manager.data_dump:
                self.datadump_manager.dump_data_to_file(
                    step_name, self.radios, crop_margin=not (self._radios_were_cropped)
                )
            return res

        return wrapper

    return decorator


#
# sub-region, shapes, etc
#


def get_subregion(sub_region, ndim=3):
    """
    Return a "normalized" sub-region in the form ((start_z, end_z), (start_y, end_y), (start_x, end_x)).

    Parameters
    ----------
    sub_region: tuple
        A tuple of tuples or tuple of integers.

    Notes
    -----
    The parameter "sub_region" is normally a tuple of tuples of integers.
    However it can be more convenient to use tuple of integers.
    This function will attempt at catching the different cases, but will fail if
    'sub_region' contains heterogeneous types (ex. tuples along with int)
    """
    if sub_region is None:
        res = ((None, None),)
    elif hasattr(sub_region[0], "__iter__"):
        if set(map(len, sub_region)) != {2}:
            raise ValueError("Expected each tuple to be in the form (start, end)")
        res = sub_region
    else:
        if len(sub_region) % 2:
            raise ValueError("Expected even number of elements")
        starts, ends = sub_region[::2], sub_region[1::2]
        res = tuple([(s, e) for s, e in zip(starts, ends)])
    if len(res) != ndim:
        res += ((None, None),) * (ndim - len(res))
    return res


#
# Writer - moved to pipeline.writer
#

from .writer import WriterManager

WriterConfigurator = deprecated_class("WriterConfigurator moved to nabu.pipeline.writer.WriterManager", do_print=True)(
    WriterManager
)


@dataclass
class EnvSettings:
    """This class centralises the definitions, possibly documentation, and access to environment variable
    driven settings.
    It is meant to be used in the following way:
          from nabu.utils import nabu_env_settings
          if not nabu_env_settings.skip_tomoscan_checks:
                do something
    """

    skip_tomoscan_checks: bool = False


def _get_nabu_environment_variables():
    nabu_env_settings = EnvSettings()
    nabu_env_settings.skip_tomoscan_checks = str2bool(os.getenv("SKIP_TOMOSCAN_CHECK", "0"))
    return nabu_env_settings


nabu_env_settings = _get_nabu_environment_variables()
