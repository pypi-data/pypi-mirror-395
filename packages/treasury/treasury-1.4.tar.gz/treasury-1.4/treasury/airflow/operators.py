from datetime import datetime, timedelta
from itertools import chain
import logging
import json
import os
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4
from pathlib import Path
import gzip

try:
    from airflow.models.baseoperator import BaseOperator
    from airflow.models.connection import Connection as AirflowConnection
except:
    class BaseOperator:
        template_fields = []

def open_writer(path: str, *, compresslevel: int = 6, newline: str = "\n"):
    """Open a text writer; transparently gzip if filename ends with .gz/.gzip."""
    if path.lower().endswith((".gz", ".gzip")):
        return gzip.open(path, mode="wt", encoding="utf-8", compresslevel=compresslevel, newline=newline)
    return open(path, mode="w", encoding="utf-8", newline=newline)

def ensure_dir(path: str) -> None:
    """Ensure parent directory exists."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)

def write_jsonl(filename, rows, postgres: bool = False, mode: str = "w", encoder_klass=None, **params):
    """
    Write one JSON document per line to `filename`.

    If postgres=True, double backslashes so that COPY (FORMAT text) does not
    eat JSON escaping (e.g., \" in HTML markup) and break the JSON stored in `doc`.
    """
    with open(filename, mode, encoding="utf-8") as f:
        for x in rows:
            if postgres:
                # json.dumps gives valid JSON; replacing '\' with '\\'
                # makes COPY(TEXT) store the correct escaped string again.
                st = json.dumps(x, cls=encoder_klass).replace("\\", "\\\\")
                f.write(st)
            else:
                json.dump(x, f, cls=encoder_klass)
            f.write("\n")

class TreasuryOrderUnload(BaseOperator):
    template_fields = list(BaseOperator.template_fields) + [
        'start_dttm',
        'end_dttm',
        'filename',
        'temp_dir',
    ]
    ui_color = '#161031'
    ui_fgcolor = '#de7900'
    do_xcom_push = True

    def __init__(
            self,
            *args,
            treasury_conn_id,
            temp_dir,
            filename=None,
            start_dttm=None,
            end_dttm=None,
            **kwargs):
        log = logging.getLogger(__name__)
        log.info('treasury unload operator: %s', kwargs['task_id'])
        super().__init__(*args, **kwargs)
        self.treasury_conn_id = treasury_conn_id
        self.filename = None
        self.api = None
        self.start_dttm = start_dttm
        self.end_dttm = end_dttm
        self.temp_dir = temp_dir
        self.filename = filename

    def output_filename(self):
        if self.filename:
            return os.path.join(self.temp_dir, self.filename)
        return os.path.join(self.temp_dir, uuid4().hex)

    def get_orders(self, output_filename, context):
        from .hooks import TreasuryHook
        hook = TreasuryHook(self.treasury_conn_id)
        self.log.info('looking for orders created between %s => %s', self.start_dttm, self.end_dttm)
        r1 = hook.api.orders_by_creation_date(self.start_dttm, self.end_dttm)
        self.log.info('looking for orders modified between %s => %s', self.start_dttm, self.end_dttm)
        r2 = hook.api.orders_by_modified_date(self.start_dttm, self.end_dttm)
        rg = []
        order_numbers = set()
        for x in chain(r1, r2):
            order_number = x['orderNo']
            if order_number not in order_numbers:
                order_numbers.add(order_number)
                rg.append(x)
        self.log.info('loaded %s orders', len(rg))
        with open(output_filename, 'w') as f:
            for x in rg:
                json.dump(x, f)
                f.write('\n')
        self.log.info('output filename: %s', output_filename)

    def execute(self, context) -> Any:
        output_filename = self.output_filename()
        self.get_orders(self.start_dttm, self.end_dttm)
        return output_filename


class TreasuryCouponUnload(BaseOperator):
    template_fields = list(BaseOperator.template_fields) + [
        'start_dttm',
        'end_dttm',
        'filename',
        'temp_dir',
    ]
    ui_color = '#161031'
    ui_fgcolor = '#de7900'
    do_xcom_push = True

    def __init__(
            self,
            *args,
            treasury_conn_id,
            temp_dir,
            filename=None,
            start_dttm=None,
            end_dttm=None,
            **kwargs):
        log = logging.getLogger(__name__)
        log.info('treasury unload operator: %s', kwargs['task_id'])
        super().__init__(*args, **kwargs)
        self.treasury_conn_id = treasury_conn_id
        self.filename = None
        self.api = None
        self.start_dttm = start_dttm
        self.end_dttm = end_dttm
        self.temp_dir = temp_dir
        self.filename = filename

    def output_filename(self):
        if self.filename:
            return os.path.join(self.temp_dir, self.filename)
        return os.path.join(self.temp_dir, uuid4().hex)

    def get_coupons(self, output_filename, context):
        from .hooks import TreasuryHook
        hook = TreasuryHook(self.treasury_conn_id)
        rg = list(hook.api.get_coupons())
        self.log.info('loaded %s coupons', len(rg))
        with open(output_filename, 'w') as f:
            for x in rg:
                json.dump(x, f)
                f.write('\n')
        self.log.info('output filename: %s', output_filename)

    def execute(self, context) -> Any:
        output_filename = self.output_filename()
        self.get_coupons(self.start_dttm, self.end_dttm)
        return output_filename

# ------------------------------------------------------------------------------
# Catalogs / Categories (taxonomy) — no yield_from_search dependency
# ------------------------------------------------------------------------------

class TreasuryCatalogUnload(BaseOperator):
    """
    Export SFCC catalogs/categories (taxonomy) as JSON-L (one doc per line).
    Each line is a category JSON with an added "catalogId" field.

    - Catalogs:  GET  /product/catalogs/v1/organizations/{org}/catalogs
    - Categories: POST /catalogs/{catalogId}/categories/search?levels={levels}
                  (manual paging with limit/offset)

    """
    treasury_conn_id: str
    temp_dir: str
    filename: Optional[str]
    page_limit: int
    levels: int

    template_fields = list(BaseOperator.template_fields) + [
        'filename',
        'temp_dir',
    ]
    ui_color = '#161031'
    ui_fgcolor = '#de7900'
    do_xcom_push = True

    def __init__(
        self,
        *args,
        treasury_conn_id: str,
        temp_dir: str,
        filename: Optional[str] = None,
        page_limit: int = 200,
        levels: int = 1,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.treasury_conn_id = treasury_conn_id
        self.temp_dir = temp_dir
        self.filename = filename
        self.page_limit = page_limit
        self.levels = levels

    # -------- utilities --------

    def output_filename(self) -> str:
        return (
            os.path.join(self.temp_dir, self.filename)
            if self.filename
            else os.path.join(self.temp_dir, uuid4().hex)
        )


    def iter_catalogs(self, api: Any, limit: int) -> Iterable[Dict[str, Any]]:
        """
        GET /product/catalogs/v1/organizations/{org}/catalogs (paged)
        """
        url = f"{api.base_catalog_url}"
        params: Dict[str, Any] = {'limit': limit, 'offset': 0}
        while True:
            r: Dict[str, Any] = api.get(url, params)  # auth/headers handled by client
            items: List[Dict[str, Any]] = (
                r.get('data') or r.get('hits') or r.get('catalogs') or []
            )
            if not items:
                break
            for it in items:
                yield it
            total = r.get('total', len(items))
            params['offset'] += limit
            if params['offset'] >= total:
                break

    def iter_categories(
        self, api: Any, catalog_id: str, limit: int, levels: int
    ) -> Iterable[Dict[str, Any]]:
        """
        POST /catalogs/{catalogId}/categories/search?levels={levels}
        Manual paging with limit/offset and explicit siteId param.
        """
        route = f"{api.base_catalog_url}/{catalog_id}/categories"

        offset = 0
        while True:

            params: Dict[str, Any] = {
                'limit': limit,
                'offset': offset,
            }

            # NOTE: GET, not POST
            r: Dict[str, Any] = api.get(route, params)

            # SCAPI collections usually use `data`, but be defensive
            hits: List[Dict[str, Any]] = (
                    r.get('data') or r.get('categories') or r.get('hits') or []
            )

            if not hits:
                break
            for cat in hits:
                yield cat
            total = r.get('total', len(hits))
            offset += limit
            if offset >= total:
                break

    # -------- main work --------

    def dump_catalogs(self, output_filename: str, api: Any | None = None) -> None:
        if api is None:
            from .hooks import TreasuryHook  # local import to avoid Airflow import cycles
            hook = TreasuryHook(self.treasury_conn_id)
            api = hook.api

        # ensure directory
        d = os.path.dirname(output_filename)
        if d:
            os.makedirs(d, exist_ok=True)

        count = 0
        # with open(output_filename, 'w', encoding='utf-8') as f:
        def rows() -> Iterable[Dict[str, Any]]:
            nonlocal count
            for catlg in self.iter_catalogs(api, limit=self.page_limit):
                catalog_id = catlg.get('id') or catlg.get('catalogId')
                if not catalog_id:
                    continue
                for cat in self.iter_categories(
                    api, catalog_id, limit=self.page_limit, levels=self.levels
                ):
                    rec = dict(cat)
                    rec.setdefault('catalogId', catalog_id)
                    # json.dump(rec, f, ensure_ascii=False)
                    # f.write('\n')
                    # n += 1
                    yield rec
        write_jsonl(output_filename, rows(), postgres=True)

        self.log.info(
            'catalog taxonomy: wrote %s category docs to %s', count, output_filename
        )

    def execute(self, context: Any) -> str:
        output_filename = self.output_filename()
        self.dump_catalogs(output_filename)
        return output_filename