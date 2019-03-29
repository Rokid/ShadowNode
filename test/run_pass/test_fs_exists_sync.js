/* Copyright 2016-present Samsung Electronics Co., Ltd. and other contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
'use strict';

var fs = require('fs');
var assert = require('assert');

{
  var filePath = process.cwd() + '/resources/tobeornottobe.txt';

  var result = fs.existsSync(filePath);
  assert.strictEqual(result, true, 'File should exist: ' + filePath);
}

{
  filePath = process.cwd() + '/resources/empty.txt';

  result = fs.existsSync(filePath);
  assert.strictEqual(result, false, 'File should not exist: ' + filePath);
}

{
  filePath = '';

  result = fs.existsSync(filePath);
  assert.strictEqual(result, false, 'File with empty should not exist');
}

{
  filePath = ' ';

  result = fs.existsSync(filePath);
  assert.strictEqual(result, false, 'File name with single whitespace check');
}
