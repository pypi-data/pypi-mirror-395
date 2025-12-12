from .crackling import * 
from morebs2.matrix_methods import is_number 

"""
Container to store cracked <Sec> instances from target <IsoRingedChain>.
"""
class CrackerSoln: 

    def __init__(self): 
        # IsoRing idn -> Sec index -> 
        #    (optima index, vector solution, ?does Crackling accept solution based on feedback Pr. value?) 
        self.D = dict() 

    def __len__(self): 
        n = 0 
        for v in self.D.values(): 
            n += len(v) 
        return n 

    def add_cracked_soln(self,cr:Crackling): 
        assert type(cr.cracked_soln) != type(None)
        assert type(cr.soln_pr) != None 
        if cr.target_ir not in self.D: 
            self.D[cr.target_ir] = dict() 
        
        assert cr.ir_sec_index not in self.D[cr.target_ir], "solution already acquired." 
        self.D[cr.target_ir][cr.ir_sec_index] = (cr.sec_opt_index,cr.cracked_soln,cr.soln_pr)
        return

    def fetch_soln(self,ir_idn,sec_index): 
        if ir_idn not in self.D: return None 
        if sec_index not in self.D[ir_idn]: return None  
        return self.D[ir_idn][sec_index] 

"""
<Cracker> is a structure that uses its given <BackgroundInfo> to conduct 
cracking on an <IsoRingedChain> in a brute-force environment. <Cracker> 
has the capacity to deploy at most `crackling_capacity` <Crackling>s at 
once. 

NOTE: 
<Cracker> may deploy more than 1 <Crackling> per <IsoRing>, although this 
is wasteful in an immobile brute-force environment such that <Crackling>s 
do not have to chase after their target <IsoRing>s. Mobile brute-force 
environments are not implemented in this program. Recall that the 
<BackgroundInfo> map is 
    <Isoring> identifier -> <Sec> index -> <HypStruct>. 
This means that every <Sec> for <IsoRing> is associated with at most 1 
<HypStruct>. Every <Crackling> that targets a <Sec> of an <IsoRing> will 
use the same <HypStruct>. 
"""
class Cracker: 

    def __init__(self,bi:BackgroundInfo,crackling_capacity:int,energy=float('inf'),verbose=False):
        assert type(bi) == BackgroundInfo 
        assert type(crackling_capacity) == int and crackling_capacity > 0 
        assert is_number(energy)
        assert type(verbose) == bool 

        self.bi = bi 
        self.crackling_capacity = crackling_capacity
        self.energy = energy 
        self.verbose = verbose 

        self.csoln = CrackerSoln() 
        # (IsoRing index, Sec index, optima index)
        self.failed_soln = [] 
        self.active_cracklings = [] 
        self.ooci = 0 
        self.target_ir_set = set()
        # successful cracks on element := (IsoRing idn, Sec idn)
        self.finished_target_list = [] 

        self.deployed_cracklings = False 
        # ?successfully finished or failed?
        self.halted = False  
        self.is_finished() 
        return

    def next_target_IsoRing_set(self):
        S = self.next_target_IsoRing_set_() 
        self.target_ir_set = S 
        if len(self.target_ir_set) == 0: return False 
        return True 

    def next_target_IsoRing_set_(self): 
        if self.verbose: print("-- Cracker cracks at index: {}".format(self.ooci))
        if len(self.bi.order_of_cracking) <= self.ooci: 
            return set() 
        return deepcopy(self.bi.order_of_cracking[self.ooci])

    def active_target_ir_size(self): 
        return len(self.target_ir_set) 

    """
    instantiate Cracklings based on info given by the two dict arguments. 

    return: 
    - ?deployment is successful? 
    """
    def deploy_cracklings(self,target_ir_to_isorepr_map:dict,target_ir_to_num_cracklings_map:dict): 
        self.deployed_cracklings = False 

        # case: halted from complete|incomplete cracking,no energy left. 
        if self.halted: return self.deployed_cracklings

        # case: no more target IsoRings 
        if len(self.target_ir_set) == 0: return self.deployed_cracklings

        # ensure crackling capacity can accomodate for number of cracklings
        #else: 
        target_irset = set(target_ir_to_num_cracklings_map.keys()) 
        assert set(target_ir_to_isorepr_map.keys()) == target_irset 
        assert target_irset.issubset(self.target_ir_set) 

        sum_wanted_cracklings = sum(target_ir_to_num_cracklings_map.values()) 

        # case: invalid Crackling allocation, error 
        if self.crackling_capacity - len(self.active_cracklings) < sum_wanted_cracklings: 
            return self.deployed_cracklings

        # allocate the Cracklings 
        for k,v in target_ir_to_num_cracklings_map.items(): 
            assert v > 0 
            for _ in range(v): 
                # case: no hypothesis for (IsoRing,Sec) exists, error 
                if not self.bi.hypothesis_exists_for_IsoRingANDSec(k,target_ir_to_isorepr_map[k]): 
                    self.active_cracklings.clear() 
                    return self.deployed_cracklings,0 

                hs = self.bi.info[k][target_ir_to_isorepr_map[k]] 
                c = Crackling(k,target_ir_to_isorepr_map[k],hs.opt_index)
                self.active_cracklings.append(c)

        self.deployed_cracklings = True 
        return self.deployed_cracklings 

    def manage_cracklings(self): 

        wanted_finishes,recracks = self.clear_finished_cracklings()

        # remove the finished IsoRing idns from `target_ir_set`
        self.target_ir_set -= wanted_finishes 

        # check if finished
        self.is_finished()
        return wanted_finishes,recracks 

    """
    return: 
    - idns of IsoRings where Cracklings cracked wanted Sec, 
      idns of IsoRings where recracking must occur for wanted Sec. 
    """
    def clear_finished_cracklings(self): 
        
        # set of IsoRing idns for Cracklings that terminated
        finished_ir_for_cracklings = set() 
        # set of IsoRing idns for Cracklings that terminated by 
        # successfully cracking the target Sec of the IsoRing.  
        wanted_finished_ir_for_cracklings = set() 

        l = 0 
        # iterate through and check each Crackling 
        while l < len(self.active_cracklings): 
            c = self.active_cracklings[l] 

            # case: extra Crackling for cracked (IsoRing,Sec)
            if c.target_ir in finished_ir_for_cracklings: 
                if self.verbose: print("-- Cracker clears extra crackling targeting IsoRing {}".format(c.target_ir))
                self.energy -= c.num_attempts 
                self.active_cracklings.pop(l) 
                continue 

            if c.terminated: 
                self.energy -= c.num_attempts 
                # case: solution acquired 
                if self.verbose: 
                    print("-- Crackling DONE.")
                    print(c) 

                if c.has_soln(): 
                    finished_ir_for_cracklings |= {c.target_ir}
                    self.csoln.add_cracked_soln(c) 
                    si = self.bi.sec_index_for_IsoRing(c.target_ir)
                    if si == c.ir_sec_index:
                        wanted_finished_ir_for_cracklings |= {c.target_ir}
                else:
                    if self.verbose: 
                        print("\t\t[!] no soln found")
                self.active_cracklings.pop(l) 
                continue 
            l += 1
        return wanted_finished_ir_for_cracklings,\
            finished_ir_for_cracklings - wanted_finished_ir_for_cracklings

    def soln_for_IsoRing(self,ir_idn):
        sec_index = self.bi.sec_index_for_IsoRing(ir_idn)
        return self.csoln.fetch_soln(ir_idn,sec_index) 

    def soln_synopsis(self): 
        print("------ CRACKER SOLUTION SYNOPSIS")
        for k in self.bi.info.keys(): 
            q = self.soln_for_IsoRing(k)
            print("[-] IsoRing {}: {}".format(k,q)) 
            print()
        

    """
    return:
    - ?failed at cracking any of the target IsoRings? 
    """
    def did_fail(self): 
        if not self.deployed_cracklings: 
            return False 

        if len(self.target_ir_set) > 0 and \
            len(self.active_cracklings) == 0: 
            self.halted = True 
            return True 
        return False 

    def is_finished(self): 
        if self.halted: return True 

        if self.energy <= 0: 
            self.halted = True 
            return True 

        return False 

    def increment_index(self): 
        self.ooci += 1