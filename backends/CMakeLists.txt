cmake_minimum_required(VERSION 2.6.4)
cmake_policy(SET CMP0017 NEW)

project(grh_backends LANGUAGES C CXX)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -I${CMAKE_SOURCE_DIR}/include -fPIC -g")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Werror")

# Final tuning
include(CheckIncludeFiles)
include(CheckLibraryExists)

# EMPTY LIBRARY
add_library(grh_empty SHARED backend.h empty.c)
install(TARGETS grh_empty DESTINATION lib64)

# PHOBOS LIBRARY
find_package(PkgConfig REQUIRED)
pkg_check_modules(glib REQUIRED IMPORTED_TARGET glib-2.0)
pkg_check_modules(json REQUIRED IMPORTED_TARGET jansson)

set(CMAKE_REQUIRED_INCLUDES "${glib_INCLUDE_DIRS}")

check_include_files("phobos_store.h" HAVE_PHOBOS_STORE_H)
check_library_exists(
	phobos_store
	phobos_put
	""
	HAVE_PHOBOS_STORE
	)

if((NOT HAVE_PHOBOS_STORE) OR (NOT HAVE_PHOBOS_STORE_H))
	message(FATAL_ERROR "Cannot find Phobos store")
else()
	add_library(grh_phobos SHARED backend.h phobos.c)

	target_link_libraries(grh_phobos PkgConfig::glib PkgConfig::json phobos_store)
	install(TARGETS grh_phobos DESTINATION lib64)
endif((NOT HAVE_PHOBOS_STORE) OR (NOT HAVE_PHOBOS_STORE_H))

# HESTIA LIBRARY
check_include_files("hestia/hestia_iosea.h" HAVE_HESTIA_H LANGUAGE CXX)

if((NOT HAVE_HESTIA_H))
	message(FATAL_ERROR "Cannot find Hestia")
else()
	add_library(grh_hestia SHARED backend.h hestia.c)

	target_link_libraries(grh_hestia hestia stdc++fs)
	install(TARGETS grh_hestia DESTINATION lib64)
endif((NOT HAVE_HESTIA_H))
