from dependencies import * 

class TemporalFilter ():

	def __init__(self, winsize, wl, wh, fps=1, step=1):
		# SlidingWindow.__init__(self, winsize, step)
		self.win_size = winsize
		self.step = step
		self.history = None

		# self.filter = IdealFilter(wl, wh, fps=fps, NFFT=winsize)

		self.frequencies = fftpack.fftfreq(winsize, d=1.0 / fps)

		# determine what indices in Fourier transform should be set to 0
		self.mask = (np.abs(self.frequencies) < wl) | (np.abs(self.frequencies) > wh)

	def add(self, data):
		if self.history is None:
			self.history = np.array(data)
		else:
			self.history = np.concatenate((self.history, data), axis=0)


	def slide_window(self):
		# next_data = SlidingWindow.next(self)
		# if self.memory is not None and self.memory.shape[0] >= self.size:
		if self.history.shape[0] > self.win_size:
			# get window
			next_data = self.history[:self.win_size]

			# slide
			self.history = self.history[self.step:]

		else:
			raise StopIteration()

		fft = fftpack.fft(next_data, axis=0)
		# print("fft shape", fft.shape)
		# print("mask shape", self.mask.shape)
		# print()
		# print(fft)


		fft[self.mask] = 0
		# print(fft)





		out = np.real(fftpack.ifft(fft, axis=0))

		return out[0]

