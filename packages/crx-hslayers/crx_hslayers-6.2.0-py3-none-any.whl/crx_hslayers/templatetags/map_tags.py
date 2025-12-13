from django import template
from random import randint

register = template.Library()

@register.simple_tag
def generate_hash(length=10):
  i = 1
  hash = ''
  characters = 'zxcvbnmlkjhgfdsaqwertyuiopZXCVBNMLKJHGFDSAQWERTYUIOP123456789'
  charLen = len(characters) - 1
  while i <= length:
    hash += characters[randint(0, charLen)]
    i += 1

  return hash
