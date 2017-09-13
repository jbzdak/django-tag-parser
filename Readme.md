A simple django tag parsing library, it simplifies
parsing your custom tags, for example let's say 
you want to parse following tag: 

     {% tag_name "labour_market" language=object.language template="template"%}

Keyword arguments (in this example) are optional. 

To install: 
   
    pip install simple-django-tag-parser

Usage:

    import django_tag_parser

    @register.tag("page_block")
    def do_page_block(parser, token):
        parser_parse = django_tag_parser.TagParser(
            args=["block_type"],
            opt_kwargs=["template_name", "language"]
        )

        return PageNode(parser_parse.parse(parser, token))

    class PageNode(template.None):
      
      def __init__(self, parsed_args):
        super().__init__()
        self.parsed_args = parsed_args


      def render(self, context):
        arguments = self.parsed_args.resolve(context) 
        language = resolved.get('language', None)
        block_type = resolved['block_type']
        # ...
        return template.render(ctx)


Requirements: 

* Recent Django (Tested with 1.11)
* Python ``3.5+`` (parameter annotations are used)
2
