from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import models
import json

def get_products(request: HttpRequest) -> HttpResponse:

    return HttpResponse('Hello Django!')


def get_product_by_id(request: HttpRequest) -> HttpResponse:

    return HttpResponse('Hello Django!')


def post_product(request: HttpRequest) -> HttpResponse:

    return HttpResponse('Hello Django!')
