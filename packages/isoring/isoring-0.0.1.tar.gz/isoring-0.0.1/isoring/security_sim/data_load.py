from ..brute_forcer.brute_force_env import * 
from morebs2.message_streamer import * 

DEFAULT_MAX_VECTOR_LENGTH = 5 
DEFAULT_MAX_NUM_VECTORS = 50 

def read_vector_file(fp,max_vector_length=DEFAULT_MAX_VECTOR_LENGTH,max_num_vectors=DEFAULT_MAX_NUM_VECTORS): 
    
    vec_list = [] 
    with open(fp, 'r') as fin:
        for line in fin:
            if max_num_vectors == 0: break 

            row = line.strip()
            vec = string_to_vector(row,float)
            assert 0 < len(vec) <= max_vector_length
            vec_list.append(vec) 
            max_num_vectors -= 1 
    
    return vec_list 
    
def load_vector_file_into_IsoRingedChain(fp,prng=default_std_Python_prng()):
    prg_ = prng_to_decimal_output(prng)
    codep_ratio = prg_() 

    vec_list = read_vector_file(fp) 
    
    return IsoRingedChain.list_of_vectors_to_IsoRingedChain(vec_list,prng=default_std_Python_prng(),\
        num_blooms_range=[DEFAULT_NUM_BLOOMS-1,DEFAULT_NUM_BLOOMS],\
        ratio_of_feedback_functions_type_1=1.0,codep_ratio=codep_ratio)

def simulation_default_BackgroundInfo_for_IsoRingedChain(irc,prng,allow_inaccuracies:bool,\
    allow_incomplete_info:bool,allow_wrong_OOC:bool,allow_one_shot_kill:bool):

    prg_ = prng_to_decimal_output(prng) 

    prioritize_actual_Sec_ratio = 1.0 
    if allow_inaccuracies: 
        actual_sec_vec_ratio_range = np.round(np.sort([prg_(),prg_()]),5)
        valid_bounds_ratio_range = np.round(np.sort([prg_(),prg_()]),5)
        suspected_isoring_to_sec_idn_error_ratio = prg_()
    else: 
        actual_sec_vec_ratio_range = [1.0,1.0]
        valid_bounds_ratio_range = [1.0,1.0] 
        suspected_isoring_to_sec_idn_error_ratio = 0.0 
         
    if allow_incomplete_info: 
        dim_covered_ratio_range = np.round(np.sort([prg_(),prg_()]),5)
    else: 
        dim_covered_ratio_range = [1.,1.]

    if allow_wrong_OOC: 
        shuffle_OOC_ratio = prg_() 
    else: 
        shuffle_OOC_ratio = 0.0 
        
    if allow_one_shot_kill:
        valid_one_shot_kill_ratio_range = [1.,1.]
    else: 
        valid_one_shot_kill_ratio_range = [0.,0.]

    bi = BackgroundInfo.extract_from_IsoRingedChain(irc,prng,actual_sec_vec_ratio_range,\
        dim_covered_ratio_range,valid_bounds_ratio_range,prioritize_actual_Sec_ratio,\
        shuffle_OOC_ratio,suspected_isoring_to_sec_idn_error_ratio,valid_one_shot_kill_ratio_range)
    return bi 

def instantiate_simulation_BruteForceEnv(bi,irc,cracker_energy:float): 
    prng = default_std_Python_prng() 
    crck = Cracker(bi,DEFAULT_MAX_NUM_VECTORS,cracker_energy,True)  
    bfe = BruteForceEnv(crck,irc,prng,True) 
    return bfe 