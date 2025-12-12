from isoring.secrets.iring import * 
import unittest

def Sec_sample_X(): 
    singleton_range = [-100,100] 
    dimension = 4 
    num_optima = 10 
    prng = default_std_Python_prng(integer_seed=527,output_range=[0,1000],rounding_depth=3)
    s = Sec.generate_bare_instance(singleton_range,dimension,num_optima,prng,idn_tag=5,set_actual_as_max_pr=True)
    return s 

def IsoRing_sample_X(feedback_function_type):
    s = Sec_sample_X()
    prng = default_std_Python_prng(integer_seed=302,output_range=[0,1000],rounding_depth=3)
    return IsoRing.generate_IsoRing_from_one_secret(s,prng,feedback_function_type,\
        num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
        sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE)

### lone file test 
"""
python3 -m tests.test_iring 
"""
###
class IsoRingClass(unittest.TestCase):

    def test__IsoRing__generate_IsoRing_from_one_secret__case1(self):

        ir0 = IsoRing_sample_X(0)
        ir1 = IsoRing_sample_X(1) 
        s = Sec_sample_X() 

        V = ir0.actual_sec_vec()
        V2 = ir1.actual_sec_vec()

        assert (V==V2).all()
        assert (V == s.seq).all() 

        S = ir0.iso_repr()
        S2 = ir1.iso_repr() 

        assert (S.seq == S2.seq).all() 
        assert (S.seq == s.seq).all() 
        assert (ir0.sec_list[ir0.actual_sec_index].seq == S.seq).all() 
        assert (ir1.sec_list[ir1.actual_sec_index].seq == S.seq).all() 
        assert ir0.actual_sec_index != 0 

    def test__IsoRing__provide_feedback_distance_vec(self): 
        ir0 = IsoRing_sample_X(0)
        ir1 = IsoRing_sample_X(1) 

        Q = np.array([ 77.685,  30.222,  87.129, -23.642])
        Q2 = np.array([ 77.685,  31.222,  87.129, -20.642])
        s00 = ir0.provide_feedback_distance_vec(Q)
        s01 = ir0.provide_feedback_distance_vec(Q2) 
        assert s00[8] == 0.
        assert 4. > s01[8] > 3.

        s10 = ir1.provide_feedback_distance_vec(Q)
        s11 = ir1.provide_feedback_distance_vec(Q2) 

        assert 820 > s10[8] > 800 
        assert 505 > s11[8] > 500

if __name__ == '__main__':
    unittest.main()
