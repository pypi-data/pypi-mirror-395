from isoring.brute_forcer.leak_functions import * 
import unittest

def SecANDprng_sample_X(): 
    prng = prg__LCG(66,3,7,3212) 
    sec = Sec.generate_bare_instance([-60.,1112.],5,6,prng,idn_tag=0,set_actual_as_max_pr=False)
    return sec,prng 

def IsoRingANDprng_sample_X(): 
    prng = prg__LCG(770,31,72,3212) 
    sec = Sec.generate_bare_instance([-60.,1112.],5,6,prng,idn_tag=0,set_actual_as_max_pr=False)
    ir = IsoRing.generate_IsoRing_from_one_secret(sec,prng,feedback_function_type=0)
    return ir,prng 


### lone file test 
"""
python3 -m tests.test_leak_functions
"""
###
class LeakFunctions(unittest.TestCase):

    def test__prng__search_space_bounds_for_vector__case1(self): 
        prng = prg__LCG(67,43,101,2112)

        vec = np.array([5.654,67.01,55.32])
        hop_size = 6 
        bound_length = 1.0 
        bounds = prng__search_space_bounds_for_vector(vec,hop_size,bound_length,prng=prng)

        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size) 
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,vec) < 0.01: 
                return 
        assert False

    def test__prng__search_space_bounds_for_vector__case2(self): 
        prng = prg__LCG(671,432,9,2112)

        vec = np.array([56.5114,67.11201,551.2132,712.3413])
        hop_size = 9 
        bound_length = 1.0 
        bounds = prng__search_space_bounds_for_vector(vec,hop_size,bound_length,prng=prng)

        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size) 
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,vec) < 0.01: 
                return 
        assert False

    def test__prng__search_space_bounds_for_vector__case3(self): 
        prng = prg__LCG(671,432,9,2112)

        vec = np.array([11.1,311.24141,56.5114,67.11201,551.2132,712.3413])
        hop_size = 3 
        bound_length = 1.0 
        bounds = prng__search_space_bounds_for_vector(vec,hop_size,bound_length,prng=prng)

        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size) 
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,vec) < 0.01: 
                return 
        assert False

    """
    correct target local optimum 
    """
    def test__prng_leak_Secret__case1(self): 
        sec,prng = SecANDprng_sample_X() 

        bounds,hop_size,pr_value = prng_leak_Secret(sec,prng,is_actual_sec_vec=True,is_valid_bounds=True)
        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size)
        i = 0 
        while True: 
            q = next(ssi) 
            i += 1 
            if euclidean_point_distance(q,sec.seq) < 0.05:
                break 

        assert i == 2208,"got {}".format(i)

    """
    correct target local optimum 
    """
    def test__prng_leak_Secret__case2(self): 
        sec,prng = SecANDprng_sample_X() 
        bounds,hop_size,pr_value = prng_leak_Secret(sec,prng,is_actual_sec_vec=True,is_valid_bounds=False)
        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size)
        stat0,stat1 = False,False
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,sec.seq) < 0.05:
                stat0 = True 
            
            q_ = vector_to_string(q,float) 
            if q_ in sec.opm: 
                stat1 = True 

        assert not stat0 and not stat1
        return

    """
    incorrect target local optimum 
    """
    def test__prng_leak_Secret__case3(self): 
        sec,prng = SecANDprng_sample_X() 
        bounds,hop_size,pr_value = prng_leak_Secret(sec,prng,is_actual_sec_vec=False,is_valid_bounds=True)
        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size)

        stat0,stat1 = False,False
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,sec.seq) < 0.05:
                stat0 = True 
            
            q_ = vector_to_string(q,float) 
            if q_ in sec.opm: 
                stat1 = True 

        assert not stat0 and stat1 
        return

    def test__prng_leak_IsoRing_into_dict__case1(self): 
        ir,prng = IsoRingANDprng_sample_X()
        D = prng_leak_IsoRing_into_dict(ir,prng,actual_sec_vec_ratio=1.0,ratio_of_dim_covered=1.0,valid_bounds_ratio=1.0,\
            prioritize_actual_Sec=True)

        assert len(D) == len(ir.sec_list)

        i = 0
        for k,v in D.items(): 
            sec = ir.sec_list[k]
            i += int(bounds_cover_actual_sec_vec(sec,v[1])) 
        assert i == len(ir.sec_list) 

        D2 = prng_leak_IsoRing_into_dict(ir,prng,actual_sec_vec_ratio=1.0,ratio_of_dim_covered=10**-6,valid_bounds_ratio=1.0,\
            prioritize_actual_Sec=True)

        assert list(D2.keys())[0] == ir.actual_sec_index

        prng2 = prg__LCG(0,1,2,3)
        D3 = prng_leak_IsoRing_into_dict(ir,prng2,actual_sec_vec_ratio=1.0,ratio_of_dim_covered=10**-6,valid_bounds_ratio=1.0,\
            prioritize_actual_Sec=False)

        assert list(D3.keys())[0] != ir.actual_sec_index

    """
    incorrect target local optimum 
    """
    def test__prng_leak_IsoRing_into_dict__case2(self): 
        ir,prng = IsoRingANDprng_sample_X()
        
        # subcase: valid bounds 
        D4 = prng_leak_IsoRing_into_dict(ir,prng,actual_sec_vec_ratio=0.0,ratio_of_dim_covered=1.0,valid_bounds_ratio=1.0,\
            prioritize_actual_Sec=False)

        i,j = 0,0
        for k,v in D4.items(): 
            sec = ir.sec_list[k]
            i += int(bounds_cover_actual_sec_vec(sec,v[1]))
            j += int(bounds_cover_one_optima_point_of_sec(sec,v[1])) 
        assert i == 0 and j == 7 

        # subcase: invalid bounds 
        D5 = prng_leak_IsoRing_into_dict(ir,prng,actual_sec_vec_ratio=0.0,ratio_of_dim_covered=1.0,valid_bounds_ratio=0.0,\
            prioritize_actual_Sec=False)

        i,j = 0,0
        for k,v in D5.items(): 
            sec = ir.sec_list[k]
            i += int(bounds_cover_actual_sec_vec(sec,v[1]))
            j += int(bounds_cover_one_optima_point_of_sec(sec,v[1])) 
        assert i == j == 0 

if __name__ == '__main__':
    unittest.main()
