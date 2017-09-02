# coding=utf-8

from invoke import task


@task
def pep8(ctx):
  ctx.run("pep8 django_tag_parser django_tag_parser_test")


@task
def lint(ctx):
  ctx.run("pylint django_tag_parser django_tag_parser_test -r n")


@task
def test(ctx):
  ctx.run("py.test -v --cov django_tag_parser --cov-report=html --cov-report=term-missing django_tag_parser_test")


@task(pre=[test, pep8, lint])
def check(ctx):
  pass




