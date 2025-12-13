from upyog.ml.imports import *
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from timm.data.imagenet_info import ImageNetInfo
import nltk

def get_all_hypernyms(synset: Synset):
    return list(synset.closure(lambda s: s.hypernyms()))

def get_hyponyms(synset: Synset):
    return synset.hyponyms()

def get_imagenet_1k_classes():
    ds = ImageNetInfo("imagenet-1k")
    ds.label_descriptions()
