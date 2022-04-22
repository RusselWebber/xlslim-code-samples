# Examples showing how to call Excel addin functions and VBA functions from Python
# To enable the eur_conversion function you will need to install the standard Excel euroconvert addin.
# See https://support.microsoft.com/en-us/office/euroconvert-function-79c8fd67-c665-450c-bb6c-15fc92f8345c

# This global is used to store a function pointer set by xlSlim
XLSIM_UDFFUNC = None


def udf_circle_area(radius: float) -> float:
    """Calculate the area of a circle using the VBA function AreaCircle"""
    return XLSIM_UDFFUNC("AreaCircle", radius)


def eur_conversion(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert to EUR using the Excel addin function EUROCONVERT."""
    return XLSIM_UDFFUNC("EUROCONVERT", amount, from_currency, to_currency)
