import numpy as np
from datetime import datetime

# Pull the data
irr_data = np.loadtxt("irr_input.csv", delimiter=",", usecols=(0, 1), dtype=object,
    converters={
        0: lambda x: int(datetime.timestamp(datetime.strptime(x.decode("utf-8"), "%m/%d/%Y")) / (60 * 60 * 24)),
        1: np.float
    }
)

# Create 2 arrays based on the inicial imput: i) array of dates and ii) array of cash flows
irr_dates = irr_data[:, 0]
irr_cfs = irr_data[:, 1]

# Identify maximum and minimum dates
irr_date_min = irr_data[:, 0].min()
irr_date_max = irr_data[:, 0].max()

# To populate dates between known cash flows with zeros so we can compute daily IRR rate
cfs = []
for i in range(irr_date_min, irr_date_max+1):
    if i in irr_dates:
        test = np.where(irr_dates == i)
        cfs.append(irr_cfs[test[0][0]])
    else:
        cfs.append(0)

# To remove unnecessary zeros at the beginning and the end of the cash flows stream
while cfs[0] == 0:
    cfs.pop(0)
while cfs[-1] == 0:
    cfs.pop(-1)

cf = [-9.06,0,1]

# Pick the staring point for Newton method. If sum of all cash flows is negative -> negative IRR is expected
start_point = .1 if sum(cf) > 0 else -.1

# Newton Method idea and derivation
#    slope = (y2-y1)/(x2-x1) => (x2-x1) = (y2-y1)/slope
#    x2 = x1 + (y2-y1)/slope
#    x2 = x1 + (0-y1)/slope
#    x2 = x1 - y1/f'(x1)

# Solving for IRR utilizing Newton's method
for i in range(20):
    start_point = start_point - sum([cf[i]/(1 + start_point)**i for i in range(len(cf))]) / sum([cf[i]*(-i)/(1+start_point)**(i+1) for i in range(len(cf))])
    print('Iteration '+str(i+1)+': '+str(start_point), end=' ')
    print(sum([cf[i]/(1+start_point)**i for i in range(len(cf))]))

# Iterative method to test negative IRR between 0% and -100%
# for start_point in range(10):
#    print(sum([cf[i]/(1+start_point*(-.1))**i for i in range(len(cf))]))