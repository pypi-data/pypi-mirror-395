from .module_loading import autodiscover_modules
from .versioned_static import VersionedStaticFiles


def cn(*args):
    """
    Combines given arguments into a single, space-separated string.
    
    This function processes various types of arguments, including strings,
    booleans, lists, and tuples, to create a clean CSS class string,
    similar to how the `clsx` library works in JavaScript.
    
    Example:
    >>> cn('flex', 'w-full', True, 'bg-red-500', False, 'rounded')
    'flex w-full bg-red-500 rounded'
    """
    class_list = []
    for item in args:
        if isinstance(item, str) and item:
            # If the item is a non-empty string, add it to the list.
            class_list = class_list + item.split(" ")
        elif isinstance(item, (list, tuple)):
            # If the item is a list or tuple, process its elements recursively.
            for sub_item in item:
                if isinstance(sub_item, str) and sub_item:
                    class_list = class_list + sub_item.split(" ")
                elif isinstance(sub_item, bool) and sub_item:
                    # Ignore a standalone True boolean inside a list/tuple.
                    continue
                
    return ' '.join(set(class_list))

def attr_to_camel(name: str) -> str:
    """Convert an attribute name to camel case.

    Args:
        name (str): The attribute name.

    Returns:
        str: The attribute name in camel case.
    """
    return " ".join(value.title() for value in name.split("_"))


def merge_props(defaults: dict, props: dict) -> dict:
    final = defaults.copy()
    if "classes" in props:
        incoming = props.pop("classes")
        current = final.get("classes", [])
        if isinstance(current, str): current = [current]
        if isinstance(incoming, str): incoming = [incoming]
        final["classes"] = current + incoming
    final.update(props)
    return final


__all__ = {
  "autodiscover_modules",
  "cn",
  "attr_to_camel",
  "merge_props"
}