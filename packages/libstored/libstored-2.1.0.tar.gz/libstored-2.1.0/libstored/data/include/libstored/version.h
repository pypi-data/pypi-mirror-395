#ifndef LIBSTORED_VERSION_H
#define LIBSTORED_VERSION_H
// SPDX-FileCopyrightText: 2020-2023 Jochem Rutgers
//
// SPDX-License-Identifier: MPL-2.0

#include <libstored/util.h>

// clang-format off
#define STORED_VERSION_MAJOR  2
#define STORED_VERSION_MINOR  1
#define STORED_VERSION_PATCH  0
#define STORED_VERSION_SUFFIX ""
#define STORED_VERSION_HASH   "3956e71bf83e0b7b9d6a1b792fadc7b4309175a6"

#define STORED_VERSION                             \
	STORED_STRINGIFY(STORED_VERSION_MAJOR)     \
	"." STORED_STRINGIFY(STORED_VERSION_MINOR) \
	"." STORED_STRINGIFY(STORED_VERSION_PATCH) \
	    STORED_VERSION_SUFFIX

#define STORED_VERSION_NUM \
	(STORED_VERSION_MAJOR * 10000L + STORED_VERSION_MINOR * 100L + STORED_VERSION_PATCH)
// clang-format on

#ifdef __cplusplus
namespace stored {
/*!
 * \brief Returns the version of libstored.
 */
constexpr char const* version() noexcept
{
	return STORED_VERSION;
}
} // namespace stored
#endif // __cplusplus
#endif // LIBSTORED_VERSION_H
