# petnames example usage

# ==========================================================
# Example 1: The simple case
# ==========================================================

from petnames import get_property

# Try resolve the user-supplied value
addr1 = get_property(arg1, 'b_my_property_name')
if not addr1:
    # Couldn't resolve. Maybe they supplied the address
    addr1 = bytes.fromhex(arg1)
connect(addr1)



# ==========================================================
# Example 2: Continue if petnames is not installed
# ==========================================================

def resolve_name(name: str, prop: str) -> bytes | None:
    try:
        from petnames import get_property
    except ImportError:
        print("petnames is not installed. PetName resolving not possible")
        return None
    res = get_property(name, prop)
    if res:
        return res[0]
    return None

# Try resolve the user-supplied value
addr1 = resolve_name(arg1, 'b_my_property_name')
if not addr1:
    # Couldn't resolve. Maybe they supplied the address
    addr1 = bytes.fromhex(arg1)
connect(addr1)



