from __future__ import annotations

from wexample_helpers.const.types import BasicValue, StringKeysDict

# Can't define key list as it can ben dynamic when using more options.
# We may use the future __extra_items__ flag in python 3.13.
# We can still be confident to the internal config check process.
DictConfig = StringKeysDict
DictConfigValue = BasicValue
