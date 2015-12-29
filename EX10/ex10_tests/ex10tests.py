from autotest import TestSet

import sys
from importlib import import_module
import itertools as it
from ast import literal_eval
from io import StringIO
import operator as op
import os

import testrunners

def ident(res):
    return res

def repreval(res):
    try:
        if isinstance(res,(tuple,list,set,dict,str)):
            return res,None
        return literal_eval(repr(res))
    except Exception:
        return res

def sortarticle(res):
    try:
        if type(res) is str:
            return res
        res = literal_eval(repr(res))
        if type(res) is not tuple or len(res)!=2:
            return res
        return tuple([res[0],type(res[1])(sorted(res[1]))])
    except Exception:
        return res

def sortarticlelist(res):
    try:
        if type(res) is not list:
            return res
        return [sortarticle(r) for r in res]
    except Exception:
        return res
    
def modans(res):
    if type(res)==list:
        cp = res[:]
        res[:1]=[(3,3)]
    return cp

def itertocycle(res):
    try:
        if iter(res) is not res:
            return res,False
        list_ = []
        for val in res:
            list_.append(val)
            if list_.index(val) != len(list_)-1:
                break
        return list_
    except Exception:
        return res
    
def article_runner(modulename, fname, args=[], kwargs={}, options={}, tname=''):
    module = import_module(modulename)
    func = getattr(module, 'Article')
    articles = [func(a) for a in 'abcd']
    if 'empty' not in options: #a->bcd.b->cd,d->a
        articles[0].add_neighbor(articles[1])
        articles[0].add_neighbor(articles[2])
        articles[0].add_neighbor(articles[3])
        articles[1].add_neighbor(articles[2])
        articles[1].add_neighbor(articles[3])
        articles[3].add_neighbor(articles[0])
    if 'runopts' in options:
        f, target, filt = options.pop('runopts')
        return None,(sortarticlelist(articles),
                     filt(getattr(articles[target], f)(*[articles[a] if type(a) is int else a for a in args])),
                     sortarticlelist(articles))
    else:
        return None,sortarticlelist(articles)
        

def unorderedlists(exp,ans):
    return type(exp) == type(ans) and sorted(exp) == sorted(ans)

def midunorderedlists(exp,ans):
    return (type(exp) == type(ans) and
            len(exp) == len(ans) and
            exp[0] == ans[0] and
            sorted(exp[1]) == sorted(ans[1]) and
            exp[2] == ans[2])


def articlecompare(exp,ans):
    return (type(exp) == type(ans) and
            len(exp) == len(ans) and
            exp[0]==ans[0] and
            unorderedlists(exp[1],ans[1]))

def articlelistcompare(exp,ans):
    return (type(exp) == type(ans) and
            len(exp) == len(ans) and
            all(articlecompare(e,a) for e,a in zip(exp,ans)))

def articletriplecompare(exp,ans):
    return (type(exp) == type(ans) and
            len(exp) == len(ans) and
            articlelistcompare(exp[0],ans[0]) and
            articlelistcompare(exp[2],ans[2]) and
            exp[1] == ans[1])

defaults = {}

articledefaults = {'modulename':'ex10',
                   'runner':article_runner,
                   'fname':'Article',
                   'args':[],
                }

emptystr = [('a',[]),('b',[]),('c',[]),('d',[])]
fullstr = [('a',['b','c','d']),('b',['c','d']),('c',[]),('d',['a'])]

artcases = {'empty':{'options':{'empty':None},
                     'ans':[emptystr],
                     'comparemethod':op.eq,
                     },
            'full':{'options':{}, #a->bcd.b->cd,c->,d->a
                    'ans':[fullstr],
                    'comparemethod':articlelistcompare,
                     },
            'len0':{'options':{'empty':None,'runopts':['__len__',2,ident]},
                    'ans':[(emptystr,0,emptystr)],
                    'comparemethod':articletriplecompare,
                     },
            'len3':{'options':{'runopts':['__len__',0,ident]},
                    'ans':[(fullstr,3,fullstr)],
                    'comparemethod':articletriplecompare,
                     },
            'in_0':{'options':{'empty':None,'runopts':['__contains__',2,ident]},
                   'args':[1],
                    'ans':[(emptystr,False,emptystr)],
                    'comparemethod':articletriplecompare,
                     },
            'in_n':{'options':{'runopts':['__contains__',0,ident]},
                   'args':['b'],
                    'ans':[(fullstr,False,fullstr)],
                    'comparemethod':articletriplecompare,
                     },
            'in_f':{'options':{'runopts':['__contains__',1,ident]},
                   'args':[0],
                    'ans':[(fullstr,False,fullstr)],
                    'comparemethod':articletriplecompare,
                     },
            'in_t':{'options':{'runopts':['__contains__',0,ident]},
                   'args':[1],
                    'ans':[(fullstr,True,fullstr)],
                    'comparemethod':articletriplecompare,
                     },
            'name':{'options':{'runopts':['get_name',3,ident]},
                   'args':[],
                    'ans':[(fullstr,'d',fullstr)],
                    'comparemethod':articletriplecompare,
                     },
            'addneigh0':{'options':{'empty':None,'runopts':['add_neighbor',3,ident]},
                   'args':[2],
                    'ans':[(emptystr,None,emptystr[:-1]+[('d',['c'])])],
                    'comparemethod':articletriplecompare,
                     },
            'addneigh3':{'options':{'runopts':['add_neighbor',3,ident]},
                   'args':[2],
                    'ans':[(fullstr,None,fullstr[:-1]+[('d',['a','c'])])],
                    'comparemethod':articletriplecompare,
                     },
            'getneigh0':{'options':{'empty':None,'runopts':['get_neighbors',3,ident]},
                   'args':[],
                    'ans':[(emptystr,[],emptystr)],
                    'comparemethod':articletriplecompare,
                     },
            'getneigh3':{'options':{'runopts':['get_neighbors',3,sortarticlelist]},
                   'args':[],
                    'ans':[(fullstr,[('a',list('bcd'))],fullstr)],
                    'comparemethod':articletriplecompare,
                     },
    }


def midarticlelist(res):
    try:
        if type(res) is not list:
            return res
        return sorted(sortarticlelist(res))
    except Exception:
        return res
    
def sortednetwork(res):
    try:
        if type(res) is str:
            return res
        res = literal_eval(repr(res))
        if type(res) is not dict:
            return res
        return {key:sortarticle(val) for key,val in res.items()}
    except Exception:
        return res
    
def network_runner(modulename, fname, args=[], kwargs={}, options={}, tname=''):
    module = import_module(modulename)
    func = getattr(module, 'WikiNetwork')
    net = func(options.pop('net'))
    if fname is not None:
        filt = options.pop('filt')
        return None,(sortednetwork(net),
                     filt(getattr(net, fname)(*args)),
                     sortednetwork(net))
    else:
        return None,sortednetwork(net)
        


networkdefaults = {'modulename':'ex10', 
                   'runner':network_runner,
                   'fname':None,
                   'args':[],
                }

net0 = []

out0 = {}

net1 = list(zip('AABBCCD',
                'BECEAEA'))

out1 = {'A':('A',list('BE')),
        'B':('B',list('CE')),
        'C':('C',list('AE')),
        'D':('D',list('A')),
        'E':('E',list('')),
        }

net2 = list(zip('AAABBCD',
                'BCDCDDB'))

out2 = {'A':('A',list('BCD')),
        'B':('B',list('CD')),
        'C':('C',list('D')),
        'D':('D',list('B')),
        }

net3 = list(zip('aabbccdeefgggh',
                'bcefbdhghdbcdg'))

out3 = {'a':('a',list('bc')),
        'b':('b',list('ef')),
        'c':('c',list('bd')),
        'd':('d',list('h')),
        'e':('e',list('gh')),
        'f':('f',list('d')),
        'g':('g',list('bcd')),
        'h':('h',list('g')),
        }

out12 = {'A':('A',list('BCDE')),
        'B':('B',list('CDE')),
        'C':('C',list('ADE')),
        'D':('D',list('AB')),
        'E':('E',list('')),
        }
netcases = {'init0':{'options':{'net':net0,},
                     'ans':[out0],
                     },
            'init1':{'options':{'net':net1,},
                      'ans':[out1],
                      },
            'init2':{'options':{'net':net2,},
                      'ans':[out2],
                      },
            'init3':{'options':{'net':net3,},
                      'ans':[out3],
                      },
            'update03':{'options':{'net':net0,
                                   'filt':ident},
                        'fname':'update_network',
                        'args':[net3],
                      'ans':[(out0,None,out3)],
                      },
            'update30':{'options':{'net':net3,
                                   'filt':ident},
                        'fname':'update_network',
                      'args':[net0],
                      'ans':[(out3,None,out3)],
                      },
            'update21':{'options':{'net':net2,
                                   'filt':ident},
                        'fname':'update_network',
                        'args':[net1],
                      'ans':[(out2,None,out12)],
                      },
            'articles0':{'options':{'net':net0,
                                   'filt':midarticlelist},
                        'fname':'get_articles',
                         'args':[],
                         'ans':[(out0,[],out0)],
                      },
            'articles1':{'options':{'net':net1,
                                   'filt':midarticlelist},
                        'fname':'get_articles',
                         'args':[],
                         'ans':[(out1,sorted(out1.values()),out1)],
                      },
            'articles2':{'options':{'net':net2,
                                   'filt':midarticlelist},
                        'fname':'get_articles',
                         'args':[],
                         'ans':[(out2,sorted(out2.values()),out2)],
                      },
            'articles3':{'options':{'net':net3,
                                   'filt':midarticlelist},
                        'fname':'get_articles',
                         'args':[],
                         'ans':[(out3,sorted(out3.values()),out3)],
                      },
            'titles0':{'options':{'net':net0,
                                   'filt':ident},
                        'fname':'get_titles',
                         'args':[],
                         'ans':[(out0,[],out0)],
                       'comparemethod':midunorderedlists,
                      },
            'titles1':{'options':{'net':net1,
                                   'filt':ident},
                        'fname':'get_titles',
                         'args':[],
                         'ans':[(out1,list('ABCDE'),out1)],
                       'comparemethod':midunorderedlists,
                      },
            'titles2':{'options':{'net':net2,
                                   'filt':ident},
                        'fname':'get_titles',
                         'args':[],
                         'ans':[(out2,list('ABCD'),out2)],
                       'comparemethod':midunorderedlists,
                      },
            'titles3':{'options':{'net':net3,
                                   'filt':ident},
                        'fname':'get_titles',
                         'args':[],
                         'ans':[(out3,list('abcdefgh'),out3)],
                       'comparemethod':midunorderedlists,
                      },
            'contains0f':{'options':{'net':net0,
                                   'filt':ident},
                        'fname':'__contains__',
                         'args':['A'],
                         'ans':[(out0,False,out0)],
                      },
            'contains1f':{'options':{'net':net1,
                                   'filt':ident},
                        'fname':'__contains__',
                         'args':['e'],
                         'ans':[(out1,False,out1)],
                      },
            'contains2f':{'options':{'net':net2,
                                   'filt':ident},
                        'fname':'__contains__',
                         'args':['E'],
                         'ans':[(out2,False,out2)],
                      },
            'contains3f':{'options':{'net':net3,
                                   'filt':ident},
                        'fname':'__contains__',
                         'args':['dd'],
                         'ans':[(out3,False,out3)],
                      },
            'contains1t':{'options':{'net':net1,
                                   'filt':ident},
                        'fname':'__contains__',
                         'args':['E'],
                         'ans':[(out1,True,out1)],
                      },
            'contains2t':{'options':{'net':net2,
                                   'filt':ident},
                        'fname':'__contains__',
                         'args':['C'],
                         'ans':[(out2,True,out2)],
                      },
            'contains3t':{'options':{'net':net3,
                                   'filt':ident},
                        'fname':'__contains__',
                         'args':['d'],
                         'ans':[(out3,True,out3)],
                      },
            'getitem1':{'options':{'net':net1,
                                   'filt':repreval},
                        'fname':'__getitem__',
                         'args':['E'],
                         'ans':[(out1,('E',[]),out1)],
                      },
            'getitem2':{'options':{'net':net2,
                                   'filt':repreval},
                        'fname':'__getitem__',
                         'args':['C'],
                         'ans':[(out2,('C',['D']),out2)],
                      },
            'getitem3':{'options':{'net':net3,
                                   'filt':repreval},
                        'fname':'__getitem__',
                         'args':['d'],
                         'ans':[(out3,('d',['h']),out3)],
                      },
            'len0':{'options':{'net':net0,
                                   'filt':ident},
                        'fname':'__len__',
                         'args':[],
                         'ans':[(out0,0,out0)],
                      },
            'len1':{'options':{'net':net1,
                                   'filt':ident},
                        'fname':'__len__',
                         'args':[],
                         'ans':[(out1,5,out1)],
                      },
            'len2':{'options':{'net':net2,
                                   'filt':ident},
                        'fname':'__len__',
                         'args':[],
                         'ans':[(out2,4,out2)],
                      },
            'len3':{'options':{'net':net3,
                                   'filt':ident},
                        'fname':'__len__',
                         'args':[],
                         'ans':[(out3,8,out3)],
                      },

            }

pgrdefaults = {'modulename':'ex10', 
                   'runner':network_runner,
                   'fname':'page_rank',
                   'args':[],
                }

pgrcases = {'net2r0d8':{'options':{'net':net2,
                                   'filt':ident},
                        'args':[0,0.8],
                        'ans':[(out2,list('ABCD'),out2)],
                    },
            'net3r0d1':{'options':{'net':net3,
                                   'filt':ident},
                        'args':[0,0.1],
                        'ans':[(out3,list('abcdefgh'),out3)],
                    },
            'net0r1d9':{'options':{'net':net0,
                               'filt':ident},
                        'args':[1],
                        'ans':[(out0,[],out0)],
                    },
            'net2r1d9':{'options':{'net':net2,
                                   'filt':ident},
                        'args':[1],
                        'ans':[(out2,list('DBCA'),out2)],
                    },
            'net3r1d9':{'options':{'net':net3,
                                   'filt':ident},
                        'args':[1],
                        'ans':[(out3,list('dghbcefa'),out3),
                               (out3,list('dhgbcefa'),out3),
                               ],
                    },
            'net2r5d9':{'options':{'net':net2,
                                   'filt':ident},
                        'args':[5],
                        'ans':[(out2,list('BDCA'),out2)],
                    },
            'net3r5d9':{'options':{'net':net3,
                                   'filt':ident},
                        'args':[5],
                        'ans':[(out3,list('ghdbcefa'),out3)],
                    },
            'net2r5d2':{'options':{'net':net2,
                                   'filt':ident},
                        'args':[5,0.2],
                        'ans':[(out2,list('DBCA'),out2)],
                    },
            'net3r5d2':{'options':{'net':net3,
                                   'filt':ident},
                        'args':[5,0.2],
                        'ans':[(out3,list('dhgbcefa'),out3)],
                    },
            'net2r5d0':{'options':{'net':net2,
                                   'filt':ident},
                        'args':[5,0.0],
                        'ans':[(out2,list('ABCD'),out2)],
                    },
            'net3r5d0':{'options':{'net':net3,
                                   'filt':ident},
                        'args':[5,0.0],
                        'ans':[(out3,list('abcdefgh'),out3)],
                    },
            
            }

jacdefaults = {'modulename':'ex10', 
                   'runner':network_runner,
                   'fname':'jaccard_index',
                   'args':[],
                }

jaccases = {'net0':{'options':{'net':net0,
                               'filt':ident},
                    'args':['a'],
                    'ans':[(out0,None,out0)],
                    },
            'net1A':{'options':{'net':net1,
                                'filt':ident},
                     'args':['A'],
                     'ans':[(out1,list('ABCDE'),out1)],
                    },
            'net1B':{'options':{'net':net1,
                                'filt':ident},
                     'args':['B'],
                     'ans':[(out1,list('BACDE'),out1)],
                    },
            'net1C':{'options':{'net':net1,
                                'filt':ident},
                     'args':['C'],
                     'ans':[(out1,list('CDABE'),out1)],
                    },
            'net1D':{'options':{'net':net1,
                                'filt':ident},
                     'args':['D'],
                     'ans':[(out1,list('DCABE'),out1)],
                    },
            'net1E':{'options':{'net':net1,
                                'filt':ident},
                     'args':['E'],
                     'ans':[(out1,None,out1)],
                    },
            'net2A':{'options':{'net':net2,
                                'filt':ident},
                     'args':['A'],
                     'ans':[(out2,list('ABCD'),out2)],
                    },
            'net2B':{'options':{'net':net2,
                                'filt':ident},
                     'args':['B'],
                     'ans':[(out2,list('BACD'),out2)],
                    },
            'net2C':{'options':{'net':net2,
                                'filt':ident},
                     'args':['C'],
                     'ans':[(out2,list('CBAD'),out2)],
                    },
            'net2D':{'options':{'net':net2,
                                'filt':ident},
                     'args':['D'],
                     'ans':[(out2,list('DABC'),out2)],
                    },
            'net3a':{'options':{'net':net3,
                                'filt':ident},
                     'args':['a'],
                     'ans':[(out3,list('agcbdefh'),out3)],
                    },
            'net3b':{'options':{'net':net3,
                                'filt':ident},
                     'args':['b'],
                     'ans':[(out3,list('bacdefgh'),out3)],
                    },
            'net3c':{'options':{'net':net3,
                                'filt':ident},
                     'args':['c'],
                     'ans':[(out3,list('cgfabdeh'),out3)],
                    },
            'net3d':{'options':{'net':net3,
                                'filt':ident},
                     'args':['d'],
                     'ans':[(out3,list('deabcfgh'),out3)],
                    },
            'net3e':{'options':{'net':net3,
                                'filt':ident},
                     'args':['e'],
                     'ans':[(out3,list('edhabcfg'),out3)],
                    },
            'net3f':{'options':{'net':net3,
                                'filt':ident},
                     'args':['f'],
                     'ans':[(out3,list('fcgabdeh'),out3)],
                    },
            'net3g':{'options':{'net':net3,
                                'filt':ident},
                     'args':['g'],
                     'ans':[(out3,list('gacfbdeh'),out3)],
                    },
            'net3h':{'options':{'net':net3,
                                'filt':ident},
                     'args':['h'],
                     'ans':[(out3,list('heabcdfg'),out3)],
                    },
            }

cycdefaults = {'modulename':'ex10', 
                   'runner':network_runner,
                   'fname':'travel_path_iterator',
                   'args':[],
                }

cyccases = {'net0':{'options':{'net':net0,
                               'filt':itertocycle},
                    'args':['a'],
                    'ans':[(out0,[],out0)],
                    },
            'net1A':{'options':{'net':net1,
                                'filt':itertocycle},
                     'args':['A'],
                     'ans':[(out1,list('AE'),out1)],
                    },
            'net1B':{'options':{'net':net1,
                                'filt':itertocycle},
                     'args':['B'],
                     'ans':[(out1,list('BE'),out1)],
                    },
            'net1C':{'options':{'net':net1,
                                'filt':itertocycle},
                     'args':['C'],
                     'ans':[(out1,list('CE'),out1)],
                    },
            'net1D':{'options':{'net':net1,
                                'filt':itertocycle},
                     'args':['D'],
                     'ans':[(out1,list('DAE'),out1)],
                    },
            'net1E':{'options':{'net':net1,
                                'filt':itertocycle},
                     'args':['E'],
                     'ans':[(out1,list('E'),out1)],
                    },
            'net2A':{'options':{'net':net2,
                                'filt':itertocycle},
                     'args':['A'],
                     'ans':[(out2,list('ADBD'),out2)],
                    },
            'net2B':{'options':{'net':net2,
                                'filt':itertocycle},
                     'args':['B'],
                     'ans':[(out2,list('BDB'),out2)],
                    },
            'net2C':{'options':{'net':net2,
                                'filt':itertocycle},
                     'args':['C'],
                     'ans':[(out2,list('CDBD'),out2)],
                    },
            'net2D':{'options':{'net':net2,
                                'filt':itertocycle},
                     'args':['D'],
                     'ans':[(out2,list('DBD'),out2)],
                    },
            'net3a':{'options':{'net':net3,
                                'filt':itertocycle},
                     'args':['a'],
                     'ans':[(out3,list('abegb'),out3)],
                    },
            'net3b':{'options':{'net':net3,
                                'filt':itertocycle},
                     'args':['b'],
                     'ans':[(out3,list('begb'),out3)],
                    },
            'net3c':{'options':{'net':net3,
                                'filt':itertocycle},
                     'args':['c'],
                     'ans':[(out3,list('cbegb'),out3)],
                    },
            'net3d':{'options':{'net':net3,
                                'filt':itertocycle},
                     'args':['d'],
                     'ans':[(out3,list('dhgbeg'),out3)],
                    },
            'net3e':{'options':{'net':net3,
                                'filt':itertocycle},
                     'args':['e'],
                     'ans':[(out3,list('egbe'),out3)],
                    },
            'net3f':{'options':{'net':net3,
                                'filt':itertocycle},
                     'args':['f'],
                     'ans':[(out3,list('fdhgbeg'),out3)],
                    },
            'net3g':{'options':{'net':net3,
                                'filt':itertocycle},
                     'args':['g'],
                     'ans':[(out3,list('gbeg'),out3)],
                    },
            'net3h':{'options':{'net':net3,
                                'filt':itertocycle},
                     'args':['h'],
                     'ans':[(out3,list('hgbeg'),out3)],
                    },
            }

fridefaults = {'modulename':'ex10', 
               'runner':network_runner,
               'fname':'friends_by_depth',
               'args':[],
               'comparemethod':midunorderedlists,
             }

fricases = {'net0':{'options':{'net':net0,
                               'filt':ident},
                    'args':['a',0],
                    'ans':[(out0,None,out0)],
                    'comparemethod':op.eq,
                    },
            'net1A0':{'options':{'net':net1,
                                'filt':ident},
                     'args':['A',0],
                     'ans':[(out1,list('A'),out1)],
                    },
            'net1B0':{'options':{'net':net1,
                                'filt':ident},
                     'args':['B',0],
                     'ans':[(out1,list('B'),out1)],
                    },
            'net1C0':{'options':{'net':net1,
                                'filt':ident},
                     'args':['C',0],
                     'ans':[(out1,list('C'),out1)],
                    },
            'net1D0':{'options':{'net':net1,
                                'filt':ident},
                     'args':['D',0],
                     'ans':[(out1,list('D'),out1)],
                    },
            'net1E0':{'options':{'net':net1,
                                'filt':ident},
                     'args':['E',0],
                     'ans':[(out1,list('E'),out1)],
                    },
            'net2A0':{'options':{'net':net2,
                                'filt':ident},
                     'args':['A',0],
                     'ans':[(out2,list('A'),out2)],
                    },
            'net2B0':{'options':{'net':net2,
                                'filt':ident},
                     'args':['B',0],
                     'ans':[(out2,list('B'),out2)],
                    },
            'net2C0':{'options':{'net':net2,
                                'filt':ident},
                     'args':['C',0],
                     'ans':[(out2,list('C'),out2)],
                    },
            'net2D0':{'options':{'net':net2,
                                'filt':ident},
                     'args':['D',0],
                     'ans':[(out2,list('D'),out2)],
                    },
            'net3a0':{'options':{'net':net3,
                                'filt':ident},
                     'args':['a',0],
                     'ans':[(out3,list('a'),out3)],
                    },
            'net3b0':{'options':{'net':net3,
                                'filt':ident},
                     'args':['b',0],
                     'ans':[(out3,list('b'),out3)],
                    },
            'net3c0':{'options':{'net':net3,
                                'filt':ident},
                     'args':['c',0],
                     'ans':[(out3,list('c'),out3)],
                    },
            'net3d0':{'options':{'net':net3,
                                'filt':ident},
                     'args':['d',0],
                     'ans':[(out3,list('d'),out3)],
                    },
            'net3e0':{'options':{'net':net3,
                                'filt':ident},
                     'args':['e',0],
                     'ans':[(out3,list('e'),out3)],
                    },
            'net3f0':{'options':{'net':net3,
                                'filt':ident},
                     'args':['f',0],
                     'ans':[(out3,list('f'),out3)],
                    },
            'net3g0':{'options':{'net':net3,
                                'filt':ident},
                     'args':['g',0],
                     'ans':[(out3,list('g'),out3)],
                    },
            'net3h0':{'options':{'net':net3,
                                'filt':ident},
                     'args':['h',0],
                     'ans':[(out3,list('h'),out3)],
                    },

            'net1A1':{'options':{'net':net1,
                                'filt':ident},
                     'args':['A',1],
                     'ans':[(out1,list('ABE'),out1)],
                    },
            'net1B1':{'options':{'net':net1,
                                'filt':ident},
                     'args':['B',1],
                     'ans':[(out1,list('BCE'),out1)],
                    },
            'net1C1':{'options':{'net':net1,
                                'filt':ident},
                     'args':['C',1],
                     'ans':[(out1,list('ACE'),out1)],
                    },
            'net1D1':{'options':{'net':net1,
                                'filt':ident},
                     'args':['D',1],
                     'ans':[(out1,list('AD'),out1)],
                    },
            'net1E1':{'options':{'net':net1,
                                'filt':ident},
                     'args':['E',1],
                     'ans':[(out1,list('E'),out1)],
                    },
            'net2A1':{'options':{'net':net2,
                                'filt':ident},
                     'args':['A',1],
                     'ans':[(out2,list('ABCD'),out2)],
                    },
            'net2B1':{'options':{'net':net2,
                                'filt':ident},
                     'args':['B',1],
                     'ans':[(out2,list('BCD'),out2)],
                    },
            'net2C1':{'options':{'net':net2,
                                'filt':ident},
                     'args':['C',1],
                     'ans':[(out2,list('CD'),out2)],
                    },
            'net2D1':{'options':{'net':net2,
                                'filt':ident},
                     'args':['D',1],
                     'ans':[(out2,list('BD'),out2)],
                    },
            'net3a1':{'options':{'net':net3,
                                'filt':ident},
                     'args':['a',1],
                     'ans':[(out3,list('abc'),out3)],
                    },
            'net3b1':{'options':{'net':net3,
                                'filt':ident},
                     'args':['b',1],
                     'ans':[(out3,list('bef'),out3)],
                    },
            'net3c1':{'options':{'net':net3,
                                'filt':ident},
                     'args':['c',1],
                     'ans':[(out3,list('bcd'),out3)],
                    },
            'net3d1':{'options':{'net':net3,
                                'filt':ident},
                     'args':['d',1],
                     'ans':[(out3,list('dh'),out3)],
                    },
            'net3e1':{'options':{'net':net3,
                                'filt':ident},
                     'args':['e',1],
                     'ans':[(out3,list('egh'),out3)],
                    },
            'net3f1':{'options':{'net':net3,
                                'filt':ident},
                     'args':['f',1],
                     'ans':[(out3,list('fd'),out3)],
                    },
            'net3g1':{'options':{'net':net3,
                                'filt':ident},
                     'args':['g',1],
                     'ans':[(out3,list('bcdg'),out3)],
                    },
            'net3h1':{'options':{'net':net3,
                                'filt':ident},
                     'args':['h',1],
                     'ans':[(out3,list('gh'),out3)],
                    },

            'net1A2':{'options':{'net':net1,
                                'filt':ident},
                     'args':['A',2],
                     'ans':[(out1,list('ABCE'),out1)],
                    },
            'net1B2':{'options':{'net':net1,
                                'filt':ident},
                     'args':['B',2],
                     'ans':[(out1,list('ABCE'),out1)],
                    },
            'net1C2':{'options':{'net':net1,
                                'filt':ident},
                     'args':['C',2],
                     'ans':[(out1,list('ABCE'),out1)],
                    },
            'net1D2':{'options':{'net':net1,
                                'filt':ident},
                     'args':['D',2],
                     'ans':[(out1,list('ABDE'),out1)],
                    },
            'net1E2':{'options':{'net':net1,
                                'filt':ident},
                     'args':['E',2],
                     'ans':[(out1,list('E'),out1)],
                    },
            'net2A2':{'options':{'net':net2,
                                'filt':ident},
                     'args':['A',2],
                     'ans':[(out2,list('ABCD'),out2)],
                    },
            'net2B2':{'options':{'net':net2,
                                'filt':ident},
                     'args':['B',2],
                     'ans':[(out2,list('BCD'),out2)],
                    },
            'net2C2':{'options':{'net':net2,
                                'filt':ident},
                     'args':['C',2],
                     'ans':[(out2,list('BCD'),out2)],
                    },
            'net2D2':{'options':{'net':net2,
                                'filt':ident},
                     'args':['D',2],
                     'ans':[(out2,list('BCD'),out2)],
                    },
            'net3a2':{'options':{'net':net3,
                                'filt':ident},
                     'args':['a',2],
                     'ans':[(out3,list('abcdef'),out3)],
                    },
            'net3b2':{'options':{'net':net3,
                                'filt':ident},
                     'args':['b',2],
                     'ans':[(out3,list('bdefgh'),out3)],
                    },
            'net3c2':{'options':{'net':net3,
                                'filt':ident},
                     'args':['c',2],
                     'ans':[(out3,list('bcdefh'),out3)],
                    },
            'net3d2':{'options':{'net':net3,
                                'filt':ident},
                     'args':['d',2],
                     'ans':[(out3,list('dgh'),out3)],
                    },
            'net3e2':{'options':{'net':net3,
                                'filt':ident},
                     'args':['e',2],
                     'ans':[(out3,list('bcdegh'),out3)],
                    },
            'net3f2':{'options':{'net':net3,
                                'filt':ident},
                     'args':['f',2],
                     'ans':[(out3,list('dfh'),out3)],
                    },
            'net3g2':{'options':{'net':net3,
                                'filt':ident},
                     'args':['g',2],
                     'ans':[(out3,list('bcdefgh'),out3)],
                    },
            'net3h2':{'options':{'net':net3,
                                'filt':ident},
                     'args':['h',2],
                     'ans':[(out3,list('bcdgh'),out3)],
                    },
            }

def checkiter(res):
    try:
        if type(res) is list:
            return res,False
        if iter(res) is not res:
            return res
        return list(res)
    except:
        return res

readdefaults = {'modulename':'ex10', 
               'fname':'read_article_links',
                }

BASE = '/cs/course/current/intro2cs/presubmit/ex10'

readcases = {'net0':{'args':[os.path.join(BASE,'net0.in')],
                     'ans':[net0]},
             'net1':{'args':[os.path.join(BASE,'net1.in')],
                     'ans':[net1]},
             'net2':{'args':[os.path.join(BASE,'net2.in')],
                     'ans':[net2]},
             'net3':{'args':[os.path.join(BASE,'net3.in')],
                     'ans':[net3]},
             }             
             

#                                'runopts':['get_neighbors',3,sortarticlelist]},
tsets = {'article':TestSet(articledefaults,artcases),
         'network':TestSet(networkdefaults,netcases),
         'pagerank':TestSet(pgrdefaults,pgrcases),
         'jaccard':TestSet(jacdefaults,jaccases),
         'path':TestSet(cycdefaults,cyccases),
         'friends':TestSet(fridefaults,fricases),
         'readfile':TestSet(readdefaults,readcases),
         }
