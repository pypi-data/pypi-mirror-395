from typing import Any

from ..api import CommerceApi
try:
    from airflow.hooks.base import BaseHook
    from airflow.compat.functools import cached_property
    from airflow.utils.types import NOTSET
    from airflow.utils.log.secrets_masker import mask_secret
except ImportError:
    from functools import cached_property


    class BaseHook:
        pass


    class ConnectionExtraConfig:
        def __init__(self, **kwargs):
            pass


    class NotSet:
        pass


    NOTSET = NotSet()


    def mask_secret(*args, **kwargs):
        pass


class TreasuryHook(BaseHook):
    """
    this class allows you to interact with the salesforce commerce cloud
    b2c commerce api by making use of the treasury api client.
    """

    conn_name_attr = 'treasury_conn_id'
    default_conn_name = 'treasury_default'
    conn_type = 'treasury_sfcc'
    hook_name = 'treasury sfcc b2c commerce api'
    default_scopes = {
        'mail',
        'roles',
        'tenantFilter',
        'profile',
        'openId',
    }

    def __init__(self, treasury_conn_id=None, timeout=None, **kwargs):
        super().__init__()
        self.treasury_conn_id = treasury_conn_id
        self.timeout = timeout or 300
        self.extra = kwargs

    @cached_property
    def api(self) -> CommerceApi:
        """Get the underlying slack_sdk.webhook.WebhookClient (cached)."""
        return CommerceApi(**self.get_connection_params())

    def get_connection_params(self):
        if self.treasury_conn_id:
            conn = self.get_connection(self.treasury_conn_id)
        else:
            conn = self.get_connection(self.default_conn_name)
        extra = conn.extra_dejson
        scopes = extra.get('scopes') or []
        if scopes:
            scopes = scopes.split(',')
            scopes = [ x.strip() for x in scopes if x ]
        scopes = set(scopes) | self.default_scopes
        timeout = extra.get('timeout')
        if timeout:
            try:
                timeout = int(timeout)
            except ValueError:
                self.log.warning('timeout was non-numeric')
        params = {
            'client_id': conn.login,
            'base_url': conn.host,
            'site_id': extra['site_id'],
            'scopes': list(scopes),
            'password': conn.password,
            'organization_id': conn.schema,
        }
        if timeout:
            params['timeout'] = timeout
        return params

    @classmethod
    def get_connection_form_widgets(cls) -> dict[str, Any]:
        """
        Returns dictionary of widgets to be added for the hook to handle extra values.
        """
        from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import IntegerField, StringField
        from wtforms.validators import NumberRange, Optional, DataRequired

        return {
            "timeout": IntegerField(
                lazy_gettext("timeout"),
                widget=BS3TextFieldWidget(),
                validators=[Optional(), NumberRange(min=1)],
                description="Optional. The maximum number of seconds the "
                            "client will wait to connect for a response from "
                            "the commerce api.",
            ),
            "scopes": StringField(
                lazy_gettext("scopes"),
                widget=BS3TextFieldWidget(),
                validators=[DataRequired()],
                description="list of scopes to use when connecting to the api."
                            "  separate scopes with a comma.",
            ),
            "site_id": StringField(
                lazy_gettext("site_id"),
                widget=BS3TextFieldWidget(),
                validators=[DataRequired()],
                description="the b2c commerce site id.",
            ),
        }

    @classmethod
    def get_ui_field_behaviour(cls) -> dict[str, Any]:
        """Returns custom field behaviour."""
        return {
            "hidden_fields": ["port", "extra"],
            "relabeling": {
                "host": "base_url",
                "login": "client_id",
                "password": "client_secret / password",
                "schema": "organization_id",
            },
            "placeholders": {
                "schema": "q_ecom_abcd_tst",
                "host": "https://abcde1fg.api.commercecloud.salesforce.com",
                "login": "abcdef01-1234-1234-1234-0123456789ab",
                "password": "abcdef1234567890",
                "timeout": "300",
                "scopes": "sfcc.orders,sfcc.promotions",
                'site_id': 'MYSITE',
            },
        }
