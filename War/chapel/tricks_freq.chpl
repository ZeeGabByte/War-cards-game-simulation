proc read_file(process_name, x) {
	// path of the file
	var name_str = process_name : string;
	var path = 'data/arr_tricks_' + name_str + '.txt';
	
	// open the file in read mode
	var file_tricks = open(path, iomode.r);
	var tricks_reader = file_tricks.reader();
	
	// read the content of the file
	var arr: [0..#x] int;
	tricks_reader.read(arr);
	
	return arr;
}


proc maxOf(arr) {
	// return the highest value of a given array
	var mmax = 0;
	for x in arr {
		if x > mmax {
			mmax = x;
		}
	} return mmax;
}


proc minOf(arr) {
	// return the lowest values of a given array
	var mmin = arr[1];
	for x in arr {
		if x < mmin {
			mmin = x;
		}
	} return mmin;
}


proc freq(arr) {
	// count the number of occurence of all values in a given array
	var mmax: int = maxOf(arr);
	var mmin: int = minOf(arr);
	var freq: [mmin..mmax] int;
	for i in mmin..mmax {
		freq[i] = arr.count(i);
	} return freq;
}


proc maxOfDomain(arrs) {
	// return the highest number of the highest index of each array
	var mmax = 0;
	for x in arrs {
		if x.domain.high > mmax {
			mmax = x.domain.high;
		}
	} return mmax;
}


proc minOfDomain(arrs) {
	// return the lowest number of the highest lowest of each array
	var mmin = 10000;  // limit
	for x in arrs {
		if x.domain.low < mmin {
			mmin = x.domain.low;
		}
	} return mmin;
}


proc merge_arrs(arrs) {
	// get the domain
	var mmin: int = minOfDomain(arrs);
	var mmax: int = maxOfDomain(arrs);
	var merged: [mmin..mmax] int;
	
	// fill the merged array with values
	for arr in arrs {
		for i in arr.domain {
			merged[i] = merged[i] + arr[i];
		}
	} return merged;
}


config const X: int = 100;  // number of wars simulated
config const Processes: int = 2;  // number of processes used


var res = merge_arrs([i in 0..#Processes] freq(read_file(i, X/Processes)));

// save res & res.domain in tricks.txt
var file_tricks = open('data/tricks.txt', iomode.cw);
var tricks_output = file_tricks.writer();
tricks_output.write((res, res.domain));
