# treasury

a simple api client for interacting with sfcc using waddle as its secrets 
manager.  named after a group of goldfinches.  pax avium.

### key config elements
- client_id
- password
- organization_id
- short_code
- base_url
- site_id
- webdav_prefix
- scopes

### scopes:
we need to add respective scope in sfcc administrative console
in order to be able to pull data elements such as orders, products, categories etc.
ex: 
- sfcc.products for products
- sfcc.catalogs for catalogs
- sfcc.orders for orders

### callable api methods and usage guidelines:

#### products_last_modified
the `CommerceApi.products_last_modified`  method can be used to retrieve all products 
by last modified date range. a preconfigured test fixture has been used to send the 
api object to pytest methods. the max limit of number of products can be retrieved in a 
single call is 200. this method takes the following input params:
- from_date
- to_date

#### product_variations
the `CommerceApi.product_variations` is used for variant information of a given product.
input param is `productid`.

#### orders_by_creation_date
orders information can be retrieved using the method `CommerceApi.product_variations`
for a given date range.
input params are `start_date` and `end_date`

#### get_orders_by_modified_date_page
`CommerceApi.get_orders_by_modified_date_page` method can be used for retrieving
orders information by last modified date.
input params are `start_date`, `end_date`
optional params are `page` and `limit`

### example test method usage
#### test fixture definition:
```python
@pytest.fixture(scope='session')
def api(sfcc_config):
    from treasury.api import CommerceApi
    return CommerceApi(sfcc_config)
```
#### writing a test
```python
# this would retrieve all products between given date range by last modified date
def test_search_modified_products(api):
    """
    can we get all products between date range
    """
    # get product info
    a = api.products_last_modified('2023-01-04T00:00:00.000Z', '2023-01-05T00:00:00.000Z')
```

### project test, build and publish to pypi.org

* `make test` -- for running the test cases
* `make build` -- build the project to identify potential errors within the code
* `make publish` -- deploy the project in pypi.org under `treasury` project
