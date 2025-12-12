from .iring import * 
from morebs2.numerical_generator import prg_choose_n
from copy import deepcopy 

def index_in_OOC(ooc,element): 
    for (i,c) in enumerate(ooc): 
        if element in c: 
            return i 
    return -1

class IsoRingedChain:

    def __init__(self,ir_list,prng=None): 
        for ir in ir_list: assert type(ir) == IsoRing
        
        # check for valid order of cracking 
        ooc,stat =IsoRingedChain.calculate_OOC_for_IsoRing_list(ir_list)
        assert stat 

        self.ir_dict = {ir.idn_tag(): ir for ir in ir_list}
        self.ooc = ooc 

        # information used in defensive procedure against Cracker 
        if type(prng) == type(None): 
            self.prng = default_std_Python_prng(output_range=[-10000,10000],rounding_depth=0) 
        else: 
            self.prng = prng 

        # set of IsoRing identifiers 
        self.finished_targetset = set()
        self.current_ir_target = set()  
        return

    #------------------- methods to interact with <Cracker>

    def set_current_ir_targetset(self,targetset):
        assert type(targetset) == set 
        if not self.accept_cracker_targetset(targetset): 
            return False 
        self.current_ir_target = targetset 
        return True 

    """
    Cracker targets instance in units of <IsoRing> sets. 
    Method uses method<accept_cracker_target>. 
    """
    def accept_cracker_targetset(self,targetset): 
        for t in targetset: 
            if not self.accept_cracker_target(t): return False 
        return True 

    """
    responds with boolean if Cracker can proceed with targeting 
    <IsoRing> `target_ir_idn`, based on 
    """
    def accept_cracker_target(self,target_ir_idn): 
        ir = self.fetch_IsoRing(target_ir_idn)  
        if type(ir) == type(None): return False 

        dep = ir.dc_set(True) 
        if dep.intersection(self.finished_targetset) != dep: 
            return False 
        return True 

    #------------------------------------------------------- 

    def repr_dict_for_IsoRings(self,isoring_idn): 
        D = {} 
        for i in isoring_idn: 
            I = self.fetch_IsoRing(i)
            assert type(I) != type(None) 
            D[I.idn_tag()] = I.current_sec_index
        return D 
 
    def register_cracked_IsoRings(self,wanted_finishes:set,recracks:set): 
        self.finished_targetset |= wanted_finishes

        Q = wanted_finishes | recracks 
        for q in Q: 
            self.shift_IsoRing(q)  
        return 

    def shift_IsoRing(self,ir_idn): 
        I = self.fetch_IsoRing(ir_idn)
        return I.register_cracked_sec_index(self.prng)

    #-------------------------------------------------------- 

    def fetch_IsoRing(self,ir_idn):
        if ir_idn not in self.ir_dict: return None 
        return self.ir_dict[ir_idn] 

    @staticmethod
    def prng__add_depANDcodep_to_IsoRingList(ir_list,prng,codep_ratio=0.0):
        assert len(ir_list) > 0 
        assert 0.0 <= codep_ratio <= 1.0 

        idns = [] 
        ir_dict = {} 
        for ir in ir_list:
            idns.append(ir.idn_tag()) 
            ir.clear_depANDcodep_sets()
            ir_dict[ir.idn_tag()] = ir
        
        oodc = IsoRingedChain.prng__idns_to_order_of_depANDcodep(idns,prng,codep_ratio)
        for j in range(len(oodc)): 
            depset = set() 
            for i in range(0,j): 
                depset |= oodc[i] 

            # add codep and dep for each in the set 
            codeps = oodc[j]
            for j_ in codeps: 
                cds = codeps - {j_} 
                ir = ir_dict[j_] 
                ir.assign_DC_set(depset,cds) 
    
    @staticmethod
    def prng__idns_to_order_of_depANDcodep(idns,prng,codep_ratio):
        assert len(set(idns)) == len(idns)

        def prg_(): 
            return int(prng())

        total_conn = len(idns) - 1 
        codep_conn = int(ceil(total_conn * codep_ratio))
        L = prg_seqsort(idns,prg_) 
        L_ = []

        while codep_conn > 0 and len(L) > 0: 
            x = modulo_in_range(prg_(),[1,codep_conn+1]) 
            S = set() 
            i = prg_() % len(L)
            l = L.pop(i)
            S |= {l}

            for _ in range(x):
                if len(L) == 0: break  
                i = prg_() % len(L)
                l = L.pop(i)
                S |= {l} 
            
            L_.append(S) 
            codep_conn -= x 

        while len(L) > 0: 
            L_.append({L.pop(0)})

        L_ = prg_seqsort(L_,prg_)
        return L_

    """
    Calculates an order-of-cracking for the list of 
    <IsoRing>s. During this calculation, determines if 
    dependencies and codependencies of every <IsoRing> 
    result in consistentn <IsoRingedChain>. 
    """
    @staticmethod 
    def calculate_OOC_for_IsoRing_list(ir_list): 
        ir_dict = {ir.idn_tag():ir for ir in ir_list} 
        ooc = [] 

        # start with codependencies and verify
        for ir in ir_list:
            cds = ir.dc_set(False)
            cds = cds | {ir.idn_tag()} 
            qi = index_in_OOC(ooc,ir.idn_tag()) 

            if qi == -1: 
                ooc.append(cds) 
                continue 

            if ooc[qi] != cds: 
                return None,False

        # order elements in first scan
        qx = deepcopy(ooc) 
        for i in range(len(ooc)):
            rx = qx[i]
            rx_ = next(iter(rx)) 
            j = index_in_OOC(ooc,rx_)

            index,stat = IsoRingedChain.order_element_in_OOC(ir_dict,ooc,j) 

            # case: error, co-dep cannot be dep 
            if not stat: 
                return None,False 

        # check for contradictions in second scan
        for i in range(len(ooc)): 
            index, stat = IsoRingedChain.order_element_in_OOC(ir_dict,ooc,i)
            if index != -1: 
                return None,False 

        return ooc, True 

    """
    Auxiliary method for <calculate_OOC_for_IsoRing_list>.
    """
    @staticmethod
    def order_element_in_OOC(ir_dict,ooc,index):

        cds = ooc[index]
        # get all dependencies 
        dep = set() 
        for idn in cds:  
            ir = ir_dict[idn] 
            dep |= ir.dc_set(True) 

        # case: codependencies cannot be dependencies 
        inter = dep.intersection(ooc[index]) 
        if len(inter) > 0: 
            return None,False  


        qi = index 
        x = None  
        for i in range(index + 1,len(ooc)): 
            inter = dep.intersection(ooc[i])  
            if len(inter) > 0: 
                x = i 
        
        if type(x) == type(None): 
            return -1,True 

        # pop element 
        q = ooc.pop(index) 
        ooc.insert(x,q) 
        return x,True   

    @staticmethod 
    def list_of_vectors_to_IsoRingedChain(vec_list,prng,num_blooms_range=[DEFAULT_NUM_BLOOMS,DEFAULT_NUM_BLOOMS+1],
        ratio_of_feedback_functions_type_1:float=1.0,codep_ratio=0.0):  

        def prg_(): return int(prng()) 

        # shuffle `vec_list`
        vec_list = prg_seqsort(vec_list,prg_)

        # generate the list of <Sec> instances 
        sec_list = [] 
        for (i,vec) in enumerate(vec_list): 
            num_optima = modulo_in_range(prg_(),DEFAULT_NUM_OPTIMA_RANGE)
            set_actual_as_max_pr = bool(prg_() % 2)
            sec = Sec.vec_to_bare_instance(vec,singleton_distance=DEFAULT_SINGLETON_DISTANCE_RANGE,\
                num_optima=num_optima,prng=prng,idn_tag=i,set_actual_as_max_pr=set_actual_as_max_pr)
            sec_list.append(sec) 

        # get the <Sec> indexes with feedback function type 1
        num_sec_ftype_1 = int(ceil(ratio_of_feedback_functions_type_1 * len(sec_list))) 
        index_list = [_ for _ in range(len(sec_list))] 

        ftype_1_indices = prg_choose_n(index_list,num_sec_ftype_1,prg_,is_unique_picker=True)

        ir_list = [] 
        for (i,sec) in enumerate(sec_list): 
            # transform each <Sec> into an <IsoRing> 
            feedback_function_type = 1 if i in ftype_1_indices else 0 
            ir = IsoRing.generate_IsoRing_from_one_secret(sec,prng,feedback_function_type,\
                num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
                sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,\
                optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE)
            ir_list.append(ir)

        IsoRingedChain.prng__add_depANDcodep_to_IsoRingList(ir_list,prng,codep_ratio)
        irc = IsoRingedChain(ir_list) 
        return irc 