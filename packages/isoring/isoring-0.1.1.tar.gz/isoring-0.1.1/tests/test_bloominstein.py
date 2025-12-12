from isoring.secrets.bloominstein import * 
import unittest

### lone file test 
"""
python3 -m tests.test_bloominstein 
"""
###
class BloomOfSecretClass(unittest.TestCase):

    def test__BloomOfSecret__next__case1(self):
        singleton_range = [-100,100] 
        dimension = 5 
        num_optima = 5 
        prng = default_std_Python_prng(integer_seed=55,output_range=[0,1000],rounding_depth=3)
        s = Sec.generate_bare_instance(singleton_range,dimension,num_optima,prng,idn_tag=0,set_actual_as_max_pr=True)

        XX = BloomOfSecret(s,prng,num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
                sec_vec_multiplier_range=[0.5,2.0],optima_multiplier_range=[0.5,2.0])

        for i in range(DEFAULT_NUM_BLOOMS):
            assert type(next(XX)) != type(None) 

        assert type(next(XX)) == type(None) 
        return

    def test__BloomOfSecret__next__case2(self):
        singleton_range = [-100,100] 
        dimension = 5 
        num_optima = 5 
        prng = default_std_Python_prng(integer_seed=55,output_range=[0,1000],rounding_depth=3)
        s = Sec.generate_bare_instance(singleton_range,dimension,num_optima,prng,idn_tag=0,set_actual_as_max_pr=True)

        num_blooms = DEFAULT_BLOOM_VECTOR_DIM_RANGE[1] - DEFAULT_BLOOM_VECTOR_DIM_RANGE[0]

        try: 
            XX = BloomOfSecret(s,prng,num_blooms=num_blooms,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
                sec_vec_multiplier_range=[0.5,2.0],optima_multiplier_range=[0.5,2.0])
            assert False 
        except: 
            assert True 

if __name__ == '__main__':
    unittest.main()
