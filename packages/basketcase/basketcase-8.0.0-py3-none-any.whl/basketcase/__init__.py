"""
Instagram media downloader.

Usage:
::
    from basketcase import BasketCase

    with BasketCase() as bc:
        resources = bc.get('https://instagram.com/example')

        for resource in resources:
            bc.save(resource)


Other useful imports:
```python
from basketcase import User, Cookie, BasketCaseError
```
"""

from basketcase.basketcase import BasketCase
from basketcase.models import User, Cookie, BasketCaseError
