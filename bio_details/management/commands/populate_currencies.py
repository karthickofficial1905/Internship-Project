from django.core.management.base import BaseCommand
from bio_details.models import Currency, Country

CURRENCIES = [
    # (code, name, currency_name, symbol, country_code)
    ('AED', 'UAE Dirham',                           'Dirham',       'د.إ',   'AE'),
    ('AFN', 'Afghan Afghani',                        'Afghani',      '؋',     'AF'),
    ('ALL', 'Albanian Lek',                          'Lek',          'L',     'AL'),
    ('AMD', 'Armenian Dram',                         'Dram',         '֏',     'AM'),
    ('ANG', 'Netherlands Antillean Guilder',         'Guilder',      'ƒ',     'AN'),
    ('AOA', 'Angolan Kwanza',                        'Kwanza',       'Kz',    'AO'),
    ('ARS', 'Argentine Peso',                        'Peso',         '$',     'AR'),
    ('AUD', 'Australian Dollar',                     'Dollar',       'A$',    'AU'),
    ('AWG', 'Aruban Florin',                         'Florin',       'ƒ',     'AW'),
    ('AZN', 'Azerbaijani Manat',                     'Manat',        '₼',     'AZ'),
    ('BAM', 'Bosnia-Herzegovina Convertible Mark',   'Mark',         'KM',    'BA'),
    ('BBD', 'Barbadian Dollar',                      'Dollar',       '$',     'BB'),
    ('BDT', 'Bangladeshi Taka',                      'Taka',         '৳',     'BD'),
    ('BGN', 'Bulgarian Lev',                         'Lev',          'лв',    'BG'),
    ('BHD', 'Bahraini Dinar',                        'Dinar',        '.د.ب',  'BH'),
    ('BIF', 'Burundian Franc',                       'Franc',        'Fr',    'BI'),
    ('BMD', 'Bermudian Dollar',                      'Dollar',       '$',     'BM'),
    ('BND', 'Brunei Dollar',                         'Dollar',       'B$',    'BN'),
    ('BOB', 'Bolivian Boliviano',                    'Boliviano',    'Bs.',   'BO'),
    ('BRL', 'Brazilian Real',                        'Real',         'R$',    'BR'),
    ('BSD', 'Bahamian Dollar',                       'Dollar',       '$',     'BS'),
    ('BTN', 'Bhutanese Ngultrum',                    'Ngultrum',     'Nu',    'BT'),
    ('BWP', 'Botswanan Pula',                        'Pula',         'P',     'BW'),
    ('BYN', 'Belarusian Ruble',                      'Ruble',        'Br',    'BY'),
    ('BZD', 'Belize Dollar',                         'Dollar',       'BZ$',   'BZ'),
    ('CAD', 'Canadian Dollar',                       'Dollar',       'C$',    'CA'),
    ('CDF', 'Congolese Franc',                       'Franc',        'Fr',    'CD'),
    ('CHF', 'Swiss Franc',                           'Franc',        'Fr',    'CH'),
    ('CLP', 'Chilean Peso',                          'Peso',         '$',     'CL'),
    ('CNY', 'Chinese Yuan',                          'Yuan',         '¥',     'CN'),
    ('COP', 'Colombian Peso',                        'Peso',         '$',     'CO'),
    ('CRC', 'Costa Rican Colon',                     'Colon',        '₡',     'CR'),
    ('CUP', 'Cuban Peso',                            'Peso',         '$',     'CU'),
    ('CVE', 'Cape Verdean Escudo',                   'Escudo',       '$',     'CV'),
    ('CZK', 'Czech Koruna',                          'Koruna',       'Kč',    'CZ'),
    ('DJF', 'Djiboutian Franc',                      'Franc',        'Fr',    'DJ'),
    ('DKK', 'Danish Krone',                          'Krone',        'kr',    'DK'),
    ('DOP', 'Dominican Peso',                        'Peso',         'RD$',   'DO'),
    ('DZD', 'Algerian Dinar',                        'Dinar',        'د.ج',   'DZ'),
    ('EGP', 'Egyptian Pound',                        'Pound',        '£',     'EG'),
    ('ERN', 'Eritrean Nakfa',                        'Nakfa',        'Nfk',   'ER'),
    ('ETB', 'Ethiopian Birr',                        'Birr',         'Br',    'ET'),
    ('EUR', 'Euro',                                  'Euro',         '€',     None),
    ('FJD', 'Fijian Dollar',                         'Dollar',       '$',     'FJ'),
    ('GBP', 'British Pound',                         'Pound',        '£',     'GB'),
    ('GEL', 'Georgian Lari',                         'Lari',         '₾',     'GE'),
    ('GHS', 'Ghanaian Cedi',                         'Cedi',         '₵',     'GH'),
    ('GMD', 'Gambian Dalasi',                        'Dalasi',       'D',     'GM'),
    ('GNF', 'Guinean Franc',                         'Franc',        'Fr',    'GN'),
    ('GTQ', 'Guatemalan Quetzal',                    'Quetzal',      'Q',     'GT'),
    ('GYD', 'Guyanese Dollar',                       'Dollar',       '$',     'GY'),
    ('HKD', 'Hong Kong Dollar',                      'Dollar',       'HK$',   'HK'),
    ('HNL', 'Honduran Lempira',                      'Lempira',      'L',     'HN'),
    ('HRK', 'Croatian Kuna',                         'Kuna',         'kn',    'HR'),
    ('HTG', 'Haitian Gourde',                        'Gourde',       'G',     'HT'),
    ('HUF', 'Hungarian Forint',                      'Forint',       'Ft',    'HU'),
    ('IDR', 'Indonesian Rupiah',                     'Rupiah',       'Rp',    'ID'),
    ('ILS', 'Israeli Shekel',                        'Shekel',       '₪',     'IL'),
    ('INR', 'Indian Rupee',                          'Rupee',        '₹',     'IN'),
    ('IQD', 'Iraqi Dinar',                           'Dinar',        'ع.د',   'IQ'),
    ('IRR', 'Iranian Rial',                          'Rial',         '﷼',     'IR'),
    ('ISK', 'Icelandic Krona',                       'Krona',        'kr',    'IS'),
    ('JMD', 'Jamaican Dollar',                       'Dollar',       'J$',    'JM'),
    ('JOD', 'Jordanian Dinar',                       'Dinar',        'د.ا',   'JO'),
    ('JPY', 'Japanese Yen',                          'Yen',          '¥',     'JP'),
    ('KES', 'Kenyan Shilling',                       'Shilling',     'KSh',   'KE'),
    ('KGS', 'Kyrgystani Som',                        'Som',          'с',     'KG'),
    ('KHR', 'Cambodian Riel',                        'Riel',         '៛',     'KH'),
    ('KMF', 'Comorian Franc',                        'Franc',        'Fr',    'KM'),
    ('KRW', 'South Korean Won',                      'Won',          '₩',     'KR'),
    ('KWD', 'Kuwaiti Dinar',                         'Dinar',        'د.ك',   'KW'),
    ('KYD', 'Cayman Islands Dollar',                 'Dollar',       '$',     'KY'),
    ('KZT', 'Kazakhstani Tenge',                     'Tenge',        '₸',     'KZ'),
    ('LAK', 'Laotian Kip',                           'Kip',          '₭',     'LA'),
    ('LBP', 'Lebanese Pound',                        'Pound',        'ل.ل',   'LB'),
    ('LKR', 'Sri Lankan Rupee',                      'Rupee',        'Rs',    'LK'),
    ('LRD', 'Liberian Dollar',                       'Dollar',       '$',     'LR'),
    ('LSL', 'Lesotho Loti',                          'Loti',         'L',     'LS'),
    ('LYD', 'Libyan Dinar',                          'Dinar',        'ل.د',   'LY'),
    ('MAD', 'Moroccan Dirham',                       'Dirham',       'د.م.',  'MA'),
    ('MDL', 'Moldovan Leu',                          'Leu',          'L',     'MD'),
    ('MGA', 'Malagasy Ariary',                       'Ariary',       'Ar',    'MG'),
    ('MKD', 'Macedonian Denar',                      'Denar',        'ден',   'MK'),
    ('MMK', 'Myanmar Kyat',                          'Kyat',         'K',     'MM'),
    ('MNT', 'Mongolian Tugrik',                      'Tugrik',       '₮',     'MN'),
    ('MOP', 'Macanese Pataca',                       'Pataca',       'P',     'MO'),
    ('MRU', 'Mauritanian Ouguiya',                   'Ouguiya',      'UM',    'MR'),
    ('MUR', 'Mauritian Rupee',                       'Rupee',        'Rs',    'MU'),
    ('MVR', 'Maldivian Rufiyaa',                     'Rufiyaa',      'Rf',    'MV'),
    ('MWK', 'Malawian Kwacha',                       'Kwacha',       'MK',    'MW'),
    ('MXN', 'Mexican Peso',                          'Peso',         '$',     'MX'),
    ('MYR', 'Malaysian Ringgit',                     'Ringgit',      'RM',    'MY'),
    ('MZN', 'Mozambican Metical',                    'Metical',      'MT',    'MZ'),
    ('NAD', 'Namibian Dollar',                       'Dollar',       '$',     'NA'),
    ('NGN', 'Nigerian Naira',                        'Naira',        '₦',     'NG'),
    ('NIO', 'Nicaraguan Cordoba',                    'Cordoba',      'C$',    'NI'),
    ('NOK', 'Norwegian Krone',                       'Krone',        'kr',    'NO'),
    ('NPR', 'Nepalese Rupee',                        'Rupee',        'Rs',    'NP'),
    ('NZD', 'New Zealand Dollar',                    'Dollar',       'NZ$',   'NZ'),
    ('OMR', 'Omani Rial',                            'Rial',         'ر.ع.',  'OM'),
    ('PAB', 'Panamanian Balboa',                     'Balboa',       'B/.',   'PA'),
    ('PEN', 'Peruvian Sol',                          'Sol',          'S/.',   'PE'),
    ('PGK', 'Papua New Guinean Kina',                'Kina',         'K',     'PG'),
    ('PHP', 'Philippine Peso',                       'Peso',         '₱',     'PH'),
    ('PKR', 'Pakistani Rupee',                       'Rupee',        'Rs',    'PK'),
    ('PLN', 'Polish Zloty',                          'Zloty',        'zł',    'PL'),
    ('PYG', 'Paraguayan Guarani',                    'Guarani',      '₲',     'PY'),
    ('QAR', 'Qatari Riyal',                          'Riyal',        'ر.ق',   'QA'),
    ('RON', 'Romanian Leu',                          'Leu',          'lei',   'RO'),
    ('RSD', 'Serbian Dinar',                         'Dinar',        'din',   'RS'),
    ('RUB', 'Russian Ruble',                         'Ruble',        '₽',     'RU'),
    ('RWF', 'Rwandan Franc',                         'Franc',        'Fr',    'RW'),
    ('SAR', 'Saudi Riyal',                           'Riyal',        'ر.س',   'SA'),
    ('SGD', 'Singapore Dollar',                      'Dollar',       'S$',    'SG'),
    ('THB', 'Thai Baht',                             'Baht',         '฿',     'TH'),
    ('TRY', 'Turkish Lira',                          'Lira',         '₺',     'TR'),
    ('USD', 'US Dollar',                             'Dollar',       '$',     'US'),
    ('ZAR', 'South African Rand',                    'Rand',         'R',     'ZA'),
]

class Command(BaseCommand):
    help = 'Populate Currency table with all world currencies'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for code, name, currency_name, symbol, country_code in CURRENCIES:
            # Try to get the country object
            try:
                country = Country.objects.get(code=country_code)
            except Country.DoesNotExist:
                country = None
                self.stdout.write(
                    self.style.WARNING(f'Country with code {country_code} not found for currency {code}')
                )

            obj, created = Currency.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'currency_name': currency_name,
                    'symbol': symbol,
                    'country': country,
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done! Created: {created_count} | Updated: {updated_count} | Total: {len(CURRENCIES)}'
        ))