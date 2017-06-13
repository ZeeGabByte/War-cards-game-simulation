proc war() {
	// distribute the deck to the two players
	
	var deck_values: [0..12] int = [i in 0..12] i;  // initialise a quarter of deck's values

	// create the full deck's values
	for i in deck_values {
		for ii in 1..#3 {
			deck_values.push_back(i);
		}
	}
	
	// shuffle the deck's values
	use Random;
	shuffle(deck_values);  // seed=0, usefull for debuging
	
	var deck: [0..#52] int = deck_values;  // initialise the deck
	var player1: [0..#26] int = deck_values[0..#26];  // initialise player1's deck
	var player2: [0..#26] int = deck_values[26..#26];  // initialise player2's deck
	
	// initialise stats
	var nb_tricks: int = 0;
	
	// trick loop
	while (player1.size > 0 && player2.size > 0 && nb_tricks < 10000) {
		nb_tricks += 1;
		
		if player1.head() > player2.head() {
			// player1 win the trick
			player1.push_back(player2.head());
			player1.push_back(player1.head());
			player1.pop_front();
			player2.pop_front();
		} else if player2.head() > player1.head() {
			// player2 win the trick
			player2.push_back(player1.head());
			player2.push_back(player2.head());
			player1.pop_front();
			player2.pop_front();
		} else {
			// escarmouche
			var escarmoucheDepth = 0;
			var start_idx_player1 = player1.find(player1.head())[2];
			var start_idx_player2 = player2.find(player2.head())[2];
			var max_player1 = player1.size + start_idx_player1 - 1;
			var max_player2 = player2.size + start_idx_player2 - 1;
			
			while if (((start_idx_player1 + escarmoucheDepth) <= max_player1) && ((start_idx_player2 + escarmoucheDepth) <= max_player2)) then player1[start_idx_player1 + escarmoucheDepth] == player2[start_idx_player2 + escarmoucheDepth] else false {
				// determine the escarmouche's depth
				escarmoucheDepth += 2;
			}
			if !(((start_idx_player1 + escarmoucheDepth) <= max_player1) && ((start_idx_player2 + escarmoucheDepth) <= max_player2)) {
				// path
				player1.clear();
				player2.clear();
			} else if player1[start_idx_player1 + escarmoucheDepth] > player2[start_idx_player2 + escarmoucheDepth] {
				// player1 win the escarmouche
				for i in 0..#escarmoucheDepth+1 {
					player1.push_back(player2.head());
					player1.push_back(player1.head());
					player1.pop_front();
					player2.pop_front();
				}
			} else {
				// player2 win the escarmouche
				for i in 0..#escarmoucheDepth+1 {
					player2.push_back(player1.head());
					player2.push_back(player2.head());
					player1.pop_front();
					player2.pop_front();
			}
			}
		}
	} if nb_tricks >= 10000 {
		// infinite war?
		writeln("Infinite war?");
		return (4, nb_tricks);
	} else if player2.size == 0 && 0 < player1.size {
		// player1 win
		return (1, nb_tricks);
	} else if player1.size == 0 && 0 < player2.size {
		// player2 win
		return (2, nb_tricks);
	} else {
		// equality
		return (3, nb_tricks);
	}
}


proc run(x, process_name) {
	// create the path of the txt file to store the results
	var name_str = process_name : string;
	var path = 'data/arr_tricks_' + name_str + '.txt';
	
	var victory_rate: 4*real = (0, 0, 0, 0);
	var tricks: [-1..0] int;
	var nb_tricks_total: real = 0.0;
	
	// calculate victory rate & store nb_tricks in an array
	for i in 1..#x {
		var res = war();
		victory_rate[res[1]] += 1;
		nb_tricks_total += res[2];
		tricks.push_back(res[2]);
	}
	var arr_tricks = tricks[1..];
	victory_rate = victory_rate / x * 100;
	
	// display stats
	writeln("\nvictory rate: \n\t- ", victory_rate);
	var nb_tricks_avg = nb_tricks_total / x;
	writeln("number of tricks (AVG): ", nb_tricks_avg);
	
	// save arr_tricks in arr_tricks.txt
	var file_tricks = open(path, iomode.cw);
	var tricks_output = file_tricks.writer();
	tricks_output.write(arr_tricks);
	
	return arr_tricks;
}


// X: number of wars to simulate, Processes: number of processes to run the task
config const X: int = 100;
config const Processes: int = 2;

// x: number of war per process
var x = (X - (X % Processes)) / Processes;

// import I/O module to write in files
use IO;

// time the execution
use Time;
var timer: Timer;
timer.start();

// start the processes
coforall i in 0..#Processes {
	run(x, i);
}

timer.stop();  // stop the timer

// display stats
writeln("\n", x * Processes, " wars simulated");
writeln("total elapsed time: ", timer.elapsed());
writeln(x * Processes / timer.elapsed(), " wars per seconds");
