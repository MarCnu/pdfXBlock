""" pdfXBlock main Python class"""

import pkg_resources
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment

class pdfXBlock(XBlock):

    '''
    Icon of the XBlock. Values : [other (default), video, problem]
    '''
    icon_class = "other"

    '''
    Fields
    '''
    display_name = String(display_name="Display Name",
        default="PDF",
        scope=Scope.settings,
        help="This name appears in the horizontal navigation at the top of the page.")

    url = String(display_name="PDF URL",
        default="https://www.bced.gov.bc.ca/exams/specs/resource_exams/precalc12/2013precalc_formula_page.pdf",
        scope=Scope.content,
        help="The URL for your PDF.")
    
    allow_download = Boolean(display_name="PDF Download Allowed",
        default=True,
        scope=Scope.content,
        help="Display a download button for this PDF.")
    
    source_text = String(display_name="Source document button text",
        default="",
        scope=Scope.content,
        help="Add a download link for the source file of your PDF. Use it for example to provide the PowerPoint file used to create this PDF.")
    
    source_url = String(display_name="Source document URL",
        default="",
        scope=Scope.content,
        help="Add a download link for the source file of your PDF. Use it for example to provide the PowerPoint file used to create this PDF.")

    '''
    Util functions
    '''
    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return unicode(resource_content)

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    '''
    Main functions
    '''
    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """
        
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_url': self.source_url
        }
        html = self.render_template('static/html/pdf_view.html', context)
        
        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/pdf.css"))
        frag.add_javascript(self.load_resource("static/js/pdf_view.js"))
        frag.initialize_js('pdfXBlockInitView')
        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_url': self.source_url
        }
        html = self.render_template('static/html/pdf_edit.html', context)
        
        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/pdf_edit.js"))
        frag.initialize_js('pdfXBlockInitEdit')
        return frag

    @XBlock.json_handler
    def save_pdf(self, data, suffix=''):
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']
        self.allow_download = True if data['allow_download'] == "True" else False # Str to Bool translation
        self.source_text = data['source_text']
        self.source_url = data['source_url']
        
        return {
            'result': 'success',
        }
