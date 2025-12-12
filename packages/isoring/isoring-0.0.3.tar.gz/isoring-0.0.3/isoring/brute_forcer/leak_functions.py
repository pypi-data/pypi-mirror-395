from ..secrets.iring import * 
from morebs2.search_space_iterator import * 
from morebs2.matrix_methods import point_in_bounds
from copy import deepcopy 

DEFAULT_HOP_SIZE_RANGE = [2,9]
DEFAULT_BOUND_LENGTH_RANGE = [1,4] 

#------------------------ methods to check bounds 
def bounds_cover_actual_sec_vec(sec,bounds): 
    return point_in_bounds(bounds,sec.seq) 

def bounds_cover_one_optima_point_of_sec(sec,bounds): 
    opt_mat = sec.optima_points() 
    
    for o in opt_mat: 
        if point_in_bounds(bounds,o): return True 
    return False 

#--------------------------------------------------

def prng__search_space_bounds_for_vector(vec,hop_size,bound_length,prng=None):

    assert bound_length >= 1.0 

    # case: prng is None 
    if type(prng) == type(None): 
        bounds = np.array([vec,vec + bound_length])
        return bounds.T 

    X = bound_length / hop_size

    def hop_from_x(x,num_hops,is_back_hop:int):
        assert type(x) in {int,float,np.float32,np.float64} 

        X_ = X if not is_back_hop else -X 

        for _ in range(num_hops):
            x += X_ 
            #x = round(x,5) 
        return round(x,5) 

    # case: calculate a bound such that iterating over it using a search 
    #       space iterator yields the point `vec`. 
    #       bound is calculated using prng 
    V = [] 
    for i in range(len(vec)): 
        left_hops = int(prng()) % hop_size
        right_hops = hop_size - left_hops 

        v0 = hop_from_x(vec[i],left_hops,True) 
        v1 = hop_from_x(vec[i],right_hops,False) 
        V.append([v0,v1]) 
    return np.array(V)

def invalid_search_space_bounds_for_vector(vec,bound_length,prng=None): 

    assert bound_length >= 1.0 
    if type(prng) == type(None): 
        start = vec + bound_length
        end = start + end 
        return np.array([start,end]).T 

    # try five times with the `prng` to output an invalid bounds 
    t = 5 
    stat = False 
    bounds = None 
    while t > 0 and not stat: 
        start = np.array([prng() for _ in range(len(vec))]) 
        end = start + bound_length 
        bounds = np.array([start,end]).T 

        if point_in_bounds(bounds,vec): 
            t -= 1 
        else: 
            stat = True 

    if stat: 
        return bounds 
    return invalid_search_space_bounds_for_vector(vec,bound_length,None) 

def SearchSpaceIterator_for_bounds(bounds,hop_size): 
    startPoint = np.copy(bounds[:,0])
    columnOrder = [i for i in range(bounds.shape[0])]  
    cycleOn = False   
    cycleIs = 0 
    ssi = SearchSpaceIterator(bounds, startPoint, columnOrder, hop_size,cycleOn, cycleIs)
    return ssi 

"""
return: 
- bound for optima point, hop size for searching over bound, corresponding Pr. value for optima point. 
"""
# NOTE: `is_actual_sec_vec` may clash with `optima_point_index`.
def prng_leak_Secret(sec,prng=None,is_actual_sec_vec:bool=True,is_valid_bounds:bool=True,optima_point_index:int=None,\
    valid_one_shot_kill:bool=False):
    assert type(sec) == Sec 
    assert type(is_actual_sec_vec) == bool 
    assert type(is_valid_bounds) == bool 

    if type(prng) == type(None): 
        prng = default_std_Python_prng() 
 
    # fetch the target optima point 
    opt_mat = sec.optima_points()
    if is_actual_sec_vec: 
        seq = deepcopy(sec.seq) 
    elif type(optima_point_index) != type(None): 
        try:
            seq = opt_mat[optima_point_index] 
        except:
            raise ValueError("invalid optima point index")
    else:
        candidates = set([_ for _ in range(opt_mat.shape[0])]) - {sec.seq_index} 
        candidates = sorted(candidates) 
        index = int(prng()) % len(candidates) 
        
        index = candidates[index]
        seq = opt_mat[index] 

    # fetch the corresponding Pr. value for optima point 
    seq_str = vector_to_string(seq,float)
    pr_value = sec.opm[seq_str]

    # mask the optima point with a bound 
    if is_valid_bounds:
        hop_size = modulo_in_range(int(prng()),DEFAULT_HOP_SIZE_RANGE) 
        bound_length = modulo_in_range(int(prng()),DEFAULT_BOUND_LENGTH_RANGE)
        if not valid_one_shot_kill: 
            bounds = prng__search_space_bounds_for_vector(seq,hop_size,bound_length,prng)
        else: 
            bounds = np.array([deepcopy(seq),seq+hop_size]).T 
    else:
        hop_size = 4 
        bound_length = modulo_in_range(int(prng()),DEFAULT_BOUND_LENGTH_RANGE) 
        bounds = invalid_search_space_bounds_for_vector(seq,bound_length,prng)
    return bounds,hop_size,pr_value 

"""
return:
- dict, sec index -> (optima point index,bounds,hop_size,pr_value)
"""
def prng_leak_IsoRing_into_dict(ir:IsoRing,prng,actual_sec_vec_ratio=1.0,ratio_of_dim_covered=1.0,valid_bounds_ratio=1.0,\
    prioritize_actual_Sec:bool=True,valid_one_shot_kill_ratio=0.0): 

    def prg_(): return int(prng()) 

    num_sec = len(ir.sec_list) 
    num_dim_covered = ceil(num_sec * ratio_of_dim_covered)  

    # order of secrets 
    ilist = [_ for _ in range(num_sec)] 
    ilist = prg_seqsort(ilist,prg_) 

    # number of actual sec vec leaks for secrets 
    num_actual_sv_leaks = int(ceil(num_dim_covered * actual_sec_vec_ratio))

    # number of valid bounds
    num_valid_bounds = int(ceil(num_dim_covered * valid_bounds_ratio))

    # number of valid one-shot kills 
    num_valid_one_shot_kills = int(ceil(num_dim_covered * valid_one_shot_kill_ratio))

    if prioritize_actual_Sec: 
        i = ilist.index(ir.actual_sec_index) 
        j = ilist.pop(i) 
        ilist.insert(0,j) 
    ilist = ilist[:num_dim_covered]
    
    D = {}
    for i in ilist:
        s = ir.sec_list[i] 
        
        if num_actual_sv_leaks > 0: 
            is_actual_sec_vec = True 
            num_actual_sv_leaks -= 1 
        else: 
            is_actual_sec_vec = False 

        if num_valid_bounds > 0: 
            is_valid_bounds = True 
            num_valid_bounds -= 1 
        else: 
            is_valid_bounds = False 

        if num_valid_one_shot_kills > 0:
            valid_one_shot_kill = True 
            num_valid_one_shot_kills -= 1 
        else: 
            valid_one_shot_kill = False 
        
        seq_index = s.seq_index()
        if is_actual_sec_vec: 
            optima_point_index = seq_index
        else: 
            ix = [_ for _ in range(len(s.opm))]
            ix2 = ix.index(seq_index)
            ix.pop(ix2)

            if len(ix) != 0: 
                ix3 = prg_() % len(ix)
                optima_point_index = ix.pop(ix3) 
            else: 
                optima_point_index = 0 
        is_actual_sec_vec = False 

        bounds,hop_size,pr_value = prng_leak_Secret(s,prng=prng,is_actual_sec_vec=is_actual_sec_vec,\
            is_valid_bounds=is_valid_bounds,optima_point_index=optima_point_index,\
            valid_one_shot_kill=valid_one_shot_kill) 

        D[i] = (optima_point_index,bounds,hop_size,pr_value) 
    return D 