import _string
import string
from typing import Sequence, Any, Mapping


class PartialFormatter(string.Formatter):

    def get_field(self, field_name: str, args: Sequence[Any], kwargs: Mapping[str, Any]) -> Any:

        first, rest = _string.formatter_field_name_split(field_name.strip())

        if (isinstance(first, int) and first < len(args)) or first in kwargs:
            obj = self.get_value(first, args, kwargs)

            # loop through the rest of the field_name, doing
            #  getattr or getitem as needed
            for is_attr, i in rest:
                if is_attr:
                    if '(' in i:
                        fct, args = i.split('(')
                        fct = getattr(obj, fct)
                        obj = fct(args.strip("\")'"))
                    else:
                        obj = getattr(obj, i)
                else:
                    obj = obj[i]

            return obj, first
        else:
            return "{" + field_name + "}", field_name

