cmake_minimum_required (VERSION 2.6)
project (instruments)

set(VERSION "0.1.4")
set(AUTHOR "Jiao Lin")
set(AUTHOR_EMAILE "jiao.lin@gmail.com")
set(VENDOR "MCViNE")
set(SUMMARY "mcvine.instruments python subpackage")
set(LICENSE "BSD")
set(RPM_APP_GROUP "Development/Tools")
set(GITHUB_URL "https://github.com/mcvine/instruments")
set (HOMEPAGE ${GITHUB_URL})

# dependencies
set (CONDA_PKGING_BUILD_DEPS "mcvine")
set (CONDA_PKGING_RUN_DEPS "mcvine")

# variables
set (PARENT_PATH "mcvine")
set (PARENT_PY_PKG "mcvine")
set (PARENT_GITHUB_URL "https://github.com/mcvine/mcvine")
set (PARENT_VERSION "1.3")
set (PARENT_RELEASE "1")
set (PKG_NAME "${PARENT_PY_PKG}.${PROJECT_NAME}")


# get cmake_utils
IF(EXISTS "cmake_utils/")
  execute_process(
    COMMAND git pull
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/cmake_utils
    )
ELSE(EXISTS "cmake_utils/")
  execute_process(
    COMMAND git clone https://github.com/danse-inelastic/cmake_utils
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
ENDIF(EXISTS "cmake_utils/")
set(CMAKE_MODULE_PATH ${PROJECT_BINARY_DIR}/cmake_utils)

# use utils
include(System) # system info
include(Dirs)   # directory structure
# set(EXPORT_ENVVARS "PYTHONPATH=${EXPORT_PYTHON}:$ENV{PYTHONPATH};LD_LIBRARY_PATH=${EXPORT_LIB}:$ENV{LD_LIBRARY_PATH};MCVINE_DIR=${EXPORT_ROOT};PATH=${EXPORT_BIN}:$ENV{PATH};EXPORT_ROOT=${EXPORT_ROOT};MCVINE_WORKFLOW=${EXPORT_ROOT}/share/workflow")
include(TestUtils)

# needs python
find_package ( PythonLibs REQUIRED )
find_package ( PythonInterp REQUIRED )
# python installation path
# set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_PY_PATH "${INSTALL_LIB_DIR}/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/site-packages")

#
enable_testing()

#
# python
file(
  COPY instruments
  DESTINATION ${EXPORT_PYTHON}/mcvine/
  FILES_MATCHING
  PATTERN "*.py"
  PATTERN "*.pml" PATTERN "*.odb"
  )


#
add_subdirectory(generic)
#
add_subdirectory(SNS)
add_subdirectory(ARCS)
add_subdirectory(SEQUOIA)
add_subdirectory(HYSPEC)
add_subdirectory(CNCS)


# install python modules 
install(DIRECTORY ${EXPORT_PYTHON}/
  DESTINATION ${INSTALL_PY_PATH}
  FILES_MATCHING
  PATTERN "*.py" PATTERN "*.so" PATTERN "*.xml"
  PATTERN "*.nxs" PATTERN "*.yml" PATTERN "*.pml" PATTERN "*.odb"
  )
# install exes
install(DIRECTORY ${EXPORT_BIN}/ DESTINATION bin 
  FILES_MATCHING
  PATTERN "*" PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
  )
# install etc
install(DIRECTORY ${EXPORT_ETC}/ DESTINATION etc)
