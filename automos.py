# ---------------------------------
#   ___  _   _ _____ _____ ___  ________ _____ 
#  / _ \| | | |_   _|  _  ||  \/  |  _  /  ___|
# / /_\ \ | | | | | | | | || .  . | | | \ `--. 
# |  _  | | | | | | | | | || |\/| | | | |`--. \
# | | | | |_| | | | \ \_/ /| |  | \ \_/ /\__/ /
# \_| |_/\___/  \_/  \___/ \_|  |_/\___/\____/ 
# AUTHORS: Ren, Orion
# VERSION: 3.1
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

    return f"{value} amps"  # Default case for extremely small values

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

def findK(ECP,LP,inp):
    W = float(input("W (um) = ")) * 1E-4  # because we move from nm -> centimeters
    VSAT = float(input("VSAT (million cm) = ")) * 1E6

    TOX = float(input("T_OX (nm) = ")) * 1E-7

    COX = SILICON_EPISOLON * COX_CONSTANT / (TOX)
    print("SOLVED: COX =", metric_amps(COX, "F/cm^2"))
    kn = (2 * W * VSAT * COX) / (ECP * LP)
    if inp == "1" or inp == "3":
        print("SOLVED: KN =", metric_amps(kn, "A/v^2"))
    else:
        print("SOLVED: KP =", metric_amps(kn, "A/v^2"))
    return kn

while 1:
    print("Enter device parameters...")

    y = float(input("y = "))
    Φ2f = float(input("Φ2f = "))
    λ = float(input("λ = "))
    kn = 0.0
    kp = 0.0
    usePrevK = "N"
    while 1:

        print("(1) LCM NMOS ")
        print("(2) LCM PMOS ")
        print("(3) SCM NMOS ")
        print("(4) SCM PMOS ")
        print("(5) Change device parameters ")

        inp = input("(1), (2), (3), (4), (5): ")
        validEq = ["1","2","3","4"]
        if(not (inp in validEq)):
            break
        is_nmos = (inp == "1" or inp == "3")
        VG = float(input("VG = "))
        VD = float(input("VD = "))
        VS = float(input("VS = "))
        VB = float(input("VB = "))

        if is_nmos:
            VTNO = is_in_enhancement(float(input("VTNO = ")), True)
        else:
            VTPO = is_in_enhancement(float(input("VTPO = ")), False)

        if kn != 0.0 or kp != 0.0:
            if is_nmos:
                usePrevK = input("use previous Kn value? (default = 0) Y or N: ")
            else:
                usePrevK = input("use previous Kp value? (default = 0) Y or N: ")
        if usePrevK == "N":
            GivenK = input("is K given? Y or N: ")
            if (GivenK == "N"):
                if is_nmos:
                    ECN = float(input("ECN = "))
                    LN = float(input("LN = "))
                    kn = findK(ECN, LN, inp)
                else:
                    ECP = float(input("ECP = "))
                    LP = float(input("LP = "))
                    kp = findK(ECP, LP, inp)
            else:
                if (inp == "3"):
                    ECN = float(input("ECN = "))
                    LN = float(input("LN = "))
                elif (inp == "4"):
                    ECP = float(input("ECP = "))
                    LP = float(input("LP = "))

                if is_nmos:
                    kn = float(input("kN = "))
                else:
                    kp = float(input("kP = "))

        if(inp == "1"):
            post_equation(LCM_NMOS(VG, VD, VS, VB, VTNO, y, Φ2f, kn, λ))
            continue

        if(inp == "2"):
            post_equation(LCM_PMOS(VG, VD, VS, VB, VTPO, y, Φ2f, kp, λ,))
            continue

        if(inp == "3"):
            post_equation(SCM_NMOS(VG, VD, VS, VB, VTNO, y, Φ2f, kn, λ, ECN, LN))
            continue
        if(inp == "4"):
            post_equation(SCM_PMOS(VG, VD, VS, VB, VTPO, y, Φ2f, kp, λ, ECP, LP))
            continue

