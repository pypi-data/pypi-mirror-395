from .cracker import * 

def one_to_one_IsoRing2Crackling_map(ir_idn:set): 
    assert type(ir_idn) == set 
    return {i:1 for i in ir_idn} 

"""
environment for a Cracker, given background information on an IsoRingedChain, to conduct brute-force guesses 
against it. 
"""
class BruteForceEnv:

    def __init__(self,crck:Cracker,irc:IsoRingedChain,prng=None,verbose=True): 
        assert type(crck) == Cracker and type(irc) == IsoRingedChain
        assert type(verbose) == bool 
        self.crck = crck 
        self.irc = irc 

        if type(prng) == type(None): 
            self.prng = default_std_Python_prng(output_range=[-10000,10000],rounding_depth=0) 
        else: 
            self.prng = prng 
        self.irc.prng = self.prng 
        self.verbose = verbose 

        self.cbridges = [] 

        self.num_iter = 0 
        return

    def __next__(self): 
        # case: finished 
        if self.is_finished(): return 

        # if no CBridges exist, declare them 
        if len(self.cbridges) == 0: 
            stat = self.first_cracking_bridges()
            if not stat: 
                return 
        
        self.run_cbridges() 
        self.num_iter += 1 
        return

    # TODO: finish 
    def is_finished(self): 
        if self.crck.halted: 
            return True 
        return False 

    def run_cbridges(self): 
        any_terminated = False 

        i = 0 
        while i < len(self.cbridges): 
            c = self.cbridges[i] 
            if c.terminated: 
                any_terminated = True 
                self.cbridges.pop(i)
                continue 
            next(c) 
            i += 1 
            

        if any_terminated: 

            wanted_finishes,recracks = self.crck.manage_cracklings() 
            if self.verbose: 
                print("# BRIDGES: ",len(self.cbridges))
                print("\t- finished cracking on IsoRings\n{}".format(wanted_finishes)) 
                print("\t- recracking on IsoRings\n{}".format(recracks)) 
                print("=======================================================") 

            self.send_IsoRingedChain_info_on_cracked(wanted_finishes,recracks) 

            if len(recracks) > 0: 
                self.add_recracking_bridges(recracks)

        self.crck.did_fail() 

    def first_cracking_bridges(self): 
        stat = self.crck.next_target_IsoRing_set()

        if self.verbose: 
            print("[!] t={}, Adding initial cracking bridges to IsoRings\n{}\n".format(self.num_iter,self.crck.target_ir_set))

        # case: no new targets, terminated
        if not stat: 
            if self.verbose: print("[X] no new target IsoRings. DONE.")
            self.crck.halted = True 
            return stat  

        # case: wrong order, IsoRingedChain does not accept
        stat = self.irc.accept_cracker_targetset(self.crck.target_ir_set)
        if not stat: 
            if self.verbose: print("[X] wrong cracking order. DONE.")
            self.crck.halted = True 
            return stat 

        stat = self.initiate_Cracker_deployment(self.crck.target_ir_set)

        self.crck.increment_index() 
        return stat 

    def add_recracking_bridges(self,recrack_set):
        assert recrack_set.issubset(self.crck.target_ir_set) 
        return self.initiate_Cracker_deployment(recrack_set)

    def initiate_Cracker_deployment(self,ir_set): 

        # send Cracker info on IsoRing iso-repr state 
        ir_state = self.irc.repr_dict_for_IsoRings(ir_set)
        i2c_map = one_to_one_IsoRing2Crackling_map(ir_set)
            
        stat = self.crck.deploy_cracklings(ir_state,i2c_map)

        # case: Cracker is stuck. 
        if not stat: 
            self.crck.halted = True 
            return stat 

        # form the bridges 
        q = -sum(i2c_map.values())
        for cr in self.crck.active_cracklings[q:]: 
            hs = self.crck.bi.hypothesis_for_IsoRingANDSec(cr.target_ir,cr.ir_sec_index) 
            ir = self.irc.fetch_IsoRing(cr.target_ir)       
            cb = CBridge(cr,hs,ir) 
            self.cbridges.append(cb) 
        return True 

    def send_IsoRingedChain_info_on_cracked(self,wanted_finishes,recracks): 
        self.irc.register_cracked_IsoRings(wanted_finishes,recracks)
        return