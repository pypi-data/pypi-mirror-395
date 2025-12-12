from .background_info import * 


def std_cracking_function(ir:IsoRing,hs:HypStruct): 
    assert type(hs) == HypStruct

    ssi = SearchSpaceIterator_for_bounds(hs.suspected_subbound,hs.hop_size)

    """
    empty function 
    """
    def process_feedback(feedback_distance_vec):  
        return

    """
    - cracking point, ?is point correct?,?is finished? 
    """
    def try_one(vec): 
        # calculate feedback vector 
        fvec = ir.provide_feedback_distance_vec(vec)  

        # case: wrong dimension 
        if type(fvec) == type(None): 
            return None,None 

        # no processing of feedback in this cracking function 
        process_feedback(fvec)

        opt_point,opt_index,opt_pr = ir.guess_equals_one_feedback(vec)
        
        # case: not an optima point 
        if type(opt_point) == type(None): 
            return None,None

        # case: optima point, check if index and pr match 
            # not the index 
        if opt_index != hs.opt_index: 
            return None,None 

            # not probability match
        return opt_point,opt_pr == hs.probability_marker

    def one_guess(): 
        if ssi.reached_end(): 
            return None,None,True 

        v = next(ssi) 
        opt_pt,bool_stat = try_one(v) 
        return opt_pt,bool_stat,False 

    return one_guess 


class Crackling: 

    def __init__(self,target_isoring_idn,isoring_sec_index,sec_optima_index): 
        self.target_ir = target_isoring_idn 
        self.ir_sec_index = isoring_sec_index
        self.sec_opt_index = sec_optima_index
    
        self.num_attempts = 0 
        self.cracked_soln = None
        self.soln_pr = None 

        self.has_bridged = False 
        self.terminated = False 
        return

    def __str__(self): 
        S = "* Target IsoRing: " + str(self.target_ir) + "\n"
        S += "* Sec index: " + str(self.ir_sec_index) + "\n"
        S += "* optima index: " + str(self.sec_opt_index) + "\n"
        S += "* attempts: " + str(self.num_attempts) + "\n"
        S += "* terminated: " + str(self.terminated) + "\n"
        S += "* accept solution: " + str(self.soln_pr) + "\n"
        return S 

    def has_soln(self): 
        return type(self.cracked_soln) != type(None) and \
            type(self.soln_pr) != type(None) 

"""
Cracking bridge. Environment for <Crackling> to attempt cracking an <IsoRing> using a 
<HypStruct>. 
"""
class CBridge:

    def __init__(self,cr:Crackling,hs:HypStruct,ir:IsoRing,cracking_func=std_cracking_function,\
        verbose=False): 
        assert type(cr) == Crackling 
        assert type(hs) == HypStruct 
        assert type(ir) == IsoRing 
        assert type(verbose) == bool 

        self.cr = cr 
        self.hs = hs 
        self.ir = ir 
        self.verbose = verbose 

        self.cracking_process = cracking_func(self.ir,self.hs)
        self.cr.has_bridged = True 
        self.terminated = False 
        return

    def __str__(self): 
        return "CBRIDGE WITH HYP" + "\n" + str(self.hs)

    def __next__(self): 
        if self.terminated: return 

        point,bool_stat,fin_stat = self.cracking_process()
        if self.verbose: 
            print("i: ",self.cr.num_attempts)
            print("-------------------------------") 

        if fin_stat: 
            self.terminated = True 

        if type(point) != type(None): 
            self.terminated = True
            self.cr.cracked_soln = point 
            self.cr.soln_pr = bool_stat 
            self.cr.terminated = True 
            if self.verbose: print("[got point] terminated @",self.cr.num_attempts)

        else: 
            if fin_stat: 
                #self.terminated = True 
                self.cr.terminated = True 
                if self.verbose: print("[no point] terminated @",self.cr.num_attempts)

        self.cr.num_attempts += 1