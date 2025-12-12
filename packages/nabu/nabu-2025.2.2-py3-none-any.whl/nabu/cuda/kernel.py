from os import linesep
import numpy as np
from cupy import RawModule
from ..processing.kernel_base import KernelBase
from ..utils import catch_warnings  # TODO use warnings.catch_warnings once python < 3.11 is dropped


class CudaKernel(KernelBase):
    """
    Helper class that wraps CUDA kernel through cupy SourceModule.

    Parameters
    -----------
    kernel_name: str
        Name of the CUDA kernel.
    filename: str, optional
        Path to the file name containing kernels definitions
    src: str, optional
        Source code of kernels definitions
    automation_params: dict, optional
        Automation parameters, see below
    sourcemodule_kwargs: optional
        Extra arguments to provide to cupy.RawModule(),

    """

    def __init__(
        self,
        kernel_name,
        filename=None,
        src=None,
        automation_params=None,
        silent_compilation_warnings=False,
        extern_c=True,
        **sourcemodule_kwargs,
    ):
        super().__init__(
            kernel_name,
            filename=filename,
            src=src,
            automation_params=automation_params,
            silent_compilation_warnings=silent_compilation_warnings,
        )

        if extern_c:
            # pycuda/pyopencl do that automatically, not cupy
            self.src = patch_sourcecode_add_externC(self.src, filename=filename)
        self.compile_kernel_source(kernel_name, sourcemodule_kwargs)

    def compile_kernel_source(self, kernel_name, sourcemodule_kwargs):
        self.sourcemodule_kwargs = sourcemodule_kwargs
        # Use NVCC by default
        if self.sourcemodule_kwargs.get("backend", None) is None:
            self.sourcemodule_kwargs["backend"] = "nvcc"
        #
        self.kernel_name = kernel_name
        with catch_warnings(action=("ignore" if self.silent_compilation_warnings else None)):  # pylint: disable=E1123
            self.module = RawModule(code=self.src, **self.sourcemodule_kwargs)
            self.module.compile()
        self.func = self.module.get_function(kernel_name)

    def follow_device_arr(self, args):
        return args

    def call(self, *args, **kwargs):
        grid, block, args, kwargs = self._prepare_call(*args, **kwargs)
        self.func(grid, block, args)

    __call__ = call


def patch_sourcecode_add_externC(src_code, filename=None):
    """
    Patch a source code to surround the relevant parts with 'extern C {}' directive
    The NVCC compiler needs this to avoid name mangling.
    """
    lines = src_code.split(linesep)
    incl_idx = []
    incl_idx_nows = []

    i = 0
    for i0, line in enumerate(lines):
        line = line.strip()
        if line.startswith(("//", "/*")):
            continue
        if line.startswith("#include"):
            incl_idx.append(i0)
            incl_idx_nows.append(i)
            i += 1
    if len(incl_idx) == 0:
        insertion_idx = 0
    else:
        if np.any(np.diff(incl_idx_nows) > 1):
            raise ValueError(
                f"'#include' should be grouped on top of the file, not separated by anything else - found #include at lines {incl_idx} in file {filename}"
            )
        else:
            insertion_idx = incl_idx[-1] + 1
    lines.insert(insertion_idx, 'extern "C" {')
    lines.append("}")
    modified_src = linesep.join(lines)
    return modified_src
