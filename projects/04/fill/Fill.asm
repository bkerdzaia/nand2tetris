// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.


(START)
	@SCREEN
	D=A	
	@addr
	M=D			// M[addr] = SCREEN
	@KBD
	D=M 		// D = M[KBD]
	@LOOPBLACK
	D;JNE		// if D != 0 jump to LOOPBLACK
(LOOPWHITE)
	@addr
	D=M			// D = M[addr]
	@KBD
	D=A-D
	@START
	D; JLE		
	@addr
	D=M
	M=M+1
	A=D
	M=0
	@LOOPWHITE
	0;JMP
(LOOPBLACK)
	@addr
	D=M			// D = M[addr]
	@KBD
	D=A-D
	@START
	D; JLE		
	@addr
	D=M
	M=M+1
	A=D
	M=-1
	@LOOPBLACK
	0;JMP
