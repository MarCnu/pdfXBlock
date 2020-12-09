import pytest
from mock import Mock

from workbench.runtime import WorkbenchRuntime
from xblock.fields import ScopeIds
from xblock.runtime import DictKeyValueStore, KvsFieldData

from pdf.pdf import PDFXBlock


def generate_scope_ids(runtime, block_type):
    """ helper to generate scope IDs for an XBlock """
    def_id = runtime.id_generator.create_definition(block_type)
    usage_id = runtime.id_generator.create_usage(def_id)
    return ScopeIds('user', block_type, def_id, usage_id)


@pytest.fixture
def pdf_xblock():
    """PDF XBlock pytest fixture."""
    runtime = WorkbenchRuntime()
    key_store = DictKeyValueStore()
    db_model = KvsFieldData(key_store)
    ids = generate_scope_ids(runtime, 'pdf')
    pdf_xblock = PDFXBlock(runtime, db_model, scope_ids=ids)
    pdf_xblock.usage_id = Mock()
    return pdf_xblock
