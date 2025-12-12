from morebs2.matrix_methods import is_vector,is_valid_range,vector_to_string,\
    string_to_vector,equal_iterables,is_vector 
from morebs2.numerical_generator import prg__LCG,prg__n_ary_alternator,modulo_in_range
import numpy as np 
import random 
import pickle 
from collections import defaultdict 

DEFAULT_SINGLETON_DISTANCE_RANGE = 10.0 
DEFAULT_NUM_OPTIMA_RANGE = [2,10]

def default_std_Python_prng(integer_seed=None,output_range=[-10**6,10**6],rounding_depth=0): 
    if type(integer_seed) == int:
        random.seed(integer_seed)

    assert output_range[0] <= output_range[1]
    assert rounding_depth >= 0 and type(rounding_depth) == int 

    def fx():
        v = random.uniform(output_range[0],output_range[1]) 
        v = round(v,rounding_depth) 

        if rounding_depth == 0: 
            return int(v) 
        return v  
    return fx

"""
every output vector sums to 1.0 
"""
def default_std_numpy_prvec(vec_length,integer_seed=None):
    assert vec_length >= 1 and type(vec_length) == int 
    if type(integer_seed) == int:
        np.random.seed(abs(integer_seed))

    X = np.random.rand(vec_length)
    S = np.sum(X) 
    assert S > 0.0 

    while abs(S - 1.0) >= 10 ** -5: 
        X = np.round(X / S,6) 
        S = np.sum(X) 
    return X 

def one_vec(prng,dimension,singleton_range): 
    assert singleton_range[0] <= singleton_range[1] 

    # guarantee a range of 100 if range is 0  
    if singleton_range[0] == singleton_range[1]: 
        singleton_range[1] += 100 

    v = [modulo_in_range(prng(),singleton_range) for _ in range(dimension)]
    return np.round(np.array(v),5) 

"""
Representation of a secret information, a vector of real numbers. Additional features 
include a map of optima to probability values. One of the optima is the vector that is the 
secret information. There are also two sets, a dependency map and a codependency map, containing 
identifier tags for secrets that must be cracked before this instance or cracked alongside this 
instance. These sets are used for situations of information retrieval where order-of-operations 
are necessary.
"""
class Sec:

    def __init__(self,sequence,optima_pr_map,dep_set=set(),codep_set=set(),idn_tag=0):

        assert is_vector(sequence)
        assert type(optima_pr_map) == defaultdict        
        assert type(dep_set) == set and type(dep_set) == type(codep_set)
        assert vector_to_string(sequence,float) in optima_pr_map
        assert abs(1.0 - sum(optima_pr_map.values())) < 10 ** -5, "got {}".format(optima_pr_map)#{}".format(sum(optima_pr_map.values()))
        assert type(idn_tag) == int 

        self.seq = sequence
        self.opm = optima_pr_map
        self.ds = dep_set
        self.cds = codep_set
        self.idn_tag = idn_tag 

    def dim(self): 
        return len(self.seq) 

    def pickle_thyself(self,fp):
        fobj = open(fp,"wb")
        q = self.to_pickle_list()
        pickle.dump(q,fobj)
        fobj.close()
        return

    def to_pickle_list(self):
        return (self.seq,self.opm,\
            self.ds,self.cds,self.idn_tag)

    @staticmethod
    def unpickle_thyself(f): 
        fobj = open(f,"rb")
        q = pickle.load(fobj)
        fobj.close()
        return Sec(q[0],q[1],q[2],q[3],q[4])

    @staticmethod
    def unpickle_thyselves(fx):
        rx_ = open(fx,"rb")
        rx = pickle.load(rx_)

    def __str__(self):
        s = "** secret {}\n".format(self.idn_tag)
        s += "\t\t" + vector_to_string(self.seq,float)
        s += "\n" + "** optima pr." + "\n"
        s += str(self.opm)
        s += "\n" + "** dep. map" + "\n"
        s += str(self.ds)
        s += "\n" + "** co-dep. map" + "\n"
        s += str(self.cds)
        return s + "\n"

    """
    bare instances do not have any dep. or co-dep. 
    """
    @staticmethod
    def generate_bare_instance(singleton_range,dimension,num_optima,prng,idn_tag=0,set_actual_as_max_pr:bool=False):

        if not is_valid_range(singleton_range,False,True): 
            assert is_valid_range(singleton_range,True,True)

        assert type(num_optima) == int and num_optima >= 1 


        # the secret 
        seq = one_vec(prng,dimension,singleton_range) 

        ## 
        return Sec.vec_to_bare_instance(seq,0,num_optima,prng,idn_tag,set_actual_as_max_pr)

    @staticmethod
    def vec_to_bare_instance(vec,singleton_distance,num_optima,prng,idn_tag=0,set_actual_as_max_pr:bool=False):
        assert is_vector(vec) 

        min_value,max_value = np.min(vec),np.max(vec) 
        singleton_range = [min_value - singleton_distance,max_value + singleton_distance] 

        ## 

        # the alternatives 
        dimension = len(vec) 
        other_seqs = [one_vec(prng,dimension,singleton_range) for _ in range(num_optima -1)] 
        other_seqs.insert(0,vec)

        stringized_seqs = set()
        for s in other_seqs:
            s_ = vector_to_string(s,float) 
            stringized_seqs |= {s_} 

        # numpy generation of corresponding Pr vector 
        # NOTE: below code is to ensure unique number of optima, even though the number may not be 
        #       `num_optima`. 
        prvec = default_std_numpy_prvec(vec_length=len(stringized_seqs),integer_seed=int(prng())) 
        stringized_seqs = sorted(stringized_seqs) 
        seq_ = vector_to_string(vec,float) 
        i = stringized_seqs.index(seq_) 
        x = stringized_seqs.pop(i) 
        stringized_seqs.insert(0,x) 

        # sort Pr vec in descending order if `set_actual_as_max_pr` 
        if set_actual_as_max_pr:
            prvec = np.sort(prvec)[::-1] 

        # make optima pr map 
        opm = defaultdict(float) 
        for s,p in zip(stringized_seqs,prvec): 
            opm[s] = p 

        return Sec(vec,opm,dep_set=set(),codep_set=set(),idn_tag=idn_tag)

    #----------------- methods to represent <Sec>'s optima points as matrices and indices 

    def seq_index(self):
        ops = self.optima_points()

        for (i,o) in enumerate(ops): 
            stat = equal_iterables(o,self.seq)
            if stat: return i 
        return -1

    def seq_pr(self):
        qx = self.optima_points_to_index_pr_map()
        si = self.seq_index()
        return qx[si] 

    """
    return: 
    - np.array,rows ordered by alphanumeric order. 
    """
    def optima_points(self):
        ks = sorted(list(self.opm.keys()))
        optima_points = [string_to_vector(v,float) for v in \
                    ks]
        optima_points = np.array(optima_points)
        return optima_points

    """
    converts opm map 
        key := stringized point
        value := Pr. value
    to a map w/ 
        key := index of ordering for stringized point
        value := Pr. value 
    """
    def optima_points_to_index_pr_map(self):

        ks = sorted(list(self.opm.keys()))
        ks = [(i,self.opm[k]) for (i,k) in enumerate(ks)]

        d = defaultdict(float,ks) 
        return d