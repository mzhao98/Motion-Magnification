from dependencies import * 
from utils import *
from filterbank import TemporalFilter



def magnify(input_video_filename, lowFreq, highFreq, output_video_filename, window_size=30, 
		magnif_factor=1, fps_bandpass=600):
	

	steer_pyr = Steerable(5)

	# Make Video Reader and Writer
	videoReader = cv2.VideoCapture(input_video_filename)
	nFrames = int(videoReader.get(cv2.CAP_PROP_FRAME_COUNT))
	
	videoWriter = make_video_writer(videoReader, output_video_filename)


	# Make Steerable Pyramid
	steer_pyr = Steerable(5)

	# Make temporal filter
	temp_filt = TemporalFilter(window_size, lowFreq, highFreq, fps=fps_bandpass)

	print("Total Number of Frames = ", nFrames)
	# alphas = np.random.normal(magnif_factor, magnif_factor/2, size=int(nFrames + window_size))

	# Fs = int(nFrames + window_size)
	# f = 5
	# sample = int(nFrames + window_size)
	# x = np.arange(sample)
	# alphas = 40*np.sin(2 * np.pi * f * x / Fs)
# nFrames + window_size
	nFrames = 100
	for frame_num in range(nFrames + window_size):
		print("frame: " + str(frame_num))
		if frame_num < nFrames:
			ret, img = videoReader.read()
			if ret == False or img is None:
				print("done")
				break

			if len(img.shape) > 2:
				gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

			pyramid_coeff = steer_pyr.buildSCFpyr(gray_img)

			# coeff is an array and subbands can be accessed as follows:
			# coeff[0] : highpass
			# coeff[1][0], coeff[1][1], coeff[1][2], coeff[1][3] : bandpass of scale 1
			# coeff[2][0], coeff[2][1], coeff[2][2], coeff[2][3] : bandpass of scale 2
			# ...
			# coeff[4]: lowpass. It can also be accessed as coeff[-1]

			pyramid_1d = flatten_coeff(pyramid_coeff)

			# Get amplitude and phase decomposition from Steerable Pyramid
			amplitudes = np.abs(pyramid_1d)
			phases = np.angle(pyramid_1d)

			# Temporally filter the phases
			temp_filt.add([phases])

			try:
				filtered_phases = temp_filt.slide_window()
			except StopIteration:
				continue

			# Magnify temporally filtered phases 
			# factor = alphas[frame_num]
			factor = 0.01
			magnified_filtered = factor * filtered_phases 
			magnified_phase = (phases - filtered_phases) + magnified_filtered

			# Reconstruct steerable pyramid
			new_1d_pyr = amplitudes * np.exp(magnified_phase * 1j)
			new_pyr_coeff = reconstruct_coeff(pyramid_coeff, new_1d_pyr)

			# Reconstruct motion-magnified image
			output_img = steer_pyr.reconSCFpyr(new_pyr_coeff)

			# output_img = np.clip(output_img, 0, 255)

			# final_img = np.stack([output_img, output_img, output_img])

			output_img[output_img>255] = 255
			output_img[output_img<0] = 0

			final_img = np.zeros( (output_img.shape[0], output_img.shape[1], 3 ) )
			final_img[:,:,0] = output_img
			final_img[:,:,1] = output_img
			final_img[:,:,2] = output_img
			# final_img = np.stack([output_img, output_img, output_img])


			# write video
			res = cv2.convertScaleAbs(final_img)
			videoWriter.write(res)


	videoReader.release()
	videoWriter.release()










if __name__ == '__main__':
	# define input and output
	input_video_filename = '../videos/tulip.mp4'
	output_video_filename = '../videos/tulip' + '_magnified_6' + '.avi'

	# params
	window_size = 10
	magnif_factor = 30
	fps_bandpass = 600

	lowFreq = 72
	highFreq = 92
	


	magnify(input_video_filename, lowFreq, highFreq, output_video_filename, window_size=window_size, 
		magnif_factor=magnif_factor, fps_bandpass=fps_bandpass)














