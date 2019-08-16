import numpy as np

def transform_cashflow(time, flow):
    new_time = []
    new_flow = []
    t_min = min(time)
    t_max = max(time)
    for i in range(t_min, t_max+1):
        new_time.append(i)
        new_flow.append(0 if not i in time else flow[time.index(i)])
    return new_time, new_flow

l = [
    # [-100, 75, 50, 0, 0],
    # [+100, +200, -100, -240, +50],
    # [+100, +200, -100, -250, +50],
    # [+100, +200, -100, -400, +50],
    # [+100, +200, -100, -600, +50],
    #[-193307, 1528415]
    [-1, -1, -1, 2.9, -1]
]

def f_npv(cf, irr):
    return sum([cf[i] / (1 + irr)**i for i in range(len(cf))])

def gradient_descent(cf, max_iter=10000000000):
    iter = 0
    cf_sum = sum(cf)
    repel_from_origin = True
    done = False
    irr = 0
    step = 0.00001
    while iter < max_iter and not done:
        npv = f_npv(cf, irr)
        npv_step = f_npv(cf, irr+step)
        print("IRR: "+str(irr) + ", NPV = " + str(npv))
        #print(" - "+str(iter) + ": " + str(npv) + " ... " + str(npv_step))
        if npv == 0:
            return irr

        # if going in the correct direction, deactivate repelling force
        if abs(npv) < abs(npv_step) and cf_sum < 0:
            repel_from_origin = False
        if abs(npv) > abs(npv_step) and cf_sum > 0:
            repel_from_origin = False

        if repel_from_origin:
            # fly away from origin until peak is reached
            if cf_sum > 0:
                irr += step * abs(npv)
            elif cf_sum < 0:
                irr -= step * abs(npv)
            else:
                return 0.0
        else:
            # do general gradient descent
            if abs(npv) < abs(npv_step):
                irr -= step * min(abs(npv), 100)
            else:
                irr += step * min(abs(npv), 100)

        if irr <= -1:
            return -1

        iter += 1

    print("cannot find npv = 0")
    return irr



def irr(values):
    res = np.roots(values[::-1])
    #mask = (res.imag == 0) #& (res.real > 0)
    #if not mask.any():
    #    return np.nan
    #print(type
    # (res))
    #print(res)
    #print(mask)
    #res = res[mask].real
    print(res)
    # NPV(rate) = 0 can have more than one solution so we return
    # only the solution closest to zero.
    rate = 1 / res - 1
    print(rate)
    rate = rate.item(np.argmin(np.abs(rate)))
    return rate

# def our_calc():
#
#     for i in l:
#         result = transform_cashflow([1, 3, 9, 20, 30], i)
#         r = np.roots(result[1][::-1])
#         print("==============================")
#         print("r: "+str(r))
#         print("r.real: "+str(r.real))
#
#         # print("r.real True: " + str(r[True].real))
#
#         print("r.imag"+str(r.imag))
#         print("reciprocal: "+str(1/r.real - 1))
#         # print((1 / r.real - 1).)
#         #print(result[1])
#         print("IRR:"+str(irr(result[1])))
#         # print("NP IRR:"+str(np.irr(result[1])))
        #print

nt, transformed_cf = transform_cashflow([1, 2, 3, 4, 5], l[0])
print(gradient_descent(transformed_cf))






"""
print(i)
print("============================")
print(result[0])
print(result[1])

irr = np.irr(result[1])
if sum(result[1]) == 0:
    irr = 0
elif sum(result[1]) > 0 and irr > 0:
    pass
elif sum(result[1]) < 0 and irr < 0:
    pass
else:
    irr = np.nan
print(irr)

annual_irr = (1 + irr)**365 - 1
print(annual_irr)
"""