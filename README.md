[![Build Status](https://travis-ci.org/rockho-team/shoop-br.svg?branch=master)](https://travis-ci.org/rockho-team/shoop-br)
[![Coverage Status](https://coveralls.io/repos/github/rockho-team/shoop-br/badge.svg?branch=master)](https://coveralls.io/github/rockho-team/shoop-br?branch=master)
[![License](https://img.shields.io/badge/license-AGPLv3-blue.svg)](LICENSE)

Shoop-BR
========

A Shoop add-on for custom Brazilian e-commerces

This module adds the following features to your Shoop:

* New customer/order address fields: *número*, *ponto de referência* and *celular*
* Custom `AUTH_USER_MODEL` without `username` field (only `email` and `password` are used)
* Additional information of brazilian customers like *CPF*, *RG*, *CNPJ*, *IE* (see [`models.py`](shoop_br/models.py) for more details)
* Customized user registration view to consider the custom `AUTH_USER_MODEL` and the additional user information
* Custom `AddressCheckoutPhase` to consider brazilian extra address`s fields
* Custom `AddressCheckoutPhase` template that automatically fills the address fields from a brazilian postal code through [ViaCEP](http://viacep.com.br) webservices
* Custom `BasketOrderCreator` to consider extra address informations
* Custom `CheckoutView` that forces user registration before checking out

## Compatibility
* Shuup v4.0.0
* [Tested on Python 2.7, 3.4 and 3.5](https://travis-ci.org/rockho-team/shoop-br)


Configuration
=============

1. In your `settings.py`:

  1.1 Add `shoop_br` to the `INSTALLED_APPS` config before any Shoop module.
  This is because *Shoop BR* overrides registration URLs as yoy can [see here](shoop_br/urls.py).

  ```
  INSTALLED_APPS = add_enabled_addons(SHOOP_ENABLED_ADDONS_FILE, [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    
    # Shoop BR
    'shoop_br',
    
    # shoop themes
    'shoop.themes.classic_gray',
    # shoop
    'shoop.addons',
    ...
  ```

  1.2 Set these configs:

  ```
  AUTH_USER_MODEL = 'shoop_br.ShoopBRUser'
  SHOOP_CHECKOUT_VIEW_SPEC = "shoop_br.views:ShoopBRCheckoutView"
  SHOOP_BASKET_ORDER_CREATOR_SPEC = "shoop_br.checkout.order_creator:ShoopBRBasketOrderCreator"
  SHOOP_HOME_CURRENCY = 'R$'
  PARLER_DEFAULT_LANGUAGE_CODE = 'pt-br'
  SHOOP_ALLOW_ANONYMOUS_ORDERS = False
  SHOOP_ADDRESS_HOME_COUNTRY = 'BR'
  SHOOP_REGISTRATION_REQUIRES_ACTIVATION = False
  ```

  **Tip**: Disable all unnecessary languages, except `pt_br`.
  The registration form has a birth date field which needs
  dates in the format `dd/mm/yyyy` (the Brazilian standard). To remove any other language,
  just replace `LANGUAGES` config in `settings.py` with this:
  ```
  LANGUAGES = [
    ('pt-br', 'Portuguese (Brazil)'),
  ]
  ```
  and *vualá*.

Tests
=====

Create your virtualenv and install Shoop and all its requirements. After that,
install `shoop-br` and run `py.test shoop_br_tests`.

Copyright
=========
Copyright (C) 2016 by [Rockho Team](https://github.com/rockho-team)

License
=======
Shoop-BR is published under the GNU Affero General Public License,
version 3 (AGPLv3). See the LICENSE file.
