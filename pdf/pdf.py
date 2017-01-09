""" pdfXBlock main Python class"""

import pkg_resources
from django.template import Context, Template

from webob.response import Response
from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment
from xblock_django.mixins import FileUploadMixin


class pdfXBlock(XBlock, FileUploadMixin):
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

    display_description = String(display_name="Display Description",
                          default="An XBlock to view PDFs",
                          scope=Scope.settings,
                          help="This description appears in the horizontal navigation at the top of the page.")

    url = String(display_name="PDF URL",
                 default="",
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
            'source_url': self.source_url,
            'thumbnail_url': self.thumbnail_url,
            'display_description': self.display_description
        }
        html = self.render_template('static/html/pdf_view.html', context)

        if hasattr(self, 'thumbnail_url'):
            print '///////////////////////////////////////' + str(self.thumbnail_url)

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
            'source_url': self.source_url,
            'display_description': self.display_description
        }
        html = self.render_template('static/html/pdf_edit.html', context)

        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/pdf_edit.js"))
        frag.initialize_js('pdfXBlockInitEdit')
        return frag

    @XBlock.handler
    def save_pdf(self, request, suffix=''):
        """
        The saving handler.
        """

        data = request.POST

        if 'display_name' in data:
            self.display_name = data['display_name']
        if 'allow_download' in data:
            self.allow_download = True if data['allow_download'] == "True" else False  # Str to Bool translation
        if 'source_text' in data:
            self.source_text = data['source_text']
        if 'source_url' in data:
            self.source_url = data['source_url']
        if 'display_description' in data:
            self.display_description = data['display_description']

        if 'pdf_file' in data:
            block_id = data['usage_id']
            if not isinstance(data['pdf_file'], basestring):
                upload = data['pdf_file']
                self.url = self.upload_to_s3('PDF', upload.file, block_id, self.url)

        if 'thumbnail' in data:
            block_id = data['usage_id']
            if not isinstance(data['thumbnail'], basestring):
                upload = data['thumbnail']
                self.thumbnail_url = self.upload_to_s3('THUMBNAIL', upload.file, block_id, self.thumbnail_url)

        return Response(json_body={
            'result': "success"
        })
