# ---------------------------------
#   ___  _   _ _____ _____ ___  ________ _____ 
#  / _ \| | | |_   _|  _  ||  \/  |  _  /  ___|
# / /_\ \ | | | | | | | | || .  . | | | \ `--. 
# |  _  | | | | | | | | | || |\/| | | | |`--. \
# | | | | |_| | | | \ \_/ /| |  | \ \_/ /\__/ /
# \_| |_/\___/  \_/  \___/ \_|  |_/\___/\____/ 
# AUTHORS: Ren, Orion
# VERSION: 3.2
# DESC: Software for the TI-NSPIRE CX-II CAS. Calculates transistor current for NMOS and PMOS MOSFETs.
# ---------------------------------
import math

COX_CONSTANT = (8.854E-14)
SILICON_EPISOLON = 3.97

def metric_amps(value, suffix = "amps"):
    metric_prefixes = [
        (1e12, "tera"),
        (1e9, "giga"),
        (1e6, "mega"),
        (1e3, "kilo"),
        (1, ""),
        (1e-3, "milli"),
        (1e-6, "micro"),
        (1e-9, "nano"),
        (1e-12, "pico")
    ]

    for factor, prefix_full in metric_prefixes:
        if abs(value) >= factor:
            converted_value = value / factor
            return f"{converted_value:.5f} {prefix_full}{suffix}"

    return f"{value} {suffix}"  # Default case for extremely small values

def LCM_NMOS(VG, VD, VS, VB, VTNO, y, Φ2f, kn, λ):
    VGS = VG - VS
    VSB = VS - VB
    VDS = VD - VS
    VTN = VTNO

    if(VS != VB):
        VTN = VTNO + y*(math.sqrt(abs(Φ2f)+VSB) - math.sqrt(abs(Φ2f)))

    VDSSAT = VGS - VTN

    if(VGS < VTN):
        print("Device is off!")
        return 0
    elif(VDS <= VDSSAT):
        print("Device is in TRIODE!")
        return kn*((VGS-VTN)*VDS-(VDS**2)/2)
    else:
        print("Device is in SATURATION!")
        return (kn/2)*((VGS-VTN)**2)*(1+λ*(VDS-VDSSAT))

def LCM_PMOS(VG, VD, VS, VB, VTPO, y, Φ2f, kp, λ):
    VSG = VS - VG
    VBS = VB - VS
    VSD = VS - VD
    VTP = VTPO

    if(VS != VB):
        VTP = VTPO - y*(math.sqrt(abs(Φ2f)+VBS) - math.sqrt(abs(Φ2f)))

    VDSSAT = VSG + VTP

    if(VSG < -VTP):
        print("Device is off!")
        return 0
    elif(VSD <= VDSSAT):
        print("Device is in TRIODE!")
        return kp*((VSG+VTP)*VSD-(VSD**2)/2)
    else:
        print("Device is in SATURATION!")
        return (kp/2)*((VSG+VTP)**2)*(1+λ*(VSD-VDSSAT))


def SCM_NMOS(VG, VD, VS, VB, VTNO, y, Φ2f, kn, λ, ECN, LN):
    VGS = VG - VS
    VSB = VS - VB
    VDS = VD - VS
    VTN = VTNO

    if(VS != VB):
        VTN = VTNO + y*(math.sqrt(abs(Φ2f)+VSB) - math.sqrt(abs(Φ2f)))

    VDSSAT = ((VGS - VTN)*ECN*LN)/((VGS - VTN) + (ECN*LN))

    if(VGS < VTN):
        print("Device is off!")
        return 0
    elif(VDS <= VDSSAT):
        print("Device is in TRIODE!")
        return (kn/(1+(VDS/(ECN*LN))))*((VGS-VTN)*VDS-(VDS**2)/2)
    else:
        print("Device is in SATURATION!")
        return (kn/2)*(ECN*LN)*(((VGS-VTN)**2)/((VGS-VTN)+(ECN*LN)))*(1+λ*(VDS-VDSSAT))


def SCM_PMOS(VG, VD, VS, VB, VTPO, y, Φ2f, kp, λ, ECP, LP):
    VSG = VS - VG
    VBS = VB - VS
    VSD = VS - VD
    VTP = VTPO

    if(VS != VB):
        VTP = VTPO - y*(math.sqrt(abs(Φ2f)+VBS) - math.sqrt(abs(Φ2f)))

    VDSSAT = ((VSG + VTP)*ECP*LP)/((VSG + VTP) + (ECP*LP))

    if(VSG < -VTP):
        print("Device is off!")
        return 0
    elif(VSD <= VDSSAT):
        print("Device is in TRIODE!")
        return (kp/(1+(VSD/(ECP*LP))))*((VSG+VTP)*VSD-(VSD**2)/2)
    else:
        print("Device is in SATURATION!")
        return (kp/2)*(ECP*LP)*(((VSG+VTP)**2)/((VSG+VTP)+(ECP*LP)))*(1+λ*(VSD-VDSSAT))

def is_in_enhancement(value, is_nmos):
    failed = False
    if(is_nmos): # nmos
        failed = (value < 0)
    else: # pmos
        failed = (value > 0)

    if(not failed):
        return value

    answer = input("The value you entered is for a depleted MOSFET. Would you like it to be an enhancement MOSFET? (y/n): ")
    if((answer.lower()[0]) == "y"):
        value = -value

        print(f"{'VTNO' if is_nmos else 'VTPO'} is now {value}")
    return value

def post_equation(equation_result):
    print("ID = " + metric_amps(equation_result))
    input("Enter to continue...")

while 1:
    print("Enter device parameters...")

    y = float(input("y = "))
    Φ2f = float(input("Φ2f = "))
    λ = float(input("λ = "))

    while 1:

        print("(1) LCM NMOS ")
        print("(2) LCM PMOS ")
        print("(3) SCM NMOS ")
        print("(4) SCM PMOS ")
        print("(5) Change device parameters ")

        inp = input("(1), (2), (3), (4), (5): ")

        if(inp == "5"):
            break

        VG = float(input("VG = "))
        VD = float(input("VD = "))
        VS = float(input("VS = "))
        VB = float(input("VB = "))

        if(inp == "1"):
            VTNO = is_in_enhancement(float(input("VTNO = ")), True)

            kn = float(input("kn = "))

            post_equation(LCM_NMOS(VG, VD, VS, VB, VTNO, y, Φ2f, kn, λ))
            continue

        if(inp == "2"):
            VTPO = is_in_enhancement(float(input("VTPO = ")), False)

            kp = float(input("kp = "))

            post_equation(LCM_PMOS(VG, VD, VS, VB, VTPO, y, Φ2f, kp, λ))
            continue

        if(inp == "3"):
            VTNO = is_in_enhancement(float(input("VTNO = ")), True)

            # kn = float(input("kn = "))
            W = float(input("W (um) = ")) * 1E-4 # because we move from nm -> centimeters
            # L = float(input("L = "))
            VSAT = float(input("VSAT (million cm) = ")) * 1E6

            TOX = float(input("T_OX (nm) = ")) * 1E-7
            ECN = float(input("ECN = "))
            LN = float(input("LN = "))

            COX = SILICON_EPISOLON*COX_CONSTANT/(TOX)
            print("SOLVED: COX =", metric_amps(COX, "F/cm^2"))
            kn = (2*W*VSAT*COX)/(ECN*LN)
            print("SOLVED: KN =", metric_amps(kn, "A/v^2"))

            post_equation(SCM_NMOS(VG, VD, VS, VB, VTNO, y, Φ2f, kn, λ, ECN, LN))

        if(inp == "4"):
            VTPO = is_in_enhancement(float(input("VTPO = ")), False)

            # kp = float(input("kp = "))
            W = float(input("W (um) = ")) * 1E-4 # because we move from nm -> centimeters
            # L = float(input("L = "))
            VSAT = float(input("VSAT (million cm) = ")) * 1E6
    
            TOX = float(input("T_OX (nm) = ")) * 1E-7
            ECP = float(input("ECP = "))
            LP = float(input("LP = "))

            COX = SILICON_EPISOLON*COX_CONSTANT/(TOX)
            print("SOLVED: COX =", metric_amps(COX, "F/cm^2"))
            kn = (2*W*VSAT*COX)/(ECP*LP)
            print("SOLVED: KN =", metric_amps(kn, "A/v^2"))

            post_equation(SCM_PMOS(VG, VD, VS, VB, VTPO, y, Φ2f, kp, λ, ECP, LP))

