from isoring.brute_forcer.brute_force_env import * 
import unittest

def veclistANDprng_sample_U(): 
    prng = prg__LCG(45.43,543.21,-42315.6666,6797.0)
    vec_size = [3,5,4,7] 
    vec_list = [] 
    for i in range(16): 
        V = one_vec(prng,vec_size[i % 4],[-2000,2000])
        vec_list.append(V) 
    return vec_list,prng 

### lone file test 
"""
python3 -m tests.test_brute_force_env  
"""
###
class BruteForceEnvClass(unittest.TestCase):

    '''
    successful crack, completely wrong answer
    '''
    def test__BruteForceEnv__next__case1(self):
        vec_list,prng = veclistANDprng_sample_U() 
        prng2 = prg__LCG(-43,-45,61,-7171)
        irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list[:3],prng2,\
            num_blooms_range=[DEFAULT_NUM_BLOOMS-2,DEFAULT_NUM_BLOOMS+1],ratio_of_feedback_functions_type_1=0.0,codep_ratio=0.9)
        bi = BackgroundInfo.extract_from_IsoRingedChain(irc,prng,[0.0,0.0],[1.0,1.0],\
                [1.0,1.0],0.0,0.0,0.0)

        print("\t\tTESTING BRUTE FORCE ENV #1") 
        crck = Cracker(bi,10,verbose=True) 
        bfe = BruteForceEnv(crck,irc,prng,True)

        assert not crck.halted 
        while not bfe.is_finished():
            next(bfe) 
        assert bfe.num_iter == 316, "got {}".format(bfe.num_iter)
        assert len(crck.csoln) == 3 

        for i in range(3): 
            soln = crck.soln_for_IsoRing(i)
            ir = irc.fetch_IsoRing(i) 
            V = ir.actual_sec_vec()
            assert not np.any(soln[1] == V) 
        print("-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")

    '''
    cracking process terminated midway, no energy left
    '''
    def test__BruteForceEnv__next__case2(self): 
        print("\t\tTESTING BRUTE FORCE ENV #2") 
        vec_list,prng = veclistANDprng_sample_U() 
        prng2 = prg__LCG(-43,-45,61,-7171)
        irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list[:3],prng2,\
            num_blooms_range=[DEFAULT_NUM_BLOOMS-2,DEFAULT_NUM_BLOOMS+1],ratio_of_feedback_functions_type_1=0.0,codep_ratio=0.9)
        bi = BackgroundInfo.extract_from_IsoRingedChain(irc,prng,[1.0,1.0],[1.0,1.0],\
                [1.0,1.0],0.0,0.0,0.0)

        crck = Cracker(bi,10,10,True)  
        bfe = BruteForceEnv(crck,irc,prng,True) 

        assert not crck.halted 
        while not bfe.is_finished(): 
            next(bfe) 
        assert crck.halted 
        assert len(crck.csoln) == 1 

        soln = crck.soln_for_IsoRing(2)
        ir = irc.fetch_IsoRing(2) 
        V = ir.actual_sec_vec()
        assert np.all(soln[1] == V)
        assert bfe.num_iter == 16, "got {}".format(bfe.num_iter)

        print("-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
        return

    '''
    cracking process on two IsoRings, wrong optima  
    '''
    def test__BruteForceEnv__next__case3(self): 
        print("\t\tTESTING BRUTE FORCE ENV #3") 
        vec_list,prng = veclistANDprng_sample_U() 

        irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list,prng,\
            num_blooms_range=[DEFAULT_NUM_BLOOMS-2,DEFAULT_NUM_BLOOMS+1],ratio_of_feedback_functions_type_1=0.0,codep_ratio=0.0)

        bi = BackgroundInfo.extract_from_IsoRingedChain(irc,prng,[0.0,0.0],[1.0,1.0],\
                [1.0,1.0],1.0,0.0,0.0)

        crck = Cracker(bi,10,verbose=True) 

        bfe = BruteForceEnv(crck,irc,prng,True) 

        for i in range(50000): 
            next(bfe) 

        Q = set(crck.csoln.D.keys())


        Q2 = set()
        for x in range(6): 
            Q2 |= bi.order_of_cracking[x] 
        assert Q == Q2 

        for k in Q2: 
            soln = crck.soln_for_IsoRing(k)
            ir = irc.fetch_IsoRing(k) 
            V = ir.actual_sec_vec()
            assert not np.any(soln[1] == V)

            # correct Sec index 
            sec_index = list(crck.csoln.D[k].keys()).pop() 
            assert sec_index == ir.actual_sec_index

            # not the correct optimum 
            S = ir.fetch_Sec(sec_index)
            assert S.seq_index() != soln[0] 
            assert vector_to_string(soln[1],float) in S.opm 

        print("-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")

    """
    cracking on a co-dependent set of size 3; recracking required. 
    """
    def test__BruteForceEnv__next__case4(self):
        print("\t\tTESTING BRUTE FORCE ENV #4") 
        vec_list,prng = veclistANDprng_sample_U() 

        prng2 = prg__LCG(-43,-45,61,-7171)
        irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list,prng2,\
            num_blooms_range=[DEFAULT_NUM_BLOOMS-2,DEFAULT_NUM_BLOOMS+1],ratio_of_feedback_functions_type_1=0.0,codep_ratio=0.9)
        bi = BackgroundInfo.extract_from_IsoRingedChain(irc,prng,[0.0,0.0],[1.0,1.0],\
                [1.0,1.0],1.0,0.0,1.0)

        crck = Cracker(bi,10,verbose=True) 
        bfe = BruteForceEnv(crck,irc,prng,True) 

        assert not crck.halted 

        for i in range(20000):  
            next(bfe) 

        assert len(crck.csoln) == 4
        assert len(bfe.cbridges) == 2 == len(crck.active_cracklings)
        assert len(crck.csoln.D[0]) == len(crck.csoln.D[14]) == 1
        assert len(crck.csoln.D[15]) == 2

        print("-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")


    """
    correct BackgroundInfo for Cracker; Cracker does not have enough energy to completely crack 
    IsoRingedChain. 
    """
    def test__BruteForceEnv__next__case5(self):
        print("\t\tTESTING BRUTE FORCE ENV #5") 
        vec_list,prng = veclistANDprng_sample_U() 

        prng2 = prg__LCG(-43,-45,61,-7171)
        irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list[:3],prng2,\
            num_blooms_range=[DEFAULT_NUM_BLOOMS-2,DEFAULT_NUM_BLOOMS+1],ratio_of_feedback_functions_type_1=0.0,codep_ratio=0.9)
        bi = BackgroundInfo.extract_from_IsoRingedChain(irc,prng,[1.0,1.0],[1.0,1.0],\
                [1.0,1.0],0.0,0.0,0.0)

        crck = Cracker(bi,10,10)  
        bfe = BruteForceEnv(crck,irc,prng,True) 

        assert not crck.halted 
        while not bfe.is_finished(): 
            next(bfe) 
         
        assert len(crck.csoln) == 1 

        soln = crck.soln_for_IsoRing(2)
        ir = irc.fetch_IsoRing(2) 
        V = ir.actual_sec_vec()
        assert np.all(soln[1] == V)
        assert bfe.num_iter == 16, "got {}".format(bfe.num_iter)

        print("-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")


    """
    completely wrong 
    """
    def test__BruteForceEnv__next__case6(self):
        print("\t\tTESTING BRUTE FORCE ENV #6") 
        vec_list,prng = veclistANDprng_sample_U() 

        prng2 = prg__LCG(-43,-45,61,-7171)
        irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list[:5],prng2,\
            num_blooms_range=[DEFAULT_NUM_BLOOMS-2,DEFAULT_NUM_BLOOMS+1],ratio_of_feedback_functions_type_1=0.0,codep_ratio=0.9)
        bi = BackgroundInfo.extract_from_IsoRingedChain(irc,prng,[1.0,1.0],[1.0,1.0],\
                [0.0,0.0],0.0,0.0,0.0)

        crck = Cracker(bi,10,50000)  
        bfe = BruteForceEnv(crck,irc,prng,True) 

        assert not crck.halted 
        while not bfe.is_finished(): 
            next(bfe) 
        assert len(crck.csoln) == 0 

        print("-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")


if __name__ == '__main__':
    unittest.main()
