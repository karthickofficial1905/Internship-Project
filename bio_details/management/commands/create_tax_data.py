from django.core.management.base import BaseCommand
from bio_details.models import Country, Tax, Currency

class Command(BaseCommand):
    help = 'Create sample country and tax data'

    def handle(self, *args, **options):
        # Create Countries
        countries_data = [
                # Asia
                {'code': 'AF', 'name': 'Afghanistan'},
                {'code': 'AM', 'name': 'Armenia'},
                {'code': 'AZ', 'name': 'Azerbaijan'},
                {'code': 'BH', 'name': 'Bahrain'},
                {'code': 'BD', 'name': 'Bangladesh'},
                {'code': 'BT', 'name': 'Bhutan'},
                {'code': 'BN', 'name': 'Brunei'},
                {'code': 'KH', 'name': 'Cambodia'},
                {'code': 'CN', 'name': 'China'},
                {'code': 'CY', 'name': 'Cyprus'},
                {'code': 'GE', 'name': 'Georgia'},
                {'code': 'IN', 'name': 'India'},
                {'code': 'ID', 'name': 'Indonesia'},
                {'code': 'IR', 'name': 'Iran'},
                {'code': 'IQ', 'name': 'Iraq'},
                {'code': 'IL', 'name': 'Israel'},
                {'code': 'JP', 'name': 'Japan'},
                {'code': 'JO', 'name': 'Jordan'},
                {'code': 'KZ', 'name': 'Kazakhstan'},
                {'code': 'KW', 'name': 'Kuwait'},
                {'code': 'KG', 'name': 'Kyrgyzstan'},
                {'code': 'LA', 'name': 'Laos'},
                {'code': 'LB', 'name': 'Lebanon'},
                {'code': 'MY', 'name': 'Malaysia'},
                {'code': 'MV', 'name': 'Maldives'},
                {'code': 'MN', 'name': 'Mongolia'},
                {'code': 'MM', 'name': 'Myanmar'},
                {'code': 'NP', 'name': 'Nepal'},
                {'code': 'KP', 'name': 'North Korea'},
                {'code': 'OM', 'name': 'Oman'},
                {'code': 'PK', 'name': 'Pakistan'},
                {'code': 'PS', 'name': 'Palestine'},
                {'code': 'PH', 'name': 'Philippines'},
                {'code': 'QA', 'name': 'Qatar'},
                {'code': 'SA', 'name': 'Saudi Arabia'},
                {'code': 'SG', 'name': 'Singapore'},
                {'code': 'KR', 'name': 'South Korea'},
                {'code': 'LK', 'name': 'Sri Lanka'},
                {'code': 'SY', 'name': 'Syria'},
                {'code': 'TW', 'name': 'Taiwan'},
                {'code': 'TJ', 'name': 'Tajikistan'},
                {'code': 'TH', 'name': 'Thailand'},
                {'code': 'TL', 'name': 'Timor-Leste'},
                {'code': 'TR', 'name': 'Turkey'},
                {'code': 'TM', 'name': 'Turkmenistan'},
                {'code': 'AE', 'name': 'United Arab Emirates'},
                {'code': 'UZ', 'name': 'Uzbekistan'},
                {'code': 'VN', 'name': 'Vietnam'},
                {'code': 'YE', 'name': 'Yemen'},

                # Europe
                {'code': 'AL', 'name': 'Albania'},
                {'code': 'AD', 'name': 'Andorra'},
                {'code': 'AT', 'name': 'Austria'},
                {'code': 'BY', 'name': 'Belarus'},
                {'code': 'BE', 'name': 'Belgium'},
                {'code': 'BA', 'name': 'Bosnia and Herzegovina'},
                {'code': 'BG', 'name': 'Bulgaria'},
                {'code': 'HR', 'name': 'Croatia'},
                {'code': 'CZ', 'name': 'Czech Republic'},
                {'code': 'DK', 'name': 'Denmark'},
                {'code': 'EE', 'name': 'Estonia'},
                {'code': 'FI', 'name': 'Finland'},
                {'code': 'FR', 'name': 'France'},
                {'code': 'DE', 'name': 'Germany'},
                {'code': 'GR', 'name': 'Greece'},
                {'code': 'HU', 'name': 'Hungary'},
                {'code': 'IS', 'name': 'Iceland'},
                {'code': 'IE', 'name': 'Ireland'},
                {'code': 'IT', 'name': 'Italy'},
                {'code': 'XK', 'name': 'Kosovo'},
                {'code': 'LV', 'name': 'Latvia'},
                {'code': 'LI', 'name': 'Liechtenstein'},
                {'code': 'LT', 'name': 'Lithuania'},
                {'code': 'LU', 'name': 'Luxembourg'},
                {'code': 'MT', 'name': 'Malta'},
                {'code': 'MD', 'name': 'Moldova'},
                {'code': 'MC', 'name': 'Monaco'},
                {'code': 'ME', 'name': 'Montenegro'},
                {'code': 'NL', 'name': 'Netherlands'},
                {'code': 'MK', 'name': 'North Macedonia'},
                {'code': 'NO', 'name': 'Norway'},
                {'code': 'PL', 'name': 'Poland'},
                {'code': 'PT', 'name': 'Portugal'},
                {'code': 'RO', 'name': 'Romania'},
                {'code': 'RU', 'name': 'Russia'},
                {'code': 'SM', 'name': 'San Marino'},
                {'code': 'RS', 'name': 'Serbia'},
                {'code': 'SK', 'name': 'Slovakia'},
                {'code': 'SI', 'name': 'Slovenia'},
                {'code': 'ES', 'name': 'Spain'},
                {'code': 'SE', 'name': 'Sweden'},
                {'code': 'CH', 'name': 'Switzerland'},
                {'code': 'UA', 'name': 'Ukraine'},
                {'code': 'GB', 'name': 'United Kingdom'},
                {'code': 'VA', 'name': 'Vatican City'},

                # Africa
                {'code': 'DZ', 'name': 'Algeria'},
                {'code': 'AO', 'name': 'Angola'},
                {'code': 'BJ', 'name': 'Benin'},
                {'code': 'BW', 'name': 'Botswana'},
                {'code': 'BF', 'name': 'Burkina Faso'},
                {'code': 'BI', 'name': 'Burundi'},
                {'code': 'CV', 'name': 'Cabo Verde'},
                {'code': 'CM', 'name': 'Cameroon'},
                {'code': 'CF', 'name': 'Central African Republic'},
                {'code': 'TD', 'name': 'Chad'},
                {'code': 'KM', 'name': 'Comoros'},
                {'code': 'CG', 'name': 'Congo'},
                {'code': 'CD', 'name': 'DR Congo'},
                {'code': 'DJ', 'name': 'Djibouti'},
                {'code': 'EG', 'name': 'Egypt'},
                {'code': 'GQ', 'name': 'Equatorial Guinea'},
                {'code': 'ER', 'name': 'Eritrea'},
                {'code': 'SZ', 'name': 'Eswatini'},
                {'code': 'ET', 'name': 'Ethiopia'},
                {'code': 'GA', 'name': 'Gabon'},
                {'code': 'GM', 'name': 'Gambia'},
                {'code': 'GH', 'name': 'Ghana'},
                {'code': 'GN', 'name': 'Guinea'},
                {'code': 'GW', 'name': 'Guinea-Bissau'},
                {'code': 'CI', 'name': "Ivory Coast"},
                {'code': 'KE', 'name': 'Kenya'},
                {'code': 'LS', 'name': 'Lesotho'},
                {'code': 'LR', 'name': 'Liberia'},
                {'code': 'LY', 'name': 'Libya'},
                {'code': 'MG', 'name': 'Madagascar'},
                {'code': 'MW', 'name': 'Malawi'},
                {'code': 'ML', 'name': 'Mali'},
                {'code': 'MR', 'name': 'Mauritania'},
                {'code': 'MU', 'name': 'Mauritius'},
                {'code': 'MA', 'name': 'Morocco'},
                {'code': 'MZ', 'name': 'Mozambique'},
                {'code': 'NA', 'name': 'Namibia'},
                {'code': 'NE', 'name': 'Niger'},
                {'code': 'NG', 'name': 'Nigeria'},
                {'code': 'RW', 'name': 'Rwanda'},
                {'code': 'ST', 'name': 'Sao Tome and Principe'},
                {'code': 'SN', 'name': 'Senegal'},
                {'code': 'SC', 'name': 'Seychelles'},
                {'code': 'SL', 'name': 'Sierra Leone'},
                {'code': 'SO', 'name': 'Somalia'},
                {'code': 'ZA', 'name': 'South Africa'},
                {'code': 'SS', 'name': 'South Sudan'},
                {'code': 'SD', 'name': 'Sudan'},
                {'code': 'TZ', 'name': 'Tanzania'},
                {'code': 'TG', 'name': 'Togo'},
                {'code': 'TN', 'name': 'Tunisia'},
                {'code': 'UG', 'name': 'Uganda'},
                {'code': 'ZM', 'name': 'Zambia'},
                {'code': 'ZW', 'name': 'Zimbabwe'},

                # Americas
                {'code': 'AG', 'name': 'Antigua and Barbuda'},
                {'code': 'AR', 'name': 'Argentina'},
                {'code': 'BS', 'name': 'Bahamas'},
                {'code': 'BB', 'name': 'Barbados'},
                {'code': 'BZ', 'name': 'Belize'},
                {'code': 'BO', 'name': 'Bolivia'},
                {'code': 'BR', 'name': 'Brazil'},
                {'code': 'CA', 'name': 'Canada'},
                {'code': 'CL', 'name': 'Chile'},
                {'code': 'CO', 'name': 'Colombia'},
                {'code': 'CR', 'name': 'Costa Rica'},
                {'code': 'CU', 'name': 'Cuba'},
                {'code': 'DM', 'name': 'Dominica'},
                {'code': 'DO', 'name': 'Dominican Republic'},
                {'code': 'EC', 'name': 'Ecuador'},
                {'code': 'SV', 'name': 'El Salvador'},
                {'code': 'GD', 'name': 'Grenada'},
                {'code': 'GT', 'name': 'Guatemala'},
                {'code': 'GY', 'name': 'Guyana'},
                {'code': 'HT', 'name': 'Haiti'},
                {'code': 'HN', 'name': 'Honduras'},
                {'code': 'JM', 'name': 'Jamaica'},
                {'code': 'MX', 'name': 'Mexico'},
                {'code': 'NI', 'name': 'Nicaragua'},
                {'code': 'PA', 'name': 'Panama'},
                {'code': 'PY', 'name': 'Paraguay'},
                {'code': 'PE', 'name': 'Peru'},
                {'code': 'KN', 'name': 'Saint Kitts and Nevis'},
                {'code': 'LC', 'name': 'Saint Lucia'},
                {'code': 'VC', 'name': 'Saint Vincent and the Grenadines'},
                {'code': 'SR', 'name': 'Suriname'},
                {'code': 'TT', 'name': 'Trinidad and Tobago'},
                {'code': 'US', 'name': 'United States'},
                {'code': 'UY', 'name': 'Uruguay'},
                {'code': 'VE', 'name': 'Venezuela'},

                # Oceania
                {'code': 'AU', 'name': 'Australia'},
                {'code': 'FJ', 'name': 'Fiji'},
                {'code': 'KI', 'name': 'Kiribati'},
                {'code': 'MH', 'name': 'Marshall Islands'},
                {'code': 'FM', 'name': 'Micronesia'},
                {'code': 'NR', 'name': 'Nauru'},
                {'code': 'NZ', 'name': 'New Zealand'},
                {'code': 'PW', 'name': 'Palau'},
                {'code': 'PG', 'name': 'Papua New Guinea'},
                {'code': 'WS', 'name': 'Samoa'},
                {'code': 'SB', 'name': 'Solomon Islands'},
                {'code': 'TO', 'name': 'Tonga'},
                {'code': 'TV', 'name': 'Tuvalu'},
                {'code': 'VU', 'name': 'Vanuatu'},
            ]

        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults={'name': country_data['name']}
            )
            if created:
                self.stdout.write(f"Created country: {country.name}")

        # Create Tax rates for each country
        tax_data = [
            # Asia
            {'country_code': 'IN', 'tax_name': 'GST',              'tax_rate': 18.00},
            {'country_code': 'CN', 'tax_name': 'VAT',              'tax_rate': 13.00},
            {'country_code': 'JP', 'tax_name': 'Consumption Tax',  'tax_rate': 10.00},
            {'country_code': 'KR', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'SG', 'tax_name': 'GST',              'tax_rate': 9.00},
            {'country_code': 'MY', 'tax_name': 'SST',              'tax_rate': 6.00},
            {'country_code': 'TH', 'tax_name': 'VAT',              'tax_rate': 7.00},
            {'country_code': 'ID', 'tax_name': 'VAT',              'tax_rate': 11.00},
            {'country_code': 'PH', 'tax_name': 'VAT',              'tax_rate': 12.00},
            {'country_code': 'VN', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'PK', 'tax_name': 'GST',              'tax_rate': 17.00},
            {'country_code': 'BD', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'LK', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'NP', 'tax_name': 'VAT',              'tax_rate': 13.00},
            {'country_code': 'MM', 'tax_name': 'Commercial Tax',   'tax_rate': 5.00},
            {'country_code': 'KH', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'LA', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'BN', 'tax_name': 'GST',              'tax_rate': 0.00},
            {'country_code': 'TW', 'tax_name': 'VAT',              'tax_rate': 5.00},
            {'country_code': 'HK', 'tax_name': 'No VAT',           'tax_rate': 0.00},
            {'country_code': 'MN', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'KZ', 'tax_name': 'VAT',              'tax_rate': 12.00},
            {'country_code': 'UZ', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'TJ', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'TM', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'KG', 'tax_name': 'VAT',              'tax_rate': 12.00},
            {'country_code': 'AZ', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'AM', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'GE', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'IL', 'tax_name': 'VAT',              'tax_rate': 17.00},
            {'country_code': 'TR', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'SA', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'AE', 'tax_name': 'VAT',              'tax_rate': 5.00},
            {'country_code': 'QA', 'tax_name': 'No VAT',           'tax_rate': 0.00},
            {'country_code': 'KW', 'tax_name': 'No VAT',           'tax_rate': 0.00},
            {'country_code': 'BH', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'OM', 'tax_name': 'VAT',              'tax_rate': 5.00},
            {'country_code': 'JO', 'tax_name': 'GST',              'tax_rate': 16.00},
            {'country_code': 'LB', 'tax_name': 'VAT',              'tax_rate': 11.00},
            {'country_code': 'IQ', 'tax_name': 'VAT',              'tax_rate': 0.00},
            {'country_code': 'IR', 'tax_name': 'VAT',              'tax_rate': 9.00},
            {'country_code': 'SY', 'tax_name': 'VAT',              'tax_rate': 0.00},
            {'country_code': 'YE', 'tax_name': 'GST',              'tax_rate': 5.00},
            {'country_code': 'AF', 'tax_name': 'Business Tax',     'tax_rate': 10.00},
            {'country_code': 'BT', 'tax_name': 'Sales Tax',        'tax_rate': 50.00},
            {'country_code': 'MV', 'tax_name': 'GST',              'tax_rate': 8.00},
            {'country_code': 'TL', 'tax_name': 'VAT',              'tax_rate': 0.00},
            {'country_code': 'KP', 'tax_name': 'No Tax',           'tax_rate': 0.00},
            {'country_code': 'PS', 'tax_name': 'VAT',              'tax_rate': 16.00},
            {'country_code': 'CY', 'tax_name': 'VAT',              'tax_rate': 19.00},

            # Europe
            {'country_code': 'DE', 'tax_name': 'VAT',              'tax_rate': 19.00},
            {'country_code': 'FR', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'GB', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'IT', 'tax_name': 'VAT',              'tax_rate': 22.00},
            {'country_code': 'ES', 'tax_name': 'VAT',              'tax_rate': 21.00},
            {'country_code': 'PT', 'tax_name': 'VAT',              'tax_rate': 23.00},
            {'country_code': 'NL', 'tax_name': 'VAT',              'tax_rate': 21.00},
            {'country_code': 'BE', 'tax_name': 'VAT',              'tax_rate': 21.00},
            {'country_code': 'AT', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'CH', 'tax_name': 'VAT',              'tax_rate': 8.10},
            {'country_code': 'SE', 'tax_name': 'VAT',              'tax_rate': 25.00},
            {'country_code': 'NO', 'tax_name': 'VAT',              'tax_rate': 25.00},
            {'country_code': 'DK', 'tax_name': 'VAT',              'tax_rate': 25.00},
            {'country_code': 'FI', 'tax_name': 'VAT',              'tax_rate': 25.50},
            {'country_code': 'IS', 'tax_name': 'VAT',              'tax_rate': 24.00},
            {'country_code': 'IE', 'tax_name': 'VAT',              'tax_rate': 23.00},
            {'country_code': 'PL', 'tax_name': 'VAT',              'tax_rate': 23.00},
            {'country_code': 'CZ', 'tax_name': 'VAT',              'tax_rate': 21.00},
            {'country_code': 'SK', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'HU', 'tax_name': 'VAT',              'tax_rate': 27.00},
            {'country_code': 'RO', 'tax_name': 'VAT',              'tax_rate': 19.00},
            {'country_code': 'BG', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'HR', 'tax_name': 'VAT',              'tax_rate': 25.00},
            {'country_code': 'SI', 'tax_name': 'VAT',              'tax_rate': 22.00},
            {'country_code': 'GR', 'tax_name': 'VAT',              'tax_rate': 24.00},
            {'country_code': 'EE', 'tax_name': 'VAT',              'tax_rate': 22.00},
            {'country_code': 'LV', 'tax_name': 'VAT',              'tax_rate': 21.00},
            {'country_code': 'LT', 'tax_name': 'VAT',              'tax_rate': 21.00},
            {'country_code': 'MT', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'LU', 'tax_name': 'VAT',              'tax_rate': 17.00},
            {'country_code': 'RU', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'UA', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'BY', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'MD', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'RS', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'BA', 'tax_name': 'VAT',              'tax_rate': 17.00},
            {'country_code': 'ME', 'tax_name': 'VAT',              'tax_rate': 21.00},
            {'country_code': 'MK', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'AL', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'XK', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'AD', 'tax_name': 'IGI',              'tax_rate': 4.50},
            {'country_code': 'MC', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'SM', 'tax_name': 'VAT',              'tax_rate': 17.00},
            {'country_code': 'VA', 'tax_name': 'No VAT',           'tax_rate': 0.00},
            {'country_code': 'LI', 'tax_name': 'VAT',              'tax_rate': 8.10},

            # Africa
            {'country_code': 'ZA', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'EG', 'tax_name': 'VAT',              'tax_rate': 14.00},
            {'country_code': 'NG', 'tax_name': 'VAT',              'tax_rate': 7.50},
            {'country_code': 'KE', 'tax_name': 'VAT',              'tax_rate': 16.00},
            {'country_code': 'GH', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'ET', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'TZ', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'UG', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'RW', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'MA', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'TN', 'tax_name': 'VAT',              'tax_rate': 19.00},
            {'country_code': 'DZ', 'tax_name': 'VAT',              'tax_rate': 19.00},
            {'country_code': 'LY', 'tax_name': 'VAT',              'tax_rate': 0.00},
            {'country_code': 'SD', 'tax_name': 'VAT',              'tax_rate': 17.00},
            {'country_code': 'SN', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'CI', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'CM', 'tax_name': 'VAT',              'tax_rate': 19.25},
            {'country_code': 'AO', 'tax_name': 'VAT',              'tax_rate': 14.00},
            {'country_code': 'MZ', 'tax_name': 'VAT',              'tax_rate': 17.00},
            {'country_code': 'ZM', 'tax_name': 'VAT',              'tax_rate': 16.00},
            {'country_code': 'ZW', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'NA', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'BW', 'tax_name': 'VAT',              'tax_rate': 14.00},
            {'country_code': 'MU', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'MG', 'tax_name': 'VAT',              'tax_rate': 20.00},
            {'country_code': 'MW', 'tax_name': 'VAT',              'tax_rate': 16.50},
            {'country_code': 'LS', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'SZ', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'MR', 'tax_name': 'VAT',              'tax_rate': 16.00},
            {'country_code': 'ML', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'BF', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'NE', 'tax_name': 'VAT',              'tax_rate': 19.00},
            {'country_code': 'TD', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'GN', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'SL', 'tax_name': 'GST',              'tax_rate': 15.00},
            {'country_code': 'LR', 'tax_name': 'GST',              'tax_rate': 10.00},
            {'country_code': 'GM', 'tax_name': 'Sales Tax',        'tax_rate': 15.00},
            {'country_code': 'TG', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'BJ', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'GA', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'CG', 'tax_name': 'VAT',              'tax_rate': 18.50},
            {'country_code': 'CD', 'tax_name': 'VAT',              'tax_rate': 16.00},
            {'country_code': 'CF', 'tax_name': 'VAT',              'tax_rate': 19.00},
            {'country_code': 'GQ', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'SS', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'SO', 'tax_name': 'Sales Tax',        'tax_rate': 10.00},
            {'country_code': 'DJ', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'ER', 'tax_name': 'Sales Tax',        'tax_rate': 5.00},
            {'country_code': 'BI', 'tax_name': 'VAT',              'tax_rate': 18.00},
            {'country_code': 'SC', 'tax_name': 'GST',              'tax_rate': 15.00},
            {'country_code': 'CV', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'ST', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'KM', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'GW', 'tax_name': 'VAT',              'tax_rate': 19.00},

            # Americas
            {'country_code': 'US', 'tax_name': 'Sales Tax',        'tax_rate': 8.25},
            {'country_code': 'CA', 'tax_name': 'HST',              'tax_rate': 13.00},
            {'country_code': 'MX', 'tax_name': 'VAT',              'tax_rate': 16.00},
            {'country_code': 'BR', 'tax_name': 'ICMS',             'tax_rate': 17.00},
            {'country_code': 'AR', 'tax_name': 'VAT',              'tax_rate': 21.00},
            {'country_code': 'CL', 'tax_name': 'VAT',              'tax_rate': 19.00},
            {'country_code': 'CO', 'tax_name': 'VAT',              'tax_rate': 19.00},
            {'country_code': 'PE', 'tax_name': 'IGV',              'tax_rate': 18.00},
            {'country_code': 'VE', 'tax_name': 'VAT',              'tax_rate': 16.00},
            {'country_code': 'EC', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'BO', 'tax_name': 'VAT',              'tax_rate': 13.00},
            {'country_code': 'PY', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'UY', 'tax_name': 'VAT',              'tax_rate': 22.00},
            {'country_code': 'GY', 'tax_name': 'VAT',              'tax_rate': 14.00},
            {'country_code': 'SR', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'GT', 'tax_name': 'VAT',              'tax_rate': 12.00},
            {'country_code': 'BZ', 'tax_name': 'GST',              'tax_rate': 12.50},
            {'country_code': 'HN', 'tax_name': 'Sales Tax',        'tax_rate': 15.00},
            {'country_code': 'SV', 'tax_name': 'VAT',              'tax_rate': 13.00},
            {'country_code': 'NI', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'CR', 'tax_name': 'VAT',              'tax_rate': 13.00},
            {'country_code': 'PA', 'tax_name': 'ITBMS',            'tax_rate': 7.00},
            {'country_code': 'CU', 'tax_name': 'Sales Tax',        'tax_rate': 10.00},
            {'country_code': 'DO', 'tax_name': 'ITBIS',            'tax_rate': 18.00},
            {'country_code': 'HT', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'JM', 'tax_name': 'GCT',              'tax_rate': 15.00},
            {'country_code': 'TT', 'tax_name': 'VAT',              'tax_rate': 12.50},
            {'country_code': 'BB', 'tax_name': 'VAT',              'tax_rate': 17.50},
            {'country_code': 'BS', 'tax_name': 'VAT',              'tax_rate': 10.00},
            {'country_code': 'GD', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'LC', 'tax_name': 'VAT',              'tax_rate': 12.50},
            {'country_code': 'VC', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'AG', 'tax_name': 'Sales Tax',        'tax_rate': 15.00},
            {'country_code': 'DM', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'KN', 'tax_name': 'VAT',              'tax_rate': 17.00},

            # Oceania
            {'country_code': 'AU', 'tax_name': 'GST',              'tax_rate': 10.00},
            {'country_code': 'NZ', 'tax_name': 'GST',              'tax_rate': 15.00},
            {'country_code': 'PG', 'tax_name': 'GST',              'tax_rate': 10.00},
            {'country_code': 'FJ', 'tax_name': 'VAT',              'tax_rate': 9.00},
            {'country_code': 'SB', 'tax_name': 'GST',              'tax_rate': 9.00},
            {'country_code': 'VU', 'tax_name': 'VAT',              'tax_rate': 15.00},
            {'country_code': 'WS', 'tax_name': 'VAGST',            'tax_rate': 15.00},
            {'country_code': 'TO', 'tax_name': 'Sales Tax',        'tax_rate': 15.00},
            {'country_code': 'KI', 'tax_name': 'Sales Tax',        'tax_rate': 0.00},
            {'country_code': 'MH', 'tax_name': 'No Tax',           'tax_rate': 0.00},
            {'country_code': 'FM', 'tax_name': 'No Tax',           'tax_rate': 0.00},
            {'country_code': 'NR', 'tax_name': 'No Tax',           'tax_rate': 0.00},
            {'country_code': 'PW', 'tax_name': 'No Tax',           'tax_rate': 0.00},
            {'country_code': 'TV', 'tax_name': 'No Tax',           'tax_rate': 0.00},
        ]

        for tax_info in tax_data:
            try:
                country = Country.objects.get(code=tax_info['country_code'])
                tax, created = Tax.objects.get_or_create(
                    country=country,
                    tax_name=tax_info['tax_name'],
                    defaults={'tax_rate': tax_info['tax_rate']}
                )
                if created:
                    self.stdout.write(f"Created tax: {tax.tax_name} ({tax.tax_rate}%) for {country.name}")
            except Country.DoesNotExist:
                self.stdout.write(f"Country {tax_info['country_code']} not found")

        # Update Currency model to link with countries (if currencies exist)
        currency_updates = [
                # Asia
                {'code': 'INR', 'country_code': 'IN'},   # Indian Rupee
                {'code': 'CNY', 'country_code': 'CN'},   # Chinese Yuan
                {'code': 'JPY', 'country_code': 'JP'},   # Japanese Yen
                {'code': 'KRW', 'country_code': 'KR'},   # South Korean Won
                {'code': 'SGD', 'country_code': 'SG'},   # Singapore Dollar
                {'code': 'MYR', 'country_code': 'MY'},   # Malaysian Ringgit
                {'code': 'THB', 'country_code': 'TH'},   # Thai Baht
                {'code': 'IDR', 'country_code': 'ID'},   # Indonesian Rupiah
                {'code': 'PHP', 'country_code': 'PH'},   # Philippine Peso
                {'code': 'VND', 'country_code': 'VN'},   # Vietnamese Dong
                {'code': 'PKR', 'country_code': 'PK'},   # Pakistani Rupee
                {'code': 'BDT', 'country_code': 'BD'},   # Bangladeshi Taka
                {'code': 'LKR', 'country_code': 'LK'},   # Sri Lankan Rupee
                {'code': 'NPR', 'country_code': 'NP'},   # Nepalese Rupee
                {'code': 'MMK', 'country_code': 'MM'},   # Myanmar Kyat
                {'code': 'KHR', 'country_code': 'KH'},   # Cambodian Riel
                {'code': 'LAK', 'country_code': 'LA'},   # Lao Kip
                {'code': 'BND', 'country_code': 'BN'},   # Brunei Dollar
                {'code': 'TWD', 'country_code': 'TW'},   # Taiwan Dollar
                {'code': 'MNT', 'country_code': 'MN'},   # Mongolian Tugrik
                {'code': 'KZT', 'country_code': 'KZ'},   # Kazakhstani Tenge
                {'code': 'UZS', 'country_code': 'UZ'},   # Uzbekistani Som
                {'code': 'TJS', 'country_code': 'TJ'},   # Tajikistani Somoni
                {'code': 'TMT', 'country_code': 'TM'},   # Turkmenistani Manat
                {'code': 'KGS', 'country_code': 'KG'},   # Kyrgyzstani Som
                {'code': 'AZN', 'country_code': 'AZ'},   # Azerbaijani Manat
                {'code': 'AMD', 'country_code': 'AM'},   # Armenian Dram
                {'code': 'GEL', 'country_code': 'GE'},   # Georgian Lari
                {'code': 'ILS', 'country_code': 'IL'},   # Israeli Shekel
                {'code': 'TRY', 'country_code': 'TR'},   # Turkish Lira
                {'code': 'SAR', 'country_code': 'SA'},   # Saudi Riyal
                {'code': 'AED', 'country_code': 'AE'},   # UAE Dirham
                {'code': 'QAR', 'country_code': 'QA'},   # Qatari Riyal
                {'code': 'KWD', 'country_code': 'KW'},   # Kuwaiti Dinar
                {'code': 'BHD', 'country_code': 'BH'},   # Bahraini Dinar
                {'code': 'OMR', 'country_code': 'OM'},   # Omani Rial
                {'code': 'JOD', 'country_code': 'JO'},   # Jordanian Dinar
                {'code': 'LBP', 'country_code': 'LB'},   # Lebanese Pound
                {'code': 'IQD', 'country_code': 'IQ'},   # Iraqi Dinar
                {'code': 'IRR', 'country_code': 'IR'},   # Iranian Rial
                {'code': 'SYP', 'country_code': 'SY'},   # Syrian Pound
                {'code': 'YER', 'country_code': 'YE'},   # Yemeni Rial
                {'code': 'AFN', 'country_code': 'AF'},   # Afghan Afghani
                {'code': 'BTN', 'country_code': 'BT'},   # Bhutanese Ngultrum
                {'code': 'MVR', 'country_code': 'MV'},   # Maldivian Rufiyaa
                {'code': 'USD', 'country_code': 'TL'},   # Timor-Leste uses USD
                {'code': 'KPW', 'country_code': 'KP'},   # North Korean Won
                {'code': 'ILS', 'country_code': 'PS'},   # Palestinian uses ILS
                {'code': 'EUR', 'country_code': 'CY'},   # Cyprus Euro

                # Europe
                {'code': 'EUR', 'country_code': 'DE'},   # Euro - Germany
                {'code': 'EUR', 'country_code': 'FR'},   # Euro - France
                {'code': 'GBP', 'country_code': 'GB'},   # British Pound
                {'code': 'EUR', 'country_code': 'IT'},   # Euro - Italy
                {'code': 'EUR', 'country_code': 'ES'},   # Euro - Spain
                {'code': 'EUR', 'country_code': 'PT'},   # Euro - Portugal
                {'code': 'EUR', 'country_code': 'NL'},   # Euro - Netherlands
                {'code': 'EUR', 'country_code': 'BE'},   # Euro - Belgium
                {'code': 'EUR', 'country_code': 'AT'},   # Euro - Austria
                {'code': 'CHF', 'country_code': 'CH'},   # Swiss Franc
                {'code': 'SEK', 'country_code': 'SE'},   # Swedish Krona
                {'code': 'NOK', 'country_code': 'NO'},   # Norwegian Krone
                {'code': 'DKK', 'country_code': 'DK'},   # Danish Krone
                {'code': 'EUR', 'country_code': 'FI'},   # Euro - Finland
                {'code': 'ISK', 'country_code': 'IS'},   # Icelandic Krona
                {'code': 'EUR', 'country_code': 'IE'},   # Euro - Ireland
                {'code': 'PLN', 'country_code': 'PL'},   # Polish Zloty
                {'code': 'CZK', 'country_code': 'CZ'},   # Czech Koruna
                {'code': 'EUR', 'country_code': 'SK'},   # Euro - Slovakia
                {'code': 'HUF', 'country_code': 'HU'},   # Hungarian Forint
                {'code': 'RON', 'country_code': 'RO'},   # Romanian Leu
                {'code': 'BGN', 'country_code': 'BG'},   # Bulgarian Lev
                {'code': 'EUR', 'country_code': 'HR'},   # Euro - Croatia
                {'code': 'EUR', 'country_code': 'SI'},   # Euro - Slovenia
                {'code': 'EUR', 'country_code': 'GR'},   # Euro - Greece
                {'code': 'EUR', 'country_code': 'EE'},   # Euro - Estonia
                {'code': 'EUR', 'country_code': 'LV'},   # Euro - Latvia
                {'code': 'EUR', 'country_code': 'LT'},   # Euro - Lithuania
                {'code': 'EUR', 'country_code': 'MT'},   # Euro - Malta
                {'code': 'EUR', 'country_code': 'LU'},   # Euro - Luxembourg
                {'code': 'RUB', 'country_code': 'RU'},   # Russian Ruble
                {'code': 'UAH', 'country_code': 'UA'},   # Ukrainian Hryvnia
                {'code': 'BYN', 'country_code': 'BY'},   # Belarusian Ruble
                {'code': 'MDL', 'country_code': 'MD'},   # Moldovan Leu
                {'code': 'RSD', 'country_code': 'RS'},   # Serbian Dinar
                {'code': 'BAM', 'country_code': 'BA'},   # Bosnia Mark
                {'code': 'EUR', 'country_code': 'ME'},   # Montenegro uses EUR
                {'code': 'MKD', 'country_code': 'MK'},   # Macedonian Denar
                {'code': 'ALL', 'country_code': 'AL'},   # Albanian Lek
                {'code': 'EUR', 'country_code': 'XK'},   # Kosovo uses EUR
                {'code': 'EUR', 'country_code': 'AD'},   # Andorra uses EUR
                {'code': 'EUR', 'country_code': 'MC'},   # Monaco uses EUR
                {'code': 'EUR', 'country_code': 'SM'},   # San Marino uses EUR
                {'code': 'EUR', 'country_code': 'VA'},   # Vatican uses EUR
                {'code': 'CHF', 'country_code': 'LI'},   # Liechtenstein uses CHF

                # Africa
                {'code': 'ZAR', 'country_code': 'ZA'},   # South African Rand
                {'code': 'EGP', 'country_code': 'EG'},   # Egyptian Pound
                {'code': 'NGN', 'country_code': 'NG'},   # Nigerian Naira
                {'code': 'KES', 'country_code': 'KE'},   # Kenyan Shilling
                {'code': 'GHS', 'country_code': 'GH'},   # Ghanaian Cedi
                {'code': 'ETB', 'country_code': 'ET'},   # Ethiopian Birr
                {'code': 'TZS', 'country_code': 'TZ'},   # Tanzanian Shilling
                {'code': 'UGX', 'country_code': 'UG'},   # Ugandan Shilling
                {'code': 'RWF', 'country_code': 'RW'},   # Rwandan Franc
                {'code': 'MAD', 'country_code': 'MA'},   # Moroccan Dirham
                {'code': 'TND', 'country_code': 'TN'},   # Tunisian Dinar
                {'code': 'DZD', 'country_code': 'DZ'},   # Algerian Dinar
                {'code': 'LYD', 'country_code': 'LY'},   # Libyan Dinar
                {'code': 'SDG', 'country_code': 'SD'},   # Sudanese Pound
                {'code': 'XOF', 'country_code': 'SN'},   # CFA Franc - Senegal
                {'code': 'XOF', 'country_code': 'CI'},   # CFA Franc - Ivory Coast
                {'code': 'XAF', 'country_code': 'CM'},   # CFA Franc - Cameroon
                {'code': 'AOA', 'country_code': 'AO'},   # Angolan Kwanza
                {'code': 'MZN', 'country_code': 'MZ'},   # Mozambican Metical
                {'code': 'ZMW', 'country_code': 'ZM'},   # Zambian Kwacha
                {'code': 'ZWL', 'country_code': 'ZW'},   # Zimbabwean Dollar
                {'code': 'NAD', 'country_code': 'NA'},   # Namibian Dollar
                {'code': 'BWP', 'country_code': 'BW'},   # Botswana Pula
                {'code': 'MUR', 'country_code': 'MU'},   # Mauritian Rupee
                {'code': 'MGA', 'country_code': 'MG'},   # Malagasy Ariary
                {'code': 'MWK', 'country_code': 'MW'},   # Malawian Kwacha
                {'code': 'LSL', 'country_code': 'LS'},   # Lesotho Loti
                {'code': 'SZL', 'country_code': 'SZ'},   # Swazi Lilangeni
                {'code': 'MRU', 'country_code': 'MR'},   # Mauritanian Ouguiya
                {'code': 'XOF', 'country_code': 'ML'},   # CFA Franc - Mali
                {'code': 'XOF', 'country_code': 'BF'},   # CFA Franc - Burkina Faso
                {'code': 'XOF', 'country_code': 'NE'},   # CFA Franc - Niger
                {'code': 'XAF', 'country_code': 'TD'},   # CFA Franc - Chad
                {'code': 'GNF', 'country_code': 'GN'},   # Guinean Franc
                {'code': 'SLL', 'country_code': 'SL'},   # Sierra Leonean Leone
                {'code': 'LRD', 'country_code': 'LR'},   # Liberian Dollar
                {'code': 'GMD', 'country_code': 'GM'},   # Gambian Dalasi
                {'code': 'XOF', 'country_code': 'TG'},   # CFA Franc - Togo
                {'code': 'XOF', 'country_code': 'BJ'},   # CFA Franc - Benin
                {'code': 'XAF', 'country_code': 'GA'},   # CFA Franc - Gabon
                {'code': 'XAF', 'country_code': 'CG'},   # CFA Franc - Congo
                {'code': 'CDF', 'country_code': 'CD'},   # Congolese Franc
                {'code': 'XAF', 'country_code': 'CF'},   # CFA Franc - CAR
                {'code': 'XAF', 'country_code': 'GQ'},   # CFA Franc - Eq. Guinea
                {'code': 'SSP', 'country_code': 'SS'},   # South Sudanese Pound
                {'code': 'SOS', 'country_code': 'SO'},   # Somali Shilling
                {'code': 'DJF', 'country_code': 'DJ'},   # Djiboutian Franc
                {'code': 'ERN', 'country_code': 'ER'},   # Eritrean Nakfa
                {'code': 'BIF', 'country_code': 'BI'},   # Burundian Franc
                {'code': 'SCR', 'country_code': 'SC'},   # Seychellois Rupee
                {'code': 'CVE', 'country_code': 'CV'},   # Cape Verdean Escudo
                {'code': 'STN', 'country_code': 'ST'},   # São Tomé Dobra
                {'code': 'KMF', 'country_code': 'KM'},   # Comorian Franc
                {'code': 'XOF', 'country_code': 'GW'},   # CFA Franc - Guinea-Bissau

                # Americas
                {'code': 'USD', 'country_code': 'US'},   # US Dollar
                {'code': 'CAD', 'country_code': 'CA'},   # Canadian Dollar
                {'code': 'MXN', 'country_code': 'MX'},   # Mexican Peso
                {'code': 'BRL', 'country_code': 'BR'},   # Brazilian Real
                {'code': 'ARS', 'country_code': 'AR'},   # Argentine Peso
                {'code': 'CLP', 'country_code': 'CL'},   # Chilean Peso
                {'code': 'COP', 'country_code': 'CO'},   # Colombian Peso
                {'code': 'PEN', 'country_code': 'PE'},   # Peruvian Sol
                {'code': 'VES', 'country_code': 'VE'},   # Venezuelan Bolivar
                {'code': 'USD', 'country_code': 'EC'},   # Ecuador uses USD
                {'code': 'BOB', 'country_code': 'BO'},   # Bolivian Boliviano
                {'code': 'PYG', 'country_code': 'PY'},   # Paraguayan Guarani
                {'code': 'UYU', 'country_code': 'UY'},   # Uruguayan Peso
                {'code': 'GYD', 'country_code': 'GY'},   # Guyanese Dollar
                {'code': 'SRD', 'country_code': 'SR'},   # Surinamese Dollar
                {'code': 'GTQ', 'country_code': 'GT'},   # Guatemalan Quetzal
                {'code': 'BZD', 'country_code': 'BZ'},   # Belize Dollar
                {'code': 'HNL', 'country_code': 'HN'},   # Honduran Lempira
                {'code': 'USD', 'country_code': 'SV'},   # El Salvador uses USD
                {'code': 'NIO', 'country_code': 'NI'},   # Nicaraguan Cordoba
                {'code': 'CRC', 'country_code': 'CR'},   # Costa Rican Colon
                {'code': 'PAB', 'country_code': 'PA'},   # Panamanian Balboa
                {'code': 'CUP', 'country_code': 'CU'},   # Cuban Peso
                {'code': 'DOP', 'country_code': 'DO'},   # Dominican Peso
                {'code': 'HTG', 'country_code': 'HT'},   # Haitian Gourde
                {'code': 'JMD', 'country_code': 'JM'},   # Jamaican Dollar
                {'code': 'TTD', 'country_code': 'TT'},   # Trinidad Dollar
                {'code': 'BBD', 'country_code': 'BB'},   # Barbadian Dollar
                {'code': 'BSD', 'country_code': 'BS'},   # Bahamian Dollar
                {'code': 'XCD', 'country_code': 'GD'},   # East Caribbean Dollar
                {'code': 'XCD', 'country_code': 'LC'},   # East Caribbean Dollar
                {'code': 'XCD', 'country_code': 'VC'},   # East Caribbean Dollar
                {'code': 'XCD', 'country_code': 'AG'},   # East Caribbean Dollar
                {'code': 'XCD', 'country_code': 'DM'},   # East Caribbean Dollar
                {'code': 'XCD', 'country_code': 'KN'},   # East Caribbean Dollar

                # Oceania
                {'code': 'AUD', 'country_code': 'AU'},   # Australian Dollar
                {'code': 'NZD', 'country_code': 'NZ'},   # New Zealand Dollar
                {'code': 'PGK', 'country_code': 'PG'},   # Papua New Guinean Kina
                {'code': 'FJD', 'country_code': 'FJ'},   # Fijian Dollar
                {'code': 'SBD', 'country_code': 'SB'},   # Solomon Islands Dollar
                {'code': 'VUV', 'country_code': 'VU'},   # Vanuatu Vatu
                {'code': 'WST', 'country_code': 'WS'},   # Samoan Tala
                {'code': 'TOP', 'country_code': 'TO'},   # Tongan Paanga
                {'code': 'AUD', 'country_code': 'KI'},   # Kiribati uses AUD
                {'code': 'USD', 'country_code': 'MH'},   # Marshall Islands uses USD
                {'code': 'USD', 'country_code': 'FM'},   # Micronesia uses USD
                {'code': 'AUD', 'country_code': 'NR'},   # Nauru uses AUD
                {'code': 'USD', 'country_code': 'PW'},   # Palau uses USD
                {'code': 'AUD', 'country_code': 'TV'},   # Tuvalu uses AUD
            ]


        for currency_update in currency_updates:
            try:
                country = Country.objects.get(code=currency_update['country_code'])
                updated_count = Currency.objects.filter(code=currency_update['code']).update(country=country)
                if updated_count > 0:
                    self.stdout.write(f"Updated {updated_count} currency records for {currency_update['code']} with country {country.name}")
            except Country.DoesNotExist:
                self.stdout.write(f"Country {currency_update['country_code']} not found")

        self.stdout.write(self.style.SUCCESS('Successfully created tax data'))