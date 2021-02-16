from __future__ import absolute_import
from celery.decorators import task
import crawling
import categorize

@task(name="say_hello")
def say_hello():
    print("Hello, celery")

@task(name="main_process")
def main_process():
    categorize.diverge("다크웹")
