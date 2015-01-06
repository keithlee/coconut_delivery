import coconut_delivery
from cStringIO import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout	

def main():
	tests = [
		("sample_paths.txt","Minimum energy: 352","Optimal jet streams: [(0, 5), (6, 11), (14, 17), (19, 24)]"), 
		("sample_paths2.txt","Minimum energy: 215", "Optimal jet streams: [(1, 5), (8, 21), (24, 29)]"), 
		("sample_paths4.txt","Minimum energy: 195","Optimal jet streams: [(0, 5), (8, 21), (24, 29)]")
	]
	for (testfile, energy, jetstreams) in tests:
		with Capturing() as output:
			coconut_delivery.main(testfile)
		print "Testing " + testfile
		assert output[0] == energy 
		assert output[1] == jetstreams

	# Testing invalid tests and tests with very long output
	extraTests = [
		("sample_paths3.txt","Error: Constant energy total 0 for jet stream [0, 5, 15] uses less fuel than jet stream. Please recheck input data"),
		("flight_paths.txt","Minimum energy: 5577696") 
	]
	for (testfile, string) in extraTests:
		with Capturing() as output:
			coconut_delivery.main(testfile)
		print "Testing " + testfile
		assert output[0] == string

if __name__ == "__main__":
	main()
