# coding=utf-8
import typing


from django.template.base import FilterExpression, token_kwargs
from django.template.exceptions import TemplateSyntaxError


class ParsedArguments(object):
    def __init__(self, parameters: typing.Mapping[str, 'FilterExpression']):
        self.parameters = parameters

    def resolve(self, context) -> typing.Mapping[str, object]:
        return {
            k: v.resolve(context)
            for k, v in self.parameters.items()
        }


class TagParser(object):

    def __init__(
        self,
        args: typing.List[str],
        kwargs: typing.List[str] = tuple(),
        opt_kwargs: typing.Sequence[str] = tuple()
    ):
        self.args = args
        self.kwargs = kwargs
        self.opt_kwargs = opt_kwargs

    def parse(self, parser, token) -> ParsedArguments:
        p = _Parser(
            args=list(self.args),
            kwargs=list(self.kwargs),
            opt_kwargs=list(self.opt_kwargs),
        )
        return p.parse(parser, token)


class _Parser(object):
    """

    This objects keeps state, hence it is not thread-safe.

    It is used in TagParser which is thread safe.
    """

    def __init__(
            self,
            args: typing.List[str],
            kwargs: typing.List[str] = tuple(),
            opt_kwargs: typing.Sequence[str] = tuple()
    ):
        self.name = None
        self.args = args
        self.kwargs = kwargs
        self.opt_kwargs = opt_kwargs
        self.unparsed_args = list(args)
        self.result = {}

    def parse(self, parser, token) -> ParsedArguments:
        bits = token.split_contents()
        self.name = bits.pop(0)
        for bit in bits:
            self.parse_bit(parser, bit)
        self.finish_parsing()
        return ParsedArguments(self.result)

    def parse_as_kwarg(self, kwarg):
        if self.unparsed_args:
            raise TemplateSyntaxError(self.__KWARGS_BEFORE_KW.format(self.name, self.unparsed_args))
        param_name, expression = kwarg.popitem()
        if param_name in self.result:
            raise TemplateSyntaxError(self.__DUPLICATED_ARG.format(self.name, param_name))
        self.result[param_name] = expression

    def parse_as_positional_args(self, expression):
        if not self.unparsed_args:
            raise TemplateSyntaxError(self.__TOO_MANY_POSITIONAL_ARGS.format(self.name, self.unparsed_args))
        param_name = self.unparsed_args.pop(0)
        self.result[param_name] = expression

    def parse_bit(self, parser, bit):
        kwarg = token_kwargs([bit], parser)
        if kwarg:
            self.parse_as_kwarg(kwarg)
        else:
            self.parse_as_positional_args(parser.compile_filter(bit))

    def finish_parsing(self):
        if self.unparsed_args:
            raise TemplateSyntaxError(self.__TOO_MANY_POSITIONAL_ARGS.format(self.name, self.unparsed_args))
        all_args = self.result.keys()
        required_kwargs = set(self.kwargs)
        missing = required_kwargs - all_args
        if missing:
            raise TemplateSyntaxError(self.__MISSING_KWARGS.format(self.name, missing))

    __KWARGS_BEFORE_KW = "Tag {} got keyword arguments while there are unparesed positional arguments {}"
    __DUPLICATED_ARG = "Tag {} got duplicate argument: {}"
    __TOO_MANY_POSITIONAL_ARGS = "Tag {} has extra positional args: {}"
    __MISSING_POSITIONAL_ARGS = "Tag {} has positional args unfilled: {}"
    __MISSING_KWARGS = "Tag {} has missing positional args {}"

