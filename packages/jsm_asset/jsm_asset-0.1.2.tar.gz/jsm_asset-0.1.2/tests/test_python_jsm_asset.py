import os
import logging
import pytest
from jsm_asset import asset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def jsm_session():
    print("Setting up JSM session fixture")
    # require environment variables to be set by the user/CI
    session = asset.AssetSession(email=os.environ['JSM_USERNAME'], api_token=os.environ['JSM_API_KEY'],
            jira_site_url=os.environ.get('JSM_INSTANCE_URL') or os.environ.get('JIRA_INSTANCE_URL'))
    yield session
    print("Tearing down JSM session fixture")


@pytest.fixture
def jsm_test_schema(jsm_session):
    # Make the fixtures defensive when the API is not reachable
    existing_schemas = [schema for schema in (jsm_session.schemas or {}).values() if getattr(schema, 'name', None) == 'pytest Schema']
    for schema in existing_schemas:
        try:
            schema.delete()
        except Exception:
            logger.exception('Failed to delete existing schema during test setup')
    print("Setting up JSM test schema fixture")
    schema = jsm_session.create_schema(object_schema_key='PTEST', name='pytest Schema', description='A schema for testing python_jsm_asset')
    yield schema
    if schema:
        try:
            schema.delete()
        except Exception:
            logger.exception('Failed to delete schema during teardown')
    print("Tearing down JSM test schema fixture")


@pytest.fixture
def jsm_test_objecttype(jsm_test_schema):
    print("Setting up JSM test object type fixture")
    obj_type = None
    if jsm_test_schema:
        obj_type = jsm_test_schema.create_object_type(name='pytest ObjectType')
    yield obj_type
    if obj_type:
        try:
            obj_type.delete()
        except Exception:
            logger.exception('Failed to delete objecttype during teardown')
    print("Tearing down JSM test object type fixture")


@pytest.fixture
def jsm_test_object(jsm_test_objecttype):
    print("Setting up JSM test object fixture")
    obj = None
    if jsm_test_objecttype:
        obj = jsm_test_objecttype.create_object(name='pytest Object')
    yield obj
    if obj:
        try:
            obj.delete()
        except Exception:
            logger.exception('Failed to delete object during teardown')
    print("Tearing down JSM test object fixture")


def test_jsm_session(jsm_session):
    assert jsm_session is not None
    assert jsm_session.workspace is not None
    assert jsm_session.asset_api_url is not None
    # Note: environment variable name may vary between setups; accept either
    assert jsm_session.jira_site_url in (os.environ.get('JIRA_INSTANCE_URL'), os.environ.get('JSM_INSTANCE_URL'))
    assert jsm_session.schemas is not None
    assert not jsm_session.asset_api_url.endswith("/")
