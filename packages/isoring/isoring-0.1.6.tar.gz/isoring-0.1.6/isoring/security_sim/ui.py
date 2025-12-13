from .data_load import * 
import sys 

original_stdout = sys.stdout

def bool_prompt(prompt_string): 

    ask = input(prompt_string) 

    ask = ask.strip() 

    if ask == "0": return False 
    if ask == "1": return True 

    print("[!!] invalid input. try again.")
    return bool_prompt(prompt_string)

Q_NEG = "\t0 is NO, 1 is YES" 
Q0 = "[?] allow inaccuracies: "
Q1 = "[?] allow incomplete info: "
Q2 = "[?] allow wrong order of cracking: " 
Q3 = "[?] allow one shot kill: " 
Q4 = "[?] load Python standard random state: " 
Q5 = "[?] save Python standard random state: " 
Q6 = "[?] enter in a positive number (leave blank for infinity):  "
Q7 = "[?] enter in range for hop size (leave blank for default [2,9], min is 3,max is 9):  " 


def intro_message(): 
    print("This is an interface to simulate the security strength of an arbitrary\n")
    print("Isomorphic Ringed Chain against a third-party's brute force attempts.\n")
    print("Simulation is not completely applicable to real-world data security threats.\n")
    print("Use at your own discretion.")
    print("-------------------------------------------------------------------------------")

def prompt_loadORsave_std_Python_random_state(is_load:bool):
    if is_load: 
        S,F = Q4,load_std_Python_random_state
    else: 
        S,F = Q5,save_std_Python_random_state

    stat = bool_prompt(S)
    if not stat: return False 

    fp = input("[?] enter in filepath:  ")
    fp = fp.strip()
    return F(fp)

def prompt_vec_filepath(): 
    print("\t[!] secrets are vectors.")
    print("\t[!] vectors must be present on every line (50 vectors,50 lines max)") 
    print("\t[!] vectors must range in length between 1 through 5.")
    print("\t[!] EX:  101,110,100,111\n") 
    fp = input("[?] enter in filepath of vectors:  ")
    fp = fp.strip()

    try: 
        irc = load_vector_file_into_IsoRingedChain(fp,prng=default_std_Python_prng())
        return irc 
    except: 
        print("\t[!] invalid filepath OR erroneous file. try again.")
        return prompt_vec_filepath()

def prompt_hop_size(): 
    H = input(Q7)

    if H.strip() == "": return 9 

    try: 
        i = int(H) 
        assert 2 < i <= 9 
        return i 
    except: 
        print("invalid hop size. try again.")
        return prompt_hop_size()

def prompt_BackgroundInfo(irc): 
    print(Q_NEG)    
    q0 = bool_prompt(Q0) 
    q1 = bool_prompt(Q1) 
    q2 = bool_prompt(Q2) 
    q3 = bool_prompt(Q3) 
    q4 = prompt_hop_size() 
    prng = default_std_Python_prng() 
    return simulation_default_BackgroundInfo_for_IsoRingedChain(\
        irc,prng,q0,q1,q2,q3,q4)   

def prompt_float(): 
    T = input(Q6)
    if T.strip() == "": return float('inf')

    try: 
        x = float(T) 
        if x <= 0: 
            print("invalid number")
            return prompt_float()
        else: 
            return x 
    except: 
        print("invalid number")
        return prompt_float() 

def prompt_Cracker_energy(bi,irc): 

    F = prompt_float() 
    return instantiate_simulation_BruteForceEnv(bi,irc,F)
    
def redirect_print(): 

    # Save original stdout
    print_fp = input("[?] enter filepath for output:  ")

    try: 
        f = open(print_fp,"w")
        sys.stdout = f
        return f 
    except: 
        print("[:-(  invalid filepath.try again.")
     
    return redirect_print()

def ui_method(): 
    intro_message()
    print(Q_NEG)     
    stat0 = prompt_loadORsave_std_Python_random_state(True) 
    if not stat0: prompt_loadORsave_std_Python_random_state(False)
    
    irc = prompt_vec_filepath()
    bi = prompt_BackgroundInfo(irc)
    bfe = prompt_Cracker_energy(bi,irc) 

    fobj = redirect_print()
    while not bfe.is_finished(): 
        next(bfe) 
    
    bfe.crck.soln_synopsis() 

    print("[$] remaining Cracker energy: {}".format(bfe.crck.energy)) 
    fobj.close() 
    sys.stdout = original_stdout
    
    print("DONE!")
    return 

if __name__ == "__main__":

    ui_method()