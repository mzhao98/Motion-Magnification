from dependencies import * 

def display_video(videoReader):
	while(videoReader.isOpened()):
			ref, frame = videoReader.read()
			if ref == True:

			#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				cv2.imshow('frame', frame)

				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			else:
				break
	videoReader.release()
	cv2.destroyAllWindows()
	return


def make_video_writer(videoReader, output_video_filename):
	# videoReader = cv2.VideoCapture(input_video_filename)

	nFrames = int(videoReader.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_width = int(videoReader.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(videoReader.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = int(videoReader.get(cv2.CAP_PROP_FPS))


	fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

	videoWriter = cv2.VideoWriter(output_video_filename, fourcc, int(fps), (frame_width, frame_height), 1)
	return videoWriter




def flatten_coeff(coeff):

	nlevels = 5
	nbands = 4

	coeff_1d = list(coeff[0].flatten())
	for lvl in range(1, nlevels-1):
		for b in range(nbands):
			coeff_1d.extend( coeff[lvl][b].flatten() )             
	coeff_1d.extend(coeff[-1].flatten())
	coeff_1d = np.array(coeff_1d)
	return coeff_1d


def reconstruct_coeff(coeff, new_arr):
	nlevels = 5
	nbands = 4

	first_shape = coeff[0].shape
	first_flat_len = np.prod(coeff[0].shape)
	
	first_img = new_arr[0:first_flat_len]
	first_img_reshape = first_img.reshape(first_shape)
	result = [first_img_reshape]

	current_index = first_flat_len

	for lvl in range(1, nlevels-1):
		to_add = []
		for b in range(nbands):
			start_index = current_index 

			part_length = np.prod(coeff[lvl][b].shape)
			end_index = current_index + part_length

			curr_img = new_arr[start_index:end_index]
			curr_img_reshaped = curr_img.reshape(coeff[lvl][b].shape)
			to_add.append(curr_img_reshaped)

			current_index = end_index
			
		result.append(to_add)


	last_shape = coeff[-1].shape
	last_flat_len = np.prod(coeff[-1].shape)
	
	last_img = new_arr[current_index: (current_index+last_flat_len)]
	last_img_reshape = last_img.reshape(last_shape)
	result.append(last_img_reshape)


	# print("results shape", len(result))
	return result

