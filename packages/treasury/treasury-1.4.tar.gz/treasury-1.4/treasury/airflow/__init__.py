def get_provider_info():
    return {
        'package-name': 'treasury',
        'name': 'treasury',
        'description': '`sales force b2c commerce api <https://developer.salesforce.com/docs/commerce/commerce-api/>`__\n',
        'versions': [
            '1.0.0',
        ],
        'dependencies': [
            'apache-airflow>=2.3.0',
        ],
        'integrations': [{
            'integration-name': 'treasury',
            'external-doc-url': 'https://pypi.org/projects/treasury',
            'tags': ['service'],
        }],
        'operators': [{
            'integration-name': 'treasury',
            'python-modules': [
                'treasury.airflow.operators',
            ],
        }],
        'hooks': [{
            'integration-name': 'treasury',
            'python-modules': [
                'treasury.airflow.hooks',
            ],
        }],
        'transfers': [],
        'connection-types': [{
            'hook-class-name': 'treasury.airflow.hooks.TreasuryHook',
            'connection-type': 'treasury_sfcc',
        }, ],
    }
