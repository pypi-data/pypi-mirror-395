from .hypothesis import * 
from ..secrets.big_secret import * 


def prng_to_decimal_output(prng):

    def f(): 
        q1 = abs(prng()) 
        q2 = abs(prng())
        if q1 == 0 or q2 == 0: return 0.0 

        if q1 < q2: return q1 / q2
        return q2 / q1 
    return f 

# NOTE: this prng must exclusively output integers 
def n_swaps_on_seq(seq,n,prng):

    ix = [_ for _ in range(len(seq))] 
    ix = prg_seqsort(ix,prng) 

    for i in range(n): 
        # pop index 
        index = ix[i%len(ix)]
        x = seq.pop(index) 

        # re-insert 
        index = prng() % (len(seq) +1)

        seq.insert(index,x) 
    return seq 

class BackgroundInfo:

    """
    info := dict, <Isoring> identifier -> <Sec> index -> <HypStruct> 
    suspected_isoring_to_sec_idn := dict, <IsoRing> -> index of <Sec> most likely to be solution. 
    order_of_cracking := list, of sets of <IsoRing> identifiers, specifying the 
                         order that a <Cracker> will attempt cracking an <IsoRingedChain>. 
    """
    # NOTE: `suspected_isoring_to_sec_idn` can be incomplete w.r.t. `info`. In these cases, 
    # <BackgroundInfo> uses method<default_most_likely_Sec_index_for_IsoRing> to decide 
    # the best <HypStruct>. 
    def __init__(self,info:dict,suspected_isoring_to_sec_idn:dict,order_of_cracking:list): 
        assert BackgroundInfo.verify_valid_info(info) 

        q = set(info.keys()) 
        c = set() 
        for o in order_of_cracking: c |= o 
        assert q == c 

        self.info = info 
        self.suspected_isoring_to_sec_idn = suspected_isoring_to_sec_idn
        self.order_of_cracking = order_of_cracking
        return

    def hypothesis_for_IsoRingANDSec(self,i,s): 
        if not self.hypothesis_exists_for_IsoRingANDSec(i,s): 
            return None 
        return self.info[i][s] 

    def hypothesis_exists_for_IsoRingANDSec(self,i,s): 
        if i not in self.info: 
            return False 
        
        if s not in self.info[i]: 
            return False 
        return True 

    @staticmethod
    def verify_valid_info(info): 
        for k,v in info.items(): 
            if not type(k) == int: return False 
            for k2,v2 in v.items(): 
                if not type(k2) == int: return False 
                if not type(v2) == HypStruct: return False 
        return True 

    # TODO: test this. 
    @staticmethod
    def extract_from_IsoRingedChain(irc,prng,actual_sec_vec_ratio_range,dim_covered_ratio_range,\
        valid_bounds_ratio_range,prioritize_actual_Sec_ratio,shuffle_OOC_ratio,\
        suspected_isoring_to_sec_idn_error_ratio,valid_one_shot_kill_ratio_range=[0.,0.]):
        assert type(irc) == IsoRingedChain 
        assert 0. <= actual_sec_vec_ratio_range[0] <= actual_sec_vec_ratio_range[1] <= 1.
        assert 0. <= dim_covered_ratio_range[0] <= dim_covered_ratio_range[1] <= 1.
        assert 0. <= valid_bounds_ratio_range[0] <= valid_bounds_ratio_range[1] <= 1.
        assert 0. <= prioritize_actual_Sec_ratio <= 1.0
        assert 0. <= shuffle_OOC_ratio <= 1.0
        assert 0. <= suspected_isoring_to_sec_idn_error_ratio <= 1.0

        def prg_(): return int(prng())

        prng_dec = prng_to_decimal_output(prng) 

        info = dict() 
        for idn_tag,ir in irc.ir_dict.items():
            # fetch all ratios and bools 
            if actual_sec_vec_ratio_range[0] == actual_sec_vec_ratio_range[1]: 
                actual_sec_vec_ratio = actual_sec_vec_ratio_range[0]
            else: 
                actual_sec_vec_ratio = modulo_in_range(prng_dec(),actual_sec_vec_ratio_range)

            if dim_covered_ratio_range[0] == dim_covered_ratio_range[1]: 
                ratio_of_dim_covered = dim_covered_ratio_range[0]
            else: 
                ratio_of_dim_covered = modulo_in_range(prng_dec(),dim_covered_ratio_range) 

            if valid_bounds_ratio_range[0] == valid_bounds_ratio_range[1]: 
                valid_bounds_ratio = valid_bounds_ratio_range[0] 
            else: 
                valid_bounds_ratio = modulo_in_range(prng_dec(),valid_bounds_ratio_range)

            if valid_one_shot_kill_ratio_range[0] == valid_one_shot_kill_ratio_range[1]: 
                valid_one_shot_kill_ratio = valid_one_shot_kill_ratio_range[0]
            else: 
                valid_one_shot_kill_ratio = modulo_in_range(prng_dec(),valid_one_shot_kill_ratio_range)

            prioritize_actual_Sec = prng_dec() <= prioritize_actual_Sec_ratio

            hdict = HypStruct.extract_from_IsoRing_into_HypStruct_dict(ir,prng,actual_sec_vec_ratio,\
                ratio_of_dim_covered,valid_bounds_ratio,prioritize_actual_Sec,valid_one_shot_kill_ratio)
            info[idn_tag] = hdict 

        # get the IsoRing identifiers for the IsoRing to Sec index error 
        i2s_error = int(ceil(suspected_isoring_to_sec_idn_error_ratio * len(info))) 
        L = sorted(info.keys())
        L = prg_seqsort(L,prg_)[:i2s_error] 
        S = dict() 
        for k in info.keys(): 
            ir = irc.fetch_IsoRing(k)
            
            # case: correct <Sec> index 
            actual = ir.actual_sec_index
            if k not in L: 
                S[k] = actual 
            else: 
                qs = [_ for _ in range(len(ir.sec_list)) if _ != actual]

                # case: no alternative Sec, use actual 
                if len(qs) == 0: 
                    S[k] = actual
                else: 
                    qi = prg_() % len(qs)
                    S[k] = qs[qi] 
               
        # get the OOC 
        num_swaps = int(ceil(shuffle_OOC_ratio * len(irc.ooc)))
        ooc = n_swaps_on_seq(deepcopy(irc.ooc),num_swaps,prg_)

        return BackgroundInfo(info,S,ooc) 

    def sec_index_for_IsoRing(self,ir_idn): 
        if ir_idn not in self.suspected_isoring_to_sec_idn: 
            return self.default_most_likely_Sec_index_for_IsoRing(ir_idn)
        return self.suspected_isoring_to_sec_idn[ir_idn]

    """
    chooses the <Sec> index with a <HypStruct> of highest probability marker. 
    """
    def default_most_likely_Sec_index_for_IsoRing(self,ir_idn): 
        if ir_idn not in self.info: return None 

        d = self.info[ir_idn] 
        if len(d) == 0: return None 

        secindex_pr = [] 
        for k,v in d.items(): 
            secindex_pr.append((k,v.probability_marker)) 
        
        secindex_pr = sorted(secindex_pr,key=lambda x:x[1],reverse=True)
        return secindex_pr[0][0]