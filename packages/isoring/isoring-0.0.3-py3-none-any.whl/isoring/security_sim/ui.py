from .data_load import * 
import sys 

original_stdout = sys.stdout


def intro_message(): 
    print("This is an interface to simulate the security strength of an arbitrary\n")
    print("Isomorphic Ringed Chain against a third-party's brute force attempts.\n")
    print("Simulation is not completely applicable to real-world data security threats.\n")
    print("Use at your own discretion.")
    print("-------------------------------------------------------------------------------")

def prompt_vec_filepath(): 
    print("\t[!] secrets are vectors.")
    print("\t[!] vectors must be present on every line.")
    print("\t[!] vectors must range in length between 1 through 5.")

    fp = input("[?] enter in filepath of vectors:  ")
    fp = fp.strip()
    irc = load_vector_file_into_IsoRingedChain(fp,prng=default_std_Python_prng())

    try: 
        irc = load_vector_file_into_IsoRingedChain(fp,prng=default_std_Python_prng())
        return irc 
    except: 
        print("\t[!] invalid filepath OR erroneous file. try again.")
        return prompt_vec_filepath()

def bool_prompt(prompt_string): 

    ask = input(prompt_string) 

    ask = ask.strip() 

    if ask == "0": return False 
    if ask == "1": return True 

    print("[!!] invalid input. try again.")
    return bool_prompt(prompt_string)

Q0 = "[?] allow inaccuracies: "
Q1 = "[?] allow incomplete info: "
Q2 = "[?] allow wrong order of cracking: " 
Q3 = "[?] allow one shot kill: " 


def prompt_BackgroundInfo(irc): 
    print("0 is NO, 1 is YES")    
    q0 = bool_prompt(Q0) 
    q1 = bool_prompt(Q1) 
    q2 = bool_prompt(Q2) 
    q3 = bool_prompt(Q3) 

    prng = default_std_Python_prng() 
    return simulation_default_BackgroundInfo_for_IsoRingedChain(\
        irc,prng,q0,q1,q2,q3)  

def prompt_float(): 
    T = input("enter in a positive number (leave blank for infinity):  ")
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
    irc = prompt_vec_filepath()
    bi = prompt_BackgroundInfo(irc)
    bfe = prompt_Cracker_energy(bi,irc) 

    fobj = redirect_print()
    while not bfe.is_finished(): 
        next(bfe) 
    
    bfe.crck.soln_synopsis() 
    fobj.close() 
    sys.stdout = original_stdout
    
    print("DONE!")
    return 

if __name__ == "__main__":

    ui_method()