from matplotlib import pyplot as plt  # import the ploting tool
from matplotlib import style  # to get good looking graphs


# load the data
file = open('data/tricks.txt', 'r')
raw_data = file.readline()

# split the frequency from the domain
data = raw_data.split(', ')

# create the plots
domain = [int(i) for i in data[1][1:-2].split('..')]
xs = list(range(domain[0], domain[1] + 1))
ys = [int(i) for i in data[0].replace('(', '').split(' ')]
X = sum(ys)

# separate xs_odd from xs_even
xs_0 = [xs[i] for i in range(0, len(xs), 2)]
xs_1 = [xs[i] for i in range(1, len(xs), 2)]
ys_0 = [ys[i]/X for i in range(0, len(ys), 2)]
ys_1 = [ys[i]/X for i in range(1, len(ys), 2)]

if xs[0] % 2:
	# xs[0] is odd
	xs_odd = xs_0
	xs_even = xs_1
	ys_odd = ys_0
	ys_even = ys_1
else:
	# xs[0] is even
	xs_odd = xs_1
	xs_even = xs_0
	ys_odd = ys_1
	ys_even = ys_0

# display the graph
style.use('ggplot')  # choose the style

fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))

ax1.plot(xs_even, ys_even, 'b', label='even')
ax1.plot(xs_odd, ys_odd, 'r', label='odd')
ax1.set_xticks(list(range(0, int(max(xs)), 150)))

plt.rc('legend', fontsize=20)
plt.subplots_adjust(left=0.04, bottom=0.03, right=1.0, top=1.0)
ax1.legend()

plt.show()
