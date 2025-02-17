Melody Harmonizer

A tool that harmonizes the given melody

Table of Content:
	1. How to run the program
	2. Quick start
	3. Configurations
	4. Color of chords
	5. Rules of connection
	6. To do list
	7. Special thanks



1. How to run the program

The program was currently tested on python 3.11. A version of 3.7 or higher will be mandatory to run the program.
required dependencies for the program:
	mido

To run the project, change your directory to the folder where 'main.py' exist, then execute main.py with python. 







2. quick start

After you executed 'main.py', enter '1' to enter the main program. 
There will be three options to choose from after you entered the main program, as shown below:
"do you want to input 1:manually, 2:from text file, 3:form midi file?(1/2/3):"

To test if the program works correctly, enter '2'. The program will read the melody from input_file.txt and output several versions of the harmony of 'Twinkle twinkle little star'

The easiest way to input a little melody will be 1, input manually. The program will then ask you to input the melody.

The note in this program have two main features: the octave it's in and the position of it in the octave. Addition to those two features, the program will also ask you to include the duration of the note.
For example: 
4/0/1 represents a middle C (C4) that holds one beat.
5/3/2.5 represents Eb5 (or D#5) that holds two and a half beats.
notice how the position was measured in semitone above the 'C' of the octave.
to input a rest, use rest/n, where n is the time of the rest.
For example:
rest/1 means a rest with the duration of one beat.
You cannot input a rest at the end of the melody.
Use comma in between to separate notes.

For example, the melody of 'Twinkle twinkle little star' will be inputted as:
4/0/1,4/0/1,4/7/1,4/7/1,4/9/1,4/9/1,4/7/2,4/5/1,4/5/1,4/4/1,4/4/1,4/2/1,4/2/1,4/0/2
you could also simplify this melody to:
4/0/2,4/7/2,4/9/2,4/7/2,4/5/2,4/4/2,4/2/2,4/0/2
if you do not want different chords for every note.
If this seems to be too complicated for you, don't worry. The document will explain how to input the melody from midi file.

After you entered your melody, you will be asked to enter the key, mode, BPM and time signature of your melody.
example of keys: C, Bb, F#...
the mode will be either major or minor. By default they are natural major and natural minor with an additional leading tone. The document will later explain how to use a different scale.
BPM has to be a float number
time signature is in the form of a/b, where a and b are all natural numbers and b is a power of two.

When you finished all of the entering, the program will ask you if you want to input 'color', which will be explained later in the document. For now, you could just enter 'n' to skip the process.

The program will now start generating midi files. If the generating process is successful, the program will create a folder called 'midifiles' under the program's root folder, which includes midi files with harmonized melody in it.







3. configurations

To change the configuration, enter '2' after you run the program, where the console shows:
"1. start the main program, 2. change configurations, 3. about the program, enter 'exit' to exit the program"
The configurations are stored in 'config.cfg' under the root directory of the program. it's recommended to make a copy of the default configuration before making any changes.
The program will then show you all of the available changes in the configuration. The explanation to each option is below:

	1. allowed chord types:
		currently, the two chord types are triad and seventh. If you only want triads to appear in the harmony, put 'triad'. If you only want seventh chords to appear in the harmony, put 'seventh'. If you want both, put 'triad, seventh'

	2. diatonic/chromatic:
		if it is set on diatonic, then all the notes in the harmony will be in the scale. If it is set on chromatic, all 12 notes in octave may appear on the harmony.

	3. number of note in a chord:
		this configuration indicates the range of the number of note in any chords in the harmony. For example, '3,5' indicates that all chords must have minimum 3 notes and maximum 5 notes, '4,4' indicates a four part harmony. Be aware that the notes does not have to be identical. 

	4. tension usage:
		this configuration indicates which tensions can exist in the chord. The position of the tension is counted from the root of the chord. For example, '1,2,8,9' allows the chord have major/minor nineth and major/minor fourth. If you want no tension to appear in the harmony, write 'none'.

	5. omit notes:
		this configuration indicates with note can be omitted from the chord. For example, '3,4,7' allows the chord to omit major/minor third of the chord, as well as the perfect fifth. Chords with root omitted was not tested. If omitting root works, the 'color' (explain later) of the chord will be calculated with the omitted root as its root. (instead of the third, which is the 'practical' root of the root omitted chord) If you don't want any notes to be omitted, write 'none'.

	6. avoiding interval in chords:
		this configuration contains four parts: avoiding interval for modification, avoiding interval for repetition, avoiding interval for bass repetition, and avoiding interval between bass and root.

		avoiding interval for modification: 
			New intervals could be created through adding tension. For example, adding a minor nineth to a minor seventh chord created a minor second (ninth) from root to nineth, and a major second (minor seventh) from nineth to third. In this case, if 1 or 2 was in the 'avoiding interval for modification', minor ninth won't be added onto the minor seventh chord. Another example will be adding a perfect fourth to a major seventh chord. A tritone will be created. To avoid it, add 6 into the 'avoiding interval for modification.	

		avoiding interval for repetition:
			This part of the configuration affects the notes a chord can repeat. For example, if it is set on '1,2,5,6', the chord cannot repeat the minor/major ninth, the perfect eleventh (fourth), and the diminished fifth (augmented eleventh) of it.

		avoiding interval for bass repetition:
			This is the 'avoiding interval for repetition' specialized for bass. For example, if the 'avoiding interval for repetition' is set on '1,2,5,6' but the avoiding interval for bass repetition is empty, the bass could be repeated no matter the position of it in the chord. Notice that the root is not necessarily the bass.

		avoiding interval between bass and root:
			This affects which note cannot be the bass. For example, if it is set on '11', then the major seventh cannot be the bass.

		Those for parts of this configuration needs to be separated by underline. For example, 6_1,2,6_ _6 indicates 6(tritone) as the avoiding interval for modification, 1(minor nineth),2(major nineth) and 6(tritone) as the avoiding interval for repetition, nothing for the avoiding interval for bass repetition, and 6(tritone) as the avoiding interval between bass and root.
	
	7. type of minor scale used:
		this configuration was suppose to work to change the scale used if you entered 'Minor' in input. For example, if the configuration is set on 'harmonic minor', then the scale using to generate the harmony should be harmonic minor scale. (i, ii, iiib, iv, v, vib, vii) However, in the current version, this configuration didn't work. To change the scale used, open library.py and find the variable 'MajorScale' or 'MinorScale' and edit it. 

	8. directory for text input file:
		the purpose of this configuration was to lessen the repetitive work for debugging. In the input process, if you entered '2' (2: from text file), the program will open the file from the directory set for this configuration.

	9. maximum output files:
		this configuration limited the number of the output of harmonies. For example: if it is 50, then after the program generated 50 harmonies, it will automatically stops

	10. minimum output files:
		this configuration limited the minimum number of harmonies generated. For example: if it is 5, then the program won't stop until it generated 5 harmonies.

	11. maximum connection for any node:
		this configuration limited how many successful connection attempt to the next chord can any chord have before it was changed to another one. For example, the chord 1-1 can connect to chord 2-1, 2-2, 2-3, 2-4. However, if the configuration is on 3, before the chord 1-1 can connect with 2-4, the chord 1-1 will changed to a different chord. Say 1-2, then the chord 1-2 can try to connect with chord 2-4. The smaller the number of the configuration is, the more diverse the harmonies are. However, if the number is too small, it will slow down the running speed of the program.

	12. maximum program running time:
		this configuration sets a 'time-out' bound for the program, in seconds. This configuration can override configuration number 10.







4. Color of chords:

Any chords are quantified in three ways in the program: tension, mood, and function.
To limit the tension and mood of chords in the harmony, in the input, when the program asks 'do you want to input color? (y/n)', enter 'y'. Then, in the following line, type the tension and mood range in the structure of:

moodMin#moodMax_tensionMin#tensionMax > moodMin#moodMax_tensionMin#tensionMax > ...

where the mood/tension range for every note was separated by '>'

the 'function' of the chord was currently only used in checking if the connection between chords are legal.
	
tension:
	The tensions of the chord in this program refers to how 'dissonant' is the chord, or how 'unpleasant' is the chord. The greater the tension is, the more dissonant the chord is.
	First, a diction recording how many interval with certain distance exists in the chord was created. 
	For example, a Major triad have one major third between the root and the third, one minor third between the third and the fifth, and one perfect fifth between the root and the fifth.
	Interval was treated the same as its inversion. For example, a major third is treated the same as a minor sixth, not affecting the consonance/dissonance of the chord.
	A major seventh chord have two major thirds, two perfect fifth, one minor third, and one major seventh.
	we record the intervals greater than tritone as their inversions. Therefore the above intervals in the major seventh are equivalent to:
	two major thirds, two perfect fourth, one minor third, and one minor second.
	
	After the diction that records all the intervals was created, the tension will be given based on those intervals.
	Each minor second/major seventh worth 3, each major second/minor seventh worth 2, each major/minor third/sixth worth 0,  each perfect fourth/fifth worth 0, and each tritone (diminished fifth/augmented fourth) worth 6.
	Addition to those, the program will check if there is any augmented fifth/diminished fourth, which sounds dissonant but have the same distance as minor sixth/major third, and diminished seventh/augmented second, which also sounds dissonant but have the same distance as major sixth/minor third. Each augmented fifth worth 3, and each diminished seventh worth 2.
	
	To get the final tension value, simply add all the values together.
	For example:
	a major triad have 0 tension			a minor triad have 0 tension
	a diminished triad have 6 tensions		an augmented triad have 3 tensions
	a major seventh have 2 tensions			a minor seventh have 2 tensions
	a dominant seventh have 8 tensions		a diminished seventh have 14 tensions
	a dominant seventh (b9) have 19 tensions	a dominant seventh (b5, b9, #9, b13) have 35 tensions
	...

mood:
	The mood of the chord in this program depends on if the chord sounds more 'major' or more 'minor'. Usually, a major chord sounds happy and a minor chord sounds sad.
	A most minor chord have mood=-100, and a most major chord have mood=100
	A diction recording intervals will also be created, but this time the distance was always counted from the bass of the chord.
	for example, a dominant seventh chord will have a major third, a perfect fifth, and a minor seventh.
	A minor second worth -10, major second worth 10, minor third worth -50, major third worth 50, perfect fourth and fifth worth 0, minor sixth worth 40, major sixth worth -40, minor seventh worth -10, and major seventh worth 10. 
	After adding up all the scores, the value will be diluted according to the tension, calculated in:
	final mood = mood * min((3/tension - 0.005*tension),2)
	when 3/tension - 0.005*tension > 2, final mood = mood*2
	when tension = 0, final mood = mood*2
	
	For example:
	a major triad have a mood of 100		a minor triad have a mood of -100
	a diminished triad have a mood of -23.6		a augmented triad have a mood of 88.7
	a minor seventh have a mood of -89.4		a major seventh have a mood of 59.1
	...

function:
	The function of the chord in this program is similar to the 'function' of a chord in popular/jazz harmony
	The three main functions, Tonic, Dominant, and Subdominant was calculated along with two other function group: SS (subdominant of subdominant), and DD (dominant of dominant)
	Any function typically have both the minor and the major version of it. 
	For example, tonic group could be split into two groups: 
		Major Tonic (I, III, V)
		and Minor Tonic (I, iiib, V)
	Those two function groups are calculated separately.
		The 'root' of a group worth 4, 
		the 'characteristic note' of a group worth 5, 
		the 'fifth' of a group worth 2, 
		the 'tritone' of a group worth 5.
		If the chord have the 'root' as the bass, it get an extra 4 scores on the function group.
	For example, for Major Dominant:
		the 'root' is the fifth degree of the scale
		the 'characteristic note' is the major seventh degree (leading tone) of the scale
		the 'fifth' is the second degree of the scale
		the tritone of the group is the leading tone of the scale combined with the fourth degree of the scale.
	A dominant seventh on the fifth degree in root position will have all of the above, with an extra 4 scores as its bass is the fifth degree of the scale, which gives the chord a total score of 20. 20 is the highest you can get for a function group.
	Notice that minor function groups don't have their tritone.







5. Rules of connection:

The rules of chord connection follows the rules for four-parts harmony for the most part.
Some of the rules including:
	1. Dominant to subdominant was forbidden (in this program, this restriction is less strict. For example, progressions such as V6 to ii and V7 to I/IV are allowed)
	2. No parallel fifth/octave
	3. No voice overlapping and crossing
	4. Distance between each adjacent parts other than to bass cannot exceed octave
	5. Tritone must either be maintained or resolved
	6. The harmony must end on tonic; it must not contains a tritone

To disable any rules, go to rules.py and change the value of any variable from line 4 to line 11 you want to disable to 'False'.







6. To do list:

There are few things needs to be working on for this project:

- The configuration module needs to be expand and organized. My plan is to add the enabling/disabling of rules into the configuration, and use a more visualized interface like:

Press 'tab' to change between settings, press 'enter' to change the status:
[*]parallel fifth [Forbidden]	[]parallel octave[Forbidden]	[]hidden fifth[Allowed]		[]hidden octave[Forbidden]

- There should be an algorithm to calculate the maximum connection allowed between nodes. Because in my experience, the first few chords in a mediocre length melody 
was rarely changed.

- The tension mood, and function values (see part 4. color) of some chords should be pre-calculated instead of real-time calculated.

- A final overall check to harmonies should be made. The user should be able to set things like "The harmony should have a lot of sudden changes in mood" or "The harmony should have a low average tension" or "The harmony shouldn't often resolve to tonic before the end". Therefore, a total count up of these things were needed.

- The inputting process should be more user friendly. I'm thinking about construct this project in a client-server mode, and write a GUI for client. Before that though, the input validations should be completed, and the input process should be able to auto-correct some typing mistakes.

- New classes should be applied to make the chord more analyzable. The classes in classes_group.analytics are my current ideas. The 'RawChord' will be able to identify any augmented or diminished intervals in the chord, and the mood (see part 4. color) determining process will be easier since all intervals can now be calculated from bass. Chord annotations would also able to be generated easily. These new classes could also distinguish equivalent chords such as G7/F and Fdim7(bb3), which would leads to different chords.

- searching algorithm should be optimized. now the time complexity to search all available harmonies is O(2^n). Don't know if a polynomial time is possible

- The modules of the program tends to be coupling. Modules would need to be re-organized.

- Complete the error messages

- The program had not been tested completely.







7. Special thanks:

（only myself)

---the read me file stops here---

I finally handed in my personal project with this program. If you don't know what it is, basically at grade 10 we will have six months to do something you are interested on.
"interest", that's a wonderful word.
Someone played DECO*27's "Vampire" two years ago, I think that's where it start. 
As I said in my report of the project, I played piano for a few years, quit after grade 5, know basic music theory since then.
But that's not interest, that's not interest.
So I went back home after the school, searched for the "Vampire", and fell into the "rabbit hole" of Vocaloid.
"Music could also be like this". The phrase "opened up a new world" is cliche, but I guess that's the best phrase to describe it.
With that thought, I wrote this program. 
Therefore, this program shouldn't be an AI, it should be a tool. The former one replaces people's creativity, while the latter one helps people to create. 
Just like Vocaloid, it's a tool, it's the music that everyone can make.

Oh, I know who I should put on the special thanks
Special thanks:
	Squid (Yes I'm talking about you!)


