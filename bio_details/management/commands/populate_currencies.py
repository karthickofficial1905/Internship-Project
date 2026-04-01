from django.core.management.base import BaseCommand
from bio_details.models import Currency, Country

CURRENCIES = [
    ('AED', 'UAE Dirham',                           'د.إ',   'AE'),
    ('AFN', 'Afghan Afghani',                        '؋',     'AF'),
    ('ALL', 'Albanian Lek',                          'L',     'AL'),
    ('AMD', 'Armenian Dram',                         '֏',     'AM'),
    ('ANG', 'Netherlands Antillean Guilder',         'ƒ',     'AN'),
    ('AOA', 'Angolan Kwanza',                        'Kz',    'AO'),
    ('ARS', 'Argentine Peso',                        '$',     'AR'),
    ('AUD', 'Australian Dollar',                     'A$',    'AU'),
    ('AWG', 'Aruban Florin',                         'ƒ',     'AW'),
    ('AZN', 'Azerbaijani Manat',                     '₼',     'AZ'),
    ('BAM', 'Bosnia-Herzegovina Convertible Mark',   'KM',    'BA'),
    ('BBD', 'Barbadian Dollar',                      '$',     'BB'),
    ('BDT', 'Bangladeshi Taka',                      '৳',     'BD'),
    ('BGN', 'Bulgarian Lev',                         'лв',    'BG'),
    ('BHD', 'Bahraini Dinar',                        '.د.ب',  'BH'),
    ('BIF', 'Burundian Franc',                       'Fr',    'BI'),
    ('BMD', 'Bermudian Dollar',                      '$',     'BM'),
    ('BND', 'Brunei Dollar',                         'B$',    'BN'),
    ('BOB', 'Bolivian Boliviano',                    'Bs.',   'BO'),
    ('BRL', 'Brazilian Real',                        'R$',    'BR'),
    ('BSD', 'Bahamian Dollar',                       '$',     'BS'),
    ('BTN', 'Bhutanese Ngultrum',                    'Nu',    'BT'),
    ('BWP', 'Botswanan Pula',                        'P',     'BW'),
    ('BYN', 'Belarusian Ruble',                      'Br',    'BY'),
    ('BZD', 'Belize Dollar',                         'BZ$',   'BZ'),
    ('CAD', 'Canadian Dollar',                       'C$',    'CA'),
    ('CDF', 'Congolese Franc',                       'Fr',    'CD'),
    ('CHF', 'Swiss Franc',                           'Fr',    'CH'),
    ('CLP', 'Chilean Peso',                          '$',     'CL'),
    ('CNY', 'Chinese Yuan',                          '¥',     'CN'),
    ('COP', 'Colombian Peso',                        '$',     'CO'),
    ('CRC', 'Costa Rican Colon',                     '₡',     'CR'),
    ('CUP', 'Cuban Peso',                            '$',     'CU'),
    ('CVE', 'Cape Verdean Escudo',                   '$',     'CV'),
    ('CZK', 'Czech Koruna',                          'Kč',    'CZ'),
    ('DJF', 'Djiboutian Franc',                      'Fr',    'DJ'),
    ('DKK', 'Danish Krone',                          'kr',    'DK'),
    ('DOP', 'Dominican Peso',                        'RD$',   'DO'),
    ('DZD', 'Algerian Dinar',                        'د.ج',   'DZ'),
    ('EGP', 'Egyptian Pound',                        '£',     'EG'),
    ('ERN', 'Eritrean Nakfa',                        'Nfk',   'ER'),
    ('ETB', 'Ethiopian Birr',                        'Br',    'ET'),
    ('EUR', 'Euro',                                  '€',     'EU'),
    ('FJD', 'Fijian Dollar',                         '$',     'FJ'),
    ('GBP', 'British Pound',                         '£',     'GB'),
    ('GEL', 'Georgian Lari',                         '₾',     'GE'),
    ('GHS', 'Ghanaian Cedi',                         '₵',     'GH'),
    ('GMD', 'Gambian Dalasi',                        'D',     'GM'),
    ('GNF', 'Guinean Franc',                         'Fr',    'GN'),
    ('GTQ', 'Guatemalan Quetzal',                    'Q',     'GT'),
    ('GYD', 'Guyanese Dollar',                       '$',     'GY'),
    ('HKD', 'Hong Kong Dollar',                      'HK$',   'HK'),
    ('HNL', 'Honduran Lempira',                      'L',     'HN'),
    ('HRK', 'Croatian Kuna',                         'kn',    'HR'),
    ('HTG', 'Haitian Gourde',                        'G',     'HT'),
    ('HUF', 'Hungarian Forint',                      'Ft',    'HU'),
    ('IDR', 'Indonesian Rupiah',                     'Rp',    'ID'),
    ('ILS', 'Israeli Shekel',                        '₪',     'IL'),
    ('INR', 'Indian Rupee',                          '₹',     'IN'),
    ('IQD', 'Iraqi Dinar',                           'ع.د',   'IQ'),
    ('IRR', 'Iranian Rial',                          '﷼',     'IR'),
    ('ISK', 'Icelandic Krona',                       'kr',    'IS'),
    ('JMD', 'Jamaican Dollar',                       'J$',    'JM'),
    ('JOD', 'Jordanian Dinar',                       'د.ا',   'JO'),
    ('JPY', 'Japanese Yen',                          '¥',     'JP'),
    ('KES', 'Kenyan Shilling',                       'KSh',   'KE'),
    ('KGS', 'Kyrgystani Som',                        'с',     'KG'),
    ('KHR', 'Cambodian Riel',                        '៛',     'KH'),
    ('KMF', 'Comorian Franc',                        'Fr',    'KM'),
    ('KRW', 'South Korean Won',                      '₩',     'KR'),
    ('KWD', 'Kuwaiti Dinar',                         'د.ك',   'KW'),
    ('KYD', 'Cayman Islands Dollar',                 '$',     'KY'),
    ('KZT', 'Kazakhstani Tenge',                     '₸',     'KZ'),
    ('LAK', 'Laotian Kip',                           '₭',     'LA'),
    ('LBP', 'Lebanese Pound',                        'ل.ل',   'LB'),
    ('LKR', 'Sri Lankan Rupee',                      'Rs',    'LK'),
    ('LRD', 'Liberian Dollar',                       '$',     'LR'),
    ('LSL', 'Lesotho Loti',                          'L',     'LS'),
    ('LYD', 'Libyan Dinar',                          'ل.د',   'LY'),
    ('MAD', 'Moroccan Dirham',                       'د.م.',  'MA'),
    ('MDL', 'Moldovan Leu',                          'L',     'MD'),
    ('MGA', 'Malagasy Ariary',                       'Ar',    'MG'),
    ('MKD', 'Macedonian Denar',                      'ден',   'MK'),
    ('MMK', 'Myanmar Kyat',                          'K',     'MM'),
    ('MNT', 'Mongolian Tugrik',                      '₮',     'MN'),
    ('MOP', 'Macanese Pataca',                       'P',     'MO'),
    ('MRU', 'Mauritanian Ouguiya',                   'UM',    'MR'),
    ('MUR', 'Mauritian Rupee',                       'Rs',    'MU'),
    ('MVR', 'Maldivian Rufiyaa',                     'Rf',    'MV'),
    ('MWK', 'Malawian Kwacha',                       'MK',    'MW'),
    ('MXN', 'Mexican Peso',                          '$',     'MX'),
    ('MYR', 'Malaysian Ringgit',                     'RM',    'MY'),
    ('MZN', 'Mozambican Metical',                    'MT',    'MZ'),
    ('NAD', 'Namibian Dollar',                       '$',     'NA'),
    ('NGN', 'Nigerian Naira',                        '₦',     'NG'),
    ('NIO', 'Nicaraguan Cordoba',                    'C$',    'NI'),
    ('NOK', 'Norwegian Krone',                       'kr',    'NO'),
    ('NPR', 'Nepalese Rupee',                        'Rs',    'NP'),
    ('NZD', 'New Zealand Dollar',                    'NZ$',   'NZ'),
    ('OMR', 'Omani Rial',                            'ر.ع.',  'OM'),
    ('PAB', 'Panamanian Balboa',                     'B/.',   'PA'),
    ('PEN', 'Peruvian Sol',                          'S/.',   'PE'),
    ('PGK', 'Papua New Guinean Kina',                'K',     'PG'),
    ('PHP', 'Philippine Peso',                       '₱',     'PH'),
    ('PKR', 'Pakistani Rupee',                       'Rs',    'PK'),
    ('PLN', 'Polish Zloty',                          'zł',    'PL'),
    ('PYG', 'Paraguayan Guarani',                    '₲',     'PY'),
    ('QAR', 'Qatari Riyal',                          'ر.ق',   'QA'),
    ('RON', 'Romanian Leu',                          'lei',   'RO'),
    ('RSD', 'Serbian Dinar',                         'din',   'RS'),
    ('RUB', 'Russian Ruble',                         '₽',     'RU'),
    ('RWF', 'Rwandan Franc',                         'Fr',    'RW'),
    ('SAR', 'Saudi Riyal',                           'ر.س',   'SA'),
    ('SGD', 'Singapore Dollar',                      'S$',    'SG'),
    ('THB', 'Thai Baht',                             '฿',     'TH'),
    ('TRY', 'Turkish Lira',                          '₺',     'TR'),
    ('USD', 'US Dollar',                             '$',     'US'),
    ('ZAR', 'South African Rand',                    'R',     'ZA'),
]

class Command(BaseCommand):
    help = 'Populate Currency table with all world currencies'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for code, name, symbol, country_code in CURRENCIES:
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