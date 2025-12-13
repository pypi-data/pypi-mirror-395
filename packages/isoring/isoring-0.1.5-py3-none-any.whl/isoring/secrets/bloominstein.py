from .secret import * 
from math import ceil 

DEFAULT_BLOOM_VECTOR_DIM_RANGE = [2,15] 
DEFAULT_NUM_BLOOMS = 6 
DEFAULT_BLOOM_MULTIPLIER_RANGE = [0.5,2.0]

"""
Used to calculate additional <Sec> instances given a base <Sec>. These additional <Sec>s are 
calculated with the aid of a pseudo-random number generator, `prng`, and accomodating parameters. 
"""
class BloomOfSecret: 

    def __init__(self,sec,prng,num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
        sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE): 

        assert type(sec) == Sec 
        assert is_valid_range(dim_range,True,False) and dim_range[0] > 0
        assert num_blooms < dim_range[1] - dim_range[0]
        assert is_valid_range(sec_vec_multiplier_range,False,True) and sec_vec_multiplier_range[0] > 0.  
        assert is_valid_range(optima_multiplier_range,False,True) and optima_multiplier_range[0] > 0.  

        self.base_sec = sec 
        self.all_sec = [self.base_sec] 
        self.num_blooms = num_blooms 
        self.svec_multiplier_range = sec_vec_multiplier_range
        self.prng = prng 
        self.dim_range = dim_range
        self.om_range = optima_multiplier_range
        
        available_dim = set([_ for _ in range(dim_range[0],dim_range[1])])
        available_dim -= {self.base_sec.dim()} 
        self.available_dim = sorted(available_dim)

    def __next__(self): 
        if len(self.all_sec) == self.num_blooms +1: return None 

        r0,r1 = min(self.all_sec[-1].seq),max(self.all_sec[-1].seq) 
        d = r1 - r0 
        median = (r1 - r0) / 2.0 
        omult = modulo_in_range(self.prng(),self.svec_multiplier_range)
        new_dist = (d * omult) / 2.0 
        r0_,r1_ = r0 - new_dist, r1 + new_dist 
        singleton_range = [r0_,r1_]
        
        di_index = int(self.prng()) % len(self.available_dim) 
        dimension = self.available_dim.pop(di_index) 

        omult = modulo_in_range(self.prng(),self.om_range) 
        num_optima = ceil(len(self.all_sec[-1].opm) * omult)

        set_actual_as_max_pr = bool(int(self.prng()) % 2) 

        S = Sec.generate_bare_instance(singleton_range,dimension,num_optima,self.prng,\
            idn_tag=self.base_sec.idn_tag,set_actual_as_max_pr=set_actual_as_max_pr)
        self.all_sec.append(S)
        return S