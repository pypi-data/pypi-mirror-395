# -*- coding: utf-8 -*-
# __init__.py

import pint

__version__ = "0.5.4"

ureg = pint.UnitRegistry(auto_reduce_dimensions=True)
ureg.define(r"percent = 0.01 = %")
ureg.define(r"item = 1")


def currency(name, symbol, aliases):
    ureg.define(
        pint.facets.plain.UnitDefinition(
            name,
            symbol,
            aliases,
            pint.facets.plain.ScaleConverter(1),
            # a separate dimension for each currency, forces exchange rates between them
            pint.util.UnitsContainer({f"[currency_{name}]": 1}),
        )
    )


currency("USD", "$", ("Dollar", "dollar", "usd"))
currency("JPY", "¥", ("Yen", "yen"))
currency("EUR", "€", ("Euro", "euro", "Eur", "eur"))

# set the exchange rates as of 23 Apr.3
ureg.define("EUR = 1.09 USD")
ureg.define("JPY = .0075 USD")
