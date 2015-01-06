import sys
import os

def main(filename):
	"""
	This program takes an input file and prints the jet stream paths that requires the least amount of energy as well as the total minimum energy.
	"""
	if os.path.exists(filename) == False:
		print "Error: file "+ filename + " does not exist."
		exit(1)
	f = open(filename, "r")

	streams = []
	constant_energy = int(f.readline())
	for line in f:
		streams.append([int(s) for s in line.rstrip().split()])
	# Sort streams by end mile 
	streams.sort(key=lambda x: x[1])
	# Variable to store tuple of (List of min paths ending with this stream, energy to get to end of this stream )
	min_paths = [] 

	# Abstract access to min_paths data to these functions. One place to check for access to min_paths data
	def get_min_path_data(index):
		return min_paths[index]

	def add_to_min_path(data):
		min_paths.append(data)

	def find_best_path(s, index):
		"""
		Finds best path for a stream
		Returns:
			Tuple of (List of paths, Energy to get to end of stream)
		"""
		# Current stream's data 
		beginning = s[0]
		end = s[1]
		energy = s[2]

		if constant_energy * (end-beginning) < energy:
			print "Error: Constant energy total " + str(constant_energy * (end-beginning)) + " for jet stream " + str(s) + \
			" uses less fuel than jet stream. Please recheck input data" 
			exit(1)

		# Calculate and return a tuple (List of paths(beginning,end) up to end of current stream, energy up to and including this path)
		if index == 0:
			return ([(beginning, end)], min(beginning * constant_energy + energy, end * constant_energy))
		else:
			# Non_overlap is the previous stream path that does not overlap with the current stream which is at index
			non_overlap_path_tuple = find_min_prev_non_overlapping_path(beginning,index)
			if non_overlap_path_tuple:
				non_overlap_energy = non_overlap_path_tuple[1]
				non_overlap_path = non_overlap_path_tuple[0]
				# The gap between the beginning of current stream and end of non overlapping stream. 
				non_overlap_gap = beginning - non_overlap_path[-1][1]
				non_overlap_path_energy = energy + non_overlap_energy + non_overlap_gap * constant_energy
			else:
				# When there is no previous overlapping path
				non_overlap_gap = beginning
				non_overlap_path_energy = energy + non_overlap_gap * constant_energy
				non_overlap_path = [] 

			(last_path, last_gap_path_energy) = calculate_last_path_data(index,end)

			# Choose path that uses less energy
			if non_overlap_path_energy <= last_gap_path_energy:
				curr_min_energy = non_overlap_path_energy 
				curr_min_path = non_overlap_path + [(beginning,end)] 
			else:
				curr_min_energy = last_gap_path_energy
				curr_min_path = last_path
			return (curr_min_path, curr_min_energy)

	def find_min_prev_non_overlapping_path(curr_stream_beginning, index):
		"""
		Find previous non-overlapping path
		Returns: 
			Tuple consisting of (List of paths up to previous non-overlapping stream, energy)
			None if there is no path 
		"""
		# Use index -1 to exclude current stream
		for i in xrange(index-1, -1, -1):
			prev_end = streams[i][1]
			# Find previous path that uses the least amount of energy
			if prev_end <= curr_stream_beginning:
				return get_min_path_data(i) 
		return None

	def calculate_last_path_data(index,end_mile):
		"""
		Calculate the previous stream's path data up to end of current stream
		Returns: 
			Tuple consisting of (List of paths up to previous stream, energy to get from last_path to current stream's end)
		"""
		# Last path is the previous stream thus i-1 index
		last_path_energy = get_min_path_data(index-1)[1]
		last_path = get_min_path_data(index-1)[0]
		# Gap between end of current stream and end of previous stream
		last_gap = end_mile - last_path[-1][1] 
		last_gap_path_energy = last_path_energy+last_gap*constant_energy
		return (last_path,last_gap_path_energy)

	for i,s in enumerate(streams):
		add_to_min_path(find_best_path(s,i))

	# Last element in min_paths is the end mile 
	print "Minimum energy: " + str(get_min_path_data(-1)[1])
	print "Optimal jet streams: " + str(get_min_path_data(-1)[0])


if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print "Error: Please pass in one filename as a parameter"
		exit(1)
