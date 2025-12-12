set(PACKAGE_VERSION "6.2.2506-168-g9f2571191")
find_package(Netgen CONFIG REQUIRED HINTS
  ${CMAKE_CURRENT_LIST_DIR}
  ${CMAKE_CURRENT_LIST_DIR}/..
  ${CMAKE_CURRENT_LIST_DIR}/../netgen
)

get_filename_component(NGSOLVE_DIR  "${NETGEN_DIR}"  ABSOLUTE)

get_filename_component(NGSOLVE_INSTALL_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)
get_filename_component(NGSOLVE_INCLUDE_DIR  "${NETGEN_INCLUDE_DIR}"  ABSOLUTE)
get_filename_component(NGSOLVE_BINARY_DIR   "${NETGEN_BINARY_DIR}"   ABSOLUTE)
get_filename_component(NGSOLVE_LIBRARY_DIR  "${NETGEN_LIBRARY_DIR}"  ABSOLUTE)
get_filename_component(NGSOLVE_PYTHON_DIR   "${NETGEN_PYTHON_DIR}"   ABSOLUTE)
get_filename_component(NGSOLVE_RESOURCE_DIR "${NETGEN_RESOURCE_DIR}" ABSOLUTE)

set(NGSOLVE_CXX_COMPILER "/opt/rh/gcc-toolset-14/root/usr/bin/c++")
set(NGSOLVE_CMAKE_BUILD_TYPE "Release")

set(NGSOLVE_CMAKE_THREAD_LIBS_INIT "")
set(NGSOLVE_MKL_LIBRARIES "MKL::MKL")
set(NGSOLVE_PYBIND_INCLUDE_DIR "")
set(NGSOLVE_PYTHON_INCLUDE_DIRS "/opt/_internal/cpython-3.13.8/include/python3.13")
set(NGSOLVE_PYTHON_LIBRARIES "Python3_LIBRARY-NOTFOUND")
set(NGSOLVE_PYTHON_PACKAGES_INSTALL_DIR  "")
set(NGSOLVE_TCL_INCLUDE_PATH "/usr/include")
set(NGSOLVE_TCL_LIBRARY "/usr/lib64/libtclstub8.6.a")
set(NGSOLVE_TK_DND_LIBRARY "")
set(NGSOLVE_TK_INCLUDE_PATH "/usr/include")
set(NGSOLVE_TK_LIBRARY "/usr/lib64/libtkstub8.6.a")
set(NGSOLVE_X11_X11_LIB "/usr/lib64/libX11.so")
set(NGSOLVE_X11_Xmu_LIB "/usr/lib64/libXmu.so")
set(NGSOLVE_ZLIB_INCLUDE_DIRS "/builds/ngsolve/ngsolve/external_dependencies/netgen/_skbuild/linux-x86_64-3.13/cmake-build/dependencies/zlib/include")
set(NGSOLVE_ZLIB_LIBRARIES "/builds/ngsolve/ngsolve/external_dependencies/netgen/_skbuild/linux-x86_64-3.13/cmake-build/dependencies/zlib/lib/libz.a")

set(NGSOLVE_INTEL_MIC       OFF)
set(NGSOLVE_USE_CCACHE ON)
set(NGSOLVE_USE_CUDA        ON)
set(NGSOLVE_USE_GUI ON)
set(NGSOLVE_USE_LAPACK      ON)
set(NGSOLVE_USE_MKL         ON)
set(NGSOLVE_USE_MPI ON)
set(NGSOLVE_USE_MUMPS       OFF)
set(NGSOLVE_USE_NUMA        )
set(NGSOLVE_USE_PARDISO     OFF)
set(NGSOLVE_USE_PYTHON ON)
set(NGSOLVE_USE_UMFPACK     OFF)
set(NGSOLVE_USE_VT          )
set(NGSOLVE_USE_VTUNE       OFF)
set(NGSOLVE_MAX_SYS_DIM       3)

set(NGSOLVE_COMPILE_FLAGS " -DHAVE_NETGEN_SOURCES -DHAVE_DLFCN_H -DHAVE_CXA_DEMANGLE -DUSE_TIMEOFDAY -DTCL -DLAPACK -DUSE_PARDISO -DNGS_PYTHON -D_GLIBCXX_USE_CXX11_ABI=1 -DNETGEN_PYTHON -DNG_PYTHON -DPYBIND11_SIMPLE_GIL_MANAGEMENT -DPARALLEL -DNG_MPI_WRAPPER" CACHE STRING "Preprocessor definitions of ngscxx")
set(NGSOLVE_LINK_FLAGS " -L$NGSCXX_DIR/../lib/python3.13/site-packages/netgen_mesher.libs -Wl,--rpath=$NGSCXX_DIR/../lib/python3.13/site-packages/netgen_mesher.libs" CACHE STRING "Link flags set in ngsld")
set(NGSOLVE_INCLUDE_DIRS /opt/_internal/cpython-3.13.8/include;/opt/_internal/cpython-3.13.8/include/python3.13 CACHE STRING "Include dirs set in ngscxx")

set(NGSOLVE_INSTALL_DIR_PYTHON  lib/python3.13/site-packages)
set(NGSOLVE_INSTALL_DIR_BIN     bin)
set(NGSOLVE_INSTALL_DIR_LIB     lib/python3.13/site-packages/netgen_mesher.libs)
set(NGSOLVE_INSTALL_DIR_INCLUDE include/netgen)
set(NGSOLVE_INSTALL_DIR_CMAKE   lib/cmake/ngsolve)
set(NGSOLVE_INSTALL_DIR_RES     share)

include(${CMAKE_CURRENT_LIST_DIR}/ngsolve-targets.cmake)

if(WIN32)
	# Libraries like ngstd, ngbla etc. are only dummy libs on Windows (there is only one library libngsolve.dll)
	# make sure that all those dummy libs link ngsolve when used with CMake
	target_link_libraries(ngstd INTERFACE ngsolve)
endif(WIN32)

if(NGSOLVE_USE_PYTHON)
  function(add_ngsolve_python_module target)
    if(NOT CMAKE_BUILD_TYPE)
      message(STATUS "Setting build type to NGSolve build type: ${NGSOLVE_CMAKE_BUILD_TYPE}")
      set(CMAKE_BUILD_TYPE ${NGSOLVE_CMAKE_BUILD_TYPE} PARENT_SCOPE)
    endif()
    add_library(${target} SHARED ${ARGN})

    find_package(PythonInterp 3 REQUIRED)
    find_package(PythonLibs 3 REQUIRED)
    target_include_directories(${target} PRIVATE ${PYTHON_INCLUDE_DIR})

    if(NETGEN_BUILD_FOR_CONDA AND NOT WIN32)
        if(APPLE)
            target_link_options(${target} PUBLIC -undefined dynamic_lookup)
        endif(APPLE)
    else(NETGEN_BUILD_FOR_CONDA AND NOT WIN32)
        target_link_libraries(${target} PUBLIC ${PYTHON_LIBRARY})
    endif(NETGEN_BUILD_FOR_CONDA AND NOT WIN32)

    set_target_properties(${target} PROPERTIES PREFIX "" CXX_STANDARD 17)
    target_link_libraries(${target} PUBLIC ngsolve)

    if(WIN32)
      set_target_properties( ${target} PROPERTIES SUFFIX ".pyd" )
    else(WIN32)
      set_target_properties(${target} PROPERTIES SUFFIX ".so")
    endif(WIN32)

    set_target_properties(${target} PROPERTIES INSTALL_RPATH "${NGSOLVE_LIBRARY_DIR}")
endfunction()
endif(NGSOLVE_USE_PYTHON)
