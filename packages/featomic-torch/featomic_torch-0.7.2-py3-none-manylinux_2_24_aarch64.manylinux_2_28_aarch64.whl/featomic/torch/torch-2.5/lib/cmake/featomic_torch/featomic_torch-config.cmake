include(CMakeFindDependencyMacro)

# use the same version for featomic as the main CMakeLists.txt
set(REQUIRED_FEATOMIC_VERSION 0.6)
find_package(featomic ${REQUIRED_FEATOMIC_VERSION} CONFIG REQUIRED)

# use the same version for metatensor_torch as the main CMakeLists.txt
set(REQUIRED_METATENSOR_TORCH_VERSION 0.8.0)
find_package(metatensor_torch ${REQUIRED_METATENSOR_TORCH_VERSION} CONFIG REQUIRED)

# use the same version for metatomic_torch as the main CMakeLists.txt
set(REQUIRED_METATOMIC_TORCH_VERSION 0.1)
find_package(metatomic_torch ${REQUIRED_METATOMIC_TORCH_VERSION} CONFIG REQUIRED)

# We can only load metatensorfeatomic_torch with the same minor version of Torch
# that was used to compile it (and is stored in BUILD_TORCH_VERSION)
set(BUILD_TORCH_VERSION 2.5.1)
set(BUILD_TORCH_MAJOR 2)
set(BUILD_TORCH_MINOR 5)

find_package(Torch ${BUILD_TORCH_VERSION} REQUIRED)

if (NOT "${BUILD_TORCH_MAJOR}" STREQUAL "${Torch_VERSION_MAJOR}")
    message(FATAL_ERROR "found incompatible torch version: featomic-torch was built against v${BUILD_TORCH_VERSION} but we found v${Torch_VERSION}")
endif()

if (NOT "${BUILD_TORCH_MINOR}" STREQUAL "${Torch_VERSION_MINOR}")
    message(FATAL_ERROR "found incompatible torch version: featomic-torch was built against v${BUILD_TORCH_VERSION} but we found v${Torch_VERSION}")
endif()


include(${CMAKE_CURRENT_LIST_DIR}/featomic_torch-targets.cmake)
