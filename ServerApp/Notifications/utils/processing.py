def _match_filter(self, filter_item, item):
    for key, value in filter_item.items():
        field, operation = key.split("_", 1)

        if field not in item:
            return False

        try:
            item_value = float(item[field])
        except ValueError:
            return False

        if operation == "$in":
            return value in item[field]
        elif operation == "$eq":
            return item[field] == value
        elif operation == "$gt":
            return item_value > float(value)
        elif operation == "$lt":
            return item_value < float(value)
        elif operation == "$btw":
            if isinstance(value, list) and len(value) == 2:
                lower_bound, upper_bound = value
                try:
                    return float(lower_bound) <= item_value <= float(upper_bound)
                except ValueError:
                    return False
            else:
                self.warnings.append({
                    "message": f"Invalid value for $btw. Expected a list of two numbers, got: {value}",
                    "field": field
                })
                return False
        else:
            print(f"Operation {operation} is not supported")
            warning = {
                "message": f"Operation {operation} is not supported",
                "field": field
            }
            if warning not in self.warnings:
                self.warnings.append(warning)
            return True

    return True
