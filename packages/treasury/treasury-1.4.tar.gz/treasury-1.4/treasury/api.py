from datetime import date
from datetime import datetime
from datetime import timedelta
import logging
from functools import partial
from pytz import utc, timezone
from requests import PreparedRequest
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2.rfc6749.tokens import prepare_bearer_headers
from deceit.api_client import ApiClient
from deceit.api_client import ApiException
from deceit.adapters import RetryAdapter
import json

from urllib3 import Retry

log = logging.getLogger(__name__)


class CommerceApiException(ApiException):
    pass


class CommerceApi(ApiClient):

    """
    This class provides a wrapper around the sales force
    commerce api.  We setup credentials for peaky peep
    in account manager, following the commerce api guide, here:
    https://developer.commercecloud.com/s/article/CommerceAPI-Client-Permissions-for-API-Endpoints

    Once we had created the api client accounts in account manager,
    we loaded the configuration into waddle.  There are about 6 configuration
    values we needed to configure this client to work, and each
    of these can be specified in the constructor to override the values
    from waddle.

    Args

        :conf (ParamBunch): the param bunch with the configuration, included
        encrypted secrets
        :base_url (str): which is the api url found in the guide, prefixed
                      by the short code which we generated from the
                      administration portal.  n.b., there is a single
                      short code for all of our instances
        :site_id (str): the site id can be found in the administration portal
                     by going to Administration > Manage Sites.
        :scopes (List(str]): a list of scopes from this page
        https://developer.commercecloud.com/s/article/CommerceAPI-AuthZ-Scope-Catalog
        :client_id (str): the client_id that we generated in account manager when
                       we created the api client record
        :password (str):  the password that we set when we created the api client
                       record.  It can be reset using account manager.
        :organization_id (str):  this value can be seen from Administration >
                              Salesforce Commerce API Settings (in the
                              admin console)
    """
    def __init__(self, conf=None,
                 base_url=None, site_id=None, scopes=None,
                 client_id=None, password=None, organization_id=None,
                 webdav_prefix=None, default_time_zone=None,
                 timeout=300, **kwargs):
        """
        :param str which: specifies which config to load from waddle
        :param int timeout: specify -1 to wait indefinitely for a response
        """
        super().__init__(
            base_url=base_url or conf.base_url,
            default_timeout=timeout,
            exception_class=CommerceApiException)

        self.site_id = site_id or conf.site_id
        self.scopes = scopes or conf.scopes
        self.conf = conf
        self.client_id = client_id or conf.client_id
        self.password = password or conf.password
        self.organization_id = organization_id or conf.organization_id
        self.default_time_zone = default_time_zone or timezone('PST8PDT')
        self.webdav_prefix = webdav_prefix
        if not self.webdav_prefix and conf:
            self.webdav_prefix = conf.webdav_prefix
        self.token_expires_at = datetime.now(utc)
        retry = Retry(total=14, status_forcelist=[429, 500, 502, 503, 504])
        self.session = OAuth2Session(client=BackendApplicationClient(
            client_id=self.client_id,
            scope=self.scope),
            auto_refresh_url='https://account.demandware.com/dwsso/oauth2/access_token')
        self.session.mount('https://', HTTPAdapter(max_retries=retry))
        self.base_coupons_url = (
          f'pricing/coupons/v1'
          f'/organizations/{self.organization_id}'
        )
        self.base_orders_url = (
            f'checkout/orders/v1'
            f'/organizations/{self.organization_id}'
        )
        self.base_products_url = (
            f'product/products/v1'
            f'/organizations/{self.organization_id}'
        )
        self.base_cdn_url = (
            f'cdn/zones/v1'
            f'/organizations/{self.organization_id}'
        )
        self.base_catalog_url = (
            f'product/catalogs/v1'
            f'/organizations/{self.organization_id}/catalogs'
        )
        self.base_coupon_redemption_search_url = (
            f'pricing/coupons/v1'
            f'/organizations/{self.organization_id}/coupons/redemptions'
        )
        self.base_customer_url = (
            f'customer/customers/v1/organizations/{self.organization_id}'
        )

    @property
    def json_headers(self):
        return {
            'content-type': 'application/json',
        }

    @property
    def tenant_id(self):
        return self.organization_id.split('_', 2)[-1]

    @property
    def scope(self):
        scopes = ' '.join(self.scopes)
        scope = f'SALESFORCE_COMMERCE_API:{self.tenant_id} {scopes}'
        return scope

    def fetch_token(self):
        token_url = 'https://account.demandware.com/dwsso/oauth2/access_token'
        self.session.fetch_token(
            token_url,
            client_id=self.client_id,
            client_secret=self.password,
            scope=self.scope)
        expires_at = self.session.token['expires_at']
        self.token_expires_at = datetime.fromtimestamp(expires_at, utc)
        self.token_expires_at -= timedelta(minutes=5)

    def send(self, method, route, params=None, form_data=None, json_data=None,
             raw=False, **kwargs):
        h = kwargs.pop('headers', None)
        headers = {}
        headers.update(self.json_headers)
        headers.update(h or {})
        response = super().send(
            method=method, route=route, params=params, form_data=form_data,
            json_data=json_data, raw=raw, headers=headers, **kwargs)
        return response

    @property
    def expired(self):
        return self.now() >= self.token_expires_at

    def presend(self, request: PreparedRequest):
        if self.expired:
            self.fetch_token()
        prepare_bearer_headers(self.session.access_token, request.headers)

    def normalize_date(self, value):
        from dateutil.parser import parse as parse_date
        from pytz import utc
        if isinstance(value, str):
            value = parse_date(value)
        elif isinstance(value, date) and not isinstance(value, datetime):
            value = datetime(
                value.year, value.month, value.day,
                tzinfo=self.default_time_zone)
            value = value.isoformat('T', 'seconds')
        if isinstance(value, datetime):
            value = value.astimezone(utc).isoformat('T', 'seconds')
        value = value[:-6].strip()
        value = f'{value}Z'
        return value

    def now(self):
        return datetime.now(self.default_time_zone)

    def fix_empty_dates(self, start_date, end_date):
        if not start_date:
            start_date = self.today() - timedelta(days=1)
        if not end_date:
            end_date = start_date + timedelta(days=1)
        return start_date, end_date

    def today(self):
        return self.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    def get_orders_by_creation_date_page(
            self,
            start_date=None,
            end_date=None, page=1, limit=100):
        start_date, end_date = self.fix_empty_dates(start_date, end_date)
        params = {
            'creationDateFrom': self.normalize_date(start_date),
            'creationDateTo': self.normalize_date(end_date),
            'sortBy': 'creation_date',
        }
        yield from self.orders_page(params, page, limit)

    def orders_by_creation_date(
            self,
            start_date=None,
            end_date=None, limit=100):
        for page in range(1, 100):
            log.info('[%s => %s] page %s', start_date, end_date, page)
            results = list(self.get_orders_by_creation_date_page(
                start_date, end_date, page, limit
            ))
            log.info('%s results', len(results))
            if results:
                yield from results
            if len(results) < limit:
                break

    def orders_page(self, params, page, limit):
        params.setdefault('siteId', self.site_id)
        params.setdefault('limit', limit)
        if page > 1:
            params.setdefault('offset', (page - 1) * limit)
        url = f'{self.base_orders_url}/orders'
        response = self.get(url, params, raw=True)
        total = response.headers.get('SFDC-Pagination-Total-Count') or 0
        log.info(
            '[%s => %s] %s-%s / %s',
            params.get('creationDateFrom') or params.get('lastModifiedDateFrom'),
            params.get('creationDateTo') or params.get('lastModifiedDateTo'),
            (page - 1) * limit + 1,  page * limit, total)
        data = self.handle_response(response)
        # headers = response.headers
        if 'data' in data:
            yield from data['data']

    def get_orders_by_modified_date_page(
            self,
            start_date=None,
            end_date=None, page=1, limit=100):
        start_date, end_date = self.fix_empty_dates(start_date, end_date)
        params = {
            'lastModifiedDateFrom': self.normalize_date(start_date),
            'lastModifiedDateTo': self.normalize_date(end_date),
        }
        yield from self.orders_page(params, page, limit)

    def orders_by_modified_date(
            self,
            start_date=None,
            end_date=None, limit=100):
        for page in range(1, 100):
            results = list(self.get_orders_by_modified_date_page(
                start_date, end_date, page, limit
            ))
            if results:
                yield from results
            if len(results) < limit:
                break

    def order(self, order_number):
        url = f'{self.base_orders_url}/orders/{order_number}'
        log.debug('[treasury / order] url: %s', url)
        params = dict(siteId=self.site_id)
        order_data = self.get(url, params)
        return order_data

    def product(self, product_id):
        url = f'{self.base_products_url}/products/{product_id}'
        params = dict(siteId=self.site_id)
        product_data = self.get(url, params)

        return product_data

    def get_coupons(self, limit=100):
        url = f'{self.base_coupons_url}/coupons?siteId={self.site_id}'
        params = {
            'limit': limit,
            'query': {
                'textQuery': {
                    'fields': [
                        'couponId',
                        'description',
                        'type',
                        'enabled'
                    ],
                    'searchPhrase': 'multiple_codes'
                }
            },
        }
        n, n_total = 0, None
        for page in range(1, 100):
            params['offset'] = (page - 1) * limit
            result = self.post(url, json_data=params)
            rg = result.get('hits') or []
            if page == 1:
                n_total = result['total']
            n += len(rg)
            yield from rg
            if n >= n_total or not rg:
                break

    def product_variations(self, product_id):  # pragma: no cover
        url = f'{self.base_products_url}/products/{product_id}/variations'
        params = dict(siteId=self.site_id)
        product_data = self.get(url, params)
        return product_data

    def coupon_redemption_search(self, coupon_id):
        url = f'{self.base_coupon_redemption_search_url}?siteId={self.site_id}'
        params = {
            "limit": 200,
            "query": {
                "textQuery": {
                    "fields": [
                        "code",
                        "couponId",
                        "customerEmail",
                        "orderNo"
                    ],
                    "searchPhrase": f"{coupon_id}"
                }
            },
        }
        coupon_redemption_data = self.post(url, json_data=params)
        return coupon_redemption_data

    def products_by_category(self, catalog_id, category_id):  # pragma: no cover
        url = f'{self.base_catalog_url}/{catalog_id}/categories/{category_id}/category-product-assignment-search'
        log.debug('[treasury] url: %s', url)
        params = {
             'query': { 'match_all_query': {},
                         },
             'select': '(**)',
             'expand': ['product_base']
        }
        product_data = self.post(url, json_data=params)
        return product_data

    # we need to pull all products updated in last couple of days
    def products_last_modified(self, from_date, to_date, max_products_per_page=120):  # pragma: no cover
        url = f'{self.base_products_url}/product-search'
        log.info('url %s', url)

        size = max_products_per_page or self.page_size
        params = {
            'limit': size,
            'offset': 0,
            'query': {
                'filtered_query': {
                    'query': {'match_all_query': {}},
                    'filter': {
                        'range_filter': {
                            'field': 'lastModified',
                            'from': self.normalize_date(from_date),
                            'to': self.normalize_date(to_date),
                            'from_inclusive': True,
                            'to_inclusive': True,
                        }
                    }
                }
            },
            'expand': ['all']
        }
        product_data = self.post(url, json_data=params)
        list_products = []
        total_records = product_data['total']
        count = 0
        log.info('[treasury] total records %s', total_records)
        while True:
            count = count + len(product_data['hits'])

            # filter products, so that we will get variants only.
            # we will not worry about parent products for now.
            list_products.extend([d['id'] for d in product_data['hits'] if 'variant' in d['type']])
            log.info('[treasury] fetched records count %s', len(list_products))

            # exit when we read all records
            if total_records <= count:
                break
            params['offset'] = count
            product_data = self.post(url, json_data=params)

        # loop through the list of products to get required data
        products = []
        for index, variant in enumerate(list_products):
            row = self.product(variant)
            products.append(row)
        return products

    def get_zone_info(self, **kwargs):
        url = f'{self.base_cdn_url}/zones/info'
        response = self.get(url, **kwargs)
        if kwargs.get('raw'):
            return response
        return response['data']

    def get_zone_id(self):
        zones = self.get_zone_info()
        webdav_prefix = self.webdav_prefix
        for x in zones:
            if x['name'].startswith(webdav_prefix):
                return x['zoneId']
        log.info('[treasury] no zone id found!')
        return None

    def get_certificates(self, zone_id=None, params=None, **kwargs):
        zone_id = zone_id or self.get_zone_id()
        url = f'{self.base_cdn_url}/zones/{zone_id}/certificates'
        response = self.get(url, params=params, **kwargs)
        return response['data']

    def update_certificate(self, certificate_id, hostname, certificate=None,
                           key=None, certificate_type='custom',
                           certificate_authority=None,
                           certificate_validation=None,
                           zone_id=None, params=None, **kwargs):  # pragma: no cover
        """
        certificate and key should be specified in pem format
        """
        zone_id = zone_id or self.get_zone_id()
        url = f'{self.base_cdn_url}/zones/{zone_id}/certificates/{certificate_id}'
        json_data = dict(hostname=hostname)
        if certificate and certificate_type == 'custom':
            json_data['certificate'] = certificate
        if key and certificate_type == 'custom':
            json_data['privateKey'] = key
        if certificate_type:
            json_data['certificateType'] = certificate_type
        if certificate_authority:
            json_data['certificateAuthority'] = certificate_authority
        if certificate_validation:
            json_data['certificateValidation'] = certificate_validation
        return self.send('patch', url, params=params, json_data=json_data, **kwargs)

    def add_certificate(self, hostname, certificate, key,
                        zone_id=None, params=None, **kwargs):  # pragma: no cover
        """
        certificate and key should be specified in pem format
        """
        zone_id = zone_id or self.get_zone_id()
        url = f'{self.base_cdn_url}/zones/{zone_id}/certificates'
        json_data = dict(
            hostname=hostname,
            certificate=certificate,
            privateKey=key,
        )
        return self.post(url, params=params, json_data=json_data, **kwargs)

    def get_firewall_rules(self):
        zone_id = self.get_zone_id()
        if zone_id:
            url = f'{self.base_cdn_url}/zones/{zone_id}/waf/rules'
            response = self.get(url)
            return response['data']
        log.info('[treasury] no zone id found!')
        return None

    def add_firewall_rules(self, type_, action, values):  # pragma: no cover
        zone_id = self.get_zone_id()
        if zone_id:
            url = f'{self.base_cdn_url}/zones/{zone_id}/firewall/rules'
            json_data = {
                'type': type_,
                'action': action,
                'values': values,
            }
            return self.post(url, json_data)
        return None

    def customer_groups(self, **kwargs):
        """
        searches for customer groups by id
        """
        url = f'{self.base_customer_url}/customer-group-search'
        json_data = {
            'query': { 'matchAllQuery': {} },
        }
        yield from self.yield_from_search(url, json_data)

    def yield_from_search(self, route, json_data, limit=200, page=1):
        """
        yields hits from a specified search
        """
        params = { 'siteId': self.site_id }
        n_total = 1
        n = 0
        while n < n_total:
            if page > 1:
                json_data['offset'] = limit * (page - 1)
            json_data['limit'] = limit
            response = self.post(route, params=params, json_data=json_data)
            hits = response['hits']
            n += len(hits)
            n_total = response['total']
            page += 1
            yield from hits

    def campaigns(self, limit=200, page=1):
        """
        searches for campaigns by start / end date
        """
        route = f'pricing/campaigns/v1/organizations/{self.organization_id}/campaigns'
        dsl = { 'matchAllQuery': {} }
        # dsl = {
        #     'filtered_query': {
        #         'query': {'match_all_query': {}},
        #         'filter': {
        #             'range_filter': {
        #                 'field': 'lastModified',
        #                 'from': self.normalize_date(start_date),
        #                 'to': self.normalize_date(end_date),
        #             },
        #         },
        #     },
        # }
        json_data = { 'query': dsl }
        yield from self.yield_from_search(route, json_data, limit=limit)


    def promotions(self):
        """
        searches for campaigns by start / end date
        """
        route = f'pricing/promotions/v1/organizations/{self.organization_id}/promotions'
        dsl = {
            'matchAllQuery': {},
        }
        json_data = { 'query': dsl }
        yield from self.yield_from_search(route, json_data=json_data)
