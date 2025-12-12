#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "featomic_torch" for configuration "Release"
set_property(TARGET featomic_torch APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(featomic_torch PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/featomic_torch.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/featomic_torch.dll"
  )

list(APPEND _cmake_import_check_targets featomic_torch )
list(APPEND _cmake_import_check_files_for_featomic_torch "${_IMPORT_PREFIX}/lib/featomic_torch.lib" "${_IMPORT_PREFIX}/bin/featomic_torch.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
