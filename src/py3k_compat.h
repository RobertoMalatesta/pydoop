/* BEGIN_COPYRIGHT
 *
 * Copyright 2009-2017 CRS4.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy
 * of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *
 * END_COPYRIGHT
 */

#ifndef PY3K_COMPAT_H
#define PY3K_COMPAT_H

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K 1
#endif

#include "buf_macros.h"
#include "Py_macros.h"

#endif 
