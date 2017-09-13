
    Usage:

    .. code-block::


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
