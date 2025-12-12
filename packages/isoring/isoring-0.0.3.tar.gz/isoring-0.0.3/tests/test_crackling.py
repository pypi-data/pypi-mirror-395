from isoring.brute_forcer.crackling import * 
import unittest

def IsoRingANDprng_sample_Y(): 
    singleton_range = [-10.,10.] 
    dimension = 5 
    num_optima = 5 
    prng = prg__LCG(43.12,-312.3,455,4000)
    prng2 = prg__LCG(43.12,455,-312.3,-4000)
    def prng3(): return prng() + prng2() 

    sec = Sec.generate_bare_instance(singleton_range,dimension,num_optima,prng,idn_tag=0,set_actual_as_max_pr=True)

    ir = IsoRing.generate_IsoRing_from_one_secret(sec,prng,feedback_function_type=0,\
            num_blooms=3,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
            sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,\
            optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE)

    return ir,prng,prng2,prng3


### lone file test 
"""
python3 -m tests.test_crackling
"""
###
class CBridgeClass(unittest.TestCase):

    def test__CBridge__next__case1(self):
        ir,_,prng2,_ = IsoRingANDprng_sample_Y() 

        actual_sec_vec_ratio = 0.0 
        ratio_of_dim_covered = 10 ** -6 
        valid_bounds_ratio = 1.0 
        hs_dict = HypStruct.extract_from_IsoRing_into_HypStruct_dict(ir,prng2,actual_sec_vec_ratio,\
                        ratio_of_dim_covered,valid_bounds_ratio,True)

        hs = hs_dict[6] 

        # subcase: wrong answer, Crackling accepts as correct answer 
        cr = Crackling(ir.idn_tag(),ir.actual_sec_index,hs.opt_index) 
        cb = CBridge(cr,hs,ir)

        while not cb.terminated: 
            next(cb) 
        assert cr.num_attempts == 26 

        assert not np.any(cr.cracked_soln == ir.actual_sec_vec()) 
        assert cr.soln_pr 

        hs_ = deepcopy(hs) 
        hs_.probability_marker += 0.05 

        # subcase: wrong answer, Crackling does not accept as correct answer 
        cr2 = Crackling(ir.idn_tag(),ir.actual_sec_index,hs.opt_index)
        cb2 = CBridge(cr2,hs_,ir)
        while not cb2.terminated: 
            next(cb2) 

        assert cr2.num_attempts == cr.num_attempts 
        assert np.all(cr.cracked_soln == cr2.cracked_soln) 
        assert not cr2.soln_pr 

        return 

    def test__CBridge__next__case2(self):
        ir,_,_,_ = IsoRingANDprng_sample_Y() 

        prng = prg__LCG(-38,-31,45,-4000)
        actual_sec_vec_ratio = 1.0 
        ratio_of_dim_covered = 10 ** -6 
        valid_bounds_ratio = 1.0 
        hs_dict2 = HypStruct.extract_from_IsoRing_into_HypStruct_dict(ir,prng,actual_sec_vec_ratio,\
                        ratio_of_dim_covered,valid_bounds_ratio,False) 
        hs3 = hs_dict2[4] 

            ## subcase: wrong dimension 
        cr3 = Crackling(ir.idn_tag(),ir.current_sec_index,hs3.opt_index)
        cb3 = CBridge(cr3,hs3,ir)
        while not cb3.terminated: 
            next(cb3) 

        assert type(cr3.cracked_soln) == type(None) 
        assert type(cr3.soln_pr) == type(None) 
        assert cr3.num_attempts == 37 


            ## subcase: correct for repr 4 
        ir.set_iso_repr(4) 
        cr4 = Crackling(ir.idn_tag(),ir.current_sec_index,hs3.opt_index)
        cb4 = CBridge(cr4,hs3,ir)
        while not cb4.terminated: 
            next(cb4) 

        assert np.all(cr4.cracked_soln == np.array([ -4.6239 , -10.55495])) 
        assert cr4.num_attempts == 4, "got {}".format(cr4.num_attempts)
        assert cr4.soln_pr

            ## subcase: correct for repr4, <Crackling> does not accept as 
            ##          correct answer 
        hs3.probability_marker += 0.05 
        cr5 = Crackling(ir.idn_tag(),ir.current_sec_index,hs3.opt_index)
        cb5 = CBridge(cr5,hs3,ir)
        while not cb5.terminated: 
            next(cb5) 

        assert np.all(cr5.cracked_soln == np.array([ -4.6239 , -10.55495])) 
        assert cr5.num_attempts == 4, "got {}".format(cr5.num_attempts)
        assert not cr5.soln_pr
        return 

if __name__ == '__main__':
    unittest.main()
