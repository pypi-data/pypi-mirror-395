from isoring.secrets.big_secret import * 
import unittest

def IsoRing_list_sample_Q(): 
    prng = prg__LCG(66,3,7,3212) 

    ir_list = [] 
    for i in range(15): 
        sec = Sec.generate_bare_instance([-60.,1112.],5,6,prng,idn_tag=i,set_actual_as_max_pr=False)

        ir = IsoRing.generate_IsoRing_from_one_secret(sec,prng,0,\
            num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
            sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,
            optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE)
        ir_list.append(ir) 

    IsoRingedChain.prng__add_depANDcodep_to_IsoRingList(ir_list,prng,codep_ratio=0.3)
    return ir_list 

def IsoRingedChain_Accessories_sample_R():

    prng = prg__LCG(66,3,7,3212) 
    prng2 = prg__LCG(16.36,13.23,74.1434,37177.05) 

    vec_lengths = [4,8,9,13] 
    vec_list = [] 
    for i in range(0,15): 
        qi = i % 4
        vec_list.append(one_vec(prng2,vec_lengths[qi],[-2000.,2000.])) 

    return vec_list,prng,prng2 

### lone file test 
"""
python3 -m tests.test_big_secret  
"""
###
class IsoRingedChainClass(unittest.TestCase):

    def test__IsoRingedChain__prng__idns_to_order_of_depANDcodep__case1(self):
        prng = default_std_Python_prng(integer_seed=302,output_range=[0,1000],rounding_depth=3)
        X = [6,1,3,10,12,43,56,13,31,42,113,57,65,78,110,95,93,91,16]

        Y = IsoRingedChain.prng__idns_to_order_of_depANDcodep(X[:],prng,0)
        for y in Y: 
            assert len(y) == 1 

        Y2 = IsoRingedChain.prng__idns_to_order_of_depANDcodep(X[:],prng,0.5)

        s = 0 
        for y in Y2: 
            if len(y) == 1: continue 
            s += len(y) - 1 
        assert s == ceil(0.5 * (len(X) - 1)), "got {} wanted {}".format(s,ceil(0.5 * (len(X) - 1)))
        return 


    def test__IsoRingedChain__calculate_OOC_for_IsoRing_list__case1(self): 

        ir_list = IsoRing_list_sample_Q()
        ooc,stat = IsoRingedChain.calculate_OOC_for_IsoRing_list(ir_list)
        assert stat

        sol = [{0, 12}, {4}, {5}, {6}, {8, 3, 11, 7}, {13}, {1}, {2}, {9, 14}, {10}]
        assert ooc == sol 

    def test__IsoRingedChain__calculate_OOC_for_IsoRing_list__case2(self): 

        ir_list = IsoRing_list_sample_Q()


        ## case 1 
        irings = ir_list[:6] 

        for ir in irings: 
            ir.clear_depANDcodep_sets() 

        irings[0].assign_DC_set({1,2,3},set())
        irings[1].assign_DC_set({0,2,3},set())
        irings[2].assign_DC_set({3},set())


        ooc,stat = IsoRingedChain.calculate_OOC_for_IsoRing_list(irings)
        assert not stat 

        ## case 2 
        for ir in irings: 
            ir.clear_depANDcodep_sets() 

        irings[0].assign_DC_set(set(),{1,2})
        irings[1].assign_DC_set(set(),{1,2})
        irings[2].assign_DC_set(set(),{1,2}) 
        irings[3].assign_DC_set({1,2},{0}) 

        ooc,stat = IsoRingedChain.calculate_OOC_for_IsoRing_list(irings)
        assert not stat 

        ## case 3 
        for ir in irings: 
            ir.clear_depANDcodep_sets()

        irings[0].assign_DC_set({1},set())
        irings[1].assign_DC_set({2},set())
        irings[2].assign_DC_set({3},set())
        irings[3].assign_DC_set(set(),set())
        irings[4].assign_DC_set({1,2,5},set())
        irings[5].assign_DC_set({0},set())

        ooc,stat = IsoRingedChain.calculate_OOC_for_IsoRing_list(irings)
        assert not stat 
        return 

    def test__IsoRingedChain__list_of_vectors_to_IsoRingedChain__case1(self): 
        
        vec_list,prng,prng2 = IsoRingedChain_Accessories_sample_R()
        irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list,prng2,num_blooms_range=[DEFAULT_NUM_BLOOMS,DEFAULT_NUM_BLOOMS+1])

        dsize = 0 
        csize = 0 
        for ir in irc.ir_dict.values(): 
            dsize += len(ir.dc_set(True))
            csize += len(ir.dc_set(False)) 

        assert dsize == 105 == csize + 105 
        return

    def test__IsoRingedChain__list_of_vectors_to_IsoRingedChain__case2(self): 
        vec_list,prng,prng2 = IsoRingedChain_Accessories_sample_R()
        irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list,prng,num_blooms_range=[DEFAULT_NUM_BLOOMS,DEFAULT_NUM_BLOOMS+1],\
            codep_ratio=1.0)

        dsize = 0 
        csize = 0 
        for ir in irc.ir_dict.values(): 
            dsize += len(ir.dc_set(True))
            csize += len(ir.dc_set(False)) 

        assert dsize == 26
        assert csize == 158

        L = set([len(o) for o in irc.ooc])
        assert L == {2,13} 

    def test__IsoRingedChain__list_of_vectors_to_IsoRingedChain__case3(self):
        prng = prg__LCG(-66,3,7,-3212) 
        prng2 = prg__LCG(16.36,13.23,74.1434,37177.05) 
        def prng3(): return prng() + prng2() 

        vec_lengths = [4,8,9,13] 
        vec_list = [] 
        for i in range(0,15): 
            qi = i % 4
            vec_list.append(one_vec(prng2,vec_lengths[qi],[-2000.,2000.])) 

        try: 
            irc = IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list,prng3,\
                num_blooms_range=[DEFAULT_NUM_BLOOMS,DEFAULT_NUM_BLOOMS+1],codep_ratio=1.0)
        except: 
            assert False 

if __name__ == '__main__':
    unittest.main()
