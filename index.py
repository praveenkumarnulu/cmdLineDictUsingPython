#!/usr/bin/env python
import click
import sys
# from .apilogic import *

import importlib
l = importlib.import_module('apilogic')


if len(sys.argv) == 1:
    l.get_random_word()
    print("Ïts working")
if len(sys.argv) == 2 and sys.argv[1] != 'play':
    l.get_full_dict(sys.argv[1])
elif len(sys.argv) == 2 and sys.argv[1] == 'play':
    l.play()
    click.echo("Inside top play")

@click.group()
def main():
    pass


@main.command()
@click.argument('word')
# @click.option('--greeting', '-g')
def defn(word):
    l.get_defn(word)
    click.echo("The entered word is:  {} ".format(word))


@main.command()
@click.argument('word')
# @click.option('--greeting', '-g')
def syn(word):
    l.get_syn(word)
    click.echo(" {} ".format(word))



@main.command()
@click.argument('word')
# @click.option('--greeting', '-g')
def ant(word):
    l.get_ant(word)
    click.echo(" {} ".format(word))


@main.command()
@click.argument('word')
# @click.option('--greeting', '-g')
def ex(word):
    l.get_examples(word)
    click.echo(" {} ".format(word))


# @main.command(name='play')
# # @click.argument()
# @click.option('--greeting', '-g')
# def play(greeting):
#     # l.play()
#     click.echo('Inside play')


if __name__ == "__main__" and len(sys.argv) > 2:
    main()