""" Unit tests for PDF XBlock """

from mock import Mock


def test_pdf_template_content(pdf_xblock):
    """ Test content of pdfXBlock's student view """
    student_fragment = pdf_xblock.render('student_view', Mock())
    assert 'pdf' in student_fragment.content


def test_pdf_studio_view(pdf_xblock):
    """ Test content of pdfXBlock's author view """
    student_fragment = pdf_xblock.render('studio_view', Mock())
    assert 'pdf' in student_fragment.content


def test_pdf_save_pdf(pdf_xblock):
    """ Test content of pdfXBlock's save action """
    request_body = b"""{
        "display_name": "foo",
        "url": "https://example.com",
        "allow_download": "True",
        "source_text": "A link",
        "source_url": "https://example.com/1.pdf"
    }"""
    request = Mock(method='POST', body=request_body)
    response = pdf_xblock.save_pdf(request)
    assert response.status_code == 200 and {'result': 'success'} == response.json
