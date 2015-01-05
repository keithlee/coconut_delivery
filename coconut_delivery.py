import sys
import os

def main(args):
	if len(args) == 2:
		if os.path.exists(args[1]) == False:
			print "Error: file "+ args[1] + " does not exist."
			exit(1)
		f = open(args[1], 'r')
	else:
		print "Error: Please pass in one filename as a parameter"
		exit(1)

	streams = []
	constant_energy = int(f.readline())
	for line in f:
		streams.append([int(s) for s in line.rstrip('\n').split()])
	# Sort streams by end mile 
	streams.sort(key=lambda x: x[1])
	# Variable to store tuple of (List of min paths ending with this stream, energy to get to end of this stream )
	min_paths = [] 

	def find_best_path(s, index):
		# Current stream's data 
		beginning = s[0]
		end = s[1]
		energy = s[2]

		if constant_energy * (end-beginning) < energy:
			print "Error: Constant energy total " + str(constant_energy * (end-beginning)) + " for jet stream " + str(s) + " uses less fuel than jet stream. Please recheck input data" 
			exit(1)

		# Calculate and return a tuple (List of paths up to end of current stream, energy up to and including this path)
		if index == 0:
			return ([(beginning, end)], min(beginning * constant_energy + energy, end * constant_energy))
		else:
			# Non_overlap is the previous stream path that does not overlap with the current stream
			non_overlap_path_tuple = find_min_prev_non_overlapping_path(s,index-1)
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

			# Last path is the previous stream
			last_path_energy = min_paths[i-1][1]
			last_path = min_paths[i-1][0]
			# Gap between end of current stream and end of previous stream
			last_gap = end - last_path[-1][1] 
			last_gap_path_energy = last_path_energy+last_gap*constant_energy

			# Choose path that uses less energy
			if non_overlap_path_energy <= last_gap_path_energy:
				curr_min_energy = non_overlap_path_energy 
				curr_min_path = non_overlap_path + [(beginning,end)] 
			else:
				curr_min_energy = last_gap_path_energy
				curr_min_path = last_path
			return (curr_min_path, curr_min_energy)

	# Find previous non-overlapping path
	# Returns tuple consisting of (List of paths up to previous non-overlapping stream, energy )
	def find_min_prev_non_overlapping_path(curr_stream, index):
		curr_beginning = curr_stream[0]
		# Index of non-overlapping stream
		min_stream_index = -1
		for i in xrange(index, -1, -1):
			end = streams[i][1]
			# Find previous path that uses the least amount of energy
			if end <= curr_beginning:
				return min_paths[i]
		return None

	for i,s in enumerate(streams):
		min_paths.append(find_best_path(s,i))

	print "Minimum energy: " + str(min_paths[-1][1])
	print "Optimal jet streams: " + str(min_paths[-1][0])

if __name__ == "__main__":
	main(sys.argv)
