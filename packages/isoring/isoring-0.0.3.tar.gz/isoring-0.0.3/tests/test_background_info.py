from isoring.brute_forcer.background_info import * 
import unittest

def IsoRingedChainANDprng_sample_T(): 
    prng = prg__LCG(-66,3,7,-3212) 
    prng2 = prg__LCG(16.36,13.23,74.1434,37177.05) 
    def prng3(): return prng() + prng2() 

    vec_lengths = [4,8,9,13] 
    vec_list = [] 
    for i in range(0,15): 
        qi = i % 4
        vec_list.append(one_vec(prng2,vec_lengths[qi],[-2000.,2000.])) 

    irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list,prng3,\
        num_blooms_range=[DEFAULT_NUM_BLOOMS,DEFAULT_NUM_BLOOMS+1],codep_ratio=0.4)

    return irc,prng3 



### lone file test 
"""
python3 -m tests.test_background_info  
"""
###
class BackgroundInfoClass(unittest.TestCase):

    def test__BackgroundInfo__extract_from_IsoRingedChain__case1(self):
        irc,prng3 = IsoRingedChainANDprng_sample_T() 

        # case: complete information 
        bi = BackgroundInfo.extract_from_IsoRingedChain(irc,prng3,actual_sec_vec_ratio_range=[1.,1.],\
            dim_covered_ratio_range=[1.,1.],valid_bounds_ratio_range=[1.,1.],prioritize_actual_Sec_ratio=1.,\
            shuffle_OOC_ratio=0.0,suspected_isoring_to_sec_idn_error_ratio=0.0)

        assert bi.order_of_cracking == irc.ooc 

        D = {k:v.actual_sec_index for k,v in irc.ir_dict.items()}

        assert bi.suspected_isoring_to_sec_idn == D 

    def test__BackgroundInfo__extract_from_IsoRingedChain__case2(self):
        irc,prng3 = IsoRingedChainANDprng_sample_T() 
        D = {k:v.actual_sec_index for k,v in irc.ir_dict.items()}

        bi2 = BackgroundInfo.extract_from_IsoRingedChain(irc,prng3,actual_sec_vec_ratio_range=[1.,1.],\
            dim_covered_ratio_range=[1.,1.],valid_bounds_ratio_range=[1.,1.],prioritize_actual_Sec_ratio=1.,\
            shuffle_OOC_ratio=0.5,suspected_isoring_to_sec_idn_error_ratio=0.5)

        assert bi2.order_of_cracking != irc.ooc 

        c = 0 
        for k,v in D.items(): 
            if bi2.suspected_isoring_to_sec_idn[k] != v: 
                c += 1 
        assert c == 8 

        bi3 = BackgroundInfo.extract_from_IsoRingedChain(irc,prng3,actual_sec_vec_ratio_range=[1.,1.],\
            dim_covered_ratio_range=[1.,1.],valid_bounds_ratio_range=[1.,1.],prioritize_actual_Sec_ratio=1.,\
            shuffle_OOC_ratio=0.5,suspected_isoring_to_sec_idn_error_ratio=0.5)

        assert bi3.order_of_cracking != irc.ooc 

        c = 0 
        for k,v in D.items(): 
            if bi3.suspected_isoring_to_sec_idn[k] != v: 
                c += 1 
        assert c == 8 

    """
    demonstrates `valid one shot kill` feature
    """
    def test__BackgroundInfo__extract_from_IsoRingedChain__case3(self): 
        irc,prng3 = IsoRingedChainANDprng_sample_T() 

        bi2 = BackgroundInfo.extract_from_IsoRingedChain(irc,prng3,actual_sec_vec_ratio_range=[1.,1.],\
            dim_covered_ratio_range=[1.,1.],valid_bounds_ratio_range=[1.,1.],prioritize_actual_Sec_ratio=1.,\
            shuffle_OOC_ratio=0.5,suspected_isoring_to_sec_idn_error_ratio=0.0,valid_one_shot_kill_ratio_range=[1.,1.]) 

        for k,v in bi2.info.items(): 
            ir = irc.fetch_IsoRing(k)
            ir.reset_iso_repr() 
            sec = ir.iso_repr()
            
            hs = v[ir.actual_sec_index]
            assert np.all(hs.suspected_subbound[:,0] == ir.actual_sec_vec()) 
            
        return

if __name__ == '__main__':
    unittest.main()
