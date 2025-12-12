/*
 * svdep.h
 *
 * Copyright 2024 Matthew Ballance and Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may 
 * not use this file except in compliance with the License.  
 * You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software 
 * distributed under the License is distributed on an "AS IS" BASIS, 
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
 * See the License for the specific language governing permissions and 
 * limitations under the License.
 */
#ifndef SVDEP_H
#define SVDEP_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _WIN32
#define SVDEP_EXPORT __declspec(dllexport)
#else
#define SVDEP_EXPORT __attribute__((visibility("default")))
#endif

/**
 * Opaque handle to an SVDep context
 */
typedef struct svdep_s *svdep_t;

/**
 * Create a new SVDep context
 * @return A new context handle, or NULL on failure
 */
SVDEP_EXPORT svdep_t svdep_create(void);

/**
 * Destroy an SVDep context
 * @param ctx The context to destroy
 */
SVDEP_EXPORT void svdep_destroy(svdep_t ctx);

/**
 * Add an include directory to search for include files
 * @param ctx The context
 * @param path The include directory path
 * @return 0 on success, non-zero on failure
 */
SVDEP_EXPORT int svdep_add_incdir(svdep_t ctx, const char *path);

/**
 * Add a root file to process
 * @param ctx The context
 * @param path The file path
 * @return 0 on success, non-zero on failure
 */
SVDEP_EXPORT int svdep_add_root_file(svdep_t ctx, const char *path);

/**
 * Build the file collection by processing all root files
 * @param ctx The context
 * @return 0 on success, non-zero on failure
 */
SVDEP_EXPORT int svdep_build(svdep_t ctx);

/**
 * Get the JSON representation of the file collection
 * The returned string is valid until the next call to svdep_get_json 
 * or until the context is destroyed.
 * @param ctx The context
 * @return JSON string, or NULL on failure
 */
SVDEP_EXPORT const char *svdep_get_json(svdep_t ctx);

/**
 * Load a file collection from JSON
 * @param ctx The context
 * @param json The JSON string
 * @return 0 on success, non-zero on failure
 */
SVDEP_EXPORT int svdep_load_json(svdep_t ctx, const char *json);

/**
 * Check if the file collection is up to date
 * @param ctx The context with loaded JSON
 * @param last_timestamp The timestamp to check against
 * @return 1 if up to date, 0 if not, -1 on error
 */
SVDEP_EXPORT int svdep_check_up_to_date(svdep_t ctx, double last_timestamp);

/**
 * Get the last error message
 * @param ctx The context
 * @return Error message string, or NULL if no error
 */
SVDEP_EXPORT const char *svdep_get_error(svdep_t ctx);

#ifdef __cplusplus
}
#endif

#endif /* SVDEP_H */
