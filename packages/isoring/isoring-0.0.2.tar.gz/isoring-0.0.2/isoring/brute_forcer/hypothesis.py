
from .leak_functions import * 
from morebs2.matrix_methods import is_proper_bounds_vector

class HypStruct:

    def __init__(self,opt_index:int,suspected_subbound,hop_size,probability_marker):
        assert type(opt_index) == int 
        assert is_proper_bounds_vector(suspected_subbound) 
        assert type(hop_size) == int and hop_size > 1 
        assert type(probability_marker) in {type(None),float,np.float32,np.float64}, "got {}".format(type(probability_marker))
        if type(probability_marker) != type(None): 
            assert 0 <= probability_marker <= 1 

        self.opt_index = opt_index 
        self.suspected_subbound = suspected_subbound
        self.hop_size = hop_size
        self.probability_marker = probability_marker
        return

    def __str__(self): 
        s = "\t\tHypothesis" + "\n"
        s += "* opt index: " + str(self.opt_index) + "\n"
        s += "* suspected subbound: \n" + str(self.suspected_subbound) + "\n\n"
        s += "* hop size: " + str(self.hop_size) + "\n"
        s += "* probability: " + str(self.probability_marker) + "\n"
        return s 

    """
    - dict, sec index -> HypStruct 
    """
    @staticmethod 
    def extract_from_IsoRing_into_HypStruct_dict(ir:IsoRing,prng,actual_sec_vec_ratio=1.0,\
        ratio_of_dim_covered=1.0,valid_bounds_ratio=1.0,prioritize_actual_Sec:bool=True,\
        valid_one_shot_kill_ratio=0.0): 

        D = prng_leak_IsoRing_into_dict(ir,prng,actual_sec_vec_ratio,ratio_of_dim_covered,\
            valid_bounds_ratio,prioritize_actual_Sec,valid_one_shot_kill_ratio)  
        D2 = {} 

        for k,v in D.items(): 
            D2[k] = HypStruct(v[0],v[1],v[2],v[3]) 
        return D2 

    """
    method is port for receiving feedback information from <IsoRing> 
    """
    def register_pointANDpr(self,point,pr): 

        if not point_in_bounds(self.suspected_subbound,point): 
            return False 

        if pr != self.probability_marker: 
            return False 

        return True 