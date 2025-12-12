
TOP              = $(_HERE_)/..

CICC_PATH        = $(TOP)/nvvm/bin
NVVMIR_LIBRARY_DIR = $(TOP)/nvvm/libdevice

PATH            += $(CICC_PATH);$(_HERE_);$(TOP)/lib;

INCLUDES        += "-I$(TOP)/include" "-I$(TOP)/include/cccl" $(_SPACE_)
SYSTEM_INCLUDES +=  $(_SPACE_)

LIBRARIES        =+ $(_SPACE_) "/LIBPATH:$(TOP)/lib/$(_WIN_PLATFORM_)"

CUDAFE_FLAGS    +=
PTXAS_FLAGS     +=
