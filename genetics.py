import random

import numpy as np

from neural import NeuralNetwork


class Genetics:
    def __init__(self,joiner,mutator):
        self.joiner=joiner
        self.mutator=mutator

    def cross_breed(self, network_a, network_b):
        network_weights_a = network_a.weights
        network_weights_b = network_b.weights
        child_weights=[]
        for a_layer,b_layer in zip(network_weights_a,network_weights_b):
            assert a_layer.shape==b_layer.shape
            offspring_layer=[]
            weights_a_flat=a_layer.flatten()
            weights_b_flat = b_layer.flatten()
            self.joiner(weights_a_flat,weights_b_flat,offspring_layer)
            offspring_layer=np.array(offspring_layer,dtype=np.float).reshape(a_layer.shape)
            offspring_layer.reshape(a_layer.shape)
            child_weights.append(offspring_layer)
        child_network=NeuralNetwork(network_a.shape_v, child_weights, symmetry_mat=network_a.symmetry_mat)
        return child_network

    def mutate(self,network,intensity,mutate_all=False):
        network_weights = network.weights
        child_weights = []
        for weights in network_weights:
            copy_gene=weights.copy()
            mutated_gene=self.mutator(copy_gene,intensity,mutate_all)
            child_weights.append(mutated_gene)
        child_network=NeuralNetwork(network.shape_v, child_weights, symmetry_mat=network.symmetry_mat)
        return child_network


def random_joiner(gene_a,gene_b,empty_gene):
    for a,b in zip(gene_a,gene_b):
        empty_gene.append(random.choice(a,b))


def zipper_joiner(gene_a,gene_b,empty_gene):
    for i,(a,b) in enumerate(zip(gene_a,gene_b)):
        empty_gene.append(b if i % 2 else a)


def average_joiner(gene_a,gene_b,empty_gene):
    for a,b in zip(gene_a,gene_b):
        empty_gene.append((b+a)/2)


def addetive_mutator(gene,intensity,mutate_all):
    if mutate_all:
        r=(np.random.random(size=gene.shape)*intensity)-(intensity/2)
    else:
        r=np.zeros_like(gene)
        max_idx=np.multiply(*gene.shape)
        indices=np.arange(0,max_idx).reshape(gene.shape)
        rand_idx=random.randint(0,max_idx)
        r[indices==rand_idx]=(np.random.random()*intensity)-(intensity/2)
    return gene+r


def multiplecative_mutator(gene,intensity,mutate_all):
    if mutate_all:
        r=(np.random.random(size=gene.shape)*(intensity-1/intensity))+(1/intensity)
        random_sign=np.putmask(1,np.random.random(size=gene.shape)>0.5,-1)
        r=r*random_sign
    else:
        r=np.ones_like(gene)
        max_idx=np.multiply(*gene.shape)
        indices=np.arange(0,max_idx).reshape(gene.shape)
        rand_idx=random.randint(0,max_idx)
        r[indices==rand_idx] = ((np.random.random()*(intensity-1/intensity))+(1/intensity))*np.random.choice([-1,1])
    return gene*r


default_genetics=Genetics(joiner=zipper_joiner, mutator=multiplecative_mutator)