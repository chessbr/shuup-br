# Shoop-BR
A Shoop add-on for custom Brazilian e-commerce

## Installation (development)

1. Download the latest release as a zip and extract anywhere.
2. Copy the `shoop_br` and `shoop_br_tests` folders and paste them into your Shoop root folder.
3. Configure, test and run!

PS: As the custom user model uses email as the `username` field, when you load Shoop mocks though `shoop_populate_mock` 
management command, remember that the default login is now `USERNAME@shoop.local` (an email) to enter in the admin panel.  

## Configuration

1. In your `settings.py`:

  1.1 Add `shoop_br` to the `INSTALLED_APPS` config before any Shoop module.
  ```
  INSTALLED_APPS = add_enabled_addons(SHOOP_ENABLED_ADDONS_FILE, [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
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

## Execution

Migrate and run as usual and be happy! :)

## Tests

TODO

## Deployment

TODO

## Copyright
Copyright (C) 2016 by [Rockho Team](https://github.com/rockho-team)

## License

Shoop-BR is published under the GNU Affero General Public License,
version 3 (AGPLv3). See the LICENSE file.
