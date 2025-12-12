from .bloominstein import * 
from morebs2.numerical_generator import prg_seqsort
from morebs2.matrix_methods import euclidean_point_distance 

def prng_point_distance_funtion(prng): 

    def f(x0,x1):
        return euclidean_point_distance(x0,x1) + prng()   
    return f 

class IsoRing:

    """
    sec_list := list, every element is a <Sec> 
    feedback_function := function, F: (vector,vector) -> float 
    """
    def __init__(self,sec_list,feedback_function,actual_sec_index=0): 
        assert len(sec_list) > 0 
        assert len(sec_list) > actual_sec_index >= 0 
        idn_tag = set() 
        for s in sec_list: 
            assert type(s) == Sec 
            idn_tag |= {s.idn_tag}
        assert len(idn_tag) == 1
        self.sec_list = sec_list 
        self.feedback_function = feedback_function
        self.actual_sec_index = actual_sec_index
        self.current_sec_index = actual_sec_index

        self.cracked_sec_indices = [] 
        return

    #------------------------ functions to accept guesses (cracking attempts) from third-party 

    """
    return: 
    - optima point, optima point index, probability value 
    """
    def guess_equals_one_feedback(self,point):
        sec = self.iso_repr() 

        opt_pts = sec.optima_points()

        for (i,o) in enumerate(opt_pts):
            dist = None 
            stat = None 
            pr = None 
            try: 
                dist = euclidean_point_distance(o,point)
                stat = dist < 0.05 
            except: 
                return None,None,None

            if stat: 
                pr = self.provide_feedback_pr(vector_to_string(o,float)) 
                assert pr != -1 
                return o,i,pr 
        return None,None,None 

    """
    return: 
    - vector of feedback scores, length equal to number of optima points for 
                                iso_repr. 
    """
    def provide_feedback_distance_vec(self,i):
        s = self.iso_repr() 
        opt_points = s.optima_points() 

        V = [] 
        for o in opt_points: 
            try: 
                v = self.feedback_function(i,o) 
                V.append(v) 
            # case: different dim. 
            except:
                return None 
        return np.array(V)  
    
    def provide_feedback_pr(self,stringized_opt_point:str): 
        s = self.iso_repr() 
        if stringized_opt_point not in s.opm: return -1 
        return s.opm[stringized_opt_point]

    #----------------------------- repr functions 

    def idn_tag(self): 
        return self.sec_list[0].idn_tag 

    def set_iso_repr(self,i):
        assert 0 <= i < len(self.sec_list) 
        self.current_sec_index = i 

    def iso_repr(self): 
        return self.sec_list[self.current_sec_index]

    def reset_iso_repr(self): 
        self.current_sec_index = self.actual_sec_index

    def actual_sec_vec(self): 
        return self.sec_list[self.actual_sec_index].seq 

    def fetch_Sec(self,i): 
        assert type(i) == int 
        assert 0 <= i < len(self.sec_list)
        return self.sec_list[i] 

    #---------------------------- switch of repr functions, for use in cracking situations 

    """
    return:
    - ?any uncracked Sec remaining? 
    """
    def register_cracked_sec_index(self,prng): 
        # case: already cracked 
        if self.current_sec_index in self.cracked_sec_indices: 
            return 

        def prg_(): return int(prng())

        # case: register as cracked 
        self.cracked_sec_indices.append(self.current_sec_index) 

            # switch to another <Sec>
        available = [_ for _ in range(len(self.sec_list)) if _ not in self.cracked_sec_indices]  
            # case: none left 
        if len(available) == 0: 
            return False 

        i = int(prng()) % len(available)
        i = available[i] 
        self.set_iso_repr(i) 
        return True 

    #------------------- dep/codep functions 

    def dc_set(self,is_dep:bool=True):
        s = self.sec_list[0]
        return s.ds if is_dep else s.cds 

    def assign_DC_set(self,ds,cds):
        assert type(ds) == set 
        for s in self.sec_list:
            s.ds = ds
            s.cds = cds 

    def clear_depANDcodep_sets(self): 
        for s in self.sec_list:
            s.ds.clear()
            s.cds.clear() 

    """
    feedback_function_type := 0 for euclidean point distance, 1 for prng noise added. 
    """
    @staticmethod 
    def generate_IsoRing_from_one_secret(sec,prng,feedback_function_type,\
        num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
        sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE): 

        assert feedback_function_type in {0,1}

        bos = BloomOfSecret(sec,prng,num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
        sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE)

        while True: 
            if type(next(bos)) == type(None): break 

        def prg_(): 
            return int(prng())

        l = [i for i in range(bos.num_blooms + 1)]
        l = prg_seqsort(l,prg_)
        
        actual_sec_index = l.index(0)
        sec_list = [bos.all_sec[i] for i in l] 

        if feedback_function_type: 
            feedback_function = prng_point_distance_funtion(prng)
        else: 
            feedback_function = euclidean_point_distance

        return IsoRing(sec_list,feedback_function,actual_sec_index=actual_sec_index)